# Recipe · FX Carry & Basis

End-to-end: build a G10 + EM FX carry panel with implied yields,
realised vol, cross-currency basis, and forward returns.

## Step 1 — Pair list

```python
G10_PAIRS = [
    "EURUSD", "USDJPY", "GBPUSD", "USDCHF",
    "AUDUSD", "NZDUSD", "USDCAD", "USDSEK", "USDNOK",
]

EM_PAIRS = [
    "USDBRL", "USDMXN", "USDCLP", "USDCOP", "USDPEN",
    "USDZAR", "USDTRY", "USDPLN", "USDHUF", "USDCZK",
    "USDKRW", "USDINR", "USDIDR", "USDPHP", "USDTHB", "USDTWD",
    "USDCNY", "USDCNH",
]

ALL_PAIRS = G10_PAIRS + EM_PAIRS
```

## Step 2 — Spot history (use a consistent fix)

```python
fix = "WMCO"   # WM/Reuters 4pm London
spot_tickers = [f"{p} {fix} Curncy" for p in ALL_PAIRS]
spot = blp.bdh(spot_tickers, ["PX_LAST"], "2010-01-01", "2025-12-31",
               periodicitySelection="DAILY",
               nonTradingDayFillOption="NON_TRADING_WEEKDAYS",
               nonTradingDayFillMethod="PREVIOUS_VALUE")
spot.columns = spot.columns.droplevel(1)
spot.columns = ALL_PAIRS    # rename to clean pair codes
```

## Step 3 — 1-month forwards

For G10, deliverable forwards. For EM (most), NDFs.

```python
fwd_tickers = [f"{p}1M Curncy" for p in ALL_PAIRS]
fwd_outright = blp.bdh(fwd_tickers, ["PX_LAST"], "2010-01-01", "2025-12-31",
                       periodicitySelection="DAILY",
                       nonTradingDayFillOption="NON_TRADING_WEEKDAYS",
                       nonTradingDayFillMethod="PREVIOUS_VALUE")
fwd_outright.columns = fwd_outright.columns.droplevel(1)
fwd_outright.columns = ALL_PAIRS
```

## Step 4 — Implied yield differential (the carry)

CIP relation:

```
F = S × (1 + r_q × t) / (1 + r_b × t)
log(F/S) ≈ (r_q − r_b) × t      (continuous, t = 1/12)
```

So the carry per month is `12 × log(F/S)` annualised, signed by
direction.

```python
import numpy as np
carry_annual = -np.log(fwd_outright / spot) * 12          # USD-base convention
# For pairs where USD is the QUOTE (e.g. EURUSD, GBPUSD, AUDUSD, NZDUSD),
# flip sign to get foreign-base carry:
USD_QUOTE = {"EURUSD","GBPUSD","AUDUSD","NZDUSD"}
for p in USD_QUOTE:
    carry_annual[p] = -carry_annual[p]
```

(Bloomberg also exposes `IMPL_YIELD_NDF_PCT` and `IMPL_DEPOSIT_RATE`
fields — useful as cross-checks.)

## Step 5 — Realised vol

```python
ret = np.log(spot / spot.shift(1))
realised_vol_60d = ret.rolling(60).std() * np.sqrt(252) * 100
```

For comparison with implied vol:

```python
ivol_tickers = [f"{p}V1M Curncy" for p in G10_PAIRS]      # ATM 1m vol
ivol = blp.bdh(ivol_tickers, ["PX_LAST"], "2010-01-01", "2025-12-31",
               periodicitySelection="DAILY")
ivol.columns = ivol.columns.droplevel(1)
ivol.columns = G10_PAIRS
```

## Step 6 — Carry-to-vol (Sharpe-like) ranking

```python
sharpe = (carry_annual / realised_vol_60d).rolling(20).mean()
top_long  = sharpe.iloc[-1].nlargest(3)        # high carry / low vol → long
top_short = sharpe.iloc[-1].nsmallest(3)       # negative carry / high vol → short
```

## Step 7 — Carry portfolio backtest

```python
def carry_portfolio(spot, carry, n_legs=3, vol_scale=True):
    # Monthly rebalance
    carry_m = carry.resample("ME").last()
    spot_m  = spot.resample("ME").last()
    ret_m   = spot_m.pct_change().shift(-1)         # forward 1m spot return

    # Rank
    ranks = carry_m.rank(axis=1)
    long_mask  = ranks > (ranks.max(axis=1) - n_legs - 0.5).values[:, None]
    short_mask = ranks <= n_legs

    # Equal-weight
    long_ret  = (ret_m * long_mask.astype(float)).sum(axis=1) / n_legs
    short_ret = (ret_m * short_mask.astype(float)).sum(axis=1) / n_legs
    pnl = long_ret - short_ret

    # Carry component (the carry you earn per month)
    carry_pnl = (carry_m * (long_mask.astype(float) - short_mask.astype(float))).sum(axis=1) / (12 * n_legs)
    return pnl, carry_pnl

pnl, carry_pnl = carry_portfolio(spot, carry_annual, n_legs=3)
```

