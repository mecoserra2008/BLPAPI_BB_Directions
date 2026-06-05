# Bonds in Excel

Yellow keys: `Govt`, `Corp`, `Mtge`, `Muni`, `Pfd`, `M-Mkt`.

For the conceptual model (curves, spreads, ratings, identifiers),
see [docs/asset_classes/bonds.md](../../docs/asset_classes/bonds.md).
This file is the **Excel translation**.

## 1 · Identifying bonds from a cell

Five interchangeable forms, all usable directly in `BDP`:

```excel
=BDP("T 4.625 02/15/35 Govt",  "YLD_YTM_MID")     ' ticker + coupon + maturity
=BDP("DBR 2.5 08/15/54 Govt",  "YLD_YTM_MID")     ' decimal coupon (safer to type)
=BDP("/cusip/91282CHV9 Govt",  "PARSEKYABLE_DES") ' by CUSIP
=BDP("/isin/DE0001102614 Govt","PARSEKYABLE_DES") ' by ISIN
=BDP("/figi/BBG00FPNNVS3 Corp","PARSEKYABLE_DES") ' by FIGI
```

The `/cusip/`, `/isin/`, `/figi/` prefixes followed by **a space and
the yellow key** resolve the identifier to a security. Returning the
parseable ticker via `PARSEKYABLE_DES` gives you a "canonical"
ticker string to store.

### ISIN-driven workbook pattern

```
   A                B                              C                    D
1  ISIN             Bloomberg ticker               Yield                Z-spread
2  US91282CHV94     =BDP("/isin/" & A2 & " Govt", "PARSEKYABLE_DES")
                    =BDP("/isin/" & A2 & " Govt", "YLD_YTM_MID")
                    =BDP("/isin/" & A2 & " Govt", "Z_SPRD_MID")
3  DE0001102614     ...
```

When a panel comes from a portfolio system (ISIN-keyed), this is
the right way in: never construct the ticker manually.

## 2 · Generic on-the-run benchmarks

The constant-maturity benchmarks Bloomberg rolls for you:

```excel
=BDP("GT2 Govt",       "YLD_YTM_MID")    ' US 2y
=BDP("GT5 Govt",       "YLD_YTM_MID")    ' US 5y
=BDP("GT10 Govt",      "YLD_YTM_MID")    ' US 10y
=BDP("GT30 Govt",      "YLD_YTM_MID")    ' US 30y
=BDP("GTGBP10Y Govt",  "YLD_YTM_MID")    ' UK 10y gilt
=BDP("GTDEM10Y Govt",  "YLD_YTM_MID")    ' German 10y bund
=BDP("GTJPY10Y Govt",  "YLD_YTM_MID")    ' JGB 10y
=BDP("GTITL10Y Govt",  "YLD_YTM_MID")    ' BTP 10y
=BDP("GTESP10Y Govt",  "YLD_YTM_MID")    ' Bonos 10y
=BDP("GTPTE10Y Govt",  "YLD_YTM_MID")    ' OT 10y
=BDP("GTFRF10Y Govt",  "YLD_YTM_MID")    ' OAT 10y
=BDP("GTBRL10Y Govt",  "YLD_YTM_MID")    ' Brazil 10y BRL
=BDP("GTMXN10Y Govt",  "YLD_YTM_MID")    ' Mexico 10y MXN
=BDP("GTCNY10Y Govt",  "YLD_YTM_MID")    ' China 10y CGB
```

For history, swap `BDP` → `BDH`:

```excel
=BDH("GT10 Govt", "YLD_YTM_MID",
     DATE(2014,1,1), TODAY(),
     "Per=cdr", "Days=W", "Fill=P", "UseDPDF=N")
```

## 3 · Pricing & yield fields with `BDP`

