# Recipe · Credit Spreads (CDS + cash)

End-to-end: pull issuer-level CDS curves, cash-bond OAS / Z-spread,
and benchmark-relative credit measures.

## Step 1 — Pick issuers and tenors

Two ways: a curated list or a screen.

```python
ISSUERS = [
    ("Telefonica",   "TEFE", "EUR"),
    ("EDP",          "EDPPL","EUR"),
    ("Iberdrola",    "IBE",  "EUR"),
    ("Total",        "TOTAL","EUR"),
    ("Volkswagen",   "VWAGY","EUR"),
    ("BMW",          "BMW",  "EUR"),
    ("Daimler/Mercedes","MBG", "EUR"),
    ("Banco Santander","SANTAN","EUR"),
    ("BBVA",         "BBVASM","EUR"),
    ("Glencore",     "GLEN", "USD"),
    ("Anglo American","AAL",  "USD"),
    ("Apple",        "AAPL", "USD"),
    ("Microsoft",    "MSFT", "USD"),
    ("JPMorgan",     "JPM",  "USD"),
    ("Goldman",      "GS",   "USD"),
]
TENORS = ["1Y", "3Y", "5Y", "7Y", "10Y"]

cds_tickers = [
    f"{issuer} CDS {ccy} SR {t} D14 Corp"
    for _, issuer, ccy in ISSUERS for t in TENORS
]
```

## Step 2 — Snapshot CDS curves

```python
snap = blp.bdp(cds_tickers,
               ["PX_LAST", "CDS_QUOTE_TYPE",
                "CDS_RECOVERY_RATE", "CDS_DV01"])

# Reshape to a wide curve panel
import pandas as pd, re
def parse(t):
    m = re.match(r"(\S+) CDS (\w+) SR (\w+) D14 Corp", t)
    return pd.Series(dict(issuer=m.group(1), ccy=m.group(2),
                          tenor=m.group(3))) if m else pd.Series()

snap = snap.merge(snap.index.to_series().apply(parse), left_index=True,
                  right_index=True)

curve = snap.pivot_table(index=["issuer","ccy"], columns="tenor",
                         values="PX_LAST")
curve = curve[TENORS]
```

## Step 3 — CDS history

```python
hist = blp.bdh(cds_tickers, ["PX_LAST"], "2018-01-01", "2025-12-31",
               periodicitySelection="DAILY",
               nonTradingDayFillOption="NON_TRADING_WEEKDAYS",
               nonTradingDayFillMethod="PREVIOUS_VALUE")
hist.columns = hist.columns.droplevel(1)
```

## Step 4 — Sovereign and index spread context

```python
SOVEREIGNS = {
    "Italy":     "ITALY CDS USD SR 5Y D14 Corp",
    "Spain":     "SPAIN CDS USD SR 5Y D14 Corp",
    "Portugal":  "PORTUG CDS USD SR 5Y D14 Corp",
    "Greece":    "GREECE CDS USD SR 5Y D14 Corp",
    "France":    "FRANCE CDS USD SR 5Y D14 Corp",
    "Germany":   "DBR CDS USD SR 5Y D14 Corp",
    "UK":        "UKIN CDS USD SR 5Y D14 Corp",
    "US":        "USGB CDS USD SR 5Y D14 Corp",
    "Brazil":    "BRAZIL CDS USD SR 5Y D14 Corp",
    "Mexico":    "MEX CDS USD SR 5Y D14 Corp",
    "Turkey":    "TURKEY CDS USD SR 5Y D14 Corp",
    "China":     "CHINA CDS USD SR 5Y D14 Corp",
}

INDICES = {
    "iTraxx Main":      "ITRX MAIN CDSI GEN 5Y Corp",
    "iTraxx Crossover": "ITRX XOVER CDSI GEN 5Y Corp",
    "iTraxx Senior Fin":"ITRX SNRFIN CDSI GEN 5Y Corp",
    "CDX IG":           "CDX IG CDSI GEN 5Y Corp",
    "CDX HY":           "CDX HY CDSI GEN 5Y Corp",
    "CDX EM":           "CDX EM CDSI GEN 5Y Corp",
}
```

`CDSI GEN` returns the on-the-run series (auto-rolls).

## Step 5 — Cash bond spreads (asset-swap, Z-spread, OAS)

For a portfolio of EUR corporates:

```python
EUR_BONDS = [
    "EDP 1 ⅞ 03/14/35 Corp",
    "TEFE 0.875 04/02/27 Corp",
    "VW 1.625 02/16/30 Corp",
    "BMW 0.5 11/06/27 Corp",
    "IBESM 1.625 03/15/30 Corp",
]

spreads = blp.bdp(EUR_BONDS,
    ["PX_LAST", "YLD_YTM_MID",
     "G_SPRD_MID",      # spread to govt
     "I_SPRD_MID",      # spread to swap (interpolated)
     "Z_SPRD_MID",      # zero-volatility
     "OAS_SPREAD_MID",  # OAS over swap curve
     "ASSET_SWAP_SPD_MID",
     "DUR_ADJ_MID",
     "RTG_BB_COMPOSITE",
     "MATURITY"])
```

