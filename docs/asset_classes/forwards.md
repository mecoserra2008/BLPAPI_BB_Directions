# Forwards & Spot

This file covers **non-listed** forwards (FX forwards, NDFs, deliverable
forwards). Listed forwards / futures are in [futures.md](futures.md).
For interest-rate forwards (FRA, forward swaps), see
[swaps.md](swaps.md).

## FX forwards (deliverable)

For G10 + most EM-investment-grade pairs.

### Outright forwards

Append a tenor to the spot ticker (yellow key `Curncy`):

```
EURUSD Curncy           spot (T+2)
EURUSDON Curncy         overnight (T+1)
EURUSDTN Curncy         tom-next
EURUSDSN Curncy         spot-next
EURUSD1W Curncy
EURUSD2W Curncy
EURUSD3W Curncy
EURUSD1M Curncy
EURUSD2M Curncy
EURUSD3M Curncy
EURUSD6M Curncy
EURUSD9M Curncy
EURUSD1Y Curncy
EURUSD18M Curncy
EURUSD2Y Curncy
EURUSD3Y Curncy
EURUSD5Y Curncy
EURUSD10Y Curncy        long-dated
```

`PX_LAST` returns the **outright** forward rate. The "points" are the
difference vs spot.

### Forward points only

Different prefix (drop the "USD" in the pair):

```
EUR1M Curncy            EUR/USD 1m forward points
EUR3M Curncy            3m points
EUR1Y Curncy
JPY1M Curncy            JPY-side points (note inversion)
GBP1M Curncy
CHF1M Curncy
AUD1M Curncy
NZD1M Curncy
CAD1M Curncy
SEK1M Curncy
NOK1M Curncy
```

Points are quoted in **pips** (e.g. `120.5` for 12.05 bps). Outright =
spot + points / 10^N where N depends on the pair (4 for most majors,
2 for USDJPY).

### Forward fields on the outright

If you address the outright (`EURUSD3M Curncy`):

```
PX_LAST                 outright forward
PX_BID, PX_ASK
FWD_POINTS              the points (signed)
FWD_BID, FWD_ASK
FWD_RATE                identical to PX_LAST when on the outright
SPOT_PRICE              the spot used to derive points
IMPL_YIELD_PCT          implied foreign-currency yield (CIP)
IMPL_DEPOSIT_RATE       same family
```

### Settle / value date control

Default forward dates roll by tenor from the spot date. For specific
broken-date forwards use overrides:

```python
ov = req.getElement("overrides").appendElement()
ov.setElement("fieldId", "SETTLE_DT")
ov.setElement("value",   "20260115")        # specific value date

ov = req.getElement("overrides").appendElement()
ov.setElement("fieldId", "FX_FORWARD_TENOR")
ov.setElement("value",   "3M")              # snapping logic
```

`SETTLE_DT` wins over `FX_FORWARD_TENOR` if both are set.

## NDFs (Non-Deliverable Forwards)

Used for currencies under capital controls. Same ticker pattern, but
settlement is in USD against a published fixing.

```
USDCNY1M Curncy           CFETS-fix NDF, 1m
USDCNY3M Curncy           ...
USDCNY1Y Curncy

USDINR1M Curncy           RBI fix
USDBRL1M Curncy           PTAX fix
USDKRW1M Curncy           KFTC fix
USDIDR1M Curncy           JISDOR
USDPHP1M Curncy
USDTWD1M Curncy
USDARS1M Curncy
USDCLP1M Curncy
USDCOP1M Curncy
USDPEN1M Curncy
USDEGP1M Curncy
USDNGN1M Curncy
USDMYR1M Curncy           technically deliverable for some, NDF in practice
```

NDF-specific fields:

```
NDF_FIX_DATE              when the fixing occurs
NDF_VAL_DT                cash-settle date (T+2 from fix)
NDF_FIX_RATE              the fixing rate (post-fix)
NDF_FIX_SOURCE            CFETS, PTAX, JISDOR, KFTC, etc.
IMPL_YIELD_NDF_PCT        implied local-currency yield from the curve
NDF_SPREAD_TO_DELIVERABLE if both NDF and deliverable forward exist
```

## NDF curves and crosses

Most NDF curves trade out to 12m, with limited 2y / 3y liquidity for
KRW, INR, BRL, MYR. Use `IMPL_YIELD_NDF_PCT` across tenors to back out
local rates.

