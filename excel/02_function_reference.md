# 02 · Function Reference

The Excel add-in exposes seven formulas. Three of them are 90% of
daily use; the others are situational.

| Function | Purpose | Returns |
|---|---|---|
| `BDP` | Bloomberg Data Point | Single value (one cell) |
| `BDH` | Bloomberg Data History | Time series (vertical or horizontal array) |
| `BDS` | Bloomberg Data Set | Bulk / table-shaped field (multi-cell array) |
| `BEQS` | Bloomberg Equity Screen | List of tickers from a saved EQS screen |
| `BCURVE` | Curve points | Tenors × discount factors / forward rates |
| `BSRCH` | Security search | Tickers matching a domain query |
| `BQL` | Bloomberg Query Language | DSL — single value, time series, or table |

All seven use **comma-separated arguments** on US/UK Excel and
**semicolons** on continental-Europe locales (DE / FR / ES / PT-PT).
Examples here use commas.

---

## 2.1 `BDP` — Bloomberg Data Point

### Signature

```
=BDP(security, field, [override1, value1, override2, value2, …])
```

| Argument | Type | Notes |
|---|---|---|
| `security` | string | A Bloomberg ticker with yellow key — `"AAPL US Equity"`, `"T 4.625 02/15/35 Govt"`, `"EURUSD Curncy"`. |
| `field` | string | A field mnemonic — `"PX_LAST"`, `"YLD_YTM_MID"`, `"BEST_EPS"`. |
| `override<i>, value<i>` | string pairs | Optional. **Every override comes as TWO arguments**: the override field id, then the value. Both are strings. |

### Examples

```excel
=BDP("AAPL US Equity", "PX_LAST")
=BDP("EDP PL Equity", "BEST_EPS", "BEST_FPERIOD_OVERRIDE", "1FY")
=BDP("T 4.625 02/15/35 Govt", "YAS_BOND_YLD",
     "YAS_BOND_PX", "98.50",
     "YAS_RISK_DT", "20250506",
     "YAS_CURVE",   "S490")
=BDP(A2 & " Equity", "CUR_MKT_CAP", "EQY_FUND_CRNCY", "EUR")
=BDP("/isin/" & A2, "PARSEKYABLE_DES")           ' resolve ISIN → ticker
```

### Behaviour

- Returns a **single cell** value. Use it for snapshots.
- Multi-cell selection + array entry (`Ctrl+Shift+Enter`) doesn't
  give you more values — you'd still get the same single value
  filled into each cell. Use `BDS` for tables.
- Override values are **strings**, including dates (`"20250506"`)
  and decimals (`"98.50"`). Excel coerces, but be defensive — pass
  via `TEXT(B2,"YYYYMMDD")` for dates from cells.
- The cell shows `#N/A Requesting Data` while in flight. Force
  refresh via **Bloomberg → Refresh Selection** or `Application.Run
  "BLP.RefreshAll"`.

### Override-pair gotcha

`BDP("AAPL US Equity", "BEST_EPS", "BEST_FPERIOD_OVERRIDE")` (3
arguments — odd) is **silently wrong** and returns the un-
overridden value. Overrides must come in pairs. Excel doesn't warn.

---

## 2.2 `BDH` — Bloomberg Data History

### Signature

```
=BDH(security, field, start, end,
     [override1, value1, …],
     [option1=value1, option2=value2, …])
```

| Argument | Type | Notes |
|---|---|---|
| `security` | string or cell | One ticker. For multiple, write multiple `BDH`s. |
| `field` | string or array | One field or `{"PX_LAST","PX_VOLUME"}` array. |
| `start` | date or `"YYYYMMDD"` | Inclusive. Use `DATE(2014,1,1)` or `"20140101"`. |
| `end` | date or `"YYYYMMDD"` | Inclusive. `TODAY()` is fine. |
| Overrides | string pairs | Same as `BDP` overrides. |
| Options | `"key=value"` strings | The big list (below). Order doesn't matter. |

### Options (all string `"key=value"`)

