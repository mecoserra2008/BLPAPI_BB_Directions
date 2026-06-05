# Currencies (FX) in Excel

Yellow key: `Curncy`. Spot, forwards, NDFs, vol — all the same key.

For the conceptual model, see
[docs/asset_classes/currencies.md](../../docs/asset_classes/currencies.md).
This file is the Excel translation.

## 1 · Spot — picking a fix

Default `BDP` source is BGN (Bloomberg Generic). For research, fix
on a deterministic source:

```excel
=BDP("EURUSD Curncy",       "PX_LAST")     ' BGN composite
=BDP("EURUSD WMCO Curncy",  "PX_LAST")     ' WM/Reuters 4pm London
=BDP("EURUSD CMPL Curncy",  "PX_LAST")     ' Composite London close
=BDP("EURUSD CMPN Curncy",  "PX_LAST")     ' Composite NY close
=BDP("EURUSD BFIX Curncy",  "PX_LAST")     ' Bloomberg FX fix
=BDP("EURUSD ECB37 Curncy", "PX_LAST")     ' ECB reference rate
```

For historical pick one and keep it:

```excel
=BDH("EURUSD WMCO Curncy", "PX_LAST",
     DATE(2010,1,1), TODAY(),
     "Per=cdr", "Days=W", "Fill=P")
```

## 2 · Cross-pairs

Crosses are first-class:

```excel
=BDP("EURGBP Curncy", "PX_LAST")
=BDP("EURJPY Curncy", "PX_LAST")
=BDP("EURCHF Curncy", "PX_LAST")
=BDP("GBPCHF Curncy", "PX_LAST")
=BDP("AUDJPY Curncy", "PX_LAST")
=BDP("NZDJPY Curncy", "PX_LAST")
```

For non-quoted crosses, derive from two USD legs:

```excel
A2: =BDP("EURUSD Curncy", "PX_LAST")     ' 1.0855 (USD per EUR)
B2: =BDP("USDZAR Curncy", "PX_LAST")     ' 18.45  (ZAR per USD)
C2: =A2*B2                                ' EUR/ZAR
```

## 3 · Outright forwards

Append a tenor:

```excel
=BDP("EURUSDON Curncy", "PX_LAST")     ' overnight
=BDP("EURUSDTN Curncy", "PX_LAST")     ' tom-next
=BDP("EURUSD1W Curncy", "PX_LAST")
=BDP("EURUSD1M Curncy", "PX_LAST")
=BDP("EURUSD3M Curncy", "PX_LAST")
=BDP("EURUSD6M Curncy", "PX_LAST")
=BDP("EURUSD1Y Curncy", "PX_LAST")
=BDP("EURUSD2Y Curncy", "PX_LAST")
=BDP("EURUSD5Y Curncy", "PX_LAST")
```

`PX_LAST` is the **outright** rate.

## 4 · Forward points only

Drop the "USD" in the pair:

```excel
=BDP("EUR1M Curncy", "PX_LAST")     ' EUR/USD 1m forward points
=BDP("EUR3M Curncy", "PX_LAST")
=BDP("GBP1M Curncy", "PX_LAST")     ' GBP/USD 1m points
=BDP("JPY1M Curncy", "PX_LAST")     ' JPY-side points
=BDP("CHF1M Curncy", "PX_LAST")
=BDP("AUD3M Curncy", "PX_LAST")
=BDP("NZD3M Curncy", "PX_LAST")
=BDP("CAD3M Curncy", "PX_LAST")
=BDP("SEK3M Curncy", "PX_LAST")
=BDP("NOK3M Curncy", "PX_LAST")
```

Points convention: pips × 10^N. For most G10 N=4; for USDJPY N=2.

Outright from points + spot in Excel:

```excel
A2: =BDP("EURUSD Curncy",   "PX_LAST")
B2: =BDP("EUR3M Curncy",    "PX_LAST")
C2: =A2 + B2/10000                      ' EUR/USD 3m outright (4 decimals)
```

For USDJPY:

```excel
A2: =BDP("USDJPY Curncy",   "PX_LAST")
B2: =BDP("JPY3M Curncy",    "PX_LAST")
C2: =A2 + B2/100                        ' USDJPY 3m outright (2 decimals)
```

## 5 · NDFs

Non-deliverable forwards for capital-controlled currencies. Same
ticker pattern, semantics differ (fixed against a published fix).

