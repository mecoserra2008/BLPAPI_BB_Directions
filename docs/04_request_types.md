# 04 · Request Types (the pull-side API)

Every pull request lives on `//blp/refdata`. The shape is identical:
build a `Request`, append elements, send, drain events. The difference
between requests is the schema of what you append and what comes back.

| Request | Granularity | Window | Per-call cap |
|---|---|---|---|
| `ReferenceDataRequest` | Snapshot | now | ~100 securities × ~250 fields |
| `HistoricalDataRequest` | Day / week / month / quarter / semi / year | unlimited (entitlement permitting) | ~25 securities × ~25 fields × dates |
| `IntradayBarRequest` | 1–1440 min | ~140 days rolling | 1 security |
| `IntradayTickRequest` | Tick | ~140 days rolling | 1 security |
| `BeqsRequest` | Snapshot of an EQS | as-of date | one screen |
| `PortfolioDataRequest` | Snapshot | now / as-of | one portfolio |

> The "per-call cap" rows are the values Bloomberg suggests for
> reasonable batches. Real hard caps are higher but performance
> degrades and you risk timeouts beyond them.

## 4.1 `ReferenceDataRequest`

Use it for: latest price, descriptive fields, current fundamentals, any
field that returns a single value or one array per security at a point
in time.

```python
svc = sess.getService("//blp/refdata")
req = svc.createRequest("ReferenceDataRequest")

for tkr in ["EDP PL Equity", "GALP PL Equity", "JMT PL Equity"]:
    req.append("securities", tkr)

for fld in ["PX_LAST", "CUR_MKT_CAP", "EQY_DVD_YLD_IND",
            "BEST_EPS", "BEST_PE_RATIO", "GICS_SECTOR_NAME"]:
    req.append("fields", fld)

# Overrides go inside the `overrides` ARRAY element
ovs = req.getElement("overrides")
ov  = ovs.appendElement()
ov.setElement("fieldId", "BEST_FPERIOD_OVERRIDE")
ov.setElement("value",   "1FY")        # next fiscal year

# Optional toggles
req.set("returnEids", True)            # entitlement IDs in the response
req.set("returnFormattedValue", False) # raw values (default), set True to
                                        # match the Terminal display string
```

**Response shape**:

```
ReferenceDataResponse
└── securityData[]
    ├── security             "EDP PL Equity"
    ├── eidData[]             # if returnEids=True
    ├── fieldExceptions[]     # one entry per failed field
    │   ├── fieldId
    │   └── errorInfo {category, message, source, code, subcategory}
    ├── securityError{...}    # if the security itself is bad
    └── fieldData
        ├── PX_LAST            3.245
        ├── CUR_MKT_CAP        12_345_000_000
        ├── BEST_EPS           0.31
        └── ...                # bulk fields nested as arrays here
```

**Always check `fieldExceptions` and `securityError`** — Bloomberg never
raises; it returns soft failures field-by-field.

```python
for msg in ev:
    for sd in msg.getElement("securityData").values():
        sec = sd.getElementAsString("security")
        if sd.hasElement("securityError"):
            log.warning("security err %s: %s", sec,
                        sd.getElement("securityError"))
            continue
        for fe in sd.getElement("fieldExceptions").values():
            log.warning("field err %s/%s: %s", sec,
                        fe.getElementAsString("fieldId"),
                        fe.getElement("errorInfo"))
        fd = sd.getElement("fieldData")
        for f in (...):
            if fd.hasElement(f):
                rows.append((sec, f, fd.getElement(f).getValue()))
```

## 4.2 `HistoricalDataRequest`

Daily / weekly / monthly / quarterly / semi-annual / yearly EOD
time series.

```python
req = svc.createRequest("HistoricalDataRequest")
req.append("securities", "SPX Index")
req.append("securities", "SX5E Index")
for f in ["PX_LAST", "PX_VOLUME", "TOT_RETURN_INDEX_GROSS_DVDS"]:
    req.append("fields", f)

req.set("startDate",            "20100101")
req.set("endDate",              "20251231")
req.set("periodicityAdjustment","CALENDAR")
req.set("periodicitySelection", "DAILY")
req.set("currency",             "EUR")
req.set("pricingOption",        "PRICING_OPTION_PRICE")
req.set("nonTradingDayFillOption","NON_TRADING_WEEKDAYS")
req.set("nonTradingDayFillMethod","PREVIOUS_VALUE")
req.set("adjustmentSplit",      True)   # split-adjust prices
req.set("adjustmentNormal",     False)  # don't apply cash dividends
req.set("adjustmentAbnormal",   True)   # apply spinoffs / specials
req.set("adjustmentFollowDPDF", False)  # ignore Terminal DPDF defaults
req.set("maxDataPoints",        100_000)
```

