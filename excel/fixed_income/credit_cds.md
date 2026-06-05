# Credit & CDS in Excel

CDS lives under yellow key `Corp`. The grammar is verbose but
regular.

For the conceptual model see
[docs/asset_classes/swaps.md](../../docs/asset_classes/swaps.md)
(CDS section) and
[docs/recipes/credit_spreads.md](../../docs/recipes/credit_spreads.md).

## 1 · Single-name CDS ticker grammar

```
<TICKER> CDS <CCY> <SR|SUB> <TENOR>Y D14 Corp
```

| Component | Notes |
|---|---|
| `TICKER` | Bloomberg issuer ticker (e.g. `JPM`, `EDPPL`, `TEFE`) |
| `CCY` | `USD` / `EUR` (most common); some names also `JPY`, `GBP` |
| Rank | `SR` (senior, default) or `SUB` (subordinated) |
| Tenor | `1Y`, `2Y`, `3Y`, `4Y`, `5Y`, `7Y`, `10Y`, `20Y`, `30Y` |
| `D14` | 2014 ISDA definitions (current). Older: `D03` (still around for legacy) |

```excel
=BDP("JPM CDS USD SR 5Y D14 Corp",  "PX_LAST")
=BDP("EDPPL CDS EUR SR 5Y D14 Corp","PX_LAST")
=BDP("TEFE CDS EUR SR 5Y D14 Corp", "PX_LAST")
=BDP("VW CDS EUR SR 5Y D14 Corp",   "PX_LAST")
=BDP("BACR CDS USD SR 5Y D14 Corp", "PX_LAST")
=BDP("DBR CDS USD SR 5Y D14 Corp",  "PX_LAST")    ' Germany sov
=BDP("ITALY CDS USD SR 5Y D14 Corp","PX_LAST")
=BDP("PORTUG CDS USD SR 5Y D14 Corp","PX_LAST")
=BDP("TURKEY CDS USD SR 5Y D14 Corp","PX_LAST")
=BDP("BRAZIL CDS USD SR 5Y D14 Corp","PX_LAST")
```

`PX_LAST` is either **par spread** (bps) or **upfront** (%) — read
`CDS_QUOTE_TYPE`.

## 2 · CDS indices

```excel
=BDP("CDX IG CDSI GEN 5Y Corp",      "PX_LAST")   ' on-the-run IG
=BDP("CDX HY CDSI GEN 5Y Corp",      "PX_LAST")   ' on-the-run HY
=BDP("CDX EM CDSI GEN 5Y Corp",      "PX_LAST")   ' on-the-run EM
=BDP("ITRX MAIN CDSI GEN 5Y Corp",   "PX_LAST")   ' iTraxx Main
=BDP("ITRX XOVER CDSI GEN 5Y Corp",  "PX_LAST")   ' iTraxx Crossover
=BDP("ITRX SNRFIN CDSI GEN 5Y Corp", "PX_LAST")   ' iTraxx Senior Fin
=BDP("ITRX SUBFIN CDSI GEN 5Y Corp", "PX_LAST")
=BDP("ITRX ASIAXJ CDSI GEN 5Y Corp", "PX_LAST")   ' iTraxx Asia ex-J
=BDP("ITRX AUS CDSI GEN 5Y Corp",    "PX_LAST")
```

`GEN` = on-the-run, auto-rolls every March / September. For a pinned
series:

```excel
=BDP("CDX IG CDSI S42 5Y Corp",      "PX_LAST")   ' Series 42, 5y
=BDP("ITRX MAIN CDSI S40 5Y Corp",   "PX_LAST")
```

## 3 · CDS curve per issuer

```
   A         B                                 C
1  Tenor     Ticker                            Spread (bps)
2  1Y        EDPPL CDS EUR SR 1Y D14 Corp     =BDP(B2,"PX_LAST")
3  3Y        EDPPL CDS EUR SR 3Y D14 Corp     =BDP(B3,"PX_LAST")
4  5Y        EDPPL CDS EUR SR 5Y D14 Corp     =BDP(B4,"PX_LAST")
5  7Y        EDPPL CDS EUR SR 7Y D14 Corp     =BDP(B5,"PX_LAST")
6  10Y       EDPPL CDS EUR SR 10Y D14 Corp    =BDP(B6,"PX_LAST")
```

