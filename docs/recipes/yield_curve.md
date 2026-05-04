# Recipe · Yield Curves (govt + swap)

End-to-end: build daily curves for a country's sovereign + swap +
spread space. Useful for monitoring, term-structure factor models, or
RV trades.

## Step 1 — Define the node lists

Common, reusable curve definitions:

```python
US_TREASURY_NODES = [
    ("3M",  "USGG3M Index"),
    ("6M",  "USGG6M Index"),
    ("1Y",  "USGG12M Index"),
    ("2Y",  "USGG2YR Index"),
    ("3Y",  "USGG3YR Index"),
    ("5Y",  "USGG5YR Index"),
    ("7Y",  "USGG7YR Index"),
    ("10Y", "USGG10YR Index"),
    ("20Y", "USGG20YR Index"),
    ("30Y", "USGG30YR Index"),
]

US_SOFR_OIS_NODES = [
    ("ON",  "SOFRRATE Index"),
    ("1M",  "USSOC Curncy"),
    ("3M",  "USSO3 Curncy"),
    ("6M",  "USSO6 Curncy"),
    ("1Y",  "USSO1 Curncy"),
    ("2Y",  "USSO2 Curncy"),
    ("3Y",  "USSO3 Curncy"),
    ("5Y",  "USSO5 Curncy"),
    ("7Y",  "USSO7 Curncy"),
    ("10Y", "USSO10 Curncy"),
    ("15Y", "USSO15 Curncy"),
    ("20Y", "USSO20 Curncy"),
    ("30Y", "USSO30 Curncy"),
]

GERMAN_BUND_NODES = [
    ("2Y",  "GTDEM2Y Govt"),
    ("5Y",  "GTDEM5Y Govt"),
    ("10Y", "GTDEM10Y Govt"),
    ("30Y", "GTDEM30Y Govt"),
]

EUR_ESTR_OIS_NODES = [
    ("ON",  "ESTRON Index"),
    ("1M",  "EESWE1M Curncy"),
    ("3M",  "EESWE3M Curncy"),
    ("6M",  "EESWE6M Curncy"),
    ("1Y",  "EESWE1 Curncy"),
    ("2Y",  "EESWE2 Curncy"),
    ("5Y",  "EESWE5 Curncy"),
    ("10Y", "EESWE10 Curncy"),
    ("30Y", "EESWE30 Curncy"),
]
```

## Step 2 — Pull a snapshot

```python
def pull_curve(nodes):
    tickers = [t for _, t in nodes]
    snap = blp.bdp(tickers, ["PX_LAST", "PX_BID", "PX_ASK"])
    snap["tenor"] = pd.Categorical([t for t, _ in nodes],
                                   categories=[t for t, _ in nodes],
                                   ordered=True)
    snap = snap.set_index("tenor").sort_index()
    return snap

curve_us = pull_curve(US_TREASURY_NODES)
curve_us_ois = pull_curve(US_SOFR_OIS_NODES)
spread = curve_us["PX_LAST"] - curve_us_ois["PX_LAST"]   # gov-OIS spread
```

## Step 3 — Pull historical surfaces

For the time-series version of the same curve:

```python
import pandas as pd

def pull_curve_history(nodes, start, end, freq="DAILY"):
    tickers = [t for _, t in nodes]
    h = blp.bdh(tickers, ["PX_LAST"], start, end,
                periodicitySelection=freq,
                nonTradingDayFillOption="NON_TRADING_WEEKDAYS",
                nonTradingDayFillMethod="PREVIOUS_VALUE")
    h.columns = h.columns.droplevel(1)
    # Rename to tenor labels
    rename = dict(zip(tickers, [t for t, _ in nodes]))
    h = h.rename(columns=rename)
    return h

us_hist = pull_curve_history(US_TREASURY_NODES,
                             "2010-01-01", "2025-12-31")
```

`us_hist` is a DataFrame indexed by date, columns by tenor. Plot:
`us_hist.iloc[-1].plot()` for the latest curve, `us_hist["10Y"].plot()`
for one tenor over time.

## Step 4 — Curve metrics

Common derived series:

```python
us_hist["2s10s"]  = us_hist["10Y"] - us_hist["2Y"]
us_hist["5s30s"]  = us_hist["30Y"] - us_hist["5Y"]
us_hist["2s5s10s"] = 2*us_hist["5Y"] - us_hist["2Y"] - us_hist["10Y"]
                                                          # butterfly
us_hist["3m10s"]  = us_hist["10Y"] - us_hist["3M"]        # NY Fed spread
```

Term-premium-style decomposition (rough):

```python
# Subtract OIS to isolate term premium / convexity
ois_hist = pull_curve_history(US_SOFR_OIS_NODES,
                              "2010-01-01", "2025-12-31")

tp_proxy = us_hist["10Y"] - ois_hist["10Y"]
```

## Step 5 — PCA decomposition (level / slope / curvature)

```python
import numpy as np
from sklearn.decomposition import PCA

# Daily changes (basis points)
chg = us_hist[["2Y","5Y","10Y","30Y"]].diff().dropna() * 100  # bps

pca = PCA(n_components=3).fit(chg)
loadings = pd.DataFrame(pca.components_.T,
                        index=["2Y","5Y","10Y","30Y"],
                        columns=["PC1_level","PC2_slope","PC3_curve"])
print(loadings)
print(pca.explained_variance_ratio_)
```

