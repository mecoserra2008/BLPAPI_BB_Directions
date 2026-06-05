# Overrides — Excel Syntax

## Rules

- **Pairs**: every override is **two arguments** — the override
  fieldId, then the value.
- **Strings**: both arguments are strings. Wrap cell references
  with `TEXT()` for dates and numbers when in doubt.
- **`BDP` / `BDS`**: pairs go after `field`. Order doesn't matter.
- **`BDH`**: pairs go after `start`/`end`, before option strings.
- **Case-sensitive fieldId**: override names are **uppercase**.
- **Odd count = silent ignore**: if you forget a value, Bloomberg
  uses the un-overridden default. No warning.

## Skeleton

```excel
=BDP(security, field,
     "OVR1_FIELDID", "value1",
     "OVR2_FIELDID", "value2",
     ...)

=BDH(security, field, start, end,
     "OVR1_FIELDID", "value1",
     "OVR2_FIELDID", "value2",
     "Per=cdr", "Days=W", "Fill=P", "UseDPDF=N")

=BDS(security, field,
     "OVR1_FIELDID", "value1",
     "OVR2_FIELDID", "value2")
```

## Fundamentals period selection

| Override | Values | Example |
|---|---|---|
| `FUND_PER` | `Q`, `S`, `A`, `Y`, `LTM` | `=BDP(...,"FUND_PER","LTM")` |
| `EQY_FUND_RELATIVE_PERIOD` | `0`, `-1`, `-2`, `-1Q`, `-1A`, `-2A` | |
| `EQY_FUND_YEAR` | `"2024"` | |
| `FUND_PER_END_DT` | `"YYYYMMDD"` | |
| `RELATIVE_PERIOD_OVERRIDE` | as above | generic alias |
| `EQY_FUND_CRNCY` | ISO (`USD`, `EUR`, `JPY`, …) | |

```excel
' LTM revenue, USD
=BDP("AAPL US Equity","IS_REVENUE","FUND_PER","LTM","EQY_FUND_CRNCY","USD")

' Q-3 ROE
=BDP("AAPL US Equity","RETURN_COM_EQY","FUND_PER","Q","EQY_FUND_RELATIVE_PERIOD","-3Q")
```

## Estimates (BEst)

| Override | Values |
|---|---|
| `BEST_FPERIOD_OVERRIDE` | `1FY`, `2FY`, `3FY`, `1FQ`, `2FQ`, ... `1BF` (blended), `1FH` |
| `BEST_FY_OVERRIDE` | `"2025"` |
| `BEST_DATA_RELEASE_DT` | `"YYYYMMDD"` — point-in-time snapshot |
| `RELATIVE_PERIOD_OVERRIDE` | `-1Q`, `-1A` |
| `EARN_HIST_TYPE_FILTER` | `First Call`, `Comparable`, `As Reported` |

```excel
' Point-in-time forward-FY EPS as of 31-Jan-2024
=BDP("AAPL US Equity","BEST_EPS",
     "BEST_FPERIOD_OVERRIDE","1FY",
     "BEST_DATA_RELEASE_DT","20240131")
```

## YAS (user-supplied price/yield analytics)

| Override | Use |
|---|---|
| `YAS_BOND_PX` | Clean price (string e.g. `"98.50"`) |
| `YAS_BOND_YLD` | Yield (e.g. `"4.32"`) |
| `YAS_RISK_DT` | Settle (YYYYMMDD) |
| `YAS_CURVE` | Curve id — `S490` (SOFR), `S514` (€STR), `S141` (SONIA), `S510` (TONA) |
| `YAS_ZSPREAD` | Spread input |
| `YAS_OAS_SPREAD` | OAS input |
| `YAS_ASW_SPREAD` | ASW input |
| `YAS_ISPREAD` | I-spread input |
| `OAS_VOL_BASIS_BVOL` | Vol for OAS (bp normal) |
| `YAS_BENCHMARK_BOND` | Force benchmark for spread |

```excel
=BDP("T 4.625 02/15/35 Govt","YAS_BOND_YLD",
     "YAS_BOND_PX","98.50",
     "YAS_RISK_DT","20250506",
     "YAS_CURVE","S490")
```

## Index members / weights

| Override | Use |
|---|---|
| `END_DATE_OVERRIDE` | `INDX_MWEIGHT_HIST` — members as of date |
| `START_DATE_OVERRIDE` | beginning of additions/deletions window |
| `INDEX_RATIO_ADJ_TYPE` | weighting method |
| `REFERENCE_DATE` | as-of for `PORTFOLIO_DATA` etc. |

```excel
=BDS("SX5E Index","INDX_MWEIGHT_HIST","END_DATE_OVERRIDE","20231229")
```

## Futures / option chains

| Override | Use |
|---|---|
| `INCLUDE_EXPIRED_CONTRACTS` | `"Y"` / `"N"` for `FUT_CHAIN`, `OPT_CHAIN` |
| `CHAIN_DATE` | `"YYYYMMDD"` |
| `CHAIN_POINTS_OVRD` | depth |
| `CHAIN_PERIODICITY_OVERRIDE` | `MONTHLY`, etc. |
| `CHAIN_EXP_DT_OVRD` | a single expiry for option chains |
| `OPTION_CHAIN_OVERRIDE` | `EXPIRATION`, `C`, `P`, `all` |
| `ROLL_METHOD` (in `BDH` option, not paired override) | `ACTIVE`, `OPEN_INT`, `RELATIVE`, `FRONT`, `RELATIVE_TO_FIRST_NOTICE` |