For NDF crosses (rare), Bloomberg supports e.g. `EURBRL1M Curncy`.

## Forward starts (forward-forward)

```
EURUSD3M3M Curncy         3m EUR/USD forward, 3m forward starting
EURUSD6M6M Curncy
USDJPY1Y1Y Curncy
```

## Forward implied carry

CIP relation: `F = S * (1 + r_quote * t) / (1 + r_base * t)`. So:

- For majors with high data quality (`EURUSD`, `GBPUSD`, `USDJPY`)
  the implied yield equals the OIS difference plus the cross-currency
  basis (see [swaps.md](swaps.md) `EUBSC*`).
- For NDFs the implied yield is the *only* observable local rate at
  the front of the curve — there's no domestic OIS market to compare.

```python
# Implied 3m USD-EUR cross-currency basis from CIP
spot   = bdp("EURUSD Curncy", "PX_LAST")["PX_LAST"]
fwd_3m = bdp("EURUSD3M Curncy", "PX_LAST")["PX_LAST"]
ois_us = bdp("USSO3M Curncy", "PX_LAST")["PX_LAST"]
ois_eu = bdp("EESWE3 Curncy", "PX_LAST")["PX_LAST"]
import math
basis = (math.log(fwd_3m / spot) - (ois_us - ois_eu)/100 * 0.25) / 0.25 * 1e4
```

## FX swaps (different from cross-currency swaps)

An FX swap = spot leg + forward leg, single instrument. Bloomberg
quotes them as **forward points**, since spot is implicit. Therefore
`EUR1M Curncy` is *both* the forward-points ticker and the FX-swap
mid quote.

## Spot — pricing source nuances

Spot tickers without modifiers default to **BGN** (Bloomberg
Generic). For research:

- `EURUSD WMCO Curncy` — WM/Reuters fix at 4pm London
- `EURUSD CMPL Curncy` — composite London close
- `EURUSD CMPN Curncy` — composite New York close
- `EURUSD BFIX Curncy` — Bloomberg FX fix (24/5)
- `EURUSD ECB37 Curncy` — ECB reference (14:15 CET)
- `EURUSD WMR1 Curncy` — WMR 11am London
- `EURUSD WMR2 Curncy` — WMR mid

For backtests, **pick a fixing source** and carry it through every
panel.

## Precious-metal forwards (XAU, XAG, XPT, XPD)

Same conventions as FX forwards:

```
XAU Curncy                gold spot, USD/oz
XAU1M Curncy              1m forward
XAU1Y Curncy
XAUEUR Curncy             EUR-quoted spot
XAUEUR3M Curncy           EUR forward
```

Implied gold lease rate via `IMPL_YIELD_PCT` (sometimes called GOFO).

## Common forward-side fields glossary

```
SPOT_PRICE                spot used in deriving the forward
FWD_POINTS                forward points (signed)
FWD_BID, FWD_ASK
FWD_RATE                  outright (when on the points ticker)
TENOR                     "3M" / "1Y" / ...
FORWARD_DATE              the forward value date
SETTLE_DT                 settle date used by analytics
IMPL_YIELD_PCT            CIP-implied foreign yield
IMPL_BORROW_RATE_BID/ASK  for asymmetric borrow markets
IMPL_DEPOSIT_RATE_BID/ASK
TOM_NEXT                  ON forward roll
```

## Pitfalls

- **`USDXXX1M` vs `XXX1M`**: the first is the outright in `XXX` per
  USD; the second is forward points only. Easy to mix up — always
  check `PX_LAST` against spot.
- **JPY pip convention**: USDJPY pip = 0.01, not 0.0001. So
  `USDJPY1M` outright at 150.10 with spot at 150.00 means 10 pips of
  forward.
- **NDF non-business day handling**: fix-date holidays push the value
  date, sometimes by several days. Don't assume T+1 from the
  declared fixing date.
- **Holiday calendars** for forwards differ from spot — e.g. a EUR/USD
  3m forward set today might value-date on a non-USD holiday. Use
  `CALENDAR_CODE` override if you need exact business-day arithmetic.
- **NDF fix sources have changed**: e.g. CNY moved to CFETS, INR to
  RBI's reference rate. If you have legacy data, check `NDF_FIX_SOURCE`
  to confirm the source matches your model.