Typically: PC1 ≈ parallel shift (~80%+), PC2 ≈ steepening, PC3 ≈
curvature.

## Step 6 — Periphery-vs-Bund spread tracker (Eurozone)

```python
COUNTRIES = {
    "France":   "GTFRF10Y Govt",
    "Italy":    "GTITL10Y Govt",
    "Spain":    "GTESP10Y Govt",
    "Portugal": "GTPTE10Y Govt",
    "Greece":   "GTGRD10Y Govt",
    "Belgium":  "GTBEF10Y Govt",
    "Netherlands": "GTNLG10Y Govt",
    "Austria":  "GTATS10Y Govt",
    "Ireland":  "GTIEP10Y Govt",
}
bund = "GTDEM10Y Govt"

tickers = [bund] + list(COUNTRIES.values())
yields = blp.bdh(tickers, ["PX_LAST"], "2010-01-01", "2025-12-31",
                 periodicitySelection="DAILY",
                 nonTradingDayFillOption="NON_TRADING_WEEKDAYS",
                 nonTradingDayFillMethod="PREVIOUS_VALUE")
yields.columns = yields.columns.droplevel(1)

spreads = pd.DataFrame({
    name: (yields[t] - yields[bund]) * 100   # bps
    for name, t in COUNTRIES.items()
})
spreads.tail()
```

## Step 7 — Forward rates

For an OIS curve, forward rates are simple to compute via the
discount factor:

```python
# Tenors as fractions of a year
tenor_yrs = {"1Y":1, "2Y":2, "3Y":3, "5Y":5, "7Y":7, "10Y":10,
             "15Y":15, "20Y":20, "30Y":30}

def ois_to_df(rates_pct, tenor_yrs):
    """Convert OIS par yields to discount factors (annual compounding)."""
    return {t: (1 + r/100) ** -tenor_yrs[t] for t, r in rates_pct.items()}

def forward(df1, df2, t1, t2):
    """Forward rate between t1 and t2 (annual)."""
    return ((df1 / df2) ** (1.0 / (t2 - t1)) - 1) * 100

snap = curve_us_ois["PX_LAST"]
df = ois_to_df(snap.to_dict(), tenor_yrs)
fwd_5y5y = forward(df["5Y"], df["10Y"], 5, 10)
fwd_5y10y = forward(df["5Y"], df["15Y"], 5, 15)
```

## Step 8 — Inflation breakevens

```python
BREAKEVENS = {
    "US":      ("USGG10YR Index", "USGGT10Y Index"),     # nominal, real
    "Germany": ("GTDEM10Y Govt",  "GTDEMI10Y Govt"),
    "UK":      ("GTGBP10Y Govt",  "GTGBII10Y Govt"),
    "France":  ("GTFRF10Y Govt",  "GTFRI10Y Govt"),
    "Italy":   ("GTITL10Y Govt",  "GTITLI10Y Govt"),
    "Japan":   ("GTJPY10Y Govt",  "GTJGBI10Y Govt"),
}

bes = {}
for country, (nom, real) in BREAKEVENS.items():
    h = blp.bdh([nom, real], ["PX_LAST"], "2014-01-01", "2025-12-31",
                periodicitySelection="DAILY")
    h.columns = h.columns.droplevel(1)
    bes[country] = h[nom] - h[real]

bes = pd.DataFrame(bes)
```

Or use the **pre-built breakeven series** when available:

```
USGGBE10 Index            US 10y breakeven (BBG-published)
USGGBE05 Index            US 5y breakeven
EURGGBE10 Index            Eurozone 10y BE
GUKGGBE10 Index            UK 10y BE
JPGGTBE10 Index            JP 10y BE
```

## Field reference for this recipe

| Field / ticker pattern | Use |
|---|---|
| `GT<CCY><TENOR> Govt` | Generic on-the-run benchmarks |
| `USGG<TENOR> Index` | US Fed-published yields |
| `<CCY>SO<TENOR> Curncy`, `EESWE<TENOR>`, `BPSO<TENOR>` | OIS swap nodes |
| `GTDEMI10Y Govt`, `USGGT10Y Index` | Real-yield linkers |
| `USGGBE10 Index` | Pre-baked breakeven |
| `PX_LAST` | Yield (in %) for govt; rate for OIS |

## Pitfalls

- **Generic tickers roll**: `GT10 Govt` is whichever issue is
  currently on-the-run. The yield series has discrete drops on each
  roll. For benchmark research it's fine; for trading PnL track a
  specific CUSIP.
- **Day-count conventions**: forward rate calculations need correct
  day counts (ACT/360, ACT/365, 30/360). Pull `DAY_CNT_DES` if precise.
- **Holiday gaps**: with `NON_TRADING_WEEKDAYS`, the curve is
  forward-filled across closed days. Mind US/EU/UK holiday mismatches
  when comparing across markets.
- **Negative-yield era**: pre-2022 European yields were negative;
  some normalisations and log transforms break.
- **ESTR vs EONIA**: pre-Oct 2022 use EONIA; post that, €STR (with a
  -8.5bp legacy spread). Splice carefully.
- **Linker quoting**: real yields are quoted negative when nominal
  + breakeven > nominal — check sign before plugging into a model.
