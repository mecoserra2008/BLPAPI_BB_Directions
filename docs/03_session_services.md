# 03 · Sessions & Services

Two `Session` flavours, one event loop model, ten or so services. Pick
the right pair, and 95% of your code is the same regardless of asset
class.

## Sync vs Async session

```python
# Sync (the easy one — poll for events)
session = blpapi.Session(opts)
session.start()

# Async (event handler runs on a worker thread; you do nothing in main)
def on_event(event, sess):
    for msg in event:
        ...
session = blpapi.Session(opts, on_event)
session.startAsync()
```

| Mode | When to use |
|---|---|
| **Sync** | Pulling reference / historical / intraday data; one-shot scripts; notebooks; short-lived ETL. |
| **Async** | Subscriptions (real-time); long-lived services; anything where you can't afford to block on `nextEvent`. |

A single async session can mix subscriptions and request/response — it
just delivers everything to the handler.

### Sync event loop, the canonical shape

```python
session.sendRequest(req)
while True:
    ev = session.nextEvent(timeout_ms=5000)   # 0 = block forever
    for msg in ev:
        handle(msg)
    if ev.eventType() == blpapi.Event.RESPONSE:
        break               # final chunk; everything else is PARTIAL_RESPONSE
```

Bloomberg returns large pull responses as a sequence of
`PARTIAL_RESPONSE` events terminated by exactly one `RESPONSE` event.
Stopping at the first `RESPONSE` for the request is correct only when
you're not multiplexing requests — which is why every request gets a
`CorrelationId` you match on.

### CorrelationIds — match responses to requests

```python
cid = blpapi.CorrelationId("equity_snapshot_eu_2025_05_03")
session.sendRequest(req, correlationId=cid)
...
for msg in ev:
    if msg.correlationIds()[0].value() == cid.value():
        handle(msg)
```

You can use any value (str, int, or arbitrary Python object). Match on
`.value()`, not `==` between objects.

## SessionOptions worth knowing

| Setter | What it does |
|---|---|
| `setServerHost / setServerPort` | Single endpoint |
| `setServerAddress(host, port, idx)` | Multiple endpoints, failover |
| `setNumStartAttempts(n)` | Retry `start()` n times |
| `setAutoRestartOnDisconnection(True)` | Reconnect transparently |
| `setKeepAliveEnabled(True)` | TCP keepalive |
| `setMaxEventQueueSize(n)` | Buffer for high-volume subscriptions |
| `setMaxPendingRequests(n)` | In-flight requests before backpressure |
| `setSlowConsumerWarningHiWaterMark` / `LoWaterMark` | Detect slow consumers |
| `setRecordSubscriptionDataReceiveTimes(True)` | Adds RX timestamps to msgs |
| `setDefaultSubscriptionService("//blp/mktdata")` | Default for `subscribe` |
| `setAuthenticationOptions(...)` | See [02_authentication.md](02_authentication.md) |
| `setTlsOptions(...)` | B-PIPE only |

## Services overview

You always call `session.openService(name)` before `getService(name)`.
Open is idempotent and cheap — call it once per service per session.

| Service | Direction | Used for |
|---|---|---|
| `//blp/refdata` | Pull | Static, history, intraday bars, ticks, EQS, portfolio |
| `//blp/mktdata` | Push (subscribe) | Real-time price ticks |
| `//blp/mktvwap` | Push | Streaming VWAP |
| `//blp/mktbar` | Push | Streaming N-second bars |
| `//blp/apiflds` | Pull | Field metadata (search, info, categorise) |
| `//blp/instruments` | Pull | Security / curve / govt autocomplete |
| `//blp/tasvc` | Pull | Server-side technical analysis (RSI, MACD, BBANDS …) |
| `//blp/exrsvc` | Pull | EMSX, IOI, custom-grid extracts |
| `//blp/srcref` | Pull | Custom user / firm reference data (UPLD lists) |
| `//blp/apiauth` | Pull | `AuthorizationRequest` for SAPI/B-PIPE |
| `//blp/dapisvc` | Push | Desktop API control (rare) |
| `//blp/apifvr` | Pull | Field value resolution |
| `//blp/refds` | Pull | Reference data sets (firm-level) |

## Request types per service

`refdata`:
- `ReferenceDataRequest` — current/static snapshot
- `HistoricalDataRequest` — daily+ time series
- `IntradayBarRequest` — N-minute OHLCV
- `IntradayTickRequest` — tick-by-tick
- `BeqsRequest` — saved EQS screen output
- `PortfolioDataRequest` — `PRTU <GO>` portfolio members & weights
- `GridRequest` — internal use

`apiflds`:
- `FieldInfoRequest` — describe one or many fields by mnemonic / id
- `FieldSearchRequest` — keyword search across fields
- `CategorizedFieldSearchRequest` — same but grouped by Bloomberg category

`instruments`:
- `instrumentListRequest` — autocomplete on security descriptions
- `curveListRequest` — list available curves matching a query
- `govtListRequest` — list government securities matching an issuer

`tasvc`:
- `studyRequest` — RSI, MACD, ADX, BBANDS, SMA, EMA, WMA, MOM, MFI, etc.

## A reusable session helper

The pattern below is in [`examples/utils.py`](../examples/utils.py).
Use it everywhere — it removes the open/close boilerplate.

```python
import blpapi
from contextlib import contextmanager

@contextmanager
def bbg_session(host="localhost", port=8194, services=("//blp/refdata",)):
    opts = blpapi.SessionOptions()
    opts.setServerHost(host)
    opts.setServerPort(port)
    sess = blpapi.Session(opts)
    if not sess.start():
        raise RuntimeError("session.start failed")
    try:
        for s in services:
            if not sess.openService(s):
                raise RuntimeError(f"openService failed: {s}")
        yield sess
    finally:
        sess.stop()
```

## Element parsing — the one helper you'll keep using

Bloomberg messages are nested `Element` trees. Convert once, work with
plain Python:

```python
def el2py(el: blpapi.Element):
    if el.isArray():
        return [el2py(el.getValueAsElement(i)) for i in range(el.numValues())]
    if el.numElements() > 0:
        return {str(el.getElement(i).name()): el2py(el.getElement(i))
                for i in range(el.numElements())}
    if el.isNull():
        return None
    # Fall back to scalar
    try:    return el.getValue()
    except: return None
```

Now `el2py(msg.asElement())` is a `dict` you can dump to JSON or load
into a DataFrame. Beware: `getValue()` returns `datetime`, `Decimal`,
`int`, `float`, `bool`, or `str` depending on the field's `DataType`.

## Session shutdown

Always `session.stop()` (or `stop(blpapi.AbstractSession.StopOption.SYNC)`).
Async sessions also need `eventDispatcher.stop()` if you used a custom
dispatcher. Forgetting `stop()` leaks a worker thread and on B-PIPE will
keep the user/app slot occupied.
