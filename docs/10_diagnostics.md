# 10 · Diagnostics & Debugging

When a request silently returns nothing — or returns the wrong number —
the failure mode is usually one of: entitlement, ticker formatting,
field formatting, override formatting, or stale state. Walk the list.

## Tools on the Terminal

| Function | What it gives you |
|---|---|
| `WAPI <GO>` | API Developer's Guide, full schema browser, sample code |
| `FLDS <GO>` | Field discovery; click a field for available overrides |
| `<security> FLDS <GO>` | Same, but only fields that return for that ticker |
| `DES <GO>` | Description of a security (incl. accepted yellow keys) |
| `ID <GO>` | Resolve any identifier (ISIN, CUSIP, FIGI) to a Bloomberg ticker |
| `API <GO>` | Live status of your DAPI session: hits used, hits remaining, subscriptions |
| `IOIA <GO>` / `BBXL` | Excel add-in diagnostics; useful to compare values you get vs Excel |
| `EUNI <GO>` | Universe of entitlements (which exchanges/feeds you can hit) |
| `WLS <GO>` | Build / reload watchlists (useful for `BeqsRequest` alternatives) |
| `EQS <GO>` | Equity screen builder; save screens for `BeqsRequest` |

## Tools in code

### Logging from the SDK

```python
import blpapi, logging
logging.basicConfig(level=logging.DEBUG)

def cb(threadId, severity, ts, category, message):
    print(f"[{ts}] {category}/{severity}: {message}")

blpapi.Logger.registerCallback(cb, blpapi.Logger.SEVERITY_DEBUG)
```

Severities: `OFF`, `FATAL`, `ERROR`, `WARN`, `INFO`, `DEBUG`, `TRACE`.
At `DEBUG` you see every wire message in / out.

### Dumping a message verbatim

```python
print(msg.toString(blpapi.SchemaTypeDefinition.PRINT_INDENTED))
# or simply
print(msg)
```

`msg.toString()` is enough most of the time.

### Tracing requests

```python
cid = blpapi.CorrelationId(f"req-{uuid.uuid4()}")
print(f"-> sending {cid.value()} req={req}")
session.sendRequest(req, correlationId=cid)
```

Always print the `Request` you're about to send. `Element.toString()`
gives a readable representation including all securities, fields,
overrides.

## Symptoms → causes table

| Symptom | Likely cause | Fix |
|---|---|---|
| `session.start()` returns `False` | Terminal not logged in / `bbcomm` down / wrong host | Re-login the Terminal; check `127.0.0.1:8194` reachable |
| Empty `securityData[]` | Ticker not recognised (yellow key wrong, missing exchange code) | Use `DES <GO>` to confirm canonical name |
| `securityData[i].securityError` present | Unrecognised security | Try `<ISIN> Equity` form, or `ID <GO>` |
| `fieldExceptions[]` non-empty | Unentitled or non-existent field on this security | Run `<sec> FLDS <GO>` to verify field |
| `fieldData` has NaNs you didn't expect | Override missing or wrong (e.g. `FUND_PER` not set for fundamentals) | Re-check overrides via `FLDS <GO>` |
| `HistoricalDataRequest` returns fewer dates than expected | `nonTradingDayFillOption` / `Calendar` mismatch | Set `nonTradingDayFillOption=ACTIVE_DAYS_ONLY` |
| `IntradayBarRequest` returns nothing | Outside ~140-day window, or weekend, or wrong UTC offset | Confirm the security trades on those datetimes; subtract local TZ |
| `IntradayBarRequest` for futures returns nothing | Generic ticker (`CL1`) won't always have intraday — try active month explicit `CLM5 Comdty` |
| Subscription delivers no data | `delayed` entitlement, market closed, or `interval=` too high | Watch `SubscriptionStatus` for messages |
| Prices off by a corporate-action factor | `adjustmentSplit/Normal/Abnormal` defaults inherited from DPDF | Set explicitly in the request |
| Same query returns different numbers on different machines | DPDF / fundamental defaults inherited from per-user Terminal config | Pin every adjustment knob and override |
| `category=LIMIT` on responses | Hit the daily / monthly cap | Cache more, batch better, ask admin to raise |
| `RESPONSE` event never arrives | Network blip without `setAutoRestartOnDisconnection`, or you're filtering events | Always also check `eventType()`, log `SESSION_STATUS` |

## Comparing to Excel

When values disagree with the BBG Excel add-in, paste the failing
ticker/field into the add-in:

```
=BDP("EDP PL Equity", "BEST_EPS", "BEST_FPERIOD_OVERRIDE", "1FY")
=BDH("EDP PL Equity", "PX_LAST", "01/01/2024", "12/31/2024", "Per=cdr,Fill=p")
```

If the Excel value is right and your Python is wrong, you've got an
override / parameter mismatch. Steal the Excel formula's parameters
verbatim. If they both agree but disagree with the Terminal, check
DPDF / pricing source.

## Network-layer debugging

```bash
# DAPI loopback up?
nc -zv 127.0.0.1 8194

# Inspect bbcomm logs (Linux/macOS via Citrix or remote terminal)
tail -F ~/.blpapi/logs/blpapi.*.log

# Force a fresh connection
killall bbcomm; open /Applications/Bloomberg/bbcomm    # macOS
```

On Windows, the equivalent path is `%APPDATA%\Bloomberg\blpapi\logs`.

## Useful environment variables

| Var | Effect |
|---|---|
| `BLPAPI_ROOT` | Path to vendored C++ SDK (only needed without wheel) |
| `BLPAPI_LOGFILE` | Override default log location |
| `BBG_ROOT` | Where `xbbg` stores its parquet cache |
| `BLPAPI_CFG` | Override default config file path |

## When all else fails

1. Reproduce the failing field call in **Excel** with the exact same
   overrides. If Excel is right, you've got a Python wiring bug.
2. If Excel and Terminal agree but the value still looks wrong, ask
   your firm's Bloomberg rep — sometimes a feed has a known issue and
   the API returns NaN where Terminal substitutes a derived value.
3. For *anything* involving entitlements, log a `WAPI` ticket — the
   support team can resolve in minutes what would take you hours.
