# 03 · Tickers, Overrides & Calendars in Excel

How to write tickers from cell parts, pass overrides without losing
your mind, control calendars and fills, and structure a workbook so
overrides are reusable.

## 3.1 Building tickers from cells

The most-used pattern: ticker in column A, yellow key constant,
field in column B.

```
   A                       B            C
1  ticker                  field        value
2  AAPL US                 PX_LAST      =BDP(A2 & " Equity", B2)
3  MSFT US                 PX_LAST      =BDP(A2 & " Equity", B2)
4  EURUSD                  PX_LAST      =BDP(A2 & " Curncy",  B2)
5  T 4.625 02/15/35        YLD_YTM_MID  =BDP(A2 & " Govt",   B2)
```

Or split yellow key into its own cell:

```
   A           B          C            D
1  ticker      yk         field        value
2  AAPL US     Equity     PX_LAST      =BDP(A2 & " " & B2, C2)
3  EURUSD      Curncy     PX_LAST      =BDP(A2 & " " & B2, C2)
4  CL1         Comdty     PX_LAST      =BDP(A2 & " " & B2, C2)
```

For multiple fields across columns:

```
   A                B          C             D            E
1  ticker           PX_LAST    CUR_MKT_CAP   BEST_PE     RTG_BB
2  AAPL US Equity   =BDP($A2, B$1) =BDP($A2,C$1) =BDP($A2,D$1) =BDP($A2,E$1)
```

Notice the **mixed reference style**: `$A2` (lock column, free row),
`B$1` (free column, lock row). Drag fills correctly in both
directions.

## 3.2 Constructing ticker strings safely

| Issue | Fix |
|---|---|
| Trailing spaces from copy-paste | `=TRIM(A2) & " Equity"` |
| Mixed case | `=UPPER(TRIM(A2)) & " Equity"` |
| Cell may be blank | `=IF(A2="","",BDP(A2 & " Equity", "PX_LAST"))` |
| ISIN lookup | `=BDP("/isin/" & A2, "PARSEKYABLE_DES")` |
| CUSIP lookup | `=BDP("/cusip/" & A2, "PARSEKYABLE_DES")` |
| FIGI lookup | `=BDP("/bbgid/" & A2, "PARSEKYABLE_DES")` |
| Add ` Govt` only if not present | `=A2 & IF(RIGHT(A2,5)=" Govt",""," Govt")` |

For complex tickers (bonds with fractional coupons, options with
strikes), do the assembly once in a helper column rather than
inline.

## 3.3 Special characters in tickers

Some Bloomberg tickers contain fractions (`½`, `⅛`, `⅝`, `⅞`). They
must appear as those exact Unicode characters, not as `1/2` or
`0.5`. The most portable workaround is to paste the canonical ticker
from `DES <GO>` or use the decimal coupon form:

```excel
' Both work, second is safer when typing:
=BDP("DBR 2 ½ 08/15/54 Govt", "YLD_YTM_MID")
=BDP("DBR 2.5 08/15/54 Govt", "YLD_YTM_MID")
```

For the **single-letter ag tickers** (corn, soy, wheat), keep the
single space:

```excel
=BDP("C 1 Comdty", "PX_LAST")          ' corn front-month
=BDP("W 1 Comdty", "PX_LAST")          ' wheat
=BDP("S 1 Comdty", "PX_LAST")          ' soy
```

## 3.4 Override pairs — the rules

Every override is **two arguments**:

```excel
=BDP(security, field,
     "OVR1_NAME", "value1",
     "OVR2_NAME", "value2",
     ...)
```

- The override name is a **field id** (uppercase, exact spelling).
- The value is a **string**.
- Order between overrides doesn't matter.
- Mixing override pairs with `key=value` options inside the same
  function is allowed only on `BDH` / `BDS` — `BDP` accepts pairs
  only.

### Common override patterns (lifted from `cheatsheets/overrides_index.md`)

```excel
' Currency-converted fundamental
=BDP("AAPL US Equity", "TRAIL_12M_REVENUE",
     "EQY_FUND_CRNCY", "EUR")

' LTM earnings
=BDP("AAPL US Equity", "TRAIL_12M_NET_INC",
     "FUND_PER", "LTM",
     "EQY_FUND_CRNCY", "USD")

' Point-in-time consensus
=BDP("AAPL US Equity", "BEST_EPS",
     "BEST_FPERIOD_OVERRIDE", "1FY",
     "BEST_DATA_RELEASE_DT", "20240131")

' Bond yield from a user-supplied price
=BDP("T 4.625 02/15/35 Govt", "YAS_BOND_YLD",
     "YAS_BOND_PX", "98.50",
     "YAS_RISK_DT", "20250506",
     "YAS_CURVE",   "S490")

' Historical index members
=BDS("SX5E Index", "INDX_MWEIGHT_HIST",
     "END_DATE_OVERRIDE", "20231229")

' Specific-date futures chain
=BDS("CL1 Comdty", "FUT_CHAIN",
     "INCLUDE_EXPIRED_CONTRACTS", "Y",
     "CHAIN_DATE", "20250502")

' Point-in-time rating
=BDP("EDP 1 ⅞ 03/14/35 Corp", "RTG_MOODY",
     "RTG_AS_OF_DT", "20240101")

' Specific reference date for portfolio members
=BDP("U12345678-12 Client", "PORTFOLIO_DATA",
     "REFERENCE_DATE", "20250502")
```

## 3.5 Override values from cells

It's idiomatic to keep the override values in cells and reference
them:

