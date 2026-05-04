# Recipe · Futures Curve & Rolls

End-to-end: term structure of a futures complex, rolling-yield
calculation, and a clean continuous total-return series.

## Step 1 — Pick the contract family

```python
CONTRACTS = {
    "WTI":   {"root": "CL", "yk": "Comdty"},
    "Brent": {"root": "CO", "yk": "Comdty"},
    "Gas":   {"root": "NG", "yk": "Comdty"},
    "Gold":  {"root": "GC", "yk": "Comdty"},
    "Copper":{"root": "HG", "yk": "Comdty"},
    "ES":    {"root": "ES", "yk": "Index"},
    "TY":    {"root": "TY", "yk": "Comdty"},
}
```

## Step 2 — Pull the chain at a date

```python
def chain_at(root, yk, asof, include_expired="N"):
    df = blp.bds(f"{root}1 {yk}", "FUT_CHAIN",
                 INCLUDE_EXPIRED_CONTRACTS=include_expired,
                 CHAIN_DATE=asof)
    return [r["Security Description"] for r in df.to_dict("records")]

today = "20250502"
contracts = chain_at("CL", "Comdty", today)         # all live WTI contracts
```

## Step 3 — Snap the term structure

```python
snap = blp.bdp(contracts,
               ["PX_LAST", "PX_SETTLE", "OPEN_INT",
                "FUT_DLV_DT_FIRST", "LAST_TRADEABLE_DT",
                "FUT_VAL_PT", "FUT_CONT_SIZE"])
snap = snap.sort_values("FUT_DLV_DT_FIRST")
```

Plot `snap.PX_LAST` vs `snap.FUT_DLV_DT_FIRST` for the curve.

## Step 4 — Compute the implied "carry" / roll yield

For consecutive contracts:

```python
import pandas as pd
snap["dlv"] = pd.to_datetime(snap["FUT_DLV_DT_FIRST"])
snap = snap.sort_values("dlv").reset_index().rename(columns={"index":"contract"})

# 1m roll yield: (front − next) / front, annualised
import numpy as np
snap["t_yrs"] = (snap.dlv - snap.dlv.iloc[0]).dt.days / 365.25
snap["roll_yield"] = (snap.PX_LAST.iloc[0] / snap.PX_LAST - 1) / snap.t_yrs.replace(0, np.nan)
```

Sign convention: positive = backwardation (long roll earns positive
carry); negative = contango (long roll earns negative carry).

Aggregate measures:

```python
# Slope between front and 12m forward
front = snap.iloc[0]
m12 = snap[snap.t_yrs >= 0.95].iloc[0]
slope_12m = (m12.PX_LAST / front.PX_LAST - 1)
```

## Step 5 — Continuous front-month series (with roll handling)

The naive `CL1 Comdty` close-to-close series has gaps at every roll.
Three options:

### (a) Pre-built total-return index (cleanest)

```python
# S&P GSCI single-commodity total return:
oil_tr = blp.bdh(["SPGSCICL Index"], ["PX_LAST"],
                 "2010-01-01","2025-12-31", periodicitySelection="DAILY")
# BCOM single-commodity:
oil_bcom = blp.bdh(["BCOMCL Index"], ["PX_LAST"],
                   "2010-01-01","2025-12-31", periodicitySelection="DAILY")
```

Use these for backtests of any allocation strategy. The methodology
(Jan/Feb/Mar roll for GSCI, more spread-out for BCOM) is documented.

### (b) Bloomberg-rolled generic series via xbbg

```python
oil_active = blp.bdh(["CL1 Comdty"], ["PX_LAST"],
                     "2010-01-01","2025-12-31",
                     periodicitySelection="DAILY",
                     adjust="all",          # <-- splice across rolls
                     roll="ACTIVE")          # active-month rule
```

`xbbg` smooths gaps using the chosen roll method. `adjust="all"` is
proportional adjustment.

### (c) Manual roll

For full control:

```python
def manual_roll(root, yk, start, end, days_before_expiry=5):
    chain = blp.bds(f"{root}1 {yk}", "FUT_CHAIN",
                    INCLUDE_EXPIRED_CONTRACTS="Y")
    contracts = pd.DataFrame(chain.to_dict("records"))
    contracts.columns = [c.lower().replace(" ","_") for c in contracts.columns]

    spec = blp.bdp(contracts.security_description.tolist(),
                   ["LAST_TRADEABLE_DT","FUT_DLV_DT_FIRST"])
    spec["last_trade"] = pd.to_datetime(spec["LAST_TRADEABLE_DT"])

    # Build a per-day mapping: which contract is "front" on date t?
    schedule = spec.sort_values("last_trade")
    schedule["roll_date"] = schedule.last_trade - pd.Timedelta(days=days_before_expiry)

    # Pull each contract's history once
    series = blp.bdh(schedule.index.tolist(), ["PX_LAST"], start, end,
                     periodicitySelection="DAILY",
                     nonTradingDayFillOption="ACTIVE_DAYS_ONLY")
    series.columns = series.columns.droplevel(1)

    # Stitch
    out = pd.Series(index=pd.date_range(start, end, freq="B"), dtype=float)
    schedule = schedule.sort_values("roll_date").reset_index()
    for i, row in schedule.iterrows():
        if i == 0:
            mask = out.index <= row.roll_date
        else:
            prev = schedule.iloc[i-1].roll_date
            mask = (out.index > prev) & (out.index <= row.roll_date)
        out.loc[mask] = series[row["index"]].reindex(out.index[mask]).values
    return out
```

