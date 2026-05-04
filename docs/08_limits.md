# 08 · Limits & Throttling

Bloomberg meters every kind of API consumption. Some of these caps are
hard (the server refuses); others are soft (you get warnings or slow
responses). Treating the limits like part of your code's correctness is
the difference between a pipeline that runs daily for a year and one
that quietly stops mid-month.

## The numbers (Terminal / DAPI / SAPI)

These are the values Bloomberg quotes most often. Your contract may
differ — `API <GO>` shows the live counters.

| Resource | Cap |
|---|---|
| **Daily data points** | ~500,000 unique `(security, field)` pairs / 24h |
| **Monthly data points** | ~5,000,000 |
| **Burst — pull side** | ~5,000 hits per 30s |
| **Concurrent subscriptions** | ~3,500 topics (Terminal) |
| **Real-time tick rate** | conflated server-side per topic per second; high-volume topics need `interval=N` |
| **Intraday history (bars / ticks)** | ~140 calendar days |
| **Securities per `ReferenceDataRequest`** | ~100 (soft) |
| **Securities per `HistoricalDataRequest`** | ~25 (soft) |
| **Fields per request** | ~400 (soft) |
| **Request timeout** | 60s default, up to 600s configurable |
| **Per-tick cap on subscriptions** | ~10 ticks/sec without conflation |

B-PIPE caps are larger and configurable per-license: typical numbers
are 10× Terminal on data points, full intraday history, and tens of
thousands of subscriptions.

## How "data points" are counted

A *data point* is one `(security, field, date-or-tick)` triple. So:

- `ReferenceDataRequest` for 100 names × 50 fields = 5,000 data points.
- `HistoricalDataRequest` for 5 names × 5 fields × 252 days = 6,300.
- `IntradayBarRequest` for one name, 1-minute bars over a single
  trading day = ~390 (US equity hours) → 390 data points × number of
  fields the bar carries.
- Bulk fields multiply by row count: `INDX_MEMBERS` on SPX = 500
  rows = 500 data points for that one field call.

This is why "always batch by securities, not by fields" is the right
default for `ReferenceDataRequest` (no multiplication), and the
opposite for `HistoricalDataRequest` (less repeated date columns).

## What happens when you hit a cap

| Cap | Symptom |
|---|---|
| Daily | `ResponseError` with `category=LIMIT`, message about daily limit. New requests start failing immediately. Reset is rolling 24h. |
| Burst | Requests stall — server queues them. `nextEvent` blocks longer than usual. |
| Subscriptions | New `subscribe` calls return `SubscriptionFailure` with reason `LIMIT_EXCEEDED`. |
| Intraday history | Empty response (no `barTickData` / `tickData`). No error. Check the requested window first. |
| Securities per request | Bloomberg silently truncates; the response only contains the first N. |

`API <GO>` on the Terminal shows the **counters** for your DAPI session
in real time — daily hits, monthly hits, current subscriptions. Always
check there before assuming a code bug.

## Defensive patterns

### 1. Cache aggressively to parquet

```python
from pathlib import Path
import hashlib, json, pandas as pd

def _key(req_dict):
    s = json.dumps(req_dict, sort_keys=True, default=str)
    return hashlib.sha1(s.encode()).hexdigest()[:16]

def cached(fn):
    def wrapper(req_dict, cache_dir=Path("./.bbcache")):
        cache_dir.mkdir(exist_ok=True)
        p = cache_dir / f"{_key(req_dict)}.parquet"
        if p.exists():
            return pd.read_parquet(p)
        df = fn(req_dict)
        df.to_parquet(p)
        return df
    return wrapper
```

### 2. Respect the burst limit with a token-bucket

```python
import time, collections

class Throttle:
    def __init__(self, max_hits=4500, window_s=30):
        self.max, self.win = max_hits, window_s
        self.q = collections.deque()
    def wait(self, n=1):
        now = time.monotonic()
        while self.q and now - self.q[0] > self.win:
            self.q.popleft()
        if len(self.q) + n > self.max:
            sleep = self.win - (now - self.q[0]) + 0.1
            time.sleep(max(sleep, 0))
        for _ in range(n):
            self.q.append(time.monotonic())
```

### 3. Watch the daily counter

When running long batches, after each chunk fetch the counter via
`//blp/refds`. If unavailable, simply count `(security × field × date)`
locally and stop ~80% of the way to the cap.

### 4. Always check `responseError` and `fieldExceptions`

A response that contains zero rows often *is* an error — buried in the
exception elements rather than raised.

### 5. Split big universes

```python
def chunked(seq, size):
    seq = list(seq)
    for i in range(0, len(seq), size):
        yield seq[i:i+size]

for batch in chunked(tickers, 100):
    pull(batch, ...)
```

For `HistoricalDataRequest`, also chunk by **date range** if you're
asking for many years × many fields. 5 years per chunk works well.

### 6. Use the right request for the question

- Want today's price for 200 names? `ReferenceDataRequest`, single call.
- Want the past 10 years of 5 fields on 100 names? Loop
  `HistoricalDataRequest` in batches of 25.
- Want every trade on AAPL today? `IntradayTickRequest`, **only if you
  truly need it** — it's the fastest way to nuke your daily cap.
- Want minute-level OHLCV for backtesting? `IntradayBarRequest` with
  the largest interval that still works for your strategy.

## B-PIPE specifics

- Caps are per *application*, not per *user*.
- The `//blp/refds` service can return reference data for non-active
  securities (delisted, matured) — useful for survivor-bias-free
  panels.
- BMIST (Bloomberg Market Image Service) provides extended intraday
  history beyond 140 days.

## Real-time tick caps

- Per-topic per-second tick rate is enforced.
- High-volume names (e.g. SPY equity, EURUSD spot) **require**
  `interval=N` (often 0.1–1.0s).
- If you don't conflate, you get `SubscriptionTerminated` with reason
  `SLOW_CONSUMER`.
- The server-side bar service (`//blp/mktbar`) conflates by
  construction, costs you nothing on the wire.