```excel
=BDP("T 4.625 02/15/35 Govt", "PX_LAST")          ' clean last
=BDP("T 4.625 02/15/35 Govt", "PX_BID")
=BDP("T 4.625 02/15/35 Govt", "PX_ASK")
=BDP("T 4.625 02/15/35 Govt", "PX_MID")
=BDP("T 4.625 02/15/35 Govt", "PX_DIRTY_MID")     ' dirty (incl. accrued)
=BDP("T 4.625 02/15/35 Govt", "ACCRUED_INTEREST")
=BDP("T 4.625 02/15/35 Govt", "YLD_YTM_BID")
=BDP("T 4.625 02/15/35 Govt", "YLD_YTM_ASK")
=BDP("T 4.625 02/15/35 Govt", "YLD_YTM_MID")
=BDP("T 4.625 02/15/35 Govt", "YLD_YTW_MID")      ' yield to worst
=BDP("T 4.625 02/15/35 Govt", "YLD_YTC_MID")      ' yield to call
=BDP("T 4.625 02/15/35 Govt", "PRICING_SOURCE")
=BDP("T 4.625 02/15/35 Govt", "PRC_AS_OF_DT")
```

### Clean vs dirty in `BDH`

```excel
' Clean price history
=BDH("EDP 1 ⅞ 03/14/35 Corp", "PX_LAST",
     DATE(2024,1,1), TODAY(),
     "Per=cdr", "Days=W", "Fill=P", "Quote=C")

' Dirty price history
=BDH("EDP 1 ⅞ 03/14/35 Corp", "PX_LAST",
     DATE(2024,1,1), TODAY(),
     "Per=cdr", "Days=W", "Fill=P", "Quote=D")

' Yield series (rather than price)
=BDH("EDP 1 ⅞ 03/14/35 Corp", "YLD_YTM_MID",
     DATE(2024,1,1), TODAY(),
     "Per=cdr", "Days=W", "Fill=P", "QtTyp=Y")
```

## 4 · Spreads & risk metrics

```excel
=BDP(A2, "G_SPRD_MID")          ' vs govt benchmark (bps)
=BDP(A2, "I_SPRD_MID")          ' vs interpolated swap (bps)
=BDP(A2, "Z_SPRD_MID")          ' zero-volatility spread (bps)
=BDP(A2, "OAS_SPREAD_MID")      ' OAS over swap curve (bps)
=BDP(A2, "ASSET_SWAP_SPD_MID")  ' asset-swap spread
=BDP(A2, "BENCHMARK_SECURITY")  ' what the spread is vs
=BDP(A2, "BENCHMARK_NAME")
=BDP(A2, "DUR_ADJ_MID")         ' modified duration
=BDP(A2, "DUR_ADJ_OAS_MID")     ' OAS-adjusted
=BDP(A2, "RISKY_DUR")           ' risky duration (CDS-style)
=BDP(A2, "MOD_DUR_MID")
=BDP(A2, "CONVEXITY")
=BDP(A2, "CONVEXITY_OAS")
=BDP(A2, "DV01")                ' $ value of 1bp
=BDP(A2, "WAL")                 ' weighted avg life
=BDP(A2, "EFF_DUR")
=BDP(A2, "KEY_RATE_DUR_2Y")
=BDP(A2, "KEY_RATE_DUR_5Y")
=BDP(A2, "KEY_RATE_DUR_10Y")
=BDP(A2, "KEY_RATE_DUR_30Y")
```

## 5 · YAS — analytics at a user-supplied price/yield

This is the Excel equivalent of clicking into **YAS <GO>** and
typing a different price. The override pattern:

