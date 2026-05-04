# Overrides Index

Overrides parameterise fields. They are appended to a request's
`overrides` element as `(fieldId, value)` pairs. **Values are always
strings**, even for numbers and dates (`YYYYMMDD`).

## Period selection (fundamentals)

| Override | Allowed values | Effect |
|---|---|---|
| `FUND_PER` | `Q`, `S`, `A`, `Y`, `LTM` | Quarterly / Semi / Annual / YTD / LTM |
| `EQY_FUND_RELATIVE_PERIOD` | `0`, `-1`, `-2`, ... `-1Q`, `-1A`, `-2A` | Period offset |
| `EQY_FUND_YEAR` | year, e.g. `2024` | Pin year |
| `FUND_PER_END_DT` | `YYYYMMDD` | Pin period end |
| `RELATIVE_PERIOD_OVERRIDE` | as above | Generic alias |

## Currency

| Override | Value | Effect |
|---|---|---|
| `EQY_FUND_CRNCY` | ISO code (`EUR`, `USD`, `JPY`, ...) | Re-currency a fundamental |
| `crncy` (in HistoricalDataRequest as request element, not override) | ISO | Re-currency a price series |

## Estimates (BEst)

| Override | Allowed values | Effect |
|---|---|---|
| `BEST_FPERIOD_OVERRIDE` | `1FY`, `2FY`, `3FY`, `1FQ`, `2FQ`, ..., `1BF`, `2BF`, `1FH`, `2FH` | Forecast period |
| `BEST_FY_OVERRIDE` | year (`2025`) | Pin fiscal year |
| `BEST_DATA_RELEASE_DT` | `YYYYMMDD` | Point-in-time consensus snapshot |
| `RELATIVE_PERIOD_OVERRIDE` | `-1Q`, `-1A` | For estimate-relative periods |
| `EARN_HIST_TYPE_FILTER` | `First Call`, `Comparable`, `As Reported` | Filter actuals |

`1FY` = next full fiscal year. `0FY` = current fiscal year.
`1BF` = blended forward (interpolation between `0FY` and `1FY`).

## Bond YAS

| Override | Effect |
|---|---|
| `YAS_BOND_PX` | User-supplied clean price; analytics return implied yield/spread |
| `YAS_BOND_YLD` | User-supplied yield; analytics return implied price |
| `YAS_RISK_DT` | Settle date for analytics (`YYYYMMDD`) |
| `YAS_CURVE` | Curve id (e.g. `S490` SOFR, `S514` €STR, `S141` SONIA) |
| `YAS_ZSPREAD`, `YAS_OAS_SPREAD` | User-supplied spreads (price comes back) |
| `YAS_ASW_SPREAD`, `YAS_ISPREAD` | Same family for ASW / I-spread |
| `YAS_BENCHMARK_BOND` | Force a specific benchmark for spread |
| `OAS_VOL_BASIS_BVOL` | Vol input for OAS (bp normal) |

## Ratings (point-in-time)

| Override | Effect |
|---|---|
| `RTG_AS_OF_DT` | `YYYYMMDD` — return rating in effect on that date |

## Index members / weights

| Override | Effect |
|---|---|
| `END_DATE_OVERRIDE` | `YYYYMMDD` — historical members for `INDX_MWEIGHT_HIST` |
| `START_DATE_OVERRIDE` | `YYYYMMDD` — start of period for additions/deletions |
| `INDEX_RATIO_ADJ_TYPE` | weighting method override |
| `REFERENCE_DATE` | as-of for `PORTFOLIO_DATA` and similar |

## Futures / option chains

| Override | Effect |
|---|---|
| `INCLUDE_EXPIRED_CONTRACTS` | `Y` / `N` for `FUT_CHAIN`, `OPT_CHAIN` |
| `CHAIN_DATE` | `YYYYMMDD` — chain composition as-of |
| `CHAIN_POINTS_OVRD` | depth of chain |
| `CHAIN_PERIODICITY_OVERRIDE` | for futures: `MONTHLY`, etc. |
| `CHAIN_EXP_DT_OVRD` | a single expiry for option chains |
| `OPTION_CHAIN_OVERRIDE` | `EXPIRATION` (per-expiry summary), `C`, `P`, `all` |
| `ROLL_METHOD` | `ACTIVE`, `OPEN_INT`, `RELATIVE`, `FRONT`, `RELATIVE_TO_FIRST_NOTICE` |

