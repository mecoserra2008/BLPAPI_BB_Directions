# Swaps (IRS, OIS, basis, CDS)

Yellow keys: `Curncy` for rate / FX swaps, `Corp` for CDS.

## Interest-rate swaps & OIS

Post-LIBOR transition (effectively complete by mid-2024) the
benchmarks are:

| Currency | Overnight benchmark | Legacy benchmark |
|---|---|---|
| USD | SOFR | LIBOR (retired 2023) |
| EUR | €STR | EONIA (replaced 2022) / 6M EURIBOR (still alive) |
| GBP | SONIA | LIBOR (retired 2024) |
| JPY | TONA | TIBOR / LIBOR |
| CHF | SARON | LIBOR (retired) |
| CAD | CORRA | CDOR (retiring) |
| AUD | RBA cash rate | BBSW |
| HKD | HKD HONIA | HIBOR |
| SGD | SORA | SOR (retired) |

### USD curves (SOFR-based)

```
USSO1 Curncy              SOFR OIS 1y
USSO2, USSO3, USSO5, USSO7, USSO10, USSO15, USSO20, USSO25, USSO30 Curncy
USSOC Curncy              SOFR spot-starting (older notation)
```

Spot-tomorrow (1m / 3m / 6m forward starting):

```
USSO1F1 Curncy            1y OIS, 1y forward starting
USSO1F2 Curncy            1y OIS, 2y forward starting
... USSO1F10
USSOA Curncy              SOFR overnight rate
```

Older USD swaps still appear (SOFR-discounted, historically 3M LIBOR
floating leg):

```
USSWAP1 Curncy ... USSWAP30 Curncy           # legacy fixed/3M LIBOR
USSW1 Curncy   ... USSW30 Curncy             # alternative ticker family
```

### EUR curves

OIS (€STR-based, the post-2022 standard):

```
EESWE1 Curncy ... EESWE30 Curncy             # €STR OIS
EUSWE1 Curncy ... EUSWE30 Curncy             # alias
```

Legacy (still quoted):

```
EUSA1 Curncy ... EUSA30 Curncy               # vs 6M EURIBOR
EUSW1 Curncy  ... EUSW30 Curncy              # vs 3M EURIBOR
```

### GBP curves

```
BPSWS1 Curncy ... BPSWS30 Curncy             # legacy (LIBOR)
BPSO1 Curncy  ... BPSO30 Curncy              # SONIA OIS
```

### JPY

```
JYSO1 Curncy  ... JYSO30 Curncy              # TONA OIS
JYSWAP1 Curncy ... JYSWAP30 Curncy           # legacy
```

### CHF

```
SFSARON1 Curncy ... SFSARON30 Curncy         # SARON OIS
SFSF1 Curncy ... SFSF30 Curncy               # legacy
```

### EM swaps

```
KRWNDS1 Curncy ... KRWNDS10 Curncy           # KRW IRS (NDIRS)
INRNDS1 Curncy ... INRNDS10 Curncy           # INR IRS (NDIRS)
BRLNDS1 Curncy ... BRLNDS10 Curncy           # BRL DI swaps
PLN1 Curncy ...                              # ZAR / PLN / TRY all have own families
ZARNDS5 Curncy
TRYNDS5 Curncy
MXNNDS5 Curncy
```

For Brazil specifically, the **DI futures curve** is the local
benchmark: `ODF1 Comdty` etc.

## Cross-currency basis (XCCY)

Bps spread on the foreign leg vs USD over the same OIS curve.

```
EUBSC1 Curncy ... EUBSC30 Curncy             # EUR/USD basis (bps)
JYBSC1 Curncy ... JYBSC30 Curncy             # JPY/USD basis
BPBSC1 Curncy ... BPBSC30 Curncy             # GBP/USD basis
SFBSC1 Curncy ...                            # CHF/USD
ADBSC1 Curncy ...                            # AUD/USD
NDBSC1 Curncy ...                            # NZD/USD
CDBSC1 Curncy ...                            # CAD/USD
```

XCCY basis is negative when USD funding is scarce (typical state).
`PX_LAST` is in bps.

