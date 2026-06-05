# Excel × Bloomberg — Quick Reference

## Functions

```excel
=BDP(security, field, [ovr1, val1], …)              ' single value
=BDH(security, field, start, end, [ovrs], [opts])   ' time series
=BDS(security, field, [ovrs], [opts])               ' bulk / table
=BEQS(screen_name, "PRIVATE" | "GLOBAL", [asOf])    ' universe from EQS
=BCURVE(curve_id, [date], [points])                 ' curve points
=BSRCH(domain)                                      ' security search
=BQL(universe, expression)                          ' modern DSL
```

## BDH option strings (most-used)

| Option | Values |
|---|---|
| `Per=` | `cdr`(daily), `cw`(weekly), `cm`(monthly), `cq`, `cs`, `cy` |
| `Days=` | `A`(all calendar), `W`(weekdays), `T`(trading days) |
| `Fill=` | `P`(previous), `B`(blank), `N`(NIL) |
| `Dir=` | `H`(horizontal), `V`(vertical, default) |
| `Sort=` | `A`(asc, default), `D`(desc) |
| `Cols=` | `Y`(header, default), `N`(no header) |
| `Dts=` | `S`(show, default), `H`(hide) |
| `QtTyp=` | `Y`(yield), `P`(price), `S`(spread) — bonds |
| `Quote=` | `C`(clean), `D`(dirty) — bonds |
| `cshAdjNormal=` | `Y` / `N` — apply cash divs |
| `cshAdjAbnormal=` | `Y` / `N` — apply specials |
| `CapChg=` | `Y` / `N` — apply splits |
| `UseDPDF=` | `Y` / `N` — follow `DPDF <GO>`; set **N** for reproducibility |
| `currency=` | `EUR` / `USD` / … |
| `Calendar=` | `US` / `EU` / `JPN` / `5D` / … |
| `Roll=` | `A`(active), `O`(open-int), `N`(notice), `F`(front) — generic futures |
| `Points=` | `Y` / `N` — FX forward points only |

## Overrides — paired args (`BDP` / `BDS`)

```excel
=BDP("AAPL US Equity", "BEST_EPS",
     "BEST_FPERIOD_OVERRIDE", "1FY",
     "BEST_DATA_RELEASE_DT", "20240131")
```

Most-used overrides (full list in
[`excel_overrides_syntax.md`](excel_overrides_syntax.md)):

| Override | Used with |
|---|---|
| `FUND_PER` | `IS_*`, `BS_*`, `CF_*` |
| `EQY_FUND_CRNCY` | fundamentals |
| `EQY_FUND_RELATIVE_PERIOD` | `-1Q`, `-1A`, … |
| `BEST_FPERIOD_OVERRIDE` | `1FY`, `2FY`, `1FQ`, `1BF` |
| `BEST_DATA_RELEASE_DT` | YYYYMMDD |
| `RTG_AS_OF_DT` | YYYYMMDD |
| `END_DATE_OVERRIDE` | `INDX_MWEIGHT_HIST` |
| `CHAIN_DATE` | `FUT_CHAIN`, `OPT_CHAIN` |
| `INCLUDE_EXPIRED_CONTRACTS` | `Y` / `N` |
| `YAS_BOND_PX` | bond YAS_* |
| `YAS_BOND_YLD` | bond YAS_* |
| `YAS_RISK_DT` | YYYYMMDD |
| `YAS_CURVE` | `S490` SOFR / `S514` €STR / `S141` SONIA / `S510` TONA |
| `CDS_RECOVERY_RATE_OVERRIDE` | decimal e.g. `0.40` |

## Cell-building tickers

```excel
=BDP(A2 & " Equity",         "PX_LAST")
=BDP(A2 & " " & B2,           C2)               ' col A ticker, col B yk, col C field
=BDP("/isin/" & A2 & " Govt", "PARSEKYABLE_DES")
=BDP("/cusip/" & A2 & " Corp","PARSEKYABLE_DES")
=BDP("/figi/" & A2 & " Corp", "PARSEKYABLE_DES")
```

Date as override:

```excel
=BDP($A2, "BEST_EPS",
     "BEST_DATA_RELEASE_DT", TEXT($B2,"YYYYMMDD"))
```

Number as override:

```excel
=BDP($A2, "YAS_BOND_YLD",
     "YAS_BOND_PX", TEXT($B2,"0.000000"))
```

## Worked recipes

### Fundamentals in EUR

```excel
=BDP("AAPL US Equity", "TRAIL_12M_REVENUE",
     "FUND_PER", "LTM",
     "EQY_FUND_CRNCY", "EUR")
```

### Point-in-time consensus

```excel
=BDP("AAPL US Equity", "BEST_EPS",
     "BEST_FPERIOD_OVERRIDE", "1FY",
     "BEST_DATA_RELEASE_DT",  "20240131")
```

### Historical index members (as of a past date)