## FX / forwards

| Override | Effect |
|---|---|
| `SETTLE_DT` | Specific value date |
| `FX_FORWARD_TENOR` | `1M`, `3M`, `1Y`, etc. |
| `FORWARD_DATE` | (alias) |

## Dividends

| Override | Effect |
|---|---|
| `EQY_INC_DVD_TYPES_FILTER` | `All` (default), `Regular`, `Special`, `Stock` |
| `START_DATE` / `END_DATE` | window for `EQY_DVD_HIST_*` family |

## Holdings / portfolios

| Override | Effect |
|---|---|
| `FUND_HOLDINGS_OVERRIDE` | `Y` (full) vs default top-10 |
| `REFERENCE_DATE` | historical holdings |
| `PORTFOLIO_AS_OF_DATE` | for PRTU portfolios |
| `PORTFOLIO_REPORTING_CRNCY` | currency override |

## Calendars & timezones

| Override | Effect |
|---|---|
| `CALENDAR_CODE` | 2-letter calendar (`US`, `EU`, `GR`, `CME`, `SIFMA`, ...) |
| `TIME_ZONE_OVERRIDE` | numeric tz id (e.g. `0` UTC, `13` EST, `23` Lisbon) |

## CDS

| Override | Effect |
|---|---|
| `CDS_QUOTE_TYPE_OVERRIDE` | `Par Spread` / `Upfront` |
| `CDS_RECOVERY_RATE_OVERRIDE` | decimal (e.g. `0.40`) |
| `CDS_FX_RATE_OVERRIDE` | for cross-currency CDS PnL |

## ESG / climate

| Override | Effect |
|---|---|
| `ESG_AS_OF_DT` | point-in-time ESG score |

## Custom / tasvc

| Override | Effect |
|---|---|
| Study attributes (RSI period, MACD fast/slow/signal, etc.) | Inside `studyRequest`, set on `studyAttributes` element |

## When you don't know which override to use

`<security> FLDS <GO>` on the Terminal, click the field, and the
right-hand pane lists every accepted override with example values.
The same metadata is available via `FieldInfoRequest` on
`//blp/apiflds`:

```python
af  = sess.getService("//blp/apiflds")
req = af.createRequest("FieldInfoRequest")
req.append("id", "BEST_EPS")
req.set("returnFieldDocumentation", True)
```

## Worked examples

### Trailing 12-month fundamentals in EUR

```python
ovs = req.getElement("overrides")
o = ovs.appendElement(); o.setElement("fieldId","FUND_PER"); o.setElement("value","LTM")
o = ovs.appendElement(); o.setElement("fieldId","EQY_FUND_CRNCY"); o.setElement("value","EUR")
```

### Point-in-time consensus EPS for next FY

```python
o = ovs.appendElement(); o.setElement("fieldId","BEST_FPERIOD_OVERRIDE"); o.setElement("value","1FY")
o = ovs.appendElement(); o.setElement("fieldId","BEST_DATA_RELEASE_DT"); o.setElement("value","20240131")
```

### Historical index weights

```python
o = ovs.appendElement(); o.setElement("fieldId","END_DATE_OVERRIDE"); o.setElement("value","20231229")
```

### Bond yield from a clean price

```python
o = ovs.appendElement(); o.setElement("fieldId","YAS_BOND_PX"); o.setElement("value","98.50")
o = ovs.appendElement(); o.setElement("fieldId","YAS_RISK_DT"); o.setElement("value","20250506")
```

### Active-roll generic future series

```python
o = ovs.appendElement(); o.setElement("fieldId","ROLL_METHOD"); o.setElement("value","ACTIVE")
```

## Override quirks to remember

- **Some fields have implicit defaults** that depend on the
  Terminal user's `DPDF <GO>`. Always pin every adjustment for
  reproducibility.
- **Override order doesn't matter** within a request.
- **Conflicting overrides**: `BEST_FY_OVERRIDE` + `BEST_FPERIOD_OVERRIDE`
  may quietly compose. Pick one.
- **String values only**: `"20250502"`, not `20250502`. `"4.625"`,
  not `4.625`.
- **Dates**: `YYYYMMDD` (no separators) for the override fieldId
  values.
- **xbbg** passes overrides as **kwargs** to its `bdp`/`bdh`/`bds`
  functions, e.g. `blp.bdp(..., BEST_DATA_RELEASE_DT="20240131")`.