| Option | Allowed values | Effect |
|---|---|---|
| `Per` | `cdr` (calendar daily, default), `cw` (weekly), `cm` (monthly), `cq` (quarterly), `cs` (semi-annual), `cy` (yearly) | Periodicity |
| `Days` | `A` (actual / calendar), `W` (weekdays), `T` (trading days) | Day count for return / fill |
| `Fill` | `P` (previous value), `B` (blank), `N` (NIL) | Non-trading day fill method |
| `Dir` | `H` (horizontal — dates across), `V` (vertical — dates down, default) | Output layout |
| `Sort` | `A` (ascending, default), `D` (descending) | Date sort order |
| `Cols` | `N` (no header row), `Y` (default header) | Column headers |
| `Dts` | `H` (hide date column), `S` (show date column, default) | Whether to render dates |
| `Headers` | `Y` / `N` | Synonym for `Cols` |
| `QtTyp` | `Y` (yield), `P` (price), `S` (spread) | Bond quote type |
| `Quote` | `C` (clean), `D` (dirty) | Clean vs dirty price |
| `cshAdjNormal` | `Y` / `N` | Apply cash divs |
| `cshAdjAbnormal` | `Y` / `N` | Apply spinoffs / specials |
| `CapChg` | `Y` / `N` | Apply capital-change adjustments (splits) |
| `UseDPDF` | `Y` / `N` | Follow Terminal's `DPDF <GO>` defaults — set **N** for reproducibility |
| `currency` | ISO code (`EUR`, `USD`, `JPY`) | Re-currency the series |
| `Roll` | `A` (active), `N` (notice-based), `R` (relative), `F` (front) | Generic-future roll method |
| `Points` | `N` (don't include points), `Y` (points only — FX forwards) | Forward-point output |
| `Calendar` | 2-letter calendar (`US`, `EU`, `JPN`, `BR`, `5D`, …) | Holiday calendar |
| `EqyFundCrncy` | ISO | Fundamentals currency |
| `Quote Calc` | `A` / `M` | Annualised vs monthly returns for some indices |

### Examples

```excel
' Simple daily history, vertical (default)
=BDH("SPX Index", "PX_LAST",
      DATE(2014,1,1), TODAY())

' Multi-field, with options
=BDH("EDP PL Equity",
      {"PX_LAST","TOT_RETURN_INDEX_GROSS_DVDS","PX_VOLUME"},
      DATE(2014,1,1), TODAY(),
      "Per=cdr", "Days=T", "Fill=P", "Sort=A", "Dir=V",
      "cshAdjNormal=Y", "cshAdjAbnormal=Y", "CapChg=Y",
      "UseDPDF=N", "currency=EUR")

' Monthly history, with override (PIT consensus)
=BDH("AAPL US Equity", "BEST_EPS",
      DATE(2018,1,1), TODAY(),
      "BEST_FPERIOD_OVERRIDE", "1FY",
      "Per=cm", "Days=W", "Fill=P")

' Bond history quoted in yield
=BDH("T 4.625 02/15/35 Govt", "YLD_YTM_MID",
      DATE(2024,1,1), TODAY(),
      "Per=cdr", "Days=W", "QtTyp=Y", "Fill=P")

' Generic future, active roll, total return
=BDH("CL1 Comdty", "PX_LAST",
      DATE(2014,1,1), TODAY(),
      "Per=cdr", "Days=T", "Roll=A")
```

### Output shape

By default `BDH` returns a **dynamic array** that spills downward
from the cell with two columns: `Dates`, then one column per field.
On older Excel without dynamic arrays you must pre-select the
target range and confirm with `Ctrl+Shift+Enter`.

When you change `start` / `end` after entering, the spill range
resizes automatically (on Excel 365 / 2021).

### `BDH` quirks worth remembering

- **`Days=A` includes weekends** with `Fill=P`. For weekday-only
  series use `Days=W` or `Days=T`.
- **`Days=T`** asks for trading days only and respects the security's
  primary calendar — but joining across markets (US + EU + JP)
  breaks alignment.
- **`Fill=B` returns blanks**, not zeros — use `IFERROR(... ,"")`
  carefully.
- **`Roll=` only applies to generic futures** (`CL1`, `TY1`); for
  specific contracts it's ignored.
- **Currency conversion** uses Bloomberg's standard FX series. For
  precise daily FX adjustment, pull spot history yourself and
  multiply.

---

## 2.3 `BDS` — Bloomberg Data Set

### Signature

```
=BDS(security, field, [override1, value1, …], [option1=value1, …])
```

### What it's for

Bulk fields — fields that return a *table per security*. Examples
in fixed income:

- `CALL_SCHEDULE` — `Date`, `Price`, `Type`
- `PUT_SCHEDULE`
- `AMORT_SCHEDULE`
- `CPN_SCHEDULE` (for step-ups)
- `INT_PMT_HIST`
- `CAPITAL_STRUCTURE_DETAILED`
- `RTG_MOODY_HIST`, `RTG_SP_HIST`, `RTG_FITCH_HIST`
- `FUT_CHAIN`
- `INDX_MEMBERS`, `INDX_MWEIGHT_HIST`
- `DVD_HIST_ALL`
- `OPT_CHAIN`
- `BLOOMBERG_PEERS`
- `EARN_ANN_DT_TIME_HIST_WITH_EPS`
- `FUND_HOLDINGS`

### Examples

```excel
' Call schedule for a callable corp bond
=BDS("EDP 1 ⅞ 03/14/35 Corp", "CALL_SCHEDULE")

' All historical Moody's rating changes
=BDS("EDP 1 ⅞ 03/14/35 Corp", "RTG_MOODY_HIST")

' Active WTI futures chain
=BDS("CL1 Comdty", "FUT_CHAIN",
     "INCLUDE_EXPIRED_CONTRACTS", "N",
     "CHAIN_DATE", "20250502")

' Historical index members at a date
=BDS("SX5E Index", "INDX_MWEIGHT_HIST",
     "END_DATE_OVERRIDE", "20231229")

' Full dividend history with type filter
=BDS("EDP PL Equity", "DVD_HIST_ALL",
     "EQY_INC_DVD_TYPES_FILTER", "Regular")
```

### Output shape

`BDS` returns a **dynamic array** sized by the bulk field's row
count × column count. The first row is column headers when
`Headers=Y` (default). To turn headers off:

```excel
=BDS("EDP 1 ⅞ 03/14/35 Corp", "CALL_SCHEDULE",
     "Headers=N")
```

To force vertical layout (default is the natural layout of the
field):

```excel
=BDS(..., "Dir=V")
```

### `BDS` quirks

- **The column-name schema is per-field**, not standardised. Some
  fields use `Ex-Date` with a hyphen, `% Out` with spaces and a
  percent. Plan your downstream cells accordingly — VLOOKUP on
  spaces and special characters is error-prone; use `INDEX/MATCH`
  with `LEFT(...)` or define named ranges.
- **Empty bulk field returns `#N/A`** — not an empty array. Wrap in
  `IFERROR` if a security simply has no callable schedule.
- **Spill conflict**: if there's anything in the spill range you
  get `#SPILL!`. Clear the range first.

---

## 2.4 `BEQS` — Bloomberg Equity Screen

```
=BEQS(screen_name, [screen_type], [as_of], [group_folder])
```

| Argument | Notes |
|---|---|
| `screen_name` | Exact name from `EQS <GO>` |
| `screen_type` | `"PRIVATE"` (your screens) or `"GLOBAL"` (shared) |
| `as_of` | `"YYYYMMDD"` to re-run as of a past date |
| `group_folder` | If you nested the screen in an EQS folder |

```excel
=BEQS("PSI20_Members", "PRIVATE")
=BEQS("EU_Banks_BBB", "PRIVATE", "20240630")
```

Returns a list of tickers + any fields the screen exports.

`BEQS` is the cleanest way to define a universe — set it up once in
`EQS <GO>`, save, and any rebuild of the workbook just re-fetches.

---

## 2.5 `BCURVE` — Curve Points

```
=BCURVE(curve_id, [date], [points])
```

| Argument | Notes |
|---|---|
| `curve_id` | Bloomberg curve ID, e.g. `"YCSW0023"` (USD SOFR OIS) |
| `date` | `"YYYYMMDD"` for historical curve |
| `points` | Optional tenor list array `{"3M","1Y","2Y","5Y","10Y","30Y"}` |

```excel
=BCURVE("YCSW0023", TODAY(),
        {"3M","1Y","2Y","5Y","10Y","30Y"})
```

Returns matched tenors × the curve's quoted values (par rates,
discount factors).

