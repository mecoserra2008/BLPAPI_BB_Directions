# Recipe · Cross-Sectional Factor Panel

A point-in-time, survivor-bias-free panel of value/quality/momentum/
size factors for a regional equity universe.

## Step 1 — Build a survivor-bias-free universe

Naïvely calling `INDX_MEMBERS` gives you *current* members — backtests
on this universe have look-ahead bias and exclude delisted names.

The right way: union month-end membership snapshots over your
backtest range.

```python
import pandas as pd

snapshots = []
for d in pd.date_range("2014-12-31", "2025-12-31", freq="ME"):
    df = blp.bds("SXXP Index", "INDX_MWEIGHT_HIST",
                 END_DATE_OVERRIDE=d.strftime("%Y%m%d"))
    df["asof"] = d
    snapshots.append(df)

mem = pd.concat(snapshots, ignore_index=True)
mem.columns = [c.lower().replace(" ", "_").replace("%", "pct")
               for c in mem.columns]

universe = (mem.assign(ticker=lambda x: x["index_member"] + " Equity")
              .loc[:, ["asof", "ticker", "pct_weight"]])
```

Now `universe` is a long DataFrame with a row per (month-end, ticker).
Delisted names appear in past months but drop out later.

## Step 2 — Pull factors at each rebalance date

We want each month-end's factor values frozen at that month-end.

### Value factors

```python
def pull_value(asof_str, tickers):
    flds = ["BEST_PE_RATIO",          # forward P/E
            "PX_TO_BOOK_RATIO",
            "PX_TO_SALES_RATIO",
            "EV_TO_T12M_EBITDA",
            "EQY_DVD_YLD_12M",
            "EARN_YLD"]                # = 1 / TRAIL P/E
    return blp.bdp(tickers, flds,
                   BEST_FPERIOD_OVERRIDE="1BF",          # blended forward
                   BEST_DATA_RELEASE_DT=asof_str,
                   EQY_FUND_RELATIVE_PERIOD="-1Q",
                   FUND_PER_END_DT=asof_str)
```

`BEST_DATA_RELEASE_DT` is the magic ingredient — without it you get
*current* consensus, not the consensus that existed at the
rebalance date.

### Quality factors

```python
def pull_quality(asof_str, tickers):
    flds = ["RETURN_COM_EQY",          # ROE
            "RETURN_ON_ASSETS",
            "RETURN_ON_INV_CAPITAL",
            "OPER_MARGIN",
            "GROSS_MARGIN",
            "BS_TOT_ASSET",
            "NET_DEBT",                 # leverage
            "BS_TOTAL_EQUITY",
            "CF_FREE_CASH_FLOW",
            "TRAIL_12M_NET_INC",
            "TRAIL_12M_FREE_CASH_FLOW"]
    return blp.bdp(tickers, flds,
                   FUND_PER="A",
                   EQY_FUND_RELATIVE_PERIOD="-1A",
                   EQY_FUND_CRNCY="EUR")
```

### Momentum factors

```python
def pull_momentum(asof_str, tickers):
    end = pd.to_datetime(asof_str)
    start_12m = (end - pd.DateOffset(months=12)).strftime("%Y-%m-%d")
    start_1m  = (end - pd.DateOffset(months=1)).strftime("%Y-%m-%d")

    p = blp.bdh(tickers, ["TOT_RETURN_INDEX_GROSS_DVDS"],
                start_12m, end.strftime("%Y-%m-%d"),
                Per="D", Fill="P")
    p.columns = p.columns.droplevel(1)
    ret_12m = p.iloc[-1] / p.iloc[0] - 1
    ret_1m  = p.iloc[-1] / p[p.index >= start_1m].iloc[0] - 1
    return pd.DataFrame({
        "ret_12_1": ret_12m - ret_1m,        # 12m skip-1m momentum
        "ret_1m":   ret_1m,
    })
```

### Size

```python
def pull_size(asof_str, tickers):
    return blp.bdp(tickers, ["CUR_MKT_CAP", "EQY_FLOAT_MKT_CAP"],
                   EQY_FUND_CRNCY="EUR")
```

### Volatility / risk

```python
def pull_risk(asof_str, tickers):
    return blp.bdp(tickers, ["HISTORICAL_VOLATILITY_60D",
                             "HISTORICAL_VOLATILITY_260D",
                             "EQY_BETA_RAW"])
```

## Step 3 — Stitch into a panel

```python
panels = []
for asof, group in universe.groupby("asof"):
    asof_str = asof.strftime("%Y%m%d")
    tkrs = group.ticker.tolist()
    if not tkrs:
        continue
    val = pull_value(asof_str, tkrs)
    qua = pull_quality(asof_str, tkrs)
    mom = pull_momentum(asof_str, tkrs)
    siz = pull_size(asof_str, tkrs)
    rsk = pull_risk(asof_str, tkrs)
    p = pd.concat([val, qua, mom, siz, rsk], axis=1)
    p["asof"] = asof
    p["ticker"] = p.index
    panels.append(p)

panel = pd.concat(panels, ignore_index=True)
```

This is `O(rebalance_dates × tickers)` BBG hits — for monthly over
10 years on Stoxx 600 you're looking at 12 × 11 × 600 × ~30 fields
= ~2.4M data points. Cache aggressively.

