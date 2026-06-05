# 05 · Real-Time & RTD

Three ways to get live updating prices into an Excel cell:

1. **`BDP` with real-time refresh** — easiest. Same formula as
   reference, just don't lock to manual refresh.
2. **`BLPSubscribe` / RTD** — proper streaming subscription via the
   add-in. Lower latency, finer control.
3. **VBA + `BlpSubscribe` events** — for custom blotters and
   alerts. See [06_vba_automation.md](06_vba_automation.md).

## 5.1 `BDP` with real-time fields

Use real-time field mnemonics (lowercase semantic, differ from
static-side):

```excel
=BDP("AAPL US Equity", "LAST_PRICE")        ' last trade
=BDP("AAPL US Equity", "BID")
=BDP("AAPL US Equity", "ASK")
=BDP("AAPL US Equity", "VOLUME")            ' cumulative session
=BDP("EURUSD Curncy",  "LAST_PRICE")
=BDP("T 4.625 02/15/35 Govt", "BID_YIELD")
```

For the cell to update live, the workbook **must** be in
auto-refresh / real-time mode. Toggle via:

- Bloomberg ribbon → **Real-Time → Activate Streaming**, or
- **Bloomberg → Options → Refresh → Real-Time**.

When active, `BDP` cells with real-time fields will tick. When
inactive they show last-fetched value.

### Static-side vs real-time-side field name pairs

| Static (refdata) | Real-time (mktdata) |
|---|---|
| `PX_LAST` | `LAST_PRICE` |
| `PX_BID` / `PX_ASK` | `BID` / `ASK` |
| `PX_VOLUME` | `VOLUME` |
| `PX_OPEN` | `OPEN` |
| `PX_HIGH` / `PX_LOW` | `HIGH` / `LOW` |
| `BID_YIELD` | `BID_YIELD` (same) |

The static-side mnemonics still work in real-time refresh mode —
they just resolve to the most recent tick. The real-time mnemonics
are more deliberate about it.

### `RT_*` event fields

For event-driven sheets (trade-by-trade), the `_RT` family:

```
EVT_TRADE_PRICE_RT
EVT_TRADE_SIZE_RT
EVT_TRADE_CONDITION_CODE_RT
RT_PX_CHG_PCT_1D
RT_PX_CHG_NET_1D
MKTDATA_EVENT_TYPE      ' TRADE / QUOTE / SUMMARY / MARKET_STATUS
MKTDATA_EVENT_SUBTYPE   ' OPENING_TRADE / CLOSING_TRADE / AUCTION / ...
LAST_TRADE_PRICE_TIME_TODAY_REALTIME
RPS_TICKER_EXCH_RT
```

```excel
=BDP("EDP PL Equity", "EVT_TRADE_PRICE_RT")
=BDP("EDP PL Equity", "MKTDATA_EVENT_TYPE")
=BDP("EDP PL Equity", "RT_PX_CHG_PCT_1D")
```

## 5.2 `BLPSubscribe` — explicit subscription

```excel
=BLPSubscribe(security, field, [option1=value1, ...])
```

Available options:

| Option | Effect |
|---|---|
| `interval=N` | Conflate updates to one every N seconds (decimal) |
| `delayed=Y` | Force delayed feed (test without real-time entitlement) |
| `pricingSource=…` | Override source (`BGN`, `CBBT`, `BVAL`, `CMPL`, `WMCO`) |
| `eventStream=ALL`/`TRADE`/`QUOTE` | Filter event types |

```excel
=BLPSubscribe("EDP PL Equity", "LAST_PRICE", "interval=2.0")
=BLPSubscribe("EURUSD Curncy", "BID", "pricingSource=BFIX")
=BLPSubscribe("T 4.625 02/15/35 Govt", "BID_YIELD", "interval=5.0")
```

Cancel:

```excel
=BLPUnsubscribe("EDP PL Equity")
```

Or via ribbon → **Real-Time → Cancel Subscriptions**.

Differences vs real-time `BDP`:

- **Lower latency** — `BLPSubscribe` is a direct stream, `BDP`
  polls.
- **No re-pull on workbook open** — subscriptions resume implicitly.
- **Better for many topics** — `BDP`-driven sheets hit per-cell
  refresh limits at scale; subscriptions are stream-based.

## 5.3 The RTD (Real-Time Data) function

Excel has a built-in `RTD` formula for any COM-RTD-server-aware
data provider. Bloomberg exposes its RTD server as `bloomberglp.RTD`:

```excel
=RTD("bloomberglp.RTD", , "//blp/mktdata/ticker/EDP PL Equity", "LAST_PRICE")
=RTD("bloomberglp.RTD", , "//blp/mktdata/ticker/EURUSD Curncy", "BID")
```

