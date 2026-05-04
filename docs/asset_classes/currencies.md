# Currencies (FX)

Yellow key: `Curncy`. Spot, forwards, NDFs, crosses, money-market
rates, OIS rates, FX vol — all under `Curncy`.

## Spot

Six-letter ISO pairs, base then quote:

```
EURUSD Curncy             1 EUR = X USD
GBPUSD Curncy             cable
USDJPY Curncy
USDCHF Curncy
AUDUSD Curncy
NZDUSD Curncy
USDCAD Curncy

EURGBP Curncy             cross
EURJPY Curncy
GBPJPY Curncy
EURCHF Curncy
```

EM majors:

```
USDCNY Curncy             onshore yuan (PBoC fix-driven)
USDCNH Curncy             offshore yuan (HK)
USDHKD Curncy
USDSGD Curncy, USDTWD Curncy, USDKRW Curncy,
USDINR Curncy, USDIDR Curncy, USDMYR Curncy, USDPHP Curncy, USDTHB Curncy, USDVND Curncy

USDBRL Curncy, USDMXN Curncy, USDARS Curncy, USDCLP Curncy, USDCOP Curncy, USDPEN Curncy, USDUYU Curncy

USDZAR Curncy, USDTRY Curncy, USDRUB Curncy, USDPLN Curncy,
USDCZK Curncy, USDHUF Curncy, USDRON Curncy,
USDILS Curncy, USDAED Curncy, USDSAR Curncy, USDEGP Curncy
```

### Pricing source matters

For FX you'll often see different sources behind the same pair:

| Source | What it is |
|---|---|
| `BGN` | Bloomberg Generic — composite from quote contributors (default for most pairs) |
| `CMPN` / `CMPL` | Composite New York / London close |
| `WMCO` | WM/Reuters fix (4pm London) |
| `BFIX` | Bloomberg FX fix |
| `EBS` | EBS interbank |
| `ECB` | ECB reference rates |
| `BFXR` | Bloomberg FX Reference |

Override via the `pricingSource` element, or explicit ticker like
`EURUSD CMPL Curncy`, `EURUSD BFIX Curncy`.

For point-in-time research, **WM/Reuters 4pm London fix** is the
standard:

```
EURUSD WMCO Curncy
USDJPY WMCO Curncy
```

## Snapshot fields

```
PX_LAST                   spot mid (depending on source)
PX_BID, PX_ASK
LAST_TRADE_DATE
PRICING_SOURCE
LAST_PX_DT
PX_OPEN, PX_HIGH, PX_LOW, PX_CLOSE_1D
HIGH_52WEEK, LOW_52WEEK
PX_VOLUME                 NA for FX (no centralized exchange)
```

## Forwards

### Outright forward rate

Append a tenor to the pair:

```
EURUSD1W Curncy           1-week outright
EURUSD1M Curncy           1-month
EURUSD3M Curncy
EURUSD6M Curncy
EURUSD9M Curncy
EURUSD1Y Curncy
EURUSD2Y Curncy           2-year
EURUSD18M Curncy
EURUSD2W Curncy
```

Tenors: `ON`, `TN`, `SN`, `1W`, `2W`, `3W`, `1M`, `2M`, `3M`, `4M`,
`5M`, `6M`, `9M`, `1Y`, `18M`, `2Y`, `3Y`, `5Y`, `10Y`.

`PX_LAST` returns the **outright** rate (= spot + points / 10^N).

### Forward points

Some workflows want the *points*, not the outright. Different ticker
prefix:

```
EUR1M Curncy              EUR/USD 1m forward points (NDF-style)
EUR3M Curncy
GBP3M Curncy
USDJPY3M Curncy           reads the whole pair's points
```

Or explicit field on the outright:

```
FWD_POINTS, FWD_BID, FWD_ASK,
PX_LAST_NDF, IMPLIED_YIELD_PCT
```

## NDFs (non-deliverable forwards)

For non-convertible / capital-controlled currencies, forwards are
non-deliverable. Bloomberg uses the same ticker pattern but with
explicit NDF fix conventions:

