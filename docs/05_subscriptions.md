# 05 · Subscriptions (real-time)

Subscriptions are the push half of the API. You ask for a stream of
price updates on a list of securities, and the server pushes
`SUBSCRIPTION_DATA` events to you. Always run them on an **async
session** with an event handler — sync polling can't keep up with
several hundred liquid names.

## Service to use

| Service | Use it for |
|---|---|
| `//blp/mktdata` | Tick-level streaming of quotes, trades, depth |
| `//blp/mktbar` | Server-side N-second bars (less data on the wire) |
| `//blp/mktvwap` | Streaming VWAP |
| `//blp/mktdepthdata` | Order book depth (entitlement-restricted) |

`//blp/mktdata` is the default; you can drop the service prefix from
topic strings if you set
`SessionOptions.setDefaultSubscriptionService("//blp/mktdata")`.

## Building a subscription list

```python
sub = blpapi.SubscriptionList()

cid_edp = blpapi.CorrelationId("EDP")
sub.add(
    "EDP PL Equity",                                   # security topic
    fields=["LAST_PRICE", "BID", "ASK", "VOLUME"],
    options=["interval=2.0"],                          # see "Options"
    correlationId=cid_edp,
)
sub.add("PSI20 Index", ["LAST_PRICE"], [], blpapi.CorrelationId("PSI20"))

session.subscribe(sub)
```

Note **`fields` are real-time mnemonics**, not the static-side ones.
There's overlap (`PX_LAST` vs `LAST_PRICE`) but they aren't
interchangeable — the real-time service uses its own dictionary.

## Real-time field names you'll actually use

| Field | What it is |
|---|---|
| `LAST_PRICE` | Last trade price (decimal) |
| `LAST_TRADE` | Same, formatted string for some venues |
| `LAST_TRADE_PRICE_TIME_TODAY_REALTIME` | Time of last trade |
| `BID` / `ASK` | NBBO bid / ask |
| `BID_SIZE` / `ASK_SIZE` | Size at top |
| `VOLUME` | Cumulative volume today |
| `LAST_TRADE_SIZE` | Size of last trade |
| `RT_PX_CHG_PCT_1D` | % change since previous close |
| `RT_PX_CHG_NET_1D` | Net change since previous close |
| `OPEN`, `HIGH`, `LOW` | Today's session marks |
| `IND_BID` / `IND_ASK` | Indicative bid / ask (FX, OTC) |
| `MKTDATA_EVENT_TYPE` | `TRADE`, `QUOTE`, `SUMMARY`, `MARKET_STATUS` |
| `MKTDATA_EVENT_SUBTYPE` | `INTRADAY_TRADE`, `OPENING_TRADE`, `CLOSING_TRADE`, `AUCTION`, `OPENING_PRICE`, `CLOSING_PRICE`, `MID`, `BID`, `ASK` |
| `EVT_TRADE_PRICE_RT` | Price of the trade event |
| `EVT_TRADE_SIZE_RT` | Size of the trade event |
| `EVT_TRADE_CONDITION_CODE_RT` | Trade condition (string of codes) |
| `RPS_TICKER_EXCH_RT` | Reporting venue |
| `BID_YIELD` / `ASK_YIELD` | Yields for bonds |

## Subscription `options` (the third tuple element)

| Option | Effect |
|---|---|
| `interval=N` | Conflate updates to one every N seconds (float). **Required for high-volume tickers.** |
| `delayed` | Force delayed feed even if you're entitled to real-time |
| `pricingSource=...` | Override pricing source (e.g. `BGN`, `CMPN`, `CMPL`) |
| `eventStream=ALL` | Default; everything available |
| `eventStream=TRADE` | Trades only |
| `eventStream=QUOTE` | Quotes only |

Conflation is enforced server-side: ticks within the interval are
aggregated; you receive one consolidated message every interval. Set
`interval=0` to disable (subject to entitlement caps).

