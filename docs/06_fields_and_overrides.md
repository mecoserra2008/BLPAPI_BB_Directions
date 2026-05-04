# 06 · Fields & Overrides

Bloomberg has on the order of **50,000 fields** ("data points"). You will
not memorise them. The two skills that matter are: (1) using
`FLDS <GO>` / `//blp/apiflds` to **find** them, and (2) understanding the
**override** mechanism that turns one field into a parametric query.

## How to discover a field

### From the Terminal
- `FLDS <GO>` — full search UI. Type the description; the right pane
  shows the mnemonic, data type, return value, and the **available
  overrides** with their accepted values.
- `<security> FLDS <GO>` — same thing, scoped to a security so you only
  see fields that actually return for it.
- `DES <GO>` on a security shows the most common ones inline.

### From code (`//blp/apiflds`)

```python
sess.openService("//blp/apiflds")
af = sess.getService("//blp/apiflds")

# 1) Search by keywords
req = af.createRequest("FieldSearchRequest")
req.set("searchSpec", "earnings announcement")
req.set("returnFieldDocumentation", True)
req.set("includeProductType", True)
req.set("includeFieldType", True)

# 2) Get info on a known mnemonic
req2 = af.createRequest("FieldInfoRequest")
req2.append("id", "PX_LAST")
req2.append("id", "BEST_EPS")
req2.set("returnFieldDocumentation", True)
```

The response carries `mnemonic`, `description`, `documentation`,
`datatype`, `categoryName`, `property[]` (override list), `overrides[]`,
`fieldType` (`Static`, `RealTime`, `Calculated`).

A worked example is in
[`examples/field_search.py`](../examples/field_search.py).

## Field naming conventions you can rely on

| Prefix / pattern | What it usually means |
|---|---|
| `PX_*` | Price family — `PX_LAST`, `PX_OPEN`, `PX_HIGH`, `PX_LOW`, `PX_BID`, `PX_ASK`, `PX_VOLUME`, `PX_MID`, `PX_SETTLE` |
| `RT_*_RT` | Real-time only counterparts |
| `IS_*` | Income-statement field (`IS_EPS`, `IS_REVENUE`, `IS_OPERATING_INCOME`) |
| `BS_*` | Balance-sheet field (`BS_TOT_ASSET`, `BS_TOT_LIAB2`) |
| `CF_*` | Cash-flow (`CF_CASH_FROM_OPER`, `CF_CAP_EXPEND_PRPTY_ADD`) |
| `BEST_*` | BEst consensus estimate (`BEST_EPS`, `BEST_TARGET_PRICE`, `BEST_DPS`) |
| `BEST_*_NUMEST` / `_HIGH` / `_LOW` / `_STDEV` / `_MEDIAN` | Estimate dispersion |
| `EQY_*` | Equity-specific (`EQY_BETA_RAW`, `EQY_DVD_YLD_IND`, `EQY_SH_OUT`) |
| `INDX_*` | Index-level (`INDX_MEMBERS`, `INDX_MWEIGHT`) |
| `FUT_*` | Futures (`FUT_CHAIN`, `FUT_CONT_SIZE`) |
| `OPT_*` | Options (`OPT_CHAIN`, `OPT_OPEN_INT`) |
| `IVOL_*` / `*_IMPVOL_*` | Implied vol |
| `DUR_*`, `OAS_*`, `Z_SPRD_*`, `I_SPRD_*`, `G_SPRD_*` | Bond analytics |
| `RTG_*` | Ratings (`RTG_MOODY`, `RTG_SP`, `RTG_FITCH`, `RTG_BB_COMPOSITE`) |
| `ID_*` | Identifiers (`ID_ISIN`, `ID_CUSIP`, `ID_BB_GLOBAL` (FIGI), `ID_SEDOL1`) |
| `DVD_*` | Dividends (`DVD_HIST_ALL`, `DVD_LAST`, `EQY_DVD_YLD_IND`) |
| `EARN_*` | Earnings (`EARN_ANN_DT`, `EARN_ANN_DT_TIME_HIST_WITH_EPS`) |
| `GICS_*` / `BICS_*` / `INDUSTRY_*` | Classification |

## Override mechanism

Many fields are **functions** of parameters. The function's parameters
are exposed as overrides. Two concrete examples:

### (a) Make a fundamentals field point at a different period

```python
req.append("securities", "AAPL US Equity")
req.append("fields",     "IS_EPS")

ovs = req.getElement("overrides")
ov  = ovs.appendElement()
ov.setElement("fieldId", "FUND_PER")
ov.setElement("value",   "Q")          # quarterly

ov  = ovs.appendElement()
ov.setElement("fieldId", "EQY_FUND_RELATIVE_PERIOD")
ov.setElement("value",   "-1")         # last completed quarter
```

### (b) Re-currency a fundamental

```python
ov  = ovs.appendElement()
ov.setElement("fieldId", "EQY_FUND_CRNCY")
ov.setElement("value",   "EUR")
```