```
   A                       B          C       D
1  Security                Price      Settle  YAS_CURVE
2  T 4.625 02/15/35 Govt   98.50      20250506  S490

=BDP($A2, "YAS_BOND_YLD",
     "YAS_BOND_PX", TEXT($B2,"0.000000"),
     "YAS_RISK_DT", TEXT($C2,"YYYYMMDD"),
     "YAS_CURVE",   $D2)
```

Why `TEXT(...)`:

- A cell holding a date is a serial number. Bloomberg wants
  `"20250506"` not `45782`. `TEXT(B2,"YYYYMMDD")` does the job.
- A cell holding a number like `98.5` becomes `"98.5"` in arg
  passing — which Bloomberg accepts, but `TEXT(...,"0.000000")` is
  more deterministic.

Tip: define **named ranges** for frequently-used override blocks.

```excel
' Named range "BondSettle" = "20250506"
=BDP($A2, "YAS_BOND_YLD", "YAS_RISK_DT", BondSettle, …)
```

## 3.6 Calendars for `BDH`

Calendar codes you'll actually use in `Calendar=…`:

| Code | Calendar |
|---|---|
| `US` | NYSE / NASDAQ |
| `EU` | TARGET / Eurozone |
| `UK` | LSE |
| `JPN` | TSE |
| `DE` | Xetra |
| `FR` | Paris |
| `IT` | Borsa Italiana |
| `ES` | BME |
| `PT` | Euronext Lisbon |
| `HK` | HKEX |
| `CH` | SIX |
| `5D` | Weekdays, no holidays |
| `7D` | All calendar days |
| `NTM` | Next-trading-month (security default) |
| `CME` | CME futures |
| `SIFMA` | US bond market early-close calendar |

Example:

```excel
=BDH("EDP PL Equity", "PX_LAST",
     DATE(2014,1,1), TODAY(),
     "Calendar=PT", "Per=cdr", "Days=T", "Fill=P")
```

When joining series from different markets, pick **one** calendar
(usually `5D` weekdays) and forward-fill: cross-market holidays
otherwise create offset bars.

## 3.7 `Per=` × `Days=` × `Fill=` matrix

`BDH` periodicity, day-count and fill together govern what the
output series actually contains.

| Combo | What you get |
|---|---|
| `Per=cdr`, `Days=A`, `Fill=P` | Every calendar day (incl. weekends), filled forward |
| `Per=cdr`, `Days=W`, `Fill=P` | Weekdays only, filled across non-trading weekdays |
| `Per=cdr`, `Days=T`, `Fill=P` | Trading days only, no fill needed |
| `Per=cdr`, `Days=W`, `Fill=B` | Weekdays, blank on non-trading |
| `Per=cm`, `Days=W`, `Fill=P` | Month-end weekday |
| `Per=cq`, `Days=W`, `Fill=P` | Quarter-end weekday |

For **research panels**, the canonical combo is
`Per=cdr / Days=W / Fill=P / UseDPDF=N`. It's reproducible across
markets without you forgetting which calendar applies.

## 3.8 Refresh control

Bloomberg formulas re-fetch in these situations:

1. **Cell entry / edit** — fresh formula always pulls.
2. **Cell dependency change** — input cell changed, formula
   re-evaluates.
3. **Manual refresh** — Bloomberg ribbon → Refresh Worksheet /
   Selection / All.
4. **Auto refresh** — if enabled in **Options → Refresh**, every
   N minutes.
5. **Real-time** — `BDP` returning a real-time field updates as
   ticks arrive.
6. **Open workbook** — if **Refresh on Open** is enabled.
7. **VBA** — `Application.Run "BLP.RefreshAll"`.

Big-workbook discipline:

- Turn off **Refresh on Open**.
- Use **Manual refresh** as the default.
- Section your workbook (one tab per asset class), refresh only
  the section you're editing.
- For monitors / dashboards, prefer `BLPSubscribe` over `BDP` with
  real-time refresh — see [05](05_realtime_rtd.md).

## 3.9 Named ranges for reusable blocks

A small workbook hygiene trick. Define:

| Name | Refers to |
|---|---|
| `Today` | `=TEXT(TODAY(),"YYYYMMDD")` |
| `EURFunds` | `="EQY_FUND_CRNCY"` (the override key) |
| `EUR` | `="EUR"` |
| `BondSettle` | `=TEXT(TODAY()+2,"YYYYMMDD")` |
| `RefDate` | (cell where you type a date — used everywhere) |

Then every formula references those:

```excel
=BDP($A2, "TRAIL_12M_REVENUE", EURFunds, EUR)
=BDP($A2, "RTG_MOODY", "RTG_AS_OF_DT", Today)
=BDS("SX5E Index", "INDX_MWEIGHT_HIST", "END_DATE_OVERRIDE", RefDate)
```

A single edit of `RefDate` re-runs the panel as-of a different date.

## 3.10 Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Override field id misspelled | Returns un-overridden value silently | Pull `FieldInfoRequest` once to confirm spelling; standardise via named ranges |
| Odd number of override args | Returns un-overridden value silently | Always pairs |
| Date as raw cell value (serial number) | Returns wrong / no data | Wrap in `TEXT(...,"YYYYMMDD")` |
| Currency override on a price (not a fundamental) | Ignored | `currency=` option in `BDH`, not an override on `BDP` |
| `Calendar=NTM` mixed with `Fill=P` and `Days=A` | Inconsistent series | Pick `Days=W` or `Days=T` deliberately |
| Cells with leading/trailing spaces in tickers | `#N/A Invalid Security` | `TRIM()` |
| Capital-letter mismatch in field names | `#N/A Field Not Applicable` | Field mnemonics are always uppercase |
| `BDS` overlap on an already-populated range | `#SPILL!` | Clear the range; or pre-size in older Excel and array-enter |