```
USDCNY1M Curncy           CFETS fixing, settlement vs CFETS
USDCNY+1M Curncy          alternative explicit NDF
USDINR1M Curncy           RBI-fix-based NDF
USDBRL1M Curncy           PTAX-fix
USDKRW1M Curncy           SAS / KFTC fix
USDIDR1M Curncy           ABS / JISDOR fix
USDPHP1M Curncy
USDTWD1M Curncy
USDARS1M Curncy
USDCLP1M Curncy
USDCOP1M Curncy
USDEGP1M Curncy
USDNGN1M Curncy
```

NDF-specific fields:

```
NDF_FIX_DATE, NDF_FIX_RATE,
NDF_VAL_DT, NDF_FIX_SOURCE,
IMPL_YIELD_NDF_PCT
```

For the implied carry on an NDF curve, the panel of
`IMPL_YIELD_NDF_PCT` across tenors gives you the local rate.

## Money-market rates and IOR / OIS

Tied to a specific benchmark:

```
SOFRRATE Index            US SOFR
ESTRON Index              EUR €STR
SONIO/N Index             GBP SONIA
TONAR Index               JPY TONA

# Older / phased-out:
US0001M Index             USD LIBOR 1m  (DEPRECATED)
US0003M Index             USD LIBOR 3m  (DEPRECATED)
US0006M Index             USD LIBOR 6m
EUR001M Index             EURIBOR 1m
EUR003M Index             EURIBOR 3m
EUR006M Index             EURIBOR 6m
BP0003M Index             GBP LIBOR (DEPRECATED)
JY0003M Index             JPY LIBOR (DEPRECATED)
```

OIS rates via swap tickers (live under `Curncy`):

```
USSO1 Curncy              SOFR OIS 1y
USSO2 Curncy, USSO5, USSO10, USSO30
USSOC Curncy              SOFR OIS spot-starting (older)
EESWE1 Curncy             €STR OIS 1y
EESWE2, EESWE5, EESWE10, EESWE30
EUSA1 Curncy              EUR swap (legacy 6M EURIBOR)
BPSWS1 Curncy             SONIA OIS legacy
SO1 Curncy                short-sterling-based old
JYSO1 Curncy              TONA OIS

# Cross-currency basis (each bar is bps over USD):
EUBSC1 Curncy, EUBSC5 Curncy, EUBSC10 Curncy
JYBSC1 Curncy, JYBSC10 Curncy
BPBSC1 Curncy, BPBSC10 Curncy
```

See [swaps.md](swaps.md) for the full curve picture.

## FX volatility

Two ways to address vol — **at-the-money straight tickers** or
**moneyness fields**.

ATM tickers:

```
EURUSDV1M Curncy          1m ATM vol
EURUSDV3M Curncy          3m
EURUSDV6M Curncy
EURUSDV1Y Curncy
USDJPYV1M Curncy
GBPUSDV3M Curncy
```

Risk reversals and butterflies:

```
EURUSD25R1M Curncy        25-delta risk reversal 1m
EURUSD25B1M Curncy        25-delta butterfly 1m
EURUSD10R1M Curncy        10-delta RR
```

Constructed surface fields on the spot ticker:

```
30DAY_IMPVOL_100.0%MNY_DF, 60DAY_IMPVOL, 90DAY_IMPVOL,
180DAY_IMPVOL, 360DAY_IMPVOL,
30DAY_IMPVOL_25DELTA_RR, 30DAY_IMPVOL_25DELTA_BF
```

## Implied vs realised

Realised vol field on a spot:

```
HISTORICAL_VOLATILITY_30D, HISTORICAL_VOLATILITY_90D
HISTORICAL_VOLATILITY_260D
```

Compare with the corresponding ATM `EURUSDV1M Curncy` for vol
risk-premium analyses.

## CIP / FX implied yields

For carry / basis-trade analytics:

```python
# 3m CIP-implied USD yield from EUR
EUR3M = bdp("EUR3M Curncy", "PX_LAST")            # forward points (e.g. 0.00125)
spot  = bdp("EURUSD Curncy", "PX_LAST")           # spot
fwd_outright = spot + EUR3M
# implied yield difference = -ln(fwd / spot) * 4
```

Or use Bloomberg's pre-baked field:

```
IMPL_YIELD_PCT, IMPL_DEPOSIT_RATE, IMPL_DEPOSIT_RATE_BID,
IMPL_DEPOSIT_RATE_ASK
```