### (c) Bond yield-to-anything

```python
req.append("securities", "T 4.625 02/15/35 Govt")
req.append("fields",     "YAS_BOND_YLD")

ov = ovs.appendElement()
ov.setElement("fieldId", "YAS_BOND_PX")
ov.setElement("value",   "98.50")       # price the yield is computed at

ov = ovs.appendElement()
ov.setElement("fieldId", "YAS_RISK_DT")
ov.setElement("value",   "20250502")    # settlement
```

> **Override values are always strings.** Even numbers and dates.
> Bloomberg coerces internally based on the field's data type.

## The override "vocabulary" — most-used keys

| Override fieldId | Used with | Sample values |
|---|---|---|
| `FUND_PER` | `IS_*`, `BS_*`, `CF_*` | `Q`, `S`, `A` (annual) |
| `EQY_FUND_RELATIVE_PERIOD` | fundamentals | `-1Q`, `-2Q`, `-1A`, `-1S` |
| `EQY_FUND_YEAR` | fundamentals | `2023` |
| `FUND_PER_END_DT` | fundamentals | `20231231` |
| `EQY_FUND_CRNCY` | fundamentals | ISO crncy |
| `BEST_FPERIOD_OVERRIDE` | `BEST_*` | `1FY`, `2FY`, `1FQ`, `2FQ`, `1BF` |
| `BEST_DATA_RELEASE_DT` | `BEST_*` | `YYYYMMDD` (point-in-time consensus) |
| `BEST_FY_OVERRIDE` | `BEST_*` | `2025` |
| `RELATIVE_PERIOD_OVERRIDE` | several | `-1Q`, `-1A` |
| `YAS_BOND_PX` | bond YAS_* | `98.5`, `100.25` |
| `YAS_BOND_YLD` | bond YAS_* | `4.32` |
| `YAS_RISK_DT` | bond | settle date |
| `YAS_ZSPREAD` | bond | bps |
| `YAS_CURVE` | bond | curve identifier e.g. `S490` |
| `OAS_VOL_BASIS_BVOL` | bond OAS | bp vol |
| `START_DATE` / `END_DATE` | many bulk | `YYYYMMDD` |
| `REFERENCE_DATE` | portfolio, indices | `YYYYMMDD` |
| `END_DATE_OVERRIDE` | indices | `YYYYMMDD` |
| `SETTLE_DT` | FX forwards | `YYYYMMDD` |
| `FX_FORWARD_TENOR` | FX | `1M`, `3M`, `1Y` |
| `CHAIN_DATE` | option/futures chains | `YYYYMMDD` |
| `OPTION_CHAIN_OVERRIDE` | `OPT_CHAIN` | `EXPIRATION`, all puts/calls |
| `INCLUDE_EXPIRED_CONTRACTS` | `FUT_CHAIN` | `Y` / `N` |
| `RTG_AS_OF_DT` | `RTG_*` | `YYYYMMDD` |
| `CALENDAR_CODE` | events | calendar id |
| `TIME_ZONE_OVERRIDE` | dates | tz id e.g. `23` (Lisbon), `0` (UTC) |
| `EQY_INC_DVD_TYPES_FILTER` | dividend hist | `Regular`, `Special`, `All` |

A fuller list is in [cheatsheets/overrides_index.md](../cheatsheets/overrides_index.md).

## Real-time vs static fields

Same physical concept, different field name. A few important pairs:

| Static (refdata) | Real-time (mktdata) |
|---|---|
| `PX_LAST` | `LAST_PRICE` |
| `PX_BID` / `PX_ASK` | `BID` / `ASK` |
| `PX_VOLUME` | `VOLUME` |
| `PX_OPEN` | `OPEN` |
| `PX_HIGH` / `PX_LOW` | `HIGH` / `LOW` |
| `LAST_TRADE_TIME` | `LAST_TRADE_PRICE_TIME_TODAY_REALTIME` |
| `BID_YIELD` | `BID_YIELD` (same name) |

The real-time service has many fields with `_RT` suffix that don't
exist on the static side at all (event semantics): `EVT_TRADE_PRICE_RT`,
`MKTDATA_EVENT_TYPE`, `RT_PX_CHG_PCT_1D`, etc.

## Formatted vs raw values

`req.set("returnFormattedValue", True)` returns the field formatted as
the Terminal would print it — e.g. yields as `4.32%`, ratings as
`"A+ *-"`. Otherwise you get the underlying numeric / categorical value.
Always work with raw unless you're rendering a UI.

## Calculated / "user" fields

Custom fields built in `FLDS <GO>` (CF function) are also queryable.
They appear with a `UDF_*` prefix. Pass them like any other mnemonic.

## Field documentation programmatically

The `documentation` element from `FieldInfoRequest` returns a sentence
or paragraph of descriptive text — useful in tooling but more
importantly for a sanity check that the field does what you expect
before burning hits on it.
