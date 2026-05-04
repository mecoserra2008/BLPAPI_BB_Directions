# Commodities

Yellow key: `Comdty`. Almost everything is **futures** (or options on
futures). Spot commodities exist for some (precious metals via
`Curncy`), and physical assessments come via `Comdty` too.

## Generic vs specific contract

Bloomberg lets you address a futures contract two ways:

| Form | Example | Meaning |
|---|---|---|
| **Generic series** | `CL1 Comdty`, `CL2 Comdty`, … `CL12 Comdty` | The Nth nearest active contract — Bloomberg rolls the underlying |
| **Specific contract** | `CLZ5 Comdty`, `CLM6 Comdty`, … | Dec-2025, Jun-2026, … |

Generic series are perfect for time-series modelling — they remove the
month-by-month gaps. Specific contracts are needed for term-structure
work (curve at a date), hedging, or accurate roll modelling.

Month codes: `F G H J K M N Q U V X Z` for Jan-Dec
(see [cheatsheets/month_codes.md](../../cheatsheets/month_codes.md)).
Year is the last digit (sometimes two digits since 2020).

## Energy

| Generic | Underlying | Exchange |
|---|---|---|
| `CL1 Comdty` | WTI Crude Oil | NYMEX |
| `CO1 Comdty` | Brent Crude | ICE Europe |
| `NG1 Comdty` | Henry Hub Natural Gas | NYMEX |
| `TZT1 Comdty` | TTF Dutch Natural Gas | ICE Endex |
| `MO1 Comdty` | Murban Crude | IFAD |
| `XB1 Comdty` | RBOB Gasoline | NYMEX |
| `HO1 Comdty` | Heating Oil / NY Harbor ULSD | NYMEX |
| `QS1 Comdty` | Gasoil (low-sulfur) | ICE Europe |
| `MO1 Comdty` | Murban | IFAD |
| `EA1 Comdty` | Coal API2 (Rotterdam) | ICE |
| `EB1 Comdty` | Coal API4 (Richards Bay) | ICE |
| `MOC1 Comdty` | EU emissions (EUA) | ICE |

Spot / physical (assessments are by Platts, Argus, OPIS):

```
USCRWTIC Index            WTI spot price
EUCRBRDT Index            Brent dated
DRGEAGAS Index            US natgas storage
```

## Precious & base metals

| Generic | Underlying | Notes |
|---|---|---|
| `GC1 Comdty` | Gold | COMEX |
| `SI1 Comdty` | Silver | COMEX |
| `HG1 Comdty` | Copper | COMEX |
| `PL1 Comdty` | Platinum | NYMEX |
| `PA1 Comdty` | Palladium | NYMEX |
| `LMAHDS03 LME Comdty` | LME Aluminium 3M | LME |
| `LMCADS03 LME Comdty` | LME Copper 3M | LME |
| `LMNIDS03 LME Comdty` | LME Nickel 3M | LME |
| `LMZSDS03 LME Comdty` | LME Zinc 3M | LME |
| `LMPBDS03 LME Comdty` | LME Lead 3M | LME |
| `LMSNDS03 LME Comdty` | LME Tin 3M | LME |

Spot precious (FX-style):

```
XAU Curncy                Gold spot, USD/oz
XAG Curncy                Silver spot
XPT Curncy                Platinum
XPD Curncy                Palladium
XAUEUR Curncy             Gold in EUR
XAUJPY Curncy             Gold in JPY
```

Note: **`XAU Curncy` lives under the `Curncy` yellow key**, not Comdty.

## Agricultural

| Generic | Underlying | Exchange |
|---|---|---|
| `C 1 Comdty` (note the space) | Corn | CBOT |
| `S 1 Comdty` | Soybeans | CBOT |
| `W 1 Comdty` | Soft Red Wheat | CBOT |
| `KW1 Comdty` | Hard Red Winter Wheat | KCBT |
| `SM1 Comdty` | Soybean Meal | CBOT |
| `BO1 Comdty` | Soybean Oil | CBOT |
| `LH1 Comdty` | Lean Hogs | CME |
| `LC1 Comdty` | Live Cattle | CME |
| `FC1 Comdty` | Feeder Cattle | CME |
| `SB1 Comdty` | Sugar #11 (raw) | ICE US |
| `KC1 Comdty` | Coffee C | ICE US |
| `CC1 Comdty` | Cocoa | ICE US |
| `CT1 Comdty` | Cotton #2 | ICE US |
| `JO1 Comdty` | Frozen OJ | ICE US |

Single-letter tickers (C, S, W) need a **space** before the digit
because the parser is column-aware:

```
C 1 Comdty       # corn — yes, with the space
S 1 Comdty       # soybeans
W 1 Comdty       # wheat
```

## Indices (commodity baskets)

```
BCOM Index            Bloomberg Commodity Index (price)
BCOMTR Index          BCOM total return
SPGSCI Index          S&P GSCI
SPGSCITR Index        S&P GSCI total return
DJP Index             iPath Dow Jones (ETN)
CRY Index             Refinitiv/CRB
RICIA Index           Rogers International Commodity Index
```

## Static / contract-spec fields

For futures (generic or specific):