| RTD arg | Meaning |
|---|---|
| 1 | ProgID — `"bloomberglp.RTD"` |
| 2 | Server name — empty for local |
| 3 | Topic (Bloomberg subscription string) |
| 4 | Field |

`RTD` and `BLPSubscribe` do the same thing under the hood. Pick
whichever style your team uses. `RTD` is more "Excel-native";
`BLPSubscribe` integrates better with Bloomberg ribbon controls.

## 5.4 Throttling and conflation

The market data service caps tick rate per topic per second. For
liquid names (SPY, EURUSD, ES1) **always** use `interval=` ≥ 0.5
seconds — otherwise:

- Excel CPU spikes.
- `SUBSCRIPTION_STATUS = SlowConsumerWarning` then
  `SubscriptionTerminated`.
- Workbook becomes unresponsive.

Realistic defaults:

| Use case | `interval=` |
|---|---|
| Blotter / monitor | 1.0 – 2.0 seconds |
| Trading dashboard | 0.5 – 1.0 seconds |
| Backtest replay | n/a — use `BDH` |
| Risk dashboard | 5.0 – 10.0 seconds |

## 5.5 Concurrent subscription cap

Bloomberg Terminal users get ~3,500 concurrent topics. SAPI more.
B-PIPE many more. **One BDP-with-real-time cell ≈ one topic**;
`BLPSubscribe` is the same. If your workbook has 4,000 ticker
cells, you'll silently drop some.

Diagnostics:

- **Bloomberg ribbon → Real-Time → Subscription Manager** shows
  active subscriptions and their state.
- `API <GO>` on the Terminal shows the cap.

## 5.6 Avoiding the "delayed feed" trap

If your entitlement includes some securities at real-time and
others delayed, an unsuspecting workbook can serve a mix. Two
defenses:

```excel
' Force delayed everywhere (for testing or unentitled venues)
=BLPSubscribe("BABA US Equity", "LAST_PRICE", "delayed=Y")

' Force a specific pricing source (NYSE Composite real-time)
=BLPSubscribe("BABA UN Equity", "LAST_PRICE", "pricingSource=BGN")
```

Always inspect **Bloomberg ribbon → Real-Time → Status** for the
green "Live" / yellow "Delayed" indicator per topic.

## 5.7 Patterns: a tiny live blotter

```
   A                       B           C           D           E
1  Security                Last        Bid         Ask         Vol
2  EDP PL Equity          =BLPSubscribe($A2,"LAST_PRICE","interval=1.0")
                          ... (drag B across to C, D, E with corresponding field)
3  GALP PL Equity         ...
4  JMT PL Equity          ...
5  PSI20 Index            ...
6  EURUSD Curncy          ...
7  T 4.625 02/15/35 Govt  =BLPSubscribe($A7,"BID_YIELD","interval=2.0")
```

If you have 50+ securities, define one named range
`SubInterval = "interval=2.0"` and reference it everywhere — easier
to retune.

## 5.8 Subscription status — telling that a feed went down

Bloomberg doesn't surface subscription status into a single cell by
default. Workarounds:

- **`MKTDATA_EVENT_TYPE`** updates with `MARKET_STATUS` when the
  venue opens / closes — useful as a heartbeat.
- **`LAST_TRADE_PRICE_TIME_TODAY_REALTIME`** is the time of the
  last trade; compare to `NOW()` for staleness:

```excel
=IF(NOW() - BDP(A2,"LAST_TRADE_PRICE_TIME_TODAY_REALTIME") > 1/24/60,
    "STALE", "LIVE")
```

`1/24/60` = 1 minute. Adjust to your liquidity threshold.

## 5.9 Workbook layout for streaming sheets

- One **named** sheet per asset class (Equity / Govt / Corp /
  Curncy / Comdty).
- Each sheet uses one common `interval=` constant.
- Top of sheet: a **status row** showing `=NOW()`, refresh count,
  last update.
- A separate **snapshot** sheet that captures values at close — VBA
  paste-special-value at 17:00 local.
- Manual refresh disabled (`Refresh on Open: OFF`) so a startup
  flood doesn't melt the connection.

## 5.10 When to skip streaming entirely

Streaming exists for monitoring and trading. For research:

- **Historical backtests** — `BDH`, never streaming.
- **End-of-day panels** — `BDH` for the series, `BDP` for the
  current snapshot.
- **Day-by-day rebalance signals** — `BDH` with `Per=cdr / Days=W /
  Fill=P` is the right answer.

Streaming feels powerful but it costs entitlement slots and CPU.
Use it only when the latency premium is real.