## Tenor structure (curve nodes)

A typical liquid curve has these nodes:

```
ON, TN, SN, 1W, 2W, 1M, 2M, 3M, 6M, 9M,
1Y, 18M, 2Y, 3Y, 4Y, 5Y, 6Y, 7Y, 8Y, 9Y, 10Y, 12Y, 15Y, 20Y, 25Y, 30Y, 40Y, 50Y
```

Address with the appropriate prefix family. Bloomberg fills missing
nodes by interpolation in `bdh` if you set the right curve overrides
on a `//blp/curve`-style request.

## Forward swaps

```
USFS0102 Curncy           1y swap, 2y forward (1y2y)
USFS0205 Curncy           2y swap, 5y forward (2y5y)
USFS0510 Curncy           5y10y
USFS0530 Curncy           5y30y

EUFS0102, EUFS0205, EUFS0510, EUFS0530 Curncy

# General pattern: <CCY>FS<tenor1><tenor2>
```

## Swaption volatility

Swaption vol matrix tickers are alphanumeric and conventional. Examples:

```
USSV0110 Curncy           Vol of 1y10y swaption (USD)
USSV0510 Curncy           5y10y swaption vol
EUSV0110 Curncy           1y10y EUR
GBSV0110 Curncy
JYSV0110 Curncy
```

`PX_LAST` returns the lognormal or normal vol depending on the ticker
family. ATM straddles, plus 25-delta:

```
USSAOAT 1Y10Y Curncy      25d ATM Straddle, 1y10y
```

## Bond-future-implied swap repo

Each bond future has implied repo and net basis:

```
TYZ5 Comdty                Bond future
NET_BASIS, IMPLIED_REPO_RATE, GROSS_BASIS,
NET_BASIS_BCT, FUT_CTD_BOND, CTD_FRWD_PX
DELIVERY_DAY_RATE
```

`FUT_CTD_BOND` returns the cheapest-to-deliver bond ticker.

## CDS — Credit Default Swaps

Yellow key: `Corp`.

### Single-name CDS

Pattern:

```
<TICKER> CDS USD SR <TENOR>Y D14 Corp
<TICKER> CDS EUR SR <TENOR>Y D14 Corp
<TICKER> CDS USD SUB <TENOR>Y D14 Corp        # subordinated

# D14 = 2014 ISDA definitions (current standard)
# Older: D03 (2003), still around for some legacy

EDPPL CDS USD SR 5Y D14 Corp
TEFE CDS EUR SR 5Y D14 Corp                   # Telefónica
JPM CDS USD SR 5Y D14 Corp
DBR CDS USD SR 5Y D14 Corp                    # German sovereign
ITALY CDS USD SR 5Y D14 Corp
PORTUG CDS USD SR 5Y D14 Corp
TURKEY CDS USD SR 5Y D14 Corp
BRAZIL CDS USD SR 5Y D14 Corp
RUSSIA CDS USD SR 5Y D14 Corp                  # historical
```

Tenors: 6M, 1Y, 2Y, 3Y, 4Y, 5Y, 7Y, 10Y, 20Y, 30Y.

### CDS Indices

```
CDX IG CDSI S42 5Y Corp                       # CDX IG 5y, current series
CDX HY CDSI S42 5Y Corp                       # CDX HY
ITRX MAIN CDSI S40 5Y Corp                    # iTraxx Main
ITRX XOVER CDSI S40 5Y Corp                   # iTraxx Crossover
ITRX SNRFIN CDSI S40 5Y Corp                  # senior financials
ITRX SUBFIN CDSI S40 5Y Corp                  # sub financials
ITRX ASIAXJ CDSI S40 5Y Corp
ITRX AUS CDSI S40 5Y Corp                     # Australia
CDX EM CDSI S38 5Y Corp                       # Emerging markets
```

Series rolls semi-annually (March / September). For research, follow
the **on-the-run** ticker — e.g. `CDX IG CDSI GEN 5Y Corp` returns the
current series.

### CDS fields

