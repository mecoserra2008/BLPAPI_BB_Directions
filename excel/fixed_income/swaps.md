# Swaps in Excel (IRS / OIS / inflation / XCCY basis)

Yellow key: `Curncy`. Every swap in Bloomberg is a `Curncy` ticker —
including USD IRS, EUR OIS, JPY basis, GBP RPI inflation swaps.

For the conceptual model and conventions, see
[docs/asset_classes/swaps.md](../../docs/asset_classes/swaps.md).
This file covers Excel cell usage.

## 1 · Snapshot par rates (the most-used `BDP` pattern)

### USD curves

```excel
=BDP("USSO1 Curncy",  "PX_LAST")     ' SOFR OIS 1y (post-LIBOR)
=BDP("USSO2 Curncy",  "PX_LAST")
=BDP("USSO5 Curncy",  "PX_LAST")
=BDP("USSO10 Curncy", "PX_LAST")
=BDP("USSO30 Curncy", "PX_LAST")

=BDP("USSWAP1 Curncy",  "PX_LAST")   ' legacy fixed/3M LIBOR
=BDP("USSWAP10 Curncy", "PX_LAST")
```

### EUR curves

```excel
=BDP("EESWE1 Curncy",  "PX_LAST")    ' €STR OIS 1y
=BDP("EESWE5 Curncy",  "PX_LAST")
=BDP("EESWE10 Curncy", "PX_LAST")
=BDP("EESWE30 Curncy", "PX_LAST")

=BDP("EUSA1 Curncy",  "PX_LAST")     ' legacy 6M EURIBOR swap
=BDP("EUSA10 Curncy", "PX_LAST")
=BDP("EUSW10 Curncy", "PX_LAST")     ' legacy 3M EURIBOR swap
```

### GBP

```excel
=BDP("BPSO1 Curncy",   "PX_LAST")    ' SONIA OIS
=BDP("BPSO10 Curncy",  "PX_LAST")
=BDP("BPSWS10 Curncy", "PX_LAST")    ' legacy GBP LIBOR
```

### JPY

```excel
=BDP("JYSO1 Curncy",   "PX_LAST")    ' TONA OIS
=BDP("JYSO10 Curncy",  "PX_LAST")
=BDP("JYSWAP10 Curncy","PX_LAST")    ' legacy
```

### CHF

```excel
=BDP("SFSARON1 Curncy", "PX_LAST")
=BDP("SFSARON10 Curncy","PX_LAST")
```

## 2 · Curve as a column layout

```
   A     B                C
1  Tenor Ticker            Par rate
2  1Y    USSO1 Curncy     =BDP(B2,"PX_LAST")
3  2Y    USSO2 Curncy     =BDP(B3,"PX_LAST")
4  3Y    USSO3 Curncy     =BDP(B4,"PX_LAST")
5  5Y    USSO5 Curncy     =BDP(B5,"PX_LAST")
6  7Y    USSO7 Curncy     =BDP(B6,"PX_LAST")
7  10Y   USSO10 Curncy    =BDP(B7,"PX_LAST")
8  15Y   USSO15 Curncy    =BDP(B8,"PX_LAST")
9  20Y   USSO20 Curncy    =BDP(B9,"PX_LAST")
10 30Y   USSO30 Curncy    =BDP(B10,"PX_LAST")
```

Drag column C down. For multiple curves side by side, repeat the
pattern in columns D/F/H.

## 3 · Historical swap rates

```excel
=BDH("USSO10 Curncy", "PX_LAST",
     DATE(2014,1,1), TODAY(),
     "Per=cdr", "Days=W", "Fill=P", "UseDPDF=N")
```

For a panel of tenors:

```excel
=BDH({"USSO2 Curncy","USSO5 Curncy","USSO10 Curncy","USSO30 Curncy"},
     "PX_LAST",
     DATE(2014,1,1), TODAY(),
     "Per=cdr", "Days=W", "Fill=P")
```

Note: array of securities only works in some add-in versions. The
safer pattern is one `BDH` per ticker, each spilling into its own
column.

## 4 · Forward swaps

Pattern: `<CCY>FS<tenor1><tenor2>`. So `USFS0510` is "5y swap, 5y
forward starting" (i.e. 5y5y).

```excel
=BDP("USFS0102 Curncy", "PX_LAST")    ' 1y2y (1y swap, 2y fwd)
=BDP("USFS0205 Curncy", "PX_LAST")    ' 2y5y
=BDP("USFS0510 Curncy", "PX_LAST")    ' 5y10y
=BDP("USFS0530 Curncy", "PX_LAST")    ' 5y30y
=BDP("USFS1010 Curncy", "PX_LAST")    ' 10y10y

=BDP("EUFS0102 Curncy", "PX_LAST")
=BDP("EUFS0510 Curncy", "PX_LAST")
```

Use these for **terminal-rate** and **breakeven-forward** analyses
without computing discount factors yourself.

## 5 · Cross-currency basis (XCCY)

Bps spread on the foreign leg vs USD-equivalent OIS.