```excel
=BDP("USDCNY1M Curncy", "PX_LAST")     ' CFETS fix
=BDP("USDCNY3M Curncy", "PX_LAST")
=BDP("USDCNY1Y Curncy", "PX_LAST")

=BDP("USDINR1M Curncy", "PX_LAST")     ' RBI fix
=BDP("USDBRL1M Curncy", "PX_LAST")     ' PTAX
=BDP("USDKRW1M Curncy", "PX_LAST")     ' KFTC
=BDP("USDIDR1M Curncy", "PX_LAST")     ' JISDOR
=BDP("USDPHP1M Curncy", "PX_LAST")
=BDP("USDTWD1M Curncy", "PX_LAST")
=BDP("USDARS1M Curncy", "PX_LAST")
=BDP("USDCLP1M Curncy", "PX_LAST")
=BDP("USDCOP1M Curncy", "PX_LAST")
=BDP("USDEGP1M Curncy", "PX_LAST")
```

NDF-specific fields:

```excel
=BDP("USDBRL1M Curncy", "NDF_FIX_DATE")
=BDP("USDBRL1M Curncy", "NDF_VAL_DT")
=BDP("USDBRL1M Curncy", "NDF_FIX_SOURCE")
=BDP("USDBRL1M Curncy", "IMPL_YIELD_NDF_PCT")  ' implied local yield
```

## 6 · NDF-implied local yield curve

For local-currency rate curves of EM countries that lack onshore
benchmarks accessible offshore:

```
   A     B                       C
1  Tenor Ticker                  Implied yield (%)
2  1M    USDBRL1M Curncy         =BDP(B2,"IMPL_YIELD_NDF_PCT")
3  3M    USDBRL3M Curncy         =BDP(B3,"IMPL_YIELD_NDF_PCT")
4  6M    USDBRL6M Curncy         =BDP(B4,"IMPL_YIELD_NDF_PCT")
5  1Y    USDBRL1Y Curncy         =BDP(B5,"IMPL_YIELD_NDF_PCT")
```

## 7 · Carry computation in cells

```
   A         B              C              D              E              F
1  Pair      Spot           1m Fwd         1m carry %     RV-vol         Carry/vol
2  EURUSD    =BDP("EURUSD Curncy","PX_LAST")
                            =BDP("EURUSD1M Curncy","PX_LAST")
                                            =-12*LN(C2/B2)*100
                                                            =BDP("EURUSDV1M Curncy","PX_LAST")
                                                                            =D2/E2
3  USDJPY    ...
4  GBPUSD    ...
```

Sign convention: for `USDxxx` pairs (USD as base), carry = log-spot
- log-fwd × 12 (positive = USD-side carry). For `xxxUSD` (USD as
quote, EURUSD/GBPUSD/AUDUSD/NZDUSD), flip the sign.

## 8 · FX volatility

ATM vol tickers:

```excel
=BDP("EURUSDV1M Curncy",  "PX_LAST")     ' 1m ATM straddle vol
=BDP("EURUSDV3M Curncy",  "PX_LAST")
=BDP("EURUSDV6M Curncy",  "PX_LAST")
=BDP("EURUSDV1Y Curncy",  "PX_LAST")
=BDP("EURUSDV2Y Curncy",  "PX_LAST")
=BDP("USDJPYV1M Curncy",  "PX_LAST")
=BDP("GBPUSDV3M Curncy",  "PX_LAST")
```

Risk reversals (skew):

```excel
=BDP("EURUSD25R1M Curncy", "PX_LAST")    ' 25-delta RR 1m
=BDP("EURUSD25R3M Curncy", "PX_LAST")
=BDP("EURUSD25R1Y Curncy", "PX_LAST")
=BDP("EURUSD10R1M Curncy", "PX_LAST")    ' 10-delta RR
```

Butterflies (curvature):

```excel
=BDP("EURUSD25B1M Curncy", "PX_LAST")    ' 25d BF
=BDP("EURUSD25B3M Curncy", "PX_LAST")
=BDP("EURUSD10B1M Curncy", "PX_LAST")
```

Constructed-surface fields on the spot ticker:

```excel
=BDP("EURUSD Curncy", "30DAY_IMPVOL_100.0%MNY_DF")    ' ATM 30d
=BDP("EURUSD Curncy", "90DAY_IMPVOL_100.0%MNY_DF")    ' ATM 3m
=BDP("EURUSD Curncy", "180DAY_IMPVOL_100.0%MNY_DF")
=BDP("EURUSD Curncy", "360DAY_IMPVOL_100.0%MNY_DF")
=BDP("EURUSD Curncy", "30DAY_IMPVOL_25DELTA_RR")
=BDP("EURUSD Curncy", "30DAY_IMPVOL_25DELTA_BF")
```