```
PX_LAST                       par-spread (bps) or upfront % (depends on convention)
CDS_QUOTE_TYPE                "Par Spread" or "Upfront"
CDS_FAIR_SPREAD               model-implied
CDS_FLAT_SPREAD               flat-curve equivalent
CDS_IMPLIED_DEFAULT_PROB      cumulative default probability
CDS_RECOVERY_RATE             assumption (default 40% for SR, 25% for SUB)
CDS_RUNNING_CPN               100 or 500 bps standard
CDS_DV01                      $ value of 1 bp
RISKY_DUR                     duration
ACCRUED_INTEREST
UPFRONT_PMT                   for traded conventions
ISDA_DEFINITION_VERSION       D03 / D14
DEFAULT_PROBABILITY           Bloomberg DRSK model (issuer-level)
```

### CDS curves

For an issuer the curve is:

```
EDPPL CDS USD SR 1Y D14 Corp
EDPPL CDS USD SR 3Y D14 Corp
EDPPL CDS USD SR 5Y D14 Corp
EDPPL CDS USD SR 7Y D14 Corp
EDPPL CDS USD SR 10Y D14 Corp
```

`bdp` across the panel gives you the curve in one call.

## Asset-swap spreads

For a cash bond, the *asset-swap spread* (ASW) is the bond's spread
over the swap curve. Field family lives on the bond:

```
ASSET_SWAP_SPD_MID           current ASW
ASSET_SWAP_SPD_BID, ASSET_SWAP_SPD_ASK
ASW_DUR_TO_WORST
```

Or compute via YAS overrides (see [bonds.md](bonds.md)).

## Inflation swaps

```
USSWITP1 Curncy ... USSWITP30 Curncy          # USD CPI swap (zero-coupon)
EUSWIT1 Curncy ... EUSWIT30 Curncy            # EUR HICPx
BPSWIT1 Curncy ... BPSWIT30 Curncy            # GBP RPI
JYSWIT1 Curncy                                 # JPY CPI
```

`PX_LAST` is the zero-coupon breakeven inflation rate (%).

## Volatility / cap-floor

```
USCV1Y10Y Curncy             1y10y caplet vol
USCV3M10Y Curncy             3m10y caplet vol
USFL3M2Y Curncy              short-end floor
```

## Building a curve in code

The most reusable pattern:

```python
import pandas as pd

CURVE_USD_OIS = [
    ("ON",   "FEDLO Index"),    # overnight effective
    ("1M",   "USSOC Curncy"),
    ("3M",   "USSO3 Curncy"),
    ("6M",   "USSO6 Curncy"),
    ("1Y",   "USSO1 Curncy"),
    ("2Y",   "USSO2 Curncy"),
    ("3Y",   "USSO3 Curncy"),
    ("5Y",   "USSO5 Curncy"),
    ("7Y",   "USSO7 Curncy"),
    ("10Y",  "USSO10 Curncy"),
    ("15Y",  "USSO15 Curncy"),
    ("20Y",  "USSO20 Curncy"),
    ("30Y",  "USSO30 Curncy"),
]

tickers = [t for _, t in CURVE_USD_OIS]
quotes  = bdp(tickers, ["PX_LAST"])
```

For *historical* curves, batch the same list into `bdh` and pivot.

## Pitfalls

- **Quote type** for CDS varies — par spread vs upfront. Always read
  `CDS_QUOTE_TYPE`.
- **Series convention**: `CDX IG GEN` rolls automatically; `S42` pins
  a specific series (will go off-the-run).
- **Recovery rate** assumptions are a model input, not a market quote
  — check `CDS_RECOVERY_RATE` if you're computing PnL or hazard.
- **Day count conventions**: USD fixed leg ACT/360 historically vs
  ACT/365 in some EM swaps. Field `DAY_CNT_DES` exposes it.
- **Curve aliases**: `EUSA10` (vs 6M EURIBOR) and `EESWE10` (€STR)
  trade at different levels post-2022. Pick the right one for the
  instrument you're discounting.
- **Sovereign CDS** quotes are USD-denominated par spread by
  convention (e.g. `ITALY CDS USD SR 5Y D14 Corp`) — using the
  EUR-denominated version gives different liquidity / quotes.