For most purposes it's easier to address swap nodes directly
(`USSO1 Curncy`, `USSO2 Curncy`, …) with `BDP`. See
[04_curves.md](04_curves.md).

Common curve ids (a subset — there are hundreds):

| Curve | ID |
|---|---|
| USD SOFR OIS | `YCSW0023` |
| USD legacy swap (3M LIBOR) | `YCSW0042` |
| EUR €STR OIS | `YCSW0514` |
| EUR 6M EURIBOR swap | `YCSW0045` |
| GBP SONIA OIS | `YCSW0141` |
| JPY TONA OIS | `YCSW0510` |
| US Treasury actives | `YCGT0025` |
| German Bund | `YCGT0016` |
| UK Gilt | `YCGT0022` |
| JGB | `YCGT0018` |

For the full list, `CRVF <GO>` on the Terminal.

---

## 2.6 `BSRCH` — Security Search

```
=BSRCH("COMDTY:NGFLOW")           ' returns tickers in the NG flow domain
=BSRCH("FI:CORP_BBB_EUR")         ' custom corp BBB EUR search
```

Mostly used by traders to plug curated security lists into a sheet.
For one-off discovery use `SECF <GO>` on the Terminal.

---

## 2.7 `BQL` — Bloomberg Query Language

Newer DSL-style formula. Lets you embed multi-step queries
(filtering, sorting, aggregation) directly in a cell.