```excel
=BDS("SX5E Index", "INDX_MWEIGHT_HIST",
     "END_DATE_OVERRIDE", "20231229")
```

### Bond yield from a clean price

```excel
=BDP("T 4.625 02/15/35 Govt", "YAS_BOND_YLD",
     "YAS_BOND_PX", "98.50",
     "YAS_RISK_DT", "20250506",
     "YAS_CURVE",   "S490")
```

### Z-spread on a corp

```excel
=BDP("EDP 1 ⅞ 03/14/35 Corp", "Z_SPRD_MID")
=BDP("EDP 1 ⅞ 03/14/35 Corp", "YAS_ZSPREAD",
     "YAS_BOND_PX","94.50","YAS_RISK_DT","20250506","YAS_CURVE","S514")
```

### Single-name CDS

```excel
=BDP("EDPPL CDS EUR SR 5Y D14 Corp", "PX_LAST")
=BDP("CDX IG CDSI GEN 5Y Corp",      "PX_LAST")
```

### Active futures chain

```excel
=BDS("CL1 Comdty", "FUT_CHAIN",
     "INCLUDE_EXPIRED_CONTRACTS", "N",
     "CHAIN_DATE", TEXT(TODAY(),"YYYYMMDD"))
```

### Historical generic future (active roll)

```excel
=BDH("TY1 Comdty", "PX_LAST",
     DATE(2014,1,1), TODAY(),
     "Per=cdr", "Days=T", "Fill=P", "Roll=A")
```

### FX spot at WMR 4pm London

```excel
=BDP("EURUSD WMCO Curncy", "PX_LAST")
=BDH("EURUSD WMCO Curncy", "PX_LAST",
     DATE(2010,1,1), TODAY(),
     "Per=cdr", "Days=W", "Fill=P")
```

### FX forward outright + points

```excel
=BDP("EURUSD3M Curncy", "PX_LAST")     ' outright
=BDP("EUR3M Curncy",    "PX_LAST")     ' points only
```

### NDF implied yield

```excel
=BDP("USDBRL3M Curncy", "IMPL_YIELD_NDF_PCT")
```

### Swap par rate

```excel
=BDP("USSO10 Curncy",  "PX_LAST")      ' 10y SOFR OIS
=BDP("EESWE10 Curncy", "PX_LAST")      ' 10y €STR OIS
=BDP("BPSO10 Curncy",  "PX_LAST")      ' 10y SONIA OIS
=BDP("JYSO10 Curncy",  "PX_LAST")      ' 10y TONA OIS
```

### XCCY basis

```excel
=BDP("EUBSC10 Curncy", "PX_LAST")      ' EUR/USD 10y, bps
=BDP("JYBSC10 Curncy", "PX_LAST")
=BDP("BPBSC10 Curncy", "PX_LAST")
```

### Inflation breakeven

```excel
=BDP("USGGBE10 Index", "PX_LAST")      ' pre-baked US 10y BE
=BDP("USSWITP10 Curncy", "PX_LAST")    ' US 10y CPI swap (ZC BE)
```

## Real-time

```excel
' Single cell (refresh-driven)
=BDP("AAPL US Equity", "LAST_PRICE")

' Subscription
=BLPSubscribe("EDP PL Equity", "LAST_PRICE", "interval=1.0")
=BLPUnsubscribe("EDP PL Equity")

' RTD-style
=RTD("bloomberglp.RTD", , "//blp/mktdata/ticker/EDP PL Equity", "LAST_PRICE")
```

## Errors quick map

| Cell shows | Meaning | First fix |
|---|---|---|
| `#NAME?` | Add-in not loaded | Re-tick in Add-Ins |
| `#N/A Requesting Data` (forever) | `bbcomm` down or Terminal locked | Restart `bbcomm` / unlock Terminal |
| `#N/A N/A` | Entitlement | `EUNI <GO>` |
| `#N/A Invalid Security` | Wrong yellow key / ticker typo | `DES <GO>` to confirm |
| `#N/A Field Not Applicable` | Field doesn't exist for this security | `<sec> FLDS <GO>` |
| `#SPILL!` | `BDS` / `BDH` array can't expand | Clear the spill range |

## Always-on defaults for research

- Bloomberg → Options → **Manual refresh**, **Refresh on Open: OFF**,
  **Use DPDF: OFF**.
- Every `BDH`: `"Per=cdr"`, `"Days=W"`, `"Fill=P"`, `"UseDPDF=N"`.
- Every fundamentals override: `EQY_FUND_CRNCY` pinned.
- Every PIT estimate: `BEST_DATA_RELEASE_DT` pinned.
- Every YAS: `YAS_RISK_DT` + `YAS_CURVE` pinned.

## Two-character locale gotcha

US/UK Excel uses `,` as argument separator.
DE/FR/ES/PT-PT Excel uses `;`. All examples above use `,`. Convert
if your locale defaults to `;` (Excel does it automatically when
you paste).