## Crosses with explicit base currencies

Cross-rates not crossed against USD are first-class:

```
EURJPY Curncy, EURGBP Curncy, EURCHF Curncy,
GBPCHF Curncy, GBPJPY Curncy, AUDJPY Curncy,
NZDJPY Curncy, AUDCHF Curncy
EURBRL Curncy, EURTRY Curncy, EURPLN Curncy
```

For a cross that isn't directly quoted, derive it from the two USD legs
or use Bloomberg's auto-cross: `XAUEUR Curncy`, `XAGJPY Curncy`,
`USDXXX Curncy` (DXY-style).

## DXY and trade-weighted indices

```
DXY Curncy                ICE Dollar Index
EUR Curncy                ECB EUR effective (legacy)
TWBR Curncy               Bloomberg trade-weighted USD
BBDXY Index               Bloomberg Dollar Index (broader)
JPMVXYG7 Index            JPMorgan G7 FX volatility
```

## Fixings and reference rates

```
ECB37 Index               ECB EUR/USD reference rate (daily)
WMCO fix tickers          via *.WMCO Curncy
PHILREFR Index            Philippines BSP reference
RBIDIRBR Index            India RBI reference
PBOCCNY Index             China PBoC fix
```

## Calendar / settle conventions

FX uses a **T+2** convention for most G10 (T+1 for USDCAD, USDTRY,
USDRUB until a holiday); FX forwards settle on the *forward value
date*, which is **not always** spot+tenor due to holiday
adjustments. Override with:

```python
ov.setElement("fieldId", "SETTLE_DT")
ov.setElement("value", "20250506")
```

`FX_FORWARD_TENOR` override is also useful when a tenor is ambiguous
(e.g. month-end).

## Common research tasks

```python
# G10 spot history (10 years, daily WMR fix)
pairs = ["EURUSD WMCO Curncy", "USDJPY WMCO Curncy",
         "GBPUSD WMCO Curncy", "USDCHF WMCO Curncy",
         "AUDUSD WMCO Curncy", "NZDUSD WMCO Curncy",
         "USDCAD WMCO Curncy", "USDSEK WMCO Curncy",
         "USDNOK WMCO Curncy"]
hist = bdh(pairs, ["PX_LAST"], "20140101", "20251231",
           periodicitySelection="DAILY",
           nonTradingDayFillOption="ACTIVE_DAYS_ONLY")

# 3m forward points panel for EM
em = ["USDBRL3M", "USDMXN3M", "USDZAR3M", "USDTRY3M",
      "USDPLN3M", "USDIDR3M", "USDINR3M", "USDKRW3M"]
em = [t + " Curncy" for t in em]
fwd = bdp(em, ["PX_LAST", "IMPL_YIELD_NDF_PCT"])

# ATM vol surface for EURUSD
vol = bdp("EURUSD Curncy",
          ["30DAY_IMPVOL_100.0%MNY_DF",
           "90DAY_IMPVOL_100.0%MNY_DF",
           "180DAY_IMPVOL_100.0%MNY_DF",
           "360DAY_IMPVOL_100.0%MNY_DF",
           "30DAY_IMPVOL_25DELTA_RR",
           "30DAY_IMPVOL_25DELTA_BF"])
```

## Pitfalls

- **Direction**: `USDxxx` is "1 USD per xxx". `EURUSD` is "USD per
  EUR". Always sanity check by comparing with a known reference.
- **Fix mismatch**: WM/Reuters at 4pm London ≠ ECB 14:15 CET ≠ NYC
  close. Pick one and stick with it.
- **NDF fix sources** vary by region and have changed (CFETS for CNH,
  KFTC for KRW, JISDOR for IDR, PTAX for BRL). Bloomberg encodes the
  current default but check `NDF_FIX_SOURCE`.
- **`USDCNY` vs `USDCNH`**: not the same currency. CNY is onshore,
  PBoC-managed. CNH is the offshore market.
- **Holidays**: FX is 24/5 *globally*, but local holidays still shift
  settle / value dates. The `nonTradingDayFillOption` flag matters for
  Asian or LatAm currencies more than for G10.