| Element | Allowed values | Default |
|---|---|---|
| `periodicityAdjustment` | `ACTUAL`, `CALENDAR`, `FISCAL` | `ACTUAL` |
| `periodicitySelection` | `DAILY`, `WEEKLY`, `MONTHLY`, `QUARTERLY`, `SEMI_ANNUALLY`, `YEARLY` | `DAILY` |
| `pricingOption` | `PRICING_OPTION_PRICE`, `PRICING_OPTION_YIELD` | `PRICING_OPTION_PRICE` |
| `nonTradingDayFillOption` | `NON_TRADING_WEEKDAYS`, `ALL_CALENDAR_DAYS`, `ACTIVE_DAYS_ONLY` | `ACTIVE_DAYS_ONLY` |
| `nonTradingDayFillMethod` | `PREVIOUS_VALUE`, `NIL_VALUE` | `PREVIOUS_VALUE` |
| `currency` | ISO 4217 e.g. `EUR`, `USD`, `JPY` | security's pricing crncy |
| `adjustmentSplit` | bool | follow DPDF |
| `adjustmentNormal` | bool (cash divs) | follow DPDF |
| `adjustmentAbnormal` | bool (specials, spinoffs) | follow DPDF |
| `adjustmentFollowDPDF` | bool | True |
| `calendarCodeOverride` | 2-letter calendar e.g. `5D`, `EU`, `US` | security default |
| `overrideOption` | `OVERRIDE_OPTION_CLOSE`, `OVERRIDE_OPTION_GPA` | `OVERRIDE_OPTION_CLOSE` |

**Response shape**: `securityData.fieldData[]` is an array, one entry
per date.

```python
for sd in msg.getElement("securityData"):     # NOTE: not .values() — single item
    sec = sd.getElementAsString("security")
    fd  = sd.getElement("fieldData")
    for i in range(fd.numValues()):
        bar = fd.getValueAsElement(i)
        d   = bar.getElementAsDatetime("date")
        px  = bar.getElementAsFloat("PX_LAST")
```

> **Adjustment defaults are dangerous.** If you don't set them, you
> inherit the Terminal user's `DPDF <GO>` settings — meaning the same
> request can return *different* numbers depending on whose Terminal
> you're connected to. Always set them explicitly in production code.

## 4.3 `IntradayBarRequest`

OHLCV bars in N-minute buckets. **One security per request.** History
is roughly the last 140 calendar days for Terminal/SAPI users; longer
on B-PIPE/B-Tick.

```python
import datetime as dt

req = svc.createRequest("IntradayBarRequest")
req.set("security",       "EDP PL Equity")
req.set("eventType",      "TRADE")          # see table
req.set("interval",       1)                # minutes (1 .. 1440)
req.set("startDateTime",  dt.datetime(2025, 5, 1, 7, 0))   # UTC!
req.set("endDateTime",    dt.datetime(2025, 5, 3, 16, 0))
req.set("gapFillInitialBar", True)
req.set("adjustmentSplit",  True)
req.set("adjustmentNormal", False)
req.set("adjustmentAbnormal", True)
req.set("adjustmentFollowDPDF", False)
```

| `eventType` | What it bars |
|---|---|
| `TRADE` | Last trade price |
| `BID` / `ASK` | National best bid / ask |
| `BID_BEST` / `ASK_BEST` | Venue-best bid / ask (alias) |
| `BEST_BID` / `BEST_ASK` | Same — older spelling, still accepted |
| `BID_YIELD` / `ASK_YIELD` | Bonds: yield-side bars |
| `MID_PRICE` | Mid (BID+ASK)/2 |
| `AT_TRADE` | Trade flagged by exchange as the official last |
| `SETTLE` | Settlement price (futures, indices) |

Response: array of `barTickData` with `time`, `open`, `high`, `low`,
`close`, `volume`, `numEvents`, `value` (notional).

## 4.4 `IntradayTickRequest`

Tick-by-tick. Same window cap, one security per request. **Heavy** —
expect to consume your daily-hit cap fast on liquid names.