```excel
' Implied yield + spreads from a clean price
=BDP("T 4.625 02/15/35 Govt", "YAS_BOND_YLD",
     "YAS_BOND_PX",  "98.50",
     "YAS_RISK_DT",  "20250506",
     "YAS_CURVE",    "S490")

' Implied price + duration from a target yield
=BDP("EDP 1 ⅞ 03/14/35 Corp", "YAS_BOND_PX",
     "YAS_BOND_YLD", "4.20",
     "YAS_RISK_DT",  "20250506",
     "YAS_CURVE",    "S514")

' Z-spread from the same user price
=BDP("EDP 1 ⅞ 03/14/35 Corp", "YAS_ZSPREAD",
     "YAS_BOND_PX",  "94.50",
     "YAS_RISK_DT",  "20250506",
     "YAS_CURVE",    "S514")

' OAS at a manual vol assumption
=BDP("AAPL 2.55 08/20/40 Corp", "YAS_OAS_SPREAD",
     "YAS_BOND_PX",        "82.30",
     "YAS_RISK_DT",        "20250506",
     "YAS_CURVE",          "S490",
     "OAS_VOL_BASIS_BVOL", "65")     ' 65 bp normal vol
```

YAS curve IDs you'll keep returning to:

| Override value | Curve |
|---|---|
| `S490` | USD SOFR OIS |
| `S514` | EUR €STR OIS |
| `S141` | GBP SONIA OIS |
| `S510` | JPY TONA OIS |
| `S023` | USD legacy LIBOR/3M swap |
| `S045` | EUR legacy 6M EURIBOR swap |
| `S016` | German bund govt |
| `S025` | US Treasury actives |
| `S022` | UK Gilt actives |

For the full list, `CRVF <GO>` on the Terminal.

### Worked YAS sheet

```
   A                            B (price)  C (settle)   D (curve)  E (yld)            F (zspread)        G (dur)
1  Bond                         Px         Settle       Curve      YAS_BOND_YLD       YAS_ZSPREAD        DUR_ADJ_MID
2  T 4.625 02/15/35 Govt        98.50      =TODAY()+1   S490
                                                                   =BDP($A2,"YAS_BOND_YLD","YAS_BOND_PX",TEXT($B2,"0.000"),"YAS_RISK_DT",TEXT($C2,"YYYYMMDD"),"YAS_CURVE",$D2)
                                                                                      =BDP($A2,"YAS_ZSPREAD",...)
                                                                                                        =BDP($A2,"DUR_ADJ_MID","YAS_BOND_PX",TEXT($B2,"0.000"))
```

Drag down for each bond. Edit columns B/C/D to re-run analytics
without touching formulas.

## 6 · Reference / static fields

```excel
=BDP(A2, "ISSUER")
=BDP(A2, "ISSUER_NAME")
=BDP(A2, "ISSUER_INDUSTRY")
=BDP(A2, "SECURITY_NAME")
=BDP(A2, "ISSUE_DT")
=BDP(A2, "MATURITY")
=BDP(A2, "ISSUE_PX")
=BDP(A2, "FIRST_COUPON_DT")
=BDP(A2, "LAST_COUPON_DT")
=BDP(A2, "CPN")
=BDP(A2, "CPN_TYP")            ' FIXED / FLOATING / ZERO / STEP
=BDP(A2, "CPN_FREQ")           ' 1, 2, 4, 12
=BDP(A2, "DAY_CNT_DES")        ' ACT/ACT, 30/360, ACT/360
=BDP(A2, "DAY_CNT")
=BDP(A2, "CALC_TYP_DES")
=BDP(A2, "AMT_ISSUED")
=BDP(A2, "AMT_OUTSTANDING")
=BDP(A2, "CRNCY")
=BDP(A2, "RANK")               ' senior / sub / secured ...
=BDP(A2, "PAYMENT_RANK")
=BDP(A2, "COUNTRY_FULL_NAME")
=BDP(A2, "COUNTRY_OF_RISK")
=BDP(A2, "MARKET_OF_ISSUE")
=BDP(A2, "MTY_TYP")            ' AT MATURITY / CALLABLE / PUTTABLE
=BDP(A2, "NXT_CALL_DT")
=BDP(A2, "NXT_CALL_PX")
=BDP(A2, "NXT_PUT_DT")
=BDP(A2, "COVERED_FLAG")
=BDP(A2, "GREEN_BOND_FLAG")
=BDP(A2, "SOCIAL_BOND_FLAG")
=BDP(A2, "SUSTAINABILITY_BOND_FLAG")
=BDP(A2, "SUKUK_FLAG")
=BDP(A2, "ID_BB_GLOBAL")       ' FIGI
=BDP(A2, "ID_ISIN")
=BDP(A2, "ID_CUSIP")
=BDP(A2, "ID_SEDOL1")
```