Build the ticker via concatenation:

```
   A         B                  C            D
1  Tenor     Issuer prefix      Suffix       Ticker
2  1Y        EDPPL CDS EUR SR   D14 Corp    =$B2 & " " & A2 & " " & $C2
3  3Y        EDPPL CDS EUR SR   D14 Corp    ...
```

Then `=BDP(D2, "PX_LAST")` etc.

## 4 · CDS-specific fields

```excel
=BDP(A2, "PX_LAST")                  ' par spread (bps) or upfront (%)
=BDP(A2, "CDS_QUOTE_TYPE")           ' "Par Spread" / "Upfront"
=BDP(A2, "CDS_FAIR_SPREAD")          ' model-implied
=BDP(A2, "CDS_FLAT_SPREAD")          ' flat-curve equivalent
=BDP(A2, "CDS_RUNNING_CPN")          ' standard 100 / 500 bps coupon
=BDP(A2, "CDS_RECOVERY_RATE")        ' default 40% SR / 25% SUB
=BDP(A2, "CDS_DV01")                 ' $ value of 1 bp
=BDP(A2, "RISKY_DUR")                ' risky duration
=BDP(A2, "CDS_IMPLIED_DEFAULT_PROB") ' cumulative default prob
=BDP(A2, "ISDA_DEFINITION_VERSION")  ' D03 / D14
=BDP(A2, "UPFRONT_PMT")              ' for traded conventions
=BDP(A2, "ACCRUED_INTEREST")
=BDP(A2, "ACCRUED_DAYS")
```

## 5 · CDS history

```excel
=BDH("EDPPL CDS EUR SR 5Y D14 Corp", "PX_LAST",
     DATE(2014,1,1), TODAY(),
     "Per=cdr", "Days=W", "Fill=P")
```

For the index history (always on-the-run via `GEN`):

```excel
=BDH("ITRX MAIN CDSI GEN 5Y Corp", "PX_LAST",
     DATE(2014,1,1), TODAY(),
     "Per=cdr", "Days=W", "Fill=P")
```

## 6 · Cash bond credit spreads (compare with CDS)

For the same issuer's cash bond:

```excel
=BDP("EDP 1 ⅞ 03/14/35 Corp", "Z_SPRD_MID")        ' Z-spread
=BDP("EDP 1 ⅞ 03/14/35 Corp", "OAS_SPREAD_MID")    ' OAS
=BDP("EDP 1 ⅞ 03/14/35 Corp", "ASSET_SWAP_SPD_MID") ' ASW
=BDP("EDP 1 ⅞ 03/14/35 Corp", "G_SPRD_MID")        ' vs govt
=BDP("EDP 1 ⅞ 03/14/35 Corp", "I_SPRD_MID")        ' vs swap interp
```

## 7 · CDS-cash basis sheet

```
Sheet "Basis":
   A                              B          C                D
1  Bond                            Z-spread   Issuer 5Y CDS    Basis (CDS - Z)
2  EDP 1 ⅞ 03/14/35 Corp          =BDP(A2,"Z_SPRD_MID")
                                              =BDP("EDPPL CDS EUR SR 5Y D14 Corp","PX_LAST")
                                                                =C2 - B2
3  TEFE 0.875 04/02/27 Corp       =BDP(A3,"Z_SPRD_MID")
                                              =BDP("TEFE CDS EUR SR 5Y D14 Corp","PX_LAST")
                                                                =C3 - B3
```

Negative basis = CDS cheap relative to cash bond (or bond rich).
Positive basis = opposite.

## 8 · Index constituents (bulk)

```excel
=BDS("CDX IG CDSI GEN 5Y Corp", "INDX_MEMBERS")
=BDS("ITRX MAIN CDSI GEN 5Y Corp", "INDX_MEMBERS")
=BDS("ITRX XOVER CDSI GEN 5Y Corp", "INDX_MEMBERS")
```

