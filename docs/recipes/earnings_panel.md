# Recipe · Earnings Panel for PEAD

End-to-end pipeline for a quarterly earnings panel:
universe → announcement dates → reported / estimate EPS → SUE →
post-announcement returns.

## Step 1 — Define the universe

Two clean ways:

```python
# (a) Members of an index, point-in-time
members = blp.bds("PSI20 Index", "INDX_MEMBERS")
tickers = [m["Member Ticker and Exchange Code"] + " Equity"
           for m in members]

# (b) Saved EQS screen (preferred: survives membership churn if you re-pull)
universe = blp.beqs("PSI20_AllShare_Liquid", typ="PRIVATE")
tickers  = universe.index.tolist()
```

For survivor-bias-free panels, pull `INDX_MWEIGHT_HIST` for the
universe at the start of each year and union — see
[factor_panel.md](factor_panel.md) for the full "history-aware"
pattern.

## Step 2 — Pull announcement dates with reported EPS

```python
import pandas as pd

frames = []
for tkr in tickers:
    h = blp.bds(tkr, "EARN_ANN_DT_TIME_HIST_WITH_EPS")
    if h.empty:
        continue
    h["ticker"] = tkr
    frames.append(h)

panel = pd.concat(frames, ignore_index=True)
panel.columns = [c.lower().replace(" ", "_") for c in panel.columns]

# Schema (typical, may vary by version of xbbg):
# announcement_date | announcement_time | period | reported_eps |
# estimated_eps | surprise_(%) | comparable_eps | sales_reported |
# sales_estimate | ticker
```

Notes:

- `announcement_time` is `AMC` (after-market close), `BMO` (before
  market open), or HH:MM. Use it to align the next trading day.
- `period` is in the local fiscal-year nomenclature
  (e.g. `Q1 2024`, `FY 2023`). Convert to fiscal-quarter end-date with
  a small mapping you build once.
- `surprise_(%)` is Bloomberg's pre-baked metric; recompute if you
  want a custom denominator (mean abs, stdev, etc.).

## Step 3 — Compute SUE (standardized unexpected earnings)

```python
# Pull rolling estimate dispersion at the announcement date
surprise = []
for _, row in panel.iterrows():
    ovr = {"BEST_DATA_RELEASE_DT": row.announcement_date.strftime("%Y%m%d"),
           "BEST_FPERIOD_OVERRIDE": "1FQ"}
    s = blp.bdp([row.ticker], ["BEST_EPS", "BEST_EPS_STDEV",
                               "BEST_EPS_NUMEST"], **ovr)
    surprise.append(s.iloc[0])
disp = pd.DataFrame(surprise).reset_index(drop=True)
panel = pd.concat([panel.reset_index(drop=True), disp], axis=1)

panel["sue"] = (panel.reported_eps - panel.best_eps) / panel.best_eps_stdev
```

Two important caveats:

1. **Point-in-time consensus**: `BEST_DATA_RELEASE_DT` snapshots the
   consensus *as of* that date — without it you get current
   consensus, which is contaminated.
2. **Fiscal quarter alignment**: `BEST_FPERIOD_OVERRIDE=1FQ` is the
   *next* fiscal quarter from the snapshot date. Confirm the period
   matches the announcement period.

## Step 4 — Map announcement to a clean event-date

Apply BMO/AMC rules:

```python
import pandas as pd
from pandas.tseries.offsets import BDay

def event_date(row):
    d = pd.to_datetime(row.announcement_date)
    if str(row.announcement_time).startswith("AMC"):
        return d + BDay(1)
    if str(row.announcement_time).startswith("BMO"):
        return d
    # If a clock time, treat as same day if before 09:30, else next BD
    try:
        hhmm = str(row.announcement_time).split()[0]
        h, m = map(int, hhmm.split(":"))
        return d if (h, m) < (9, 30) else d + BDay(1)
    except Exception:
        return d + BDay(1)

panel["event_date"] = panel.apply(event_date, axis=1)
```

## Step 5 — Pull post-announcement returns