## Step 6 — CDS-cash basis

```python
# Compute basis: CDS_5Y − Z_spread of a similar-maturity bond (in bps)
import numpy as np
cds_5y = blp.bdp(["EDPPL CDS EUR SR 5Y D14 Corp"], ["PX_LAST"]).iloc[0,0]
bond_z = blp.bdp(["EDP 1 ⅞ 03/14/35 Corp"], ["Z_SPRD_MID"]).iloc[0,0]
basis_bp = cds_5y - bond_z
```

Negative basis → bond looks rich vs CDS (or CDS cheap), positive →
opposite.

## Step 7 — Issuer rating + composite

```python
ISSUERS_LIST = ["EDP", "TEFE", "IBESM", "JPM", "GS"]
# Most-recent issuer-level rating fields are on debt, not equity.
# Pull via a representative bond and back-resolve issuer:
ratings = blp.bdp(EUR_BONDS,
    ["RTG_MOODY","RTG_SP","RTG_FITCH","RTG_BB_COMPOSITE",
     "RTG_BB_DEFAULT_PROB", "DEFAULT_PROBABILITY",
     "ISSUER","ISSUER_INDUSTRY"])
```

## Step 8 — Pre-built credit indices for backtesting

```python
INDICES_TR = [
    "LECCTREU Index",   # Euro Aggregate Corporate TR
    "LF98TREU Index",   # Euro HY 100 TR
    "LP01TRGB Index",   # GBP Treasury TR
    "LP02TRGB Index",   # GBP IG TR
    "G0Q0 Index",       # ICE BofA US Corp TR
    "H0A0 Index",       # ICE BofA US HY TR
    "ER00 Index",       # ICE BofA Euro Corp
    "HE00 Index",       # ICE BofA Euro HY
    "JCEMCM Index",     # CEMBI Composite TR
    "JPEIDIVR Index",   # EMBI Global Diversified
]

idx_hist = blp.bdh(INDICES_TR, ["PX_LAST", "OAS_SPREAD_MID"],
                   "2010-01-01", "2025-12-31",
                   periodicitySelection="DAILY")
```

## Step 9 — High-yield distress monitor

```python
# CDX HY mid + percent of names trading wide of 1000bp
hy_index = "CDX HY CDSI GEN 5Y Corp"
hy_constituents = blp.bds(hy_index, "INDX_MEMBERS")
member_tickers = [m["Member Ticker and Exchange Code"] + " Corp"
                  for m in hy_constituents]
member_spreads = blp.bdp(member_tickers, ["PX_LAST"])
distress_pct = (member_spreads.PX_LAST > 1000).mean()
```

## Field reference for this recipe

| Field | Use |
|---|---|
| `PX_LAST` (CDS) | Par-spread (bps) or upfront (%) — check `CDS_QUOTE_TYPE` |
| `CDS_QUOTE_TYPE` | `Par Spread` or `Upfront` |
| `CDS_RECOVERY_RATE` | Default 40% SR / 25% SUB |
| `CDS_DV01`, `RISKY_DUR` | Sensitivity, duration |
| `CDS_FAIR_SPREAD` | Model-implied (use sparingly) |
| `Z_SPRD_MID`, `I_SPRD_MID`, `G_SPRD_MID` | Cash bond spreads |
| `OAS_SPREAD_MID` | OAS over swap curve |
| `ASSET_SWAP_SPD_MID` | ASW |
| `DUR_ADJ_MID`, `MOD_DUR_MID` | Bond duration |
| `RTG_*` | Ratings family |
| `DEFAULT_PROBABILITY` | Bloomberg DRSK model |
| `INDX_MEMBERS` | CDS-index constituents |

## Pitfalls

- **Quote type matters**: `PX_LAST` for `JPM CDS USD SR 5Y D14 Corp`
  is par-spread (bps). For some HY single-names with running coupon
  conventions, `PX_LAST` is upfront-points (%). `CDS_QUOTE_TYPE`
  resolves it.
- **Series rolls**: `S40` (March-25 series) goes off-the-run when
  `S41` arrives (Sept-25). Use `GEN` to track on-the-run; pin a
  specific series when modelling a trade.
- **CDS index components**: `INDX_MEMBERS` returns the *current*
  members. Past series had different memberships — consult ISDA
  series-roll documentation if you need historical composition.
- **Sovereign vs corp basis**: corp CDS usually quotes par-spread,
  sovereign CDS often quotes upfront in distressed cases. Check.
- **Default probability**: `DEFAULT_PROBABILITY` is Bloomberg's DRSK
  estimate; `BB_DEFAULT_PROB_5YR` is from CDS-implied. They differ.
- **EM CDS data quality**: many off-the-run EM tenors quote sparsely.
  Filter on `LAST_PX_DT` to avoid stale data.
- **Jump-to-default**: for CDS positions, model a discrete recovery
  payoff. Spread × duration is a small-spread approximation.
