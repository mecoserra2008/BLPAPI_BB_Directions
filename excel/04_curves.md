# 04 · Building Curves in Excel

Two ways to render a curve in a worksheet:

1. **Node-by-node** with `BDP` (or `BDH` for history) on each
   tenor's individual ticker. Maximum control. Always works.
2. **`BCURVE`** — Bloomberg's pre-built curve object. One formula,
   one spill. Less verbose.

Both are useful. Node-by-node is the right default for research;
`BCURVE` is convenient for dashboards and quick term-structure
charts.

## 4.1 Node-by-node — the standard pattern

A canonical layout for a USD SOFR OIS curve:

```
   A         B               C            D            E
1  Tenor     Ticker          Yield (now)  3M Δ (bps)   1Y Δ (bps)
2  ON        SOFRRATE Index  =BDP(B2,"PX_LAST")
3  1M        USSOC Curncy    =BDP(B3,"PX_LAST")
4  3M        USSO3 Curncy    =BDP(B4,"PX_LAST")
5  6M        USSO6 Curncy    =BDP(B5,"PX_LAST")
6  1Y        USSO1 Curncy    =BDP(B6,"PX_LAST")
7  2Y        USSO2 Curncy    =BDP(B7,"PX_LAST")
8  3Y        USSO3 Curncy    ...
9  5Y        USSO5 Curncy
10 7Y        USSO7 Curncy
11 10Y       USSO10 Curncy
12 15Y       USSO15 Curncy
13 20Y       USSO20 Curncy
14 30Y       USSO30 Curncy
```

For historical:

```
   A    B               C
1  Tenor Ticker          Yield at 2024-12-31
2  1M   USSOC Curncy    =INDEX(BDH(B2,"PX_LAST",DATE(2024,12,31),DATE(2024,12,31),"Per=cdr","Fill=P","Days=W","Dts=H"),1,1)
```

The `INDEX(...,1,1)` extracts the value from `BDH`'s array spill —
useful when you want a single historical point in a single cell.

## 4.2 Curve sets to keep handy

### USD

```
SOFRRATE Index     # SOFR overnight
USSOC Curncy       # SOFR OIS spot-starting (1m proxy)
USSO3 Curncy       # 3m
USSO6 Curncy       # 6m
USSO1 ... USSO30 Curncy
USFS0102 Curncy    # 1y1y forward
USFS0205 Curncy    # 2y5y forward
USFS0510 Curncy    # 5y10y forward
USFS0530 Curncy    # 5y30y forward
USSWAP1 ... USSWAP30 Curncy   # legacy LIBOR-based fixed/3M (still useful for splices)
```

US Treasury actives:

```
GT2 Govt, GT3 Govt, GT5 Govt, GT7 Govt, GT10 Govt, GT20 Govt, GT30 Govt
USGG3M Index, USGG6M Index, USGG12M Index,
USGG2YR Index ... USGG30YR Index    # Fed H.15 yields
```

### EUR

```
ESTRON Index       # €STR overnight
EESWE1M Curncy     # €STR OIS 1m
EESWE3M Curncy
EESWE6M Curncy
EESWE1 ... EESWE30 Curncy
EUSA1 ... EUSA30 Curncy             # legacy vs 6M EURIBOR
EUSW1 ... EUSW30 Curncy             # legacy vs 3M EURIBOR
EUBSC1 ... EUBSC30 Curncy           # EUR/USD cross-currency basis (bps)
```

German bunds (benchmark):

```
GTDEM2Y Govt, GTDEM5Y Govt, GTDEM10Y Govt, GTDEM30Y Govt
```

Periphery vs Bund (raw level + spread computed via subtraction):

```
GTFRF10Y Govt, GTITL10Y Govt, GTESP10Y Govt, GTPTE10Y Govt,
GTGRD10Y Govt, GTNLG10Y Govt, GTBEF10Y Govt
```

### GBP

```
SONIO/N Index      # SONIA overnight
BPSO1 ... BPSO30 Curncy     # SONIA OIS
BPSWS1 ... BPSWS30 Curncy   # legacy LIBOR
BPBSC1 ... BPBSC30 Curncy   # GBP/USD basis (bps)
GTGBP2Y Govt ... GTGBP30Y Govt
```

### JPY

```
TONAR Index
JYSO1 ... JYSO30 Curncy     # TONA OIS
JYBSC1 ... JYBSC30 Curncy   # JPY/USD basis
GTJPY10Y Govt
```

### CHF

```
SFSARON1 ... SFSARON30 Curncy
GTCHF10Y Govt
```

See the existing [docs/asset_classes/swaps.md](../docs/asset_classes/swaps.md)
for the full set of legacy + post-LIBOR swap families across CCYs.

## 4.3 Spread tickers

Some spread series are pre-computed and Bloomberg-published:

```
USYC2Y10 Index            US 2y-10y curve (bps)
USYC2Y30 Index            US 2y-30y
USYC3M10 Index            US 3m-10y (NY Fed favourite)
USGGBE10 Index            US 10y breakeven
USGGT10Y Index            US 10y real yield (TIPS)
```

Pull them like any other index:

```excel
=BDP("USYC2Y10 Index", "PX_LAST")
=BDH("USYC2Y10 Index", "PX_LAST",
     DATE(2010,1,1), TODAY(), "Per=cdr", "Days=W", "Fill=P")
```

## 4.4 `BCURVE` — the alternative

```excel
=BCURVE("YCSW0023", TODAY(),
        {"3M","1Y","2Y","5Y","10Y","30Y"})
```

Returns a spilled table of (tenor, value) pairs from the requested
curve. Useful when:

- You want every official Bloomberg curve point with one formula.
- You want historical curves: substitute the date.
- You don't want to maintain a tenor → ticker map.