## Async event handler

```python
import blpapi, threading

def on_event(event, sess):
    et = event.eventType()
    if et == blpapi.Event.SUBSCRIPTION_DATA:
        for msg in event:
            cid  = msg.correlationIds()[0].value()
            if msg.hasElement("LAST_PRICE"):
                px = msg.getElementAsFloat("LAST_PRICE")
                # do something — fast! the dispatcher thread is blocked while you run
    elif et == blpapi.Event.SUBSCRIPTION_STATUS:
        for msg in event:
            print("status", msg.messageType(), msg)

opts = blpapi.SessionOptions()
opts.setServerHost("localhost"); opts.setServerPort(8194)
opts.setDefaultSubscriptionService("//blp/mktdata")
opts.setMaxEventQueueSize(100_000)         # buffer for spiky feeds

session = blpapi.Session(opts, on_event)
session.startAsync()
session.openServiceAsync("//blp/mktdata")
session.subscribe(sub)

threading.Event().wait()                   # park forever
```

> **Don't do work in `on_event`.** Push the message onto a queue, let a
> worker thread do the heavy lifting. Blocking the dispatcher backs up
> the entire socket and Bloomberg will start dropping you for being a
> "slow consumer".

## Subscription lifecycle

| Event type | Meaning |
|---|---|
| `SESSION_STATUS` | Session up/down |
| `SERVICE_STATUS` | A service became available |
| `SUBSCRIPTION_STATUS` | Per-topic subscription health |
| `SUBSCRIPTION_DATA` | The actual ticks |

`SUBSCRIPTION_STATUS` carries one of:
- `SubscriptionStarted`
- `SubscriptionStreamsActivated`
- `SubscriptionFailure` (look at `reason.errorCode`, `reason.description`)
- `SubscriptionTerminated` (entitlement revoked, security delisted, …)
- `SlowConsumerWarning` / `SlowConsumerWarningCleared`
- `DataLoss` (rare; you fell behind so far the server gave up)

Always log status messages — they're how you find out a subscription
quietly died at 3am.

## Adding / dropping mid-stream

```python
session.unsubscribe(sub_to_drop)
session.subscribe(sub_to_add)
session.resubscribe(existing_sub)          # change fields/options
```

`resubscribe` keeps the correlation id stable — useful for swapping the
conflation interval without losing state.

## Capacity

- Terminal: typically up to ~3,500 concurrent topics.
- SAPI: configured per server (often 10K–25K).
- B-PIPE: tens of thousands; per-tick caps apply.
- The number of *topics* and the *tick rate* both count. A liquid name
  on `eventStream=ALL` with no conflation can burn through your capacity
  on its own.

## Getting historical depth via subscription "playback"

There isn't a true playback mode in `mktdata`. For replay you need:

1. **`IntradayTickRequest`** for past days (up to ~140 days back), or
2. **B-Tick / B-PIPE BMIST** for deeper history (separately licensed).

Don't try to back-fill by leaving a subscription running on a closed
market; you'll get nothing.

## VWAP and bar streams

`//blp/mktvwap`:

```python
sub.add("EDP PL Equity",
        fields=["VWAP", "VWAP_VOLUME"],
        options=["VWAP_START_TIME=09:00",
                 "VWAP_END_TIME=17:30"],
        correlationId=cid)
```

`//blp/mktbar`:

```python
# topic: "//blp/mktbar/ticker/<ticker>?type=Last_Price&interval=5"
sub.add("//blp/mktbar/ticker/EDP PL Equity",
        ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"],
        ["type=Last_Price", "interval=5"],          # 5-second bars
        correlationId=cid)
```

## Authorization with subscriptions (SAPI/B-PIPE)

```python
session.subscribe(sub, identity)
```

Pass the `Identity`. Bloomberg checks entitlements per topic — if any
topic is unentitled you'll get a `SubscriptionFailure` for that topic
only; the rest keep running.