## 7 · Floaters

```excel
=BDP(A2, "FLT_BENCHMARK_INDEX")    ' SOFR / ESTR / EURIBOR / SONIA / TONA
=BDP(A2, "FLT_SPREAD")             ' bps over the index
=BDP(A2, "FLT_RESET_DT")
=BDP(A2, "FLT_RESET_FREQ")
=BDP(A2, "FLT_CAP")
=BDP(A2, "FLT_FLOOR")
=BDP(A2, "NEXT_RESET_DT")
=BDP(A2, "DISC_MARGIN")            ' discount margin (FRN spread analytics)
```

## 8 · Ratings

Snapshot:

```excel
=BDP(A2, "RTG_MOODY")
=BDP(A2, "RTG_SP")
=BDP(A2, "RTG_FITCH")
=BDP(A2, "RTG_BB_COMPOSITE")
=BDP(A2, "RTG_MOODY_OUTLOOK")
=BDP(A2, "RTG_SP_OUTLOOK")
=BDP(A2, "DEFAULT_PROBABILITY")        ' Bloomberg DRSK
```

Point-in-time:

```excel
=BDP(A2, "RTG_MOODY",  "RTG_AS_OF_DT", "20240101")
=BDP(A2, "RTG_SP",     "RTG_AS_OF_DT", "20240101")
```

Full history (bulk via `BDS`):

```excel
=BDS(A2, "RTG_MOODY_HIST")
=BDS(A2, "RTG_SP_HIST")
=BDS(A2, "RTG_FITCH_HIST")
=BDS(A2, "RTG_BB_COMP_HIST")
```

Each row: `Date`, `Rating`, `Outlook`, `Action`.

## 9 · Cash-flow schedules (bulk)

```excel
=BDS(A2, "CALL_SCHEDULE")           ' Date / Price / Type
=BDS(A2, "PUT_SCHEDULE")
=BDS(A2, "AMORT_SCHEDULE")          ' Date / Amount / Factor
=BDS(A2, "CPN_SCHEDULE")            ' step-ups / step-downs
=BDS(A2, "SINKING_FUND_SCHEDULE")
=BDS(A2, "INT_PMT_HIST")
=BDS(A2, "PAYMENT_HISTORY")
```

For a callable's "next call window" alongside the bond ticker:

```excel
B2: =BDP(A2, "NXT_CALL_DT")
C2: =BDP(A2, "NXT_CALL_PX")
D2: (start of bulk call schedule) =BDS(A2, "CALL_SCHEDULE")
```

`D2` will spill — leave room down and right.

## 10 · Capital structure & issuer

```excel
=BDS(A2, "CAPITAL_STRUCTURE_DETAILED")    ' full debt stack
=BDP(A2, "EQY_TICKER_FROM_DEBT")          ' issuer's listed equity
=BDP(A2, "ISSUER_PARENT_EQY_TICKER")
=BDP(A2, "PARENT_COMP_TICKER")
=BDP(A2, "ULT_PARENT_TICKER_EXCHANGE")
=BDP(A2, "NEAREST_LIQ_5Y_BOND")           ' the issuer's most liquid 5y
```

## 11 · MBS specifics