Common `curve_id`s:

| Curve | ID |
|---|---|
| USD SOFR OIS | `YCSW0023` |
| USD legacy (3M LIBOR) | `YCSW0042` |
| USD Fed funds OIS | `YCSW0490` |
| EUR €STR OIS | `YCSW0514` |
| EUR 6M EURIBOR swap | `YCSW0045` |
| EUR 3M EURIBOR swap | `YCSW0030` |
| GBP SONIA OIS | `YCSW0141` |
| GBP LIBOR (legacy) | `YCSW0022` |
| JPY TONA OIS | `YCSW0510` |
| CHF SARON OIS | `YCSW0234` |
| US Treasury actives | `YCGT0025` |
| German Bund | `YCGT0016` |
| UK Gilt | `YCGT0022` |
| JGB | `YCGT0018` |
| French OAT | `YCGT0014` |
| Italian BTP | `YCGT0040` |
| Spanish Bonos | `YCGT0061` |
| US TIPS real | `YCGT0118` |
| German Linker | `YCGT0203` |

Find more via `CRVF <GO>` on the Terminal.

## 4.5 Worksheet pattern: term structure on a single date

```
   A          B                              C
1  Curve ID   YCSW0023                       (USD SOFR OIS)
2  As of      =TODAY()
3
4  Tenor      Value
5  =BCURVE($B$1, $B$2, $A6:$A20)   (this spills both A6:A.. and B6:B..)
6  ...
```

If you prefer tenor in column A *fixed* and `BCURVE` to fill only
value into column B:

```
   A      B
1  Tenor  Value
2  3M     =INDEX(BCURVE("YCSW0023", TODAY(), $A2:$A20), MATCH($A2, $A$2:$A$20, 0), 1)
3  6M     =INDEX(BCURVE("YCSW0023", TODAY(), $A2:$A20), MATCH($A3, $A$2:$A$20, 0), 1)
...
```

Bit ugly. The node-by-node approach is cleaner for fixed tenor
layouts.

## 4.6 Historical term structure (curve over time)

Build a wide DataFrame: dates down rows, tenors across columns,
each cell is a `BDH` last-value for that date/tenor.

```
        B               C               D               E
1                       3M              1Y              5Y              10Y
2       Date            USSO3M Curncy   USSO1 Curncy    USSO5 Curncy    USSO10 Curncy
3       2014-01-01      =BDP(...)?      ...
```

For long history use one `BDH` per tenor (down a column), then
merge by date in a second sheet.

```excel
C3:  =BDH(C$2, "PX_LAST", $B$3, $B$1000, "Per=cdr", "Days=W", "Fill=P",
          "Dts=H", "Cols=N", "Sort=A")
```

`Dts=H` hides the date column (we have our own), `Cols=N` suppresses
header row, `Sort=A` ascending. The series spills down column C.

## 4.7 Forward rates from a curve

Given par OIS rates in column B, discount factors and forwards in
columns C and D:

```
   A      B                C                                          D
1  Tenor  Rate (%)         DF                                         Fwd
2  1Y     =BDP("USSO1 Curncy","PX_LAST")  =1/(1+B2/100)^A2 (numeric)  -
3  2Y     =BDP("USSO2 Curncy","PX_LAST")  =1/(1+B3/100)^A3            =(C2/C3)^(1/(A3-A2)) - 1
4  3Y     =BDP("USSO3 Curncy","PX_LAST")  =1/(1+B4/100)^A4            =(C3/C4)^(1/(A4-A3)) - 1
...
```

Annual compounding shown for clarity; production-grade conversion
needs the correct day-count (ACT/360 for USD, ACT/365 for GBP, etc.)
— better to read those off the curve metadata or `YAS_*` fields.

## 4.8 Curve plot in Excel

Insert a scatter chart with:

- **X** = tenor in years (column A or a numeric tenor column).
- **Y** = rate.

A tenor-to-years helper:

```
=IFERROR(VALUE(LEFT(A2,LEN(A2)-1)) *
  IF(RIGHT(A2,1)="Y",1, IF(RIGHT(A2,1)="M",1/12,
   IF(RIGHT(A2,1)="W",7/365, IF(RIGHT(A2,1)="D",1/365, 1/12)))),
   0)
```

For curve movement: a simple "now vs 1m ago vs 1y ago" three-line
chart drives 80% of the daily curve monitor use-case.

## 4.9 Inflation breakevens (curves with two legs)

A pre-baked breakeven series:

```
USGGBE05 Index            US 5y BE
USGGBE10 Index            US 10y BE
USGGBE30 Index            US 30y BE
```

Or compute it yourself:

```excel
B2: =BDP("USGG10YR Index","PX_LAST")     ' 10y nominal
B3: =BDP("USGGT10Y Index","PX_LAST")     ' 10y real (TIPS)
B4: =B2-B3                                ' 10y breakeven (%)
```

For EUR: `GTDEM10Y Govt − GTDEMI10Y Govt`. For UK: `GTGBP10Y Govt −
GTGBII10Y Govt`. The point is: where Bloomberg publishes the spread,
use it; otherwise compute and document.

## 4.10 Tip: cache the curve to a static range

When the same curve drives many cells, refresh once into a static
"snapshot" range and have downstream formulas read from there. This
avoids triggering N `BDP`s on every recalc.

```
Sheet "Curve":
   A         B (live BDP)         C (snapshot — paste-special-value)
1  Tenor     Rate                 Snapshot rate
2  1M        =BDP(...)            (paste value periodically)
3  3M        ...
```

Downstream sheets reference column C, not column B. Combined with
**Manual refresh**, this gives you reproducibility without paying
the refresh cost on every cell change elsewhere.