```excel
=BDP("EUBSC10 Curncy", "PX_LAST")    ' 10y EUR/USD basis (bps)
=BDP("JYBSC10 Curncy", "PX_LAST")    ' 10y JPY/USD basis
=BDP("BPBSC10 Curncy", "PX_LAST")    ' 10y GBP/USD basis
=BDP("SFBSC10 Curncy", "PX_LAST")    ' 10y CHF/USD basis
=BDP("ADBSC10 Curncy", "PX_LAST")    ' AUD/USD
=BDP("NDBSC10 Curncy", "PX_LAST")    ' NZD/USD
=BDP("CDBSC10 Curncy", "PX_LAST")    ' CAD/USD
```

Full XCCY tenor strip across G10:

```
   A      B                  C                  D                  E
1  Tenor  EUR/USD             JPY/USD            GBP/USD            CHF/USD
2  1Y     =BDP("EUBSC1 Curncy","PX_LAST")
                              =BDP("JYBSC1 Curncy","PX_LAST")
                                                  =BDP("BPBSC1 Curncy","PX_LAST")
                                                                      =BDP("SFBSC1 Curncy","PX_LAST")
3  2Y     ... 5Y, 10Y, 30Y    ...                ...                ...
```

## 6 · Inflation swaps (zero-coupon breakevens)

```excel
=BDP("USSWITP1 Curncy",   "PX_LAST")    ' USD CPI 1y zero-coupon
=BDP("USSWITP5 Curncy",   "PX_LAST")    ' 5y
=BDP("USSWITP10 Curncy",  "PX_LAST")    ' 10y
=BDP("USSWITP30 Curncy",  "PX_LAST")    ' 30y

=BDP("EUSWIT1 Curncy",   "PX_LAST")     ' EUR HICPx 1y
=BDP("EUSWIT10 Curncy",  "PX_LAST")
=BDP("EUSWIT30 Curncy",  "PX_LAST")

=BDP("BPSWIT10 Curncy",  "PX_LAST")     ' GBP RPI 10y
=BDP("JYSWIT10 Curncy",  "PX_LAST")     ' JPY CPI 10y
```

`PX_LAST` is the zero-coupon breakeven inflation rate (%).

Compare to govt-linker breakeven (`USGGBE10 Index` etc.) for the
"swap-linker basis".

## 7 · Swaption volatility

The ATM swaption vol grid:

```excel
=BDP("USSV0110 Curncy", "PX_LAST")   ' USD 1y10y ATM straddle vol
=BDP("USSV0510 Curncy", "PX_LAST")   ' USD 5y10y
=BDP("USSV1010 Curncy", "PX_LAST")
=BDP("USSV0101 Curncy", "PX_LAST")
=BDP("EUSV0110 Curncy", "PX_LAST")
=BDP("EUSV0510 Curncy", "PX_LAST")
=BDP("GBSV0110 Curncy", "PX_LAST")
=BDP("JYSV0110 Curncy", "PX_LAST")
```

Read: `<CCY>SV<expiry><tail>` where both expiry and tail are
2-character tenors (`01`, `02`, `05`, `10`, `30`).

## 8 · FRA points (older convention but still quoted)

```excel
=BDP("US0003M Index",  "PX_LAST")    ' 3m USD LIBOR (retired)
=BDP("EUR003M Index",  "PX_LAST")    ' 3m EURIBOR
=BDP("USOSFR3 Index",  "PX_LAST")    ' 3m SOFR (compounded)
```

FRA points themselves (e.g. 3M3M, 3M6M, 6M9M) live under their own
ticker family — see `FRA <GO>` for ICE-Tradition tickers.

## 9 · Building a curve sheet — full layout

```
Sheet "USD Curves":

   A     B                C                       D                       E
1  Tenor SOFR OIS         Legacy LIBOR swap       Forward swap (5yNy)     Treasury yld
2  1Y    USSO1            USSWAP1                                          GT1 Govt
3  2Y    USSO2            USSWAP2                                          GT2 Govt
4  3Y    USSO3            USSWAP3                                          GT3 Govt
5  5Y    USSO5            USSWAP5                                          GT5 Govt
6  7Y    USSO7            USSWAP7                                          GT7 Govt
7  10Y   USSO10           USSWAP10                USFS0510                 GT10 Govt
8  15Y   USSO15           USSWAP15
9  20Y   USSO20           USSWAP20                                         GT20 Govt
10 30Y   USSO30           USSWAP30                USFS0530                 GT30 Govt

(rates in column F-J: =BDP(B2 & " Curncy","PX_LAST") etc.)
```

Then derived columns: govt-swap spread, swap-OIS spread, forward
breakeven, etc.

## 10 · Historical curve panel

For a panel of tenors over time (one column per tenor):