Each row: `Member Ticker and Exchange Code`. Concatenate `<TICKER>
CDS USD SR 5Y D14 Corp` to back-fill member-level spreads:

```
   A             B                                       C
1  Member        Member CDS ticker                       Spread
2  =BDS(...)     ="JPM" & " CDS USD SR 5Y D14 Corp"      =BDP(B2,"PX_LAST")
                 (built from A2's "Member" field)
```

## 9 · Sovereign CDS curve (5Y default)

```excel
=BDP("ITALY CDS USD SR 5Y D14 Corp",   "PX_LAST")
=BDP("SPAIN CDS USD SR 5Y D14 Corp",   "PX_LAST")
=BDP("PORTUG CDS USD SR 5Y D14 Corp",  "PX_LAST")
=BDP("GREECE CDS USD SR 5Y D14 Corp",  "PX_LAST")
=BDP("FRANCE CDS USD SR 5Y D14 Corp",  "PX_LAST")
=BDP("DBR CDS USD SR 5Y D14 Corp",     "PX_LAST")    ' Germany
=BDP("UKIN CDS USD SR 5Y D14 Corp",    "PX_LAST")
=BDP("USGB CDS USD SR 5Y D14 Corp",    "PX_LAST")
=BDP("JAPAN CDS USD SR 5Y D14 Corp",   "PX_LAST")
=BDP("CHINA CDS USD SR 5Y D14 Corp",   "PX_LAST")
=BDP("BRAZIL CDS USD SR 5Y D14 Corp",  "PX_LAST")
=BDP("MEX CDS USD SR 5Y D14 Corp",     "PX_LAST")
=BDP("TURKEY CDS USD SR 5Y D14 Corp",  "PX_LAST")
=BDP("SOAF CDS USD SR 5Y D14 Corp",    "PX_LAST")    ' South Africa
=BDP("INDON CDS USD SR 5Y D14 Corp",   "PX_LAST")
=BDP("PHILIP CDS USD SR 5Y D14 Corp",  "PX_LAST")
=BDP("SAUDI CDS USD SR 5Y D14 Corp",   "PX_LAST")
=BDP("RUSSIA CDS USD SR 5Y D14 Corp",  "PX_LAST")    ' limited post-2022
```

Some sovereigns also quote in EUR: `ITALY CDS EUR SR 5Y D14 Corp`.

## 10 · Credit total-return / IG-HY indices (cash side)

```excel
=BDP("LECCTREU Index", "PX_LAST")     ' Euro IG Aggregate TR
=BDP("LF98TREU Index", "PX_LAST")     ' Euro HY TR
=BDP("G0Q0 Index",     "PX_LAST")     ' ICE BofA US Corporate TR
=BDP("H0A0 Index",     "PX_LAST")     ' ICE BofA US HY TR
=BDP("ER00 Index",     "PX_LAST")     ' ICE BofA Euro Corp
=BDP("HE00 Index",     "PX_LAST")     ' ICE BofA Euro HY
=BDP("JCEMCM Index",   "PX_LAST")     ' CEMBI Composite TR
=BDP("JPEIDIVR Index", "PX_LAST")     ' EMBI Global Diversified
=BDP("LEMBTRUU Index", "PX_LAST")     ' Bloomberg EM USD Bond TR
=BDP("LUACTRUU Index", "PX_LAST")     ' Bloomberg US Corp Aggregate TR
=BDP("LUH9TRUU Index", "PX_LAST")     ' Bloomberg US HY TR
=BDP("LBUSTRUU Index", "PX_LAST")     ' Bloomberg US Aggregate TR
```

Each of these has matching `OAS_SPREAD_MID` (index-level OAS):

```excel
=BDP("LECCTREU Index", "OAS_SPREAD_MID")     ' Euro IG OAS (bps)
=BDP("LF98TREU Index", "OAS_SPREAD_MID")     ' Euro HY OAS
=BDP("H0A0 Index",     "OAS_SPREAD_MID")     ' US HY OAS
```

## 11 · Default-probability and recovery