```excel
=BDP("FNCL 5.5 Mtge", "PX_LAST")
=BDP("FNCL 5.5 Mtge", "WAC")       ' weighted avg coupon
=BDP("FNCL 5.5 Mtge", "WAM")       ' weighted avg maturity
=BDP("FNCL 5.5 Mtge", "WALA")      ' weighted avg loan age
=BDP("FNCL 5.5 Mtge", "ORIG_AMT")
=BDP("FNCL 5.5 Mtge", "OUT_BAL")
=BDP("FNCL 5.5 Mtge", "PSA_SPEED")
=BDP("FNCL 5.5 Mtge", "CPR_1MO")
=BDP("FNCL 5.5 Mtge", "CPR_3MO")
=BDP("FNCL 5.5 Mtge", "CPR_6MO")
=BDP("FNCL 5.5 Mtge", "PREPAY_SPEED_RANGE")
=BDP("FNCL 5.5 Mtge", "MTG_TBA_PRICING")
```

## 12 · Money-market / T-bills

```excel
=BDP("B 0 12/05/25 Govt", "PX_DISCOUNT")
=BDP("B 0 12/05/25 Govt", "YLD_BANK_DISC")
=BDP("B 0 12/05/25 Govt", "YLD_DISC")
=BDP("B 0 12/05/25 Govt", "YLD_MMKT_BOND_EQUIV")
```

## 13 · Trading conventions / settlement

Compute a market-convention settlement date in Excel:

```excel
' US Treasuries: T+1
B2: =WORKDAY(TODAY(), 1, MyHolidayRange)

' EUR / UK / JP corp: T+2 (varies)
C2: =WORKDAY(TODAY(), 2, MyHolidayRange)
```

`MyHolidayRange` is a named range with holidays for the relevant
market. Bloomberg's `YAS_RISK_DT` override accepts whatever date you
pass — sanity-check against `WORKDAY` results.

## 14 · Common reproducible-research worksheet

```
Sheet "Universe":      one row per bond, columns A-F static metadata
Sheet "Live":          A=ticker, B-K live BDP analytics
Sheet "YAS":           A=ticker, B=user price, C=settle, D=curve, E-J YAS_* analytics
Sheet "History":       A=date, B+ one BDH per bond's YLD_YTM_MID
Sheet "Ratings":       per-bond historic ratings via BDS
Sheet "Cashflow":      per-bond CALL_SCHEDULE / AMORT_SCHEDULE
Sheet "Params":        named cells: RefDate, BondSettle, EURFunds, RatingAsOf, ...
```

## 15 · Pitfalls

- **Pence-quoted gilts**: `BARC LN Equity` is in pence; UK gilts
  are in £ par (100). Don't mix.
- **`PX_LAST` is clean for bonds**: add `ACCRUED_INTEREST` for
  dirty, or set `Quote=D` in `BDH`.
- **`adjustmentFollowDPDF` confuses bond panels**: not relevant for
  bonds but `UseDPDF=N` is still safer in `BDH`.
- **`#N/A Field Not Applicable`** on `BS_*` for a Govt bond: those
  fields don't apply to sovereigns. Pull issuer fields instead via
  `EQY_TICKER_FROM_DEBT` → equity-side fields.
- **YAS curve mismatch**: passing `YAS_CURVE=S490` (SOFR) on a EUR
  bond computes a USD-discounted Z-spread — wrong. Match curve to
  bond currency.
- **`#N/A Invalid Security`** when typing fractional coupons by
  hand: prefer the decimal form (`DBR 2.5 08/15/54 Govt`).
- **CDS recovery assumption**: `CDS_RECOVERY_RATE` defaults to 40%
  SR / 25% SUB. Override for non-standard names.
- **TIPS yields are real**: `YLD_YTM_MID` on a linker is the real
  yield. Pair with the breakeven to get nominal-equivalent.
- **Stale BVAL prints**: `LAST_PX_DT` tells you when the bond last
  traded / re-priced. Filter `IF(TODAY()-BDP(A2,"LAST_PX_DT")>5,
  "STALE", "OK")` for liquidity-aware panels.