This stitches without proportional adjustment — for a TR series you
need to compute returns within each contract and chain them.

## Step 6 — Open-interest-weighted active month

For each date, find the contract with the highest OI and use it as
front:

```python
def oi_weighted_front(date, contracts):
    """contracts is the DataFrame from chain_at(...)"""
    snap = blp.bdp(contracts, ["OPEN_INT","FUT_DLV_DT_FIRST"],
                   REFERENCE_DATE=date)
    snap = snap.sort_values("FUT_DLV_DT_FIRST")
    snap = snap[pd.to_datetime(snap["FUT_DLV_DT_FIRST"]) > pd.Timestamp(date)]
    return snap.OPEN_INT.idxmax()
```

This is closer to how passive commodity ETFs roll.

## Step 7 — CFTC speculative positioning context

For a positioning overlay:

```python
COT_FIELDS = [
    "NCOMM_LONG_POS",        # non-commercial long
    "NCOMM_SHORT_POS",       # non-commercial short
    "COMM_LONG_POS",
    "COMM_SHORT_POS",
    "NRPT_LONG_POS",         # non-reportable
    "NRPT_SHORT_POS",
    "OI_AGG",                # total open interest
]

cot = blp.bdh(["CL1 Comdty"], COT_FIELDS,
              "2014-01-01","2025-12-31", periodicitySelection="WEEKLY")
cot.columns = cot.columns.droplevel(1)
cot["spec_net"]  = cot.NCOMM_LONG_POS - cot.NCOMM_SHORT_POS
cot["comm_net"]  = cot.COMM_LONG_POS - cot.COMM_SHORT_POS
cot["spec_pct"]  = cot.spec_net / cot.OI_AGG
```

## Step 8 — Rolling yield as a strategy signal

For commodity carry portfolios:

```python
ROOTS = ["CL","CO","NG","HO","XB",      # energy
         "GC","SI","HG",                  # metals
         "C ","S ","W ","KC","SB","CT",   # ags
         "LH","LC"]                       # livestock

carry_panel = []
for r in ROOTS:
    chain = blp.bds(f"{r}1 Comdty", "FUT_CHAIN",
                    INCLUDE_EXPIRED_CONTRACTS="N")
    contracts = [m["Security Description"]
                 for m in chain.to_dict("records")][:2]
    px = blp.bdp(contracts, ["PX_LAST"]).PX_LAST
    if len(px) == 2:
        carry_panel.append({"root": r,
                            "front": px.iloc[0],
                            "next":  px.iloc[1],
                            "ann_carry": (px.iloc[0]/px.iloc[1] - 1) * 12})
carry_df = pd.DataFrame(carry_panel).sort_values("ann_carry")
```

## Field reference

| Field | Use |
|---|---|
| `FUT_CHAIN` | List active (and optionally expired) contracts |
| `INCLUDE_EXPIRED_CONTRACTS` | `Y/N` override |
| `CHAIN_DATE` | as-of date for the chain |
| `PX_LAST`, `PX_SETTLE` | Closing / settlement prices |
| `OPEN_INT`, `OPEN_INT_DATE` | OI snapshot |
| `FUT_DLV_DT_FIRST`, `FUT_DLV_DT_LAST` | Delivery window |
| `LAST_TRADEABLE_DT` | Last trading day |
| `FUT_NOTICE_FIRST` | First notice (for physically-settled) |
| `FUT_VAL_PT`, `FUT_CONT_SIZE` | Multipliers |
| `ROLL_METHOD` (override) | Generic roll rule |
| `NCOMM_LONG_POS`, `NCOMM_SHORT_POS` | CFTC spec positioning |

## Pitfalls

- **`CL1 Comdty` is not a return series.** Backtests on close-to-close
  CL1 mis-attribute returns at every roll.
- **Different roll rules → different P&L.** Document the rule.
- **Liquidity at the back end** is thin — don't read deep curve points
  as fair value.
- **Holiday calendars** for global commodities: ICE Brent vs NYMEX WTI
  have different early closes around US holidays. Use
  `LAST_TRADEABLE_DT` as truth.
- **Notice-day risk**: physically-settled futures stop trading on
  the last trade date but you must close *before* the first notice
  if you don't want delivery. Some passive backtests roll on
  notice-1.
- **Expired contracts**: `INCLUDE_EXPIRED_CONTRACTS=Y` is needed for
  historical backtests; `=N` (default) only returns live.
- **CFTC report timing**: Tuesday positions, released Friday 15:30
  ET — don't use as same-week signal.