```excel
B2: =BDH("USSO2 Curncy",  "PX_LAST", DATE(2014,1,1), TODAY(), "Per=cdr","Days=W","Fill=P","Dts=H","Cols=N","Sort=A")
C2: =BDH("USSO5 Curncy",  "PX_LAST", DATE(2014,1,1), TODAY(), "Per=cdr","Days=W","Fill=P","Dts=H","Cols=N","Sort=A")
D2: =BDH("USSO10 Curncy", "PX_LAST", DATE(2014,1,1), TODAY(), "Per=cdr","Days=W","Fill=P","Dts=H","Cols=N","Sort=A")
E2: =BDH("USSO30 Curncy", "PX_LAST", DATE(2014,1,1), TODAY(), "Per=cdr","Days=W","Fill=P","Dts=H","Cols=N","Sort=A")

A2: dates column — =BDH("USSO10 Curncy","PX_LAST",...,"Dts=S","Cols=N") and discard column 2
```

`Dts=H` hides the date column so the spill is just values. `Cols=N`
suppresses headers. Provide one dates column from one of the
series (or use `WORKDAY` to build the calendar).

## 11 · Pre-computed slope / curve indices

```excel
=BDP("USYC2Y10 Index",  "PX_LAST")    ' US 2y-10y curve (bps)
=BDP("USYC2Y30 Index",  "PX_LAST")
=BDP("USYC3M10 Index",  "PX_LAST")    ' NY Fed slope
=BDP("USYC5Y30 Index",  "PX_LAST")
```

Bloomberg also publishes country-level govt slopes:

```
.GBSPDE10Y Index           Germany 10y yield (proxy for level)
.IBSPDE10Y Index           IT-DE 10y spread
.SBSPDE10Y Index           ES-DE 10y spread
.PBSPDE10Y Index           PT-DE 10y spread
```

(Period prefixes are alternative formats — some installs strip them.)

## 12 · Discount factor / forward calc in cells

Given OIS par rates in `B2:B10` and tenor in years in `A2:A10`:

```excel
C2: =1/(1+B2/100)^A2                          ' discount factor (annual comp)
D2: (skip first row)
D3: =(C2/C3)^(1/(A3-A2)) - 1                  ' forward rate, annual
```

For ACT/360 USD swap conventions:

```excel
C2: =1/(1+B2/100*A2*360/365)                  ' approximate ACT/360 day-count
```

For production use OIS bootstrapping from continuous-time discount
factors — see `BCURVE` for discount factors directly.

## 13 · CDS curves (issuer 5y is canonical, but full curve exists)

```excel
=BDP("EDPPL CDS EUR SR 5Y D14 Corp", "PX_LAST")
=BDP("EDPPL CDS EUR SR 1Y D14 Corp", "PX_LAST")
=BDP("EDPPL CDS EUR SR 3Y D14 Corp", "PX_LAST")
=BDP("EDPPL CDS EUR SR 7Y D14 Corp", "PX_LAST")
=BDP("EDPPL CDS EUR SR 10Y D14 Corp", "PX_LAST")
```

See [credit_cds.md](credit_cds.md).

## 14 · Common reproducible swaps worksheet

```
Sheet "Curves":  par rates + computed DF + forwards
Sheet "Basis":   XCCY basis grid (EUR/JPY/GBP/CHF/AUD/NZD/CAD, 1y to 30y)
Sheet "Inflation": ZC breakevens + cash linker compare
Sheet "Swaption": ATM grid (1m, 3m, 1y, 5y by 2y/5y/10y/30y tail)
Sheet "Params":  named cells (Today, FwdDate, IRSCurveCcy)
```

## 15 · Pitfalls

- **Curve naming drift**: USD post-LIBOR is `USSO*` (SOFR), pre-LIBOR
  is `USSWAP*` (3M LIBOR fixed/float). They quote at different
  levels (a 10y USSO10 ≠ USSWAP10). Stitching pre-2023 + post-2023
  series requires a swap spread.
- **EUR €STR vs 6M EURIBOR**: `EESWE*` (OIS) vs `EUSA*` (vs 6M
  EURIBOR). Different conventions, different discount curves —
  match to your trade.
- **Quote in % vs bps**: par swap rates in %, basis in bps. The
  `PX_LAST` is whatever the ticker quotes in — read the chart
  scale.
- **Inflation swap fixing lag**: 3-month CPI lag conventional, so a
  10y ZC inflation swap is not a 10y forward CPI — adjust for
  seasonality / lag if needed.
- **Calendars**: USD swap fixes against the SOFR publication
  calendar (US bond holidays), not the equity calendar. Different
  `Calendar=US` vs `Calendar=SIFMA` give different non-trading days.
- **Cross-currency basis sign**: negative = USD scarce on the
  cross. Some Bloomberg sources flip the sign — verify with a known
  observation (EUBSC10 ≈ -5 to -25 bps over the last decade).
- **Forward swap addressing**: `USFS<expiry><tail>` is *expiry*
  first, then *tail*. So `USFS0510` is 5y expiry × 10y tail (5y5y? No:
  it's "5y swap, 5y forward" — i.e. starts in 5y, length 10y - 5y = …
  actually means a 1y swap starting in 5y for some families). The
  semantics differ across families — `DES <GO>` is the only
  authoritative source. Always verify.
