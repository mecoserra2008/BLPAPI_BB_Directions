# 09 · High-Level Wrappers (xbbg, pdblp, blp)

Raw `blpapi` is verbose. For research code you want a wrapper that
returns DataFrames. Three are widely used:

| Library | Maintainer | Style | Status |
|---|---|---|---|
| **`xbbg`** | Cheng Yu (PhD) | pandas-native, on-disk caching, calendars | actively maintained |
| **`pdblp`** | Matthew Gilbert | older, minimal | stable, unmaintained |
| **`blp`** | Matthew Gilbert | newer, async-friendly | actively maintained |

Recommendation: **use `xbbg` by default**, drop to raw `blpapi` only
when you need a service or override the wrapper doesn't expose
(e.g. `//blp/tasvc`, `//blp/instruments`, custom EQS overrides).

## `xbbg` cookbook

```python
from xbbg import blp
import pandas as pd
```

### Snapshot (`bdp`)

`bdp` = Bloomberg Data Point (single value per security/field).

```python
df = blp.bdp(
    tickers=['EDP PL Equity', 'GALP PL Equity', 'JMT PL Equity'],
    flds=['PX_LAST', 'CUR_MKT_CAP', 'GICS_SECTOR_NAME', 'BEST_EPS'],
    BEST_FPERIOD_OVERRIDE='1FY',         # overrides as keyword args
)
# DataFrame indexed by ticker, columns are fields
```

### History (`bdh`)

```python
df = blp.bdh(
    tickers='SPX Index',
    flds=['PX_LAST', 'TOT_RETURN_INDEX_GROSS_DVDS'],
    start_date='2010-01-01',
    end_date='2025-12-31',
    Per='D',                             # D, W, M, Q, S, Y
    Fill='P',                            # P=previous, B=blank
    adjust='-',                          # '-' = no adjust; 'all' = split+div
    currency='EUR',
)
# Two-level columns: (ticker, field). Date index.
```

### Intraday bars (`bdib`)

```python
df = blp.bdib(
    ticker='EDP PL Equity',
    dt='2025-05-02',                     # one day at a time
    typ='TRADE',                         # TRADE, BID, ASK, ...
    interval=1,                          # minutes
    session='allday',                    # 'day_session', 'allday'
)
```

### Bulk / reference data (`bds`)

`bds` = Bloomberg Data Set. Use it for bulk fields.

```python
members = blp.bds('SPX Index',  'INDX_MEMBERS')
divs    = blp.bds('EDP PL Equity', 'DVD_HIST_ALL')
chain   = blp.bds('CL1 Comdty', 'FUT_CHAIN', INCLUDE_EXPIRED_CONTRACTS='Y')
opts    = blp.bds('AAPL US Equity', 'OPT_CHAIN')
```

### Equity screen (`beqs`)

```python
universe = blp.beqs('PSI20_Members', typ='PRIVATE')
```

### Real-time (`live`)

`xbbg` has a `live` iterator over a subscription. Useful for tooling,
not for production:

```python
for tick in blp.live(['EDP PL Equity'], flds=['LAST_PRICE'], max_cnt=100):
    print(tick)
```

### Caching

`xbbg` writes parquet caches under `~/.xbbg` by default. Configure with
the `BBG_ROOT` env var. Same `bdh` call twice in a day = one round-trip.

## `pdblp` cookbook

Slightly different style; useful if you can't install `xbbg`.

```python
import pdblp

con = pdblp.BCon(timeout=5000)           # ms
con.start()

snap = con.ref(['AAPL US Equity'], ['PX_LAST', 'CUR_MKT_CAP'])
hist = con.bdh(['AAPL US Equity'], ['PX_LAST'],
               '20100101', '20251231',
               elms=[("periodicitySelection", "DAILY")])
bars = con.bdib('AAPL US Equity', '2025-05-02', '2025-05-02',
                event_type='TRADE', interval=1)
bulk = con.bulkref(['SPX Index'], ['INDX_MEMBERS'])
```

`pdblp` returns long-format DataFrames (one row per
ticker-field-value), which can be more convenient for `.pivot_table`.

## `blp` (matthewgilbert)

Aimed at people who like SQL-shaped APIs:

```python
import blp
bquery = blp.BlpQuery().start()

bquery.bdp(['AAPL US Equity'], ['PX_LAST'])
bquery.bdh(['AAPL US Equity'], ['PX_LAST'], '20240101', '20251231')
bquery.bds(['SPX Index'], 'INDX_MEMBERS')
bquery.beqs('My Screen', screen_type='PRIVATE')
bquery.bdib('AAPL US Equity', '20250502')
```

Strength: cleaner async support, plays well with `asyncio`-based
servers.

## When to drop down to raw `blpapi`

You'll need raw if:

- You want **`//blp/instruments`** autocomplete (security search by
  description prefix).
- You need **`//blp/tasvc`** server-side studies.
- You need a non-trivial `EQS` invocation with multiple overrides
  passed in non-keyword form.
- You're streaming subscriptions in production and want full control
  of the event loop.
- You need `Identity` separation in a multi-tenant SAPI process.
- You're using **partial responses** to start processing data before
  the full response arrives (large historical pulls).

## Mixing wrappers and raw blpapi

`xbbg` exposes its underlying session as `xbbg.io.conn.create_connection()`
returning a `blpapi.Session`. If you need to run a one-off raw request
inside a script that otherwise uses `xbbg`, reuse the session — opening
two sessions on DAPI may double-count your hits and on B-PIPE wastes a
slot.

## Pitfalls

- `xbbg`'s `bdh` doesn't expose every adjustment toggle by name —
  use the `adjust` shortcut or pass `**{'adjustmentSplit': True, ...}`
  as kwargs.
- `pdblp`'s `bdh` doesn't accept the same enum spellings as
  `xbbg` (`periodicitySelection` vs `Per`); read the docstring.
- All three wrappers swallow `fieldExceptions` by default (you don't
  see *which* (security, field) pairs failed). For production-grade
  diagnostics, use raw or post-process by checking for unexpected NaNs.