## 9 · Realised vs implied (a one-cell ratio)

```
A2: =BDP("EURUSD Curncy", "HISTORICAL_VOLATILITY_30D")
B2: =BDP("EURUSDV1M Curncy", "PX_LAST")
C2: =B2 - A2                ' vol premium (bps if both in %)
```

## 10 · Forward-implied money-market rate (Excel-side CIP)

CIP relation gives you implied rates from spot + forward:

```
A2: =BDP("EURUSD Curncy", "PX_LAST")
B2: =BDP("EURUSD3M Curncy", "PX_LAST")
C2: =A2 - B2  (just to show — implied yield is from log ratios)
D2: =-LN(B2/A2)/0.25*100        ' (% implied carry, annualised)
```

For NDF curves use `IMPL_YIELD_NDF_PCT` directly (already
annualised %).

## 11 · Precious metals as `Curncy`

```excel
=BDP("XAU Curncy", "PX_LAST")          ' Gold spot, USD/oz
=BDP("XAG Curncy", "PX_LAST")          ' Silver
=BDP("XPT Curncy", "PX_LAST")          ' Platinum
=BDP("XPD Curncy", "PX_LAST")          ' Palladium
=BDP("XAUEUR Curncy", "PX_LAST")       ' Gold in EUR
=BDP("XAUJPY Curncy", "PX_LAST")
=BDP("XAU1M Curncy", "PX_LAST")        ' 1m gold forward
=BDP("XAU1Y Curncy", "PX_LAST")        ' 1y gold forward
```

## 12 · DXY and trade-weighted

```excel
=BDP("DXY Curncy",   "PX_LAST")        ' ICE Dollar Index
=BDP("BBDXY Index",  "PX_LAST")        ' Bloomberg Dollar Index
=BDP("TWBR Curncy",  "PX_LAST")        ' Bloomberg trade-weighted
=BDP("JPMVXYG7 Index","PX_LAST")       ' JPM G7 FX vol
```

## 13 · Worked sheet — G10 + EM monitor

```
Sheet "FX Spot":     pairs in column A, BDP("PX_LAST") in B, 5d/30d/YTD change in C-E
Sheet "Fwd Outright": pairs × tenors (1M/3M/6M/1Y) grid
Sheet "Carry":       pairs in A, spot/fwd in B/C, carry % in D, vol in E, Sharpe in F
Sheet "Vol":         ATM 1m/3m/6m/1y grid; 25d RR / BF beside
Sheet "EM NDF":      same as Spot but with NDF curve (1M/3M/6M/1Y) + IMPL_YIELD_NDF_PCT
```

## 14 · Pitfalls

- **`USDxxx` vs `xxxUSD`** is real: direction matters for carry
  signs. Sanity-check one pair before trusting the table.
- **Pip convention**: USDJPY pip = 0.01. EURUSD pip = 0.0001. The
  forward-points ticker (`JPY1M Curncy`) is quoted in pips, so
  outright = spot + points / 100 for JPY pairs, + points / 10000
  for most other G10.
- **NDF fix mismatch**: each currency has its own fix source
  (CFETS for CNH, PTAX for BRL, JISDOR for IDR, KFTC for KRW, RBI
  for INR). The "deliverable" forward and the NDF can have
  different curves; watch `NDF_FIX_SOURCE`.
- **`USDCNY` vs `USDCNH`**: different markets, different curves.
  Onshore (CNY) is PBoC-managed; offshore (CNH) is the
  deliverable market. Carry derived from CNY is artificial.
- **`WMCO` fix is published 16:15 London** — using it for any
  intra-day refresh just freezes on yesterday's close.
- **ECB37 fix is 14:15 CET, once a day** — same caveat.
- **Holiday gaps in EM**: with `Fill=P`, realised vol gets biased
  low by long stale-quote runs over local holidays. Use `Fill=B`
  and drop NaN bars before computing returns.
- **Carry vs basis**: G10 CIP-implied carry should equal OIS rate
  differential + XCCY basis. Mismatches signal stale points
  ticker or fix-source confusion.
- **Cross-derived crosses** (EUR/ZAR = EURUSD × USDZAR) have
  rounding error; for a single name use the direct cross when
  Bloomberg quotes it.