## Step 4 — Cross-sectional standardisation

```python
def winsorize_z(s):
    s = s.clip(s.quantile(0.01), s.quantile(0.99))
    return (s - s.mean()) / s.std()

# Per-date z-scores
for col in ["best_pe_ratio", "px_to_book_ratio", "ev_to_t12m_ebitda",
            "eqy_dvd_yld_12m", "earn_yld",
            "return_com_eqy", "return_on_inv_capital",
            "ret_12_1", "ret_1m",
            "cur_mkt_cap", "historical_volatility_260d"]:
    panel[f"z_{col}"] = panel.groupby("asof")[col].transform(winsorize_z)
```

Note: invert sign for "lower is better" factors (P/E, P/B, P/S, EV/EBITDA,
vol) before combining.

```python
panel["z_pe_inv"]      = -panel["z_best_pe_ratio"]
panel["z_pb_inv"]      = -panel["z_px_to_book_ratio"]
panel["z_evebitda_inv"]= -panel["z_ev_to_t12m_ebitda"]
panel["z_size_inv"]    = -panel["z_cur_mkt_cap"]
panel["z_vol_inv"]     = -panel["z_historical_volatility_260d"]

panel["value_score"]   = panel[["z_pe_inv","z_pb_inv","z_evebitda_inv",
                                "z_eqy_dvd_yld_12m","z_earn_yld"]].mean(axis=1)
panel["quality_score"] = panel[["z_return_com_eqy","z_return_on_inv_capital"]].mean(axis=1)
panel["momentum_score"]= panel[["z_ret_12_1"]]
```

## Step 5 — Backtest

```python
# Forward 1m return on each rebalance
panel = panel.sort_values(["ticker", "asof"])
panel["fwd_ret_1m"] = panel.groupby("ticker")["asof"].transform(
    lambda dates: dates.shift(-1).map(lambda d: ...))   # join to prices
```

Better: pre-pull a wide return panel and merge.

```python
all_tickers = sorted(panel.ticker.unique())
prc = blp.bdh(all_tickers, ["TOT_RETURN_INDEX_GROSS_DVDS"],
              "2014-12-01", "2025-12-31", Per="M", Fill="P")
prc.columns = prc.columns.droplevel(1)
ret_m = prc.pct_change().shift(-1)        # forward 1m return

panel["fwd_ret_1m"] = panel.apply(
    lambda r: ret_m.loc[r.asof, r.ticker]
              if (r.asof in ret_m.index and r.ticker in ret_m.columns)
              else None, axis=1)
```

## Step 6 — Decile portfolios

```python
panel["v_decile"] = panel.groupby("asof")["value_score"].transform(
    lambda s: pd.qcut(s, 10, labels=False, duplicates="drop"))

results = panel.dropna(subset=["fwd_ret_1m","v_decile"]).groupby(
    ["asof","v_decile"])["fwd_ret_1m"].mean().unstack()
results["L-S"] = results[9] - results[0]
results.cumsum().plot()
```

## Step 7 — Cache

The right caching scheme keys on `(asof, panel_definition_hash)` →
parquet. Then re-runs become instant.

```python
import json, hashlib
def panel_key(asof, fields, universe_hash):
    h = hashlib.sha1(json.dumps([asof, fields, universe_hash],
                                default=str, sort_keys=True).encode()).hexdigest()[:12]
    return f"./.cache/panel_{h}.parquet"
```

## Field reference for this recipe

| Field | Use |
|---|---|
| `INDX_MWEIGHT_HIST` | Historical index members + weights |
| `BEST_PE_RATIO`, `BEST_DATA_RELEASE_DT` | Forward P/E (PIT) |
| `PX_TO_BOOK_RATIO` | P/B |
| `EV_TO_T12M_EBITDA` | EV/EBITDA |
| `EQY_DVD_YLD_12M` | Trailing dividend yield |
| `RETURN_COM_EQY`, `RETURN_ON_INV_CAPITAL` | Quality |
| `OPER_MARGIN`, `GROSS_MARGIN` | Quality |
| `TOT_RETURN_INDEX_GROSS_DVDS` | Returns / momentum |
| `CUR_MKT_CAP` | Size |
| `HISTORICAL_VOLATILITY_*` | Vol / low-vol factor |
| `EQY_BETA_RAW` | Beta |

## Pitfalls

- **Look-ahead in fundamentals**: `BS_TOT_ASSET` for "now" is the
  *latest reported*. If a Q4 2023 release comes out March 2024, that
  value won't be available for a Feb 2024 rebalance. Use
  `LATEST_ANNOUNCEMENT_DT` to filter.
- **Look-ahead in estimates**: always set `BEST_DATA_RELEASE_DT`.
- **Currency drift**: make sure all market-cap-like factors are in a
  consistent currency (`EQY_FUND_CRNCY=EUR`).
- **Sector neutralisation**: cross-section z-scores by sector
  (`GICS_SECTOR_NAME`) for cleaner factor isolation.
- **Universe churn**: ensure dropped names exit after the rebalance,
  not at re-entry. Match on `(asof, ticker)` strictly.
- **Total return for delisted names**: `TOT_RETURN_INDEX_GROSS_DVDS`
  continues until the delisting date and then NaN. Don't backfill
  with last close — count it as the actual delisting return (which
  may be zero if the company went bankrupt).