```
FUT_TICK_SIZE             tick size in price terms
FUT_TICK_VAL              tick value in currency
FUT_VAL_PT                value of a 1-point move
FUT_CONT_SIZE             contract size (e.g. 1000 bbl)
FUT_TRADING_UNITS         description of the underlying unit
FUT_CUR_GEN_TICKER        for a generic, the underlying specific
FUT_GEN_FIRST_TRADE_DT    first trade date of the current generic
FUT_FIRST_TRADE_DT        first trade date of the contract
FUT_NOTICE_FIRST          first notice date
FUT_DLV_DT_FIRST, FUT_DLV_DT_LAST
LAST_TRADEABLE_DT         last day to trade
FUT_CUR_OPT_RATE          current open interest
FUT_AGGTE_VOL             aggregate vol across maturities
FUT_AGGTE_OPEN_INT        aggregate OI across maturities
OPEN_INT                  open interest, this contract
OPEN_INT_DATE             OI date
EXCH_CODE
SETTLE_DT
CONTRACT_VALUE            CUR_MKT_VAL equivalent
```

## Futures chain (`FUT_CHAIN`)

Bulk field with one row per active contract:

```python
req.append("securities", "CL1 Comdty")
req.append("fields",     "FUT_CHAIN")
ov = req.getElement("overrides").appendElement()
ov.setElement("fieldId", "INCLUDE_EXPIRED_CONTRACTS"); ov.setElement("value", "Y")
ov = req.getElement("overrides").appendElement()
ov.setElement("fieldId", "CHAIN_DATE"); ov.setElement("value", "20250502")
```

Row schema: `Security Description` (e.g. `CLM5 Comdty`).

## Generic-roll behaviour

Bloomberg has internal rules for when `CL1` rolls from one specific
contract to the next (active month, expiry, last-trading-day-N). For
backtests this matters — different schemes give materially different
returns.

Override the roll method when fetching history:

```python
ov = req.getElement("overrides").appendElement()
ov.setElement("fieldId", "ROLL_METHOD"); ov.setElement("value", "ACTIVE")
# values: ACTIVE, OPEN_INT, RELATIVE, FRONT, ...
```

Or use `xbbg.blp.bdh(..., roll='ACTIVE')`.

For research, three families of total-return commodity series:

1. **`USCRWTIC Index`-style spot index** — physical reference, no
   carry.
2. **`CL1 Comdty` close** — front future, *not roll-adjusted* (gap on
   each roll day).
3. **`SPGSCICL Index`** — single-commodity total-return sub-index from
   GSCI; pre-rolled. Equivalent for BCOM:
   `BCOMCL Index`, `BCOMNG Index`, etc.

For backtesting commodity factor models, `SP-GSCI` total-return
sub-indices are the cleanest: no rolls to model, S&P publishes a
documented methodology.

## Physical / cash assessments

Many cash markets are surveyed (Platts, Argus, OPIS, IHS Markit). They
typically live as **`<TICKER> Index`** rather than under Comdty:

```
USPM00LL Index           Platts WTI Mid Cash
EUBRBOSS Index           Argus Brent
NGNJBHHC Index           Henry Hub spot
DRGEAGAS Index           US natgas storage
USPMSMC Index            US gasoline rack
```

## Curve / term structure recipe

```python
# As-of date curve for WTI:
chain = bds("CL1 Comdty", "FUT_CHAIN",
            INCLUDE_EXPIRED_CONTRACTS="N",
            CHAIN_DATE="20250502")
contracts = [r["Security Description"] for r in chain]
quotes = bdp(contracts, ["PX_LAST", "FUT_DLV_DT_FIRST", "OPEN_INT"])
# Plot price vs first-delivery date for the term structure
```

## Spreads (calendar)

Address calendar spreads directly with the special syntax:

```
CL1-CL2 Comdty                      # WTI front-vs-2nd
CL1-CL12 Comdty                     # 1-year carry
CO1-CL1 Comdty                      # Brent-WTI arb
HG1-LMCADS03 LME Comdty             # COMEX-LME copper arb
```

Bloomberg returns the spread as `PX_LAST = leg1 − leg2`.

## Crack and spark spreads

```
CL1 Comdty − HO1 Comdty             # crack proxy (manually compute)
NG1 Comdty                          # power markets:
PJWHRTD Index                       # PJM Western Hub Real-Time
```

Pre-built crack contracts:

```
CR1 Comdty                          # 3:2:1 Crack (NYMEX)
HO1-CL1 Comdty                      # heating-crack (manual)
RB1-CL1 Comdty                      # gasoline-crack
```

## Volatility & options on futures

```
CLZ5C 80 Comdty                     # WTI Dec-25 80-strike call
GCM6P 2300 Comdty                   # Gold Jun-26 2300-strike put
```

Fields parallel to equity options: `IVOL_MID`, `DELTA_MID`,
`GAMMA_MID`, `THETA_MID`, `VEGA_MID`, `OPT_CHAIN`.

For implied vol *surfaces* on the front future:

```
CL1_IV_30D, CL1_IV_60D, CL1_IV_90D, CL1_IV_180D
30DAY_IMPVOL_100.0%MNY_DF           # ATM 30d
30DAY_IMPVOL_90.0%MNY_DF            # 10% OTM
```

## Inventory / fundamentals

```
DOEASCRD Index            US crude inventories (DOE)
DOEAGAS Index             US gasoline inventories
DOEUSALC Index            DOE Cushing crude
COTSP Index               COT speculator positioning (CFTC)
COMOPENINT Index          aggregate OI all commodities
```

Use these as macro inputs to commodity strategies — the Bloomberg
identifier doesn't show its source clearly, so confirm via `DES <GO>`.