## Step 8 — Cross-currency basis (G10 only)

CIP holds approximately for G10 pairs; deviations are the
**XCCY basis**.

```python
BASIS = {
    "EURUSD": "EUBSC10 Curncy",
    "GBPUSD": "BPBSC10 Curncy",
    "USDJPY": "JYBSC10 Curncy",
    "USDCHF": "SFBSC10 Curncy",
    "AUDUSD": "ADBSC10 Curncy",
    "NZDUSD": "NDBSC10 Curncy",
    "USDCAD": "CDBSC10 Curncy",
    "USDSEK": "SKBSC10 Curncy",
    "USDNOK": "NKBSC10 Curncy",
}
basis_h = blp.bdh(list(BASIS.values()), ["PX_LAST"],
                  "2014-01-01", "2025-12-31",
                  periodicitySelection="DAILY",
                  nonTradingDayFillOption="NON_TRADING_WEEKDAYS",
                  nonTradingDayFillMethod="PREVIOUS_VALUE")
basis_h.columns = basis_h.columns.droplevel(1)
basis_h.columns = [p for p in BASIS]
```

`PX_LAST` is in bps. Negative = USD scarce on the cross-currency
funding market.

## Step 9 — EM-specific: NDF-implied local rates

```python
# Pull IMPL_YIELD_NDF_PCT for an EM panel
em_ndf = [f"USD{c}1M Curncy" for c in
          ["BRL","MXN","KRW","INR","IDR","TRY","ZAR","PLN","HUF","COP","CLP"]]

ndf_yields = blp.bdh(em_ndf, ["IMPL_YIELD_NDF_PCT"],
                     "2014-01-01","2025-12-31",
                     periodicitySelection="DAILY")
```

## Step 10 — Carry-to-CDS overlay (sovereign credit gate)

Filter the EM long basket by sovereign CDS:

```python
em_cds = [f"{c} CDS USD SR 5Y D14 Corp"
          for c in ["BRAZIL","MEX","COLOM","CHILE","PERU",
                    "SOAF","TURKEY","INDON","PHILIP","INDIA","INDOM"]]
cds_h = blp.bdh(em_cds, ["PX_LAST"], "2014-01-01","2025-12-31",
                periodicitySelection="DAILY")
```

Rule: drop a candidate from longs if 5Y CDS > 95th percentile of its
own history.

## Field reference

| Field / ticker | Use |
|---|---|
| `<PAIR> WMCO Curncy` | Spot (WM 4pm fix) |
| `<PAIR>1M Curncy` | 1m forward outright |
| `IMPL_YIELD_NDF_PCT` | Implied local yield from NDF |
| `<PAIR>V1M Curncy` | ATM 1m vol |
| `<XX>BSC10 Curncy` | 10y XCCY basis (bps) |
| `<COUNTRY> CDS USD SR 5Y D14 Corp` | Sovereign 5Y CDS |
| `30DAY_IMPVOL_25DELTA_RR` | RR (skew measure) |
| `HISTORICAL_VOLATILITY_60D` | Realised vol |

## Pitfalls

- **Direction conventions**: USDxxx is "1 USD per xxx". For carry,
  signs depend on which currency you go long. Walk through one
  pair manually first to confirm.
- **Holiday gaps**: EM holidays differ. With `PREVIOUS_VALUE` fill,
  realised vol is biased low across long stale-quote runs.
- **Capital controls**: USDCNY is fix-managed; carry derived from it
  is artificial. Use USDCNH for offshore-tradeable carry.
- **Crisis FX vol**: USDARS, USDTRY, USDRUB blow up periodically;
  ranking/sorting rules need vol-scaling or % moves capped.
- **Rolldown vs carry**: this recipe is "1m carry only". Rolldown
  along the curve (e.g. 1m → ON) adds another 5–20% of total
  expected return, depending on shape.
- **NDF fix mismatch**: `IMPL_YIELD_NDF_PCT` uses the fix Bloomberg
  considers default. If your strategy uses a different fix (e.g.
  CFETS vs SAFE for CNY), recompute manually.