```
=BQL(universe, "let(... ) get(... ) for(... ) preferences(...)")
```

### Why it exists

The classic `BDP` / `BDH` / `BDS` family is field-by-field — fetch
once per `(security, field)`. BQL lets you ask compound questions
in a single formula: *"return the 10 largest current SX5E members
by market cap, with their current PE and 1-year forward EPS"*.

### Basic shape

```excel
=BQL("members('SX5E Index')",
     "name, cur_mkt_cap, pe_ratio")
```

The universe is the first argument; the expression is the second.
Output spills as a table.

### Filtering and sorting

```excel
=BQL("members('SX5E Index')",
     "let(#mc = cur_mkt_cap()) "
   & "get(name, #mc) "
   & "for(filter(#mc > 50e9)) "
   & "preferences(addcols=true)")
```

### Time series via BQL

```excel
=BQL("'AAPL US Equity'",
     "px_last(dates=range(-1y, 0d), per=d, fill=prev)")
```

### Why analysts use it

- Compound logic without VBA.
- Cross-sectional ranking / filtering.
- Built-in functions for moving averages, lags, percentiles.
- "BQL Builder" ribbon button shows you generated syntax.

### Why analysts skip it

- Learning curve — BQL has its own dialect.
- Errors are cryptic (`BQL Error: 1234`).
- Caching behaviour differs from BDP/BDH; harder to predict refresh
  cost.
- Not all overrides map cleanly.

If you're new, start with `BDP` / `BDH` / `BDS`. Move to BQL once
the same query needs to span 5+ formulas.

---

## When to use which

| Need | Use |
|---|---|
| One value, now | `BDP` |
| One value, with overrides | `BDP` with paired overrides |
| Time series | `BDH` |
| Time series across many securities | `BDH` per security (loop in VBA), or `BQL` |
| A table per security (members, divs, ratings, chain) | `BDS` |
| A universe from EQS | `BEQS` |
| Curve points | direct tickers + `BDP`, or `BCURVE` |
| Multi-step / ranked / filtered | `BQL` |
| Real-time stream | `BDP` with real-time refresh, or `BLPSubscribe` (see [05](05_realtime_rtd.md)) |

## Refresh semantics (preview, see [03](03_tickers_overrides_calendars.md))

- `BDP` re-evaluates on cell input changes, refresh commands, or
  the global refresh interval.
- `BDH` is **expensive** — pulls a full series each time. Refresh
  manually.
- `BDS` is similarly expensive.
- `BQL` may cache intermediate results (uses subscriptions
  internally).

For large workbooks, **Manual refresh** mode is the only sane
default.