```python
req = svc.createRequest("IntradayTickRequest")
req.set("security",      "EDP PL Equity")
ev_types = req.getElement("eventTypes")
ev_types.appendValue("TRADE")
ev_types.appendValue("BID")
ev_types.appendValue("ASK")
req.set("startDateTime", dt.datetime(2025, 5, 2, 7, 0))
req.set("endDateTime",   dt.datetime(2025, 5, 2, 16, 0))
req.set("includeConditionCodes",      True)
req.set("includeNonPlottableEvents",  True)
req.set("includeExchangeCodes",       True)
req.set("includeBrokerCodes",         False)
req.set("includeRpsCodes",            True)
req.set("includeBicMicCodes",         True)
req.set("includeActionCodes",         True)
req.set("includeYields",              True)   # bonds
req.set("includeTradeTime",           True)
```

`eventTypes`: `TRADE`, `BID`, `ASK`, `AT_TRADE`, `BEST_BID`, `BEST_ASK`,
`SETTLE`. Pick only the ones you need — each multiplies the volume.

Response: `tickData[]` with `time`, `type`, `value`, `size`,
`conditionCodes`, `exchangeCode`, `rpsCode`, `bicMicCode`, etc.

Trade-condition codes vary by venue (e.g. NYSE `@`, `T`, `TI`; LSE `O`,
`X`; Euronext `MO`, `XT`). Filter unwanted prints — opening auctions,
closing auctions, off-book trades, late prints — by their condition.

## 4.5 `BeqsRequest` — universe from a saved EQS

Probably the cleanest way to build a research universe. Set up the
screen on the Terminal in `EQS <GO>`, save it, then:

```python
req = svc.createRequest("BeqsRequest")
req.set("screenName", "PSI20_Members")     # exact name from EQS
req.set("screenType", "PRIVATE")           # or "GLOBAL" for shared screens
# req.set("Group",      "MyFolder")        # optional, when you nest in folders
# req.set("languageId", "ENGLISH")
# req.set("asOfDate",   "20250502")        # historical screen
```

Response: same `securityData` array as `ReferenceDataRequest`, with
whatever fields the screen included.

## 4.6 `PortfolioDataRequest`

Pulls members and weights for a portfolio defined in `PRTU <GO>`. The
portfolio's name is something like `U12345678-12 Client`.

```python
req = svc.createRequest("PortfolioDataRequest")
req.append("securities", "U12345678-12 Client")
req.append("fields", "PORTFOLIO_DATA")           # bulk, members + weights
# Or shortcut fields:
# req.append("fields", "PORTFOLIO_MEMBERS")
# req.append("fields", "PORTFOLIO_MWEIGHT")
# req.append("fields", "PORTFOLIO_MPOSITION")
ovs = req.getElement("overrides")
ov = ovs.appendElement()
ov.setElement("fieldId", "REFERENCE_DATE")
ov.setElement("value", "20250502")
```

`PORTFOLIO_DATA` is a bulk field with `Security`, `Position`,
`Market Value`, `Weight`, `Cost Basis`, `Position Date`. See
[docs/07_bulk_fields.md](07_bulk_fields.md) for the iteration pattern.

## 4.7 `studyRequest` (technical analysis on the server)

```python
sess.openService("//blp/tasvc")
ta  = sess.getService("//blp/tasvc")
req = ta.createRequest("studyRequest")

ps  = req.getElement("priceSource")
ps.setElement("securityName", "AAPL US Equity")
sd  = ps.getElement("dataRange")
sd.setChoice("historical")
hist = sd.getElement("historical")
hist.setElement("startDate", "20240101")
hist.setElement("endDate",   "20251231")

st  = req.getElement("studyAttributes")
st.setChoice("rsiStudyAttributes")
rsi = st.getElement("rsiStudyAttributes")
rsi.setElement("priceSourceType", "CLOSE")
rsi.setElement("period", 14)
```

The `tasvc` service supports many studies (RSI, MACD, BBANDS, SMA, EMA,
WMA, MOM, MFI, OBV, ADX, ATR, CCI, ROC, STOCH, TRIX, VWAP, …). It's
strictly equivalent to fetching close prices + computing locally; the
upside is that it counts as one hit per study, not N rows.

## 4.8 Throughput tips

- **Batch securities**, not fields: `ReferenceDataRequest` likes wide.
- **Batch fields** for `HistoricalDataRequest` only up to ~25.
  Bloomberg counts `securities × fields × dates` against limits.
- **Cache to parquet** if you re-run the same script — your hit cap is
  not infinite. The recipes folder shows the pattern.
- Cache with the **request hash** as key: `(securities, fields,
  start, end, periodicity, overrides)` → file path.