```excel
=BDP("EDPPL CDS EUR SR 5Y D14 Corp", "CDS_IMPLIED_DEFAULT_PROB")
=BDP("EDPPL CDS EUR SR 5Y D14 Corp", "CDS_RECOVERY_RATE")
=BDP("EDPPL CDS EUR SR 5Y D14 Corp", "RISKY_DUR")

' Issuer-level (DRSK / DRAM models, available on equity ticker)
=BDP("EDP PL Equity", "DEFAULT_PROBABILITY")
=BDP("EDP PL Equity", "DEFAULT_RISK_LEVEL")        ' IG1 / IG2 / ...
=BDP("EDP PL Equity", "RTG_BB_DEFAULT_PROB")
```

Custom recovery for analytics:

```excel
=BDP("EDPPL CDS EUR SR 5Y D14 Corp", "CDS_IMPLIED_DEFAULT_PROB",
     "CDS_RECOVERY_RATE_OVERRIDE", "0.25")
```

## 12 · Sample monitor sheet

```
Sheet "Credit monitor":
   A                          B (5Y CDS)         C (1d Δ)          D (30d Δ)         E (1y high)        F (1y low)
1  iTraxx Main                =BDP("ITRX MAIN CDSI GEN 5Y Corp","PX_LAST")
                                                  =B1 - BDH(... TODAY()-1)
                                                                     =B1 - BDH(... TODAY()-30)
                                                                                       =MAX(BDH(... TODAY()-365, TODAY()))
                                                                                                          =MIN(BDH(... TODAY()-365, TODAY()))
2  iTraxx Xover
3  CDX IG
4  CDX HY
5  CDX EM
6  EDPPL 5Y
7  TEFE 5Y
8  VW 5Y
...
```

## 13 · Worked sovereign basis monitor

```
Sheet "Sov basis":
   A          B (10y govt yld)       C (5y CDS)            D (Bund 10y)         E (10y spread)
1  Italy      =BDP("GTITL10Y Govt","YLD_YTM_MID")
                                      =BDP("ITALY CDS USD SR 5Y D14 Corp","PX_LAST")
                                                            =BDP("GTDEM10Y Govt","YLD_YTM_MID")
                                                                                  =(B1-D1)*100
2  Spain      ...
3  Portugal   ...
4  France     ...
5  Greece     ...
```

## 14 · Pitfalls

- **Quote type**: most single-names quote par-spread (bps); some HY
  trade with running coupon and quote *upfront* (%). Read
  `CDS_QUOTE_TYPE` before trusting `PX_LAST`.
- **Series rolls semi-annually**: every March / September. `GEN`
  follows; `S42` pins. Backtests need consistent treatment.
- **Index composition changes**: 125-name iTraxx Main is *not* the
  same 125 names across series. For historical composition use
  `INDX_MEMBERS_HIST` (if entitled) or ISDA roll documentation.
- **CDS-cash basis sign**: many conventions. Stick to one
  formula (`basis = CDS_spread − bond_Z_spread`) and document.
- **Sovereign CDS conventions vary**: Italy / Greece typically
  quote upfront when distressed; periphery EUR-denominated CDS
  (`ITALY CDS EUR SR 5Y D14 Corp`) trades less than USD-denominated.
- **EUR-denominated CDS for non-EUR issuers**: e.g.
  `BRAZIL CDS EUR SR 5Y D14 Corp` exists but is much thinner —
  quotes can be stale.
- **Recovery assumption** is a *model input*, not a quote.
  Bloomberg's default may differ from your firm's; always set
  `CDS_RECOVERY_RATE_OVERRIDE` for reproducible PnL.
- **CDS DV01 ≠ bond DV01**: CDS DV01 is per-bp-of-spread; bond DV01
  is per-bp-of-yield. They are similar in magnitude but not
  interchangeable for hedging.
- **Sub vs senior** matters: `SUB` curves are wider and have lower
  recovery assumption. Don't substitute.
- **Restructuring clause**: D14 (2014 ISDA) standardised; D03
  varieties had MR / MM / NR clause variations. For pre-2014
  historical splices, document which clause you're stitching.