```excel
=BDS("CL1 Comdty","FUT_CHAIN",
     "INCLUDE_EXPIRED_CONTRACTS","Y",
     "CHAIN_DATE","20250502")
```

## Ratings

| Override | Use |
|---|---|
| `RTG_AS_OF_DT` | YYYYMMDD — point-in-time rating |

```excel
=BDP("EDP 1 ⅞ 03/14/35 Corp","RTG_MOODY","RTG_AS_OF_DT","20240101")
```

## CDS

| Override | Use |
|---|---|
| `CDS_QUOTE_TYPE_OVERRIDE` | `"Par Spread"` / `"Upfront"` |
| `CDS_RECOVERY_RATE_OVERRIDE` | decimal e.g. `"0.40"` |
| `CDS_FX_RATE_OVERRIDE` | cross-currency CDS PnL |

```excel
=BDP("EDPPL CDS EUR SR 5Y D14 Corp","CDS_IMPLIED_DEFAULT_PROB",
     "CDS_RECOVERY_RATE_OVERRIDE","0.25")
```

## FX / forwards

| Override | Use |
|---|---|
| `SETTLE_DT` | Specific value date |
| `FX_FORWARD_TENOR` | `"1M"`, `"3M"`, `"1Y"` |
| `FORWARD_DATE` | alias |

## Calendars / timezones

| Override | Use |
|---|---|
| `CALENDAR_CODE` | `"US"`, `"EU"`, `"GR"`, `"CME"`, `"SIFMA"`, … |
| `TIME_ZONE_OVERRIDE` | numeric tz id |

## Dividends

| Override | Use |
|---|---|
| `EQY_INC_DVD_TYPES_FILTER` | `"All"`, `"Regular"`, `"Special"`, `"Stock"` |
| `START_DATE`, `END_DATE` | bulk window |

## Holdings / portfolios

| Override | Use |
|---|---|
| `FUND_HOLDINGS_OVERRIDE` | `"Y"` for full vs default top-10 |
| `REFERENCE_DATE` | historical holdings |
| `PORTFOLIO_AS_OF_DATE` | PRTU portfolio |
| `PORTFOLIO_REPORTING_CRNCY` | currency |

## Worked: dates from cells

Dates in Excel are serial numbers; Bloomberg wants `YYYYMMDD`
strings.

```excel
' D2 holds an Excel date
=BDP($A2,"BEST_EPS",
     "BEST_DATA_RELEASE_DT", TEXT($D2,"YYYYMMDD"))

' D2 holds a yield number
=BDP($A2,"YAS_BOND_PX",
     "YAS_BOND_YLD", TEXT($D2,"0.0000"))
```

## Worked: cached override blocks via named ranges

Define once in **Formulas → Name Manager**:

| Name | Refers to |
|---|---|
| `EUR` | `="EUR"` |
| `FundsCcy` | `="EQY_FUND_CRNCY"` |
| `Period1FY` | `="1FY"` |
| `PerFP` | `="BEST_FPERIOD_OVERRIDE"` |
| `BondCurveEUR` | `="S514"` |
| `BondCurveUSD` | `="S490"` |
| `RefDate` | a cell where you type the as-of |
| `Today` | `=TEXT(TODAY(),"YYYYMMDD")` |
| `Settle` | `=TEXT(WORKDAY(TODAY(),2),"YYYYMMDD")` |

Then:

```excel
=BDP($A2,"BEST_EPS", PerFP, Period1FY, "BEST_DATA_RELEASE_DT", Today)
=BDP($A2,"TRAIL_12M_REVENUE", FundsCcy, EUR)
=BDP($A2,"YAS_BOND_YLD","YAS_BOND_PX",TEXT($B2,"0.000"),"YAS_RISK_DT",Settle,"YAS_CURVE",BondCurveEUR)
=BDS("SX5E Index","INDX_MWEIGHT_HIST","END_DATE_OVERRIDE",RefDate)
```

Edit `RefDate` once → every panel re-runs as-of that date.

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Forgot value for an override | Returns un-overridden value silently | Make sure pairs |
| Date passed as cell number, not string | Wrong / no data | `TEXT(...,"YYYYMMDD")` |
| Lowercase override fieldId | Override ignored | Always uppercase |
| `EQY_FUND_CRNCY` on a price (not fundamental) | Ignored | Use `currency=` option in `BDH` |
| `BEST_FPERIOD_OVERRIDE=1FY` and `BEST_FY_OVERRIDE=2025` | Conflict; behaviour undefined | Pick one |
| YAS curve mismatched to bond CCY | Spreads off | `S490` for USD, `S514` for EUR, etc. |
| `RTG_AS_OF_DT` on a non-rated security | Returns blank | Confirm name is rated |
| Override on a bulk field (`BDS`) on a security with no rows | `#N/A` | Wrap in `IFERROR` |
| Comma vs semicolon separator (locale) | `#NAME?` | Use the separator your Excel locale expects |