```python
# Build a list of (ticker, start, end) windows
panel["t_minus_1"] = panel["event_date"] - BDay(1)
panel["t_plus_1"]  = panel["event_date"] + BDay(1)
panel["t_plus_5"]  = panel["event_date"] + BDay(5)
panel["t_plus_60"] = panel["event_date"] + BDay(60)

# Pull total-return series wide enough to cover all windows
start = panel["t_minus_1"].min().strftime("%Y-%m-%d")
end   = panel["t_plus_60"].max().strftime("%Y-%m-%d")

prices = blp.bdh(tickers, ["TOT_RETURN_INDEX_GROSS_DVDS"],
                 start, end, Per="D",
                 Fill="P")  # forward fill non-trading days
prices.columns = prices.columns.droplevel(1)

def cum_return(ticker, d0, d1):
    s = prices[ticker]
    a, b = s.asof(d0), s.asof(d1)
    return (b / a - 1) if pd.notna(a) and pd.notna(b) else None

for w in ["t_plus_1", "t_plus_5", "t_plus_60"]:
    panel[f"car_{w}"] = panel.apply(
        lambda r: cum_return(r.ticker, r.t_minus_1, r[w]), axis=1)
```

## Step 6 — Benchmark-adjust (optional)

```python
bench = blp.bdh(["PSI20 Index"], ["TOT_RETURN_INDEX_GROSS_DVDS"],
                start, end, Per="D", Fill="P")
bench = bench["PSI20 Index"]["TOT_RETURN_INDEX_GROSS_DVDS"]

def excess_return(ticker, d0, d1):
    s = prices[ticker]
    aS, bS = s.asof(d0), s.asof(d1)
    aB, bB = bench.asof(d0), bench.asof(d1)
    if any(pd.isna(v) for v in (aS, bS, aB, bB)):
        return None
    return (bS/aS) - (bB/aB)

panel["car_excl_5"]  = panel.apply(
    lambda r: excess_return(r.ticker, r.t_minus_1, r.t_plus_5), axis=1)
```

## Step 7 — Sort into deciles, report

```python
panel["sue_decile"] = pd.qcut(panel.sue, 10, labels=False, duplicates="drop")
summary = panel.groupby("sue_decile").agg(
    n=("car_excl_5", "size"),
    mean_car_5=("car_excl_5", "mean"),
    mean_car_60=("car_t_plus_60", "mean"),
    median_car_5=("car_excl_5", "median"))
print(summary)
```

The "PEAD" pattern: top decile drifts positive over weeks; bottom
decile drifts negative.

## Caching

This pipeline asks for ~thousands of `bds` and a ~few hundred `bdh`
hits. Without caching you'll burn through the daily limit fast. The
two big wins:

1. Cache `EARN_ANN_DT_TIME_HIST_WITH_EPS` per ticker — it changes
   only after the next earnings call.
2. Cache `BEST_EPS` snapshots per `(ticker, announcement_date)` —
   they never change after the date passes.

Both are perfect parquet candidates with a (ticker, period) primary
key.

## Field reference for this recipe

| Field | Used for |
|---|---|
| `EARN_ANN_DT_TIME_HIST_WITH_EPS` | Announcement schedule + actuals |
| `BEST_EPS` | Consensus EPS estimate (point-in-time) |
| `BEST_EPS_STDEV` | Estimate dispersion (denom of SUE) |
| `BEST_EPS_NUMEST` | Number of estimates |
| `TOT_RETURN_INDEX_GROSS_DVDS` | Adjusted total return |
| `INDX_MEMBERS_HIST` | Survivor-bias-free universe |

Override reference:

| Override | Value |
|---|---|
| `BEST_DATA_RELEASE_DT` | YYYYMMDD; pin to announcement-1 for clean PIT |
| `BEST_FPERIOD_OVERRIDE` | `1FQ` (next quarter), `2FQ`, `1FY` |
| `EQY_FUND_CRNCY` | If you want consistent currency |
| `END_DATE_OVERRIDE` | For `INDX_MWEIGHT_HIST` membership |

## Pitfalls

- **AMC / BMO**: Bloomberg sometimes records `Time Not Supplied` —
  treat as AMC (skip same-day) by default.
- **Multi-class shares**: report once per issuer. Use
  `EQY_FUND_TICKER` to dedupe.
- **Restated earnings**: `EARN_ANN_DT_TIME_HIST_WITH_EPS` reflects
  the *latest* values, including post-restatements. For PIT-correct
  surprise you want the originally-reported figure — use
  `OPER_EPS_NA_AS_REPORTED_OF_PER_END` with date overrides.
- **Pre-announcements**: companies sometimes pre-announce; the
  "announcement date" is the formal earnings call. Pre-announcements
  show up under `LAST_ANNOUNCEMENT_DT` separately.
- **Special items**: `IS_EPS` includes them; `IS_DIL_EPS_CONT_OPS`
  doesn't. Choose one definition and stick with it across reported
  and estimated.
