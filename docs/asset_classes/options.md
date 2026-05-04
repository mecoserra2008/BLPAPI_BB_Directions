# Options & Volatility

Equity options, equity-index options, FX options, options on futures
and bonds. Yellow key follows the underlying.

## Listed equity options

### Ticker grammar

```
<UNDERLYING> <COUNTRY> <DD/MM/YY> <C|P><STRIKE> Equity
```

Examples:

```
AAPL US 12/19/25 C200 Equity         AAPL Dec 19 2025 200 Call
SPX US 12/19/25 P5000 Index          SPX Dec 19 2025 5000 Put
EDP PL 06/20/25 C3.5 Equity          EDP Jun 20 2025 3.50 Call
SAN SM 06/20/25 C5 Equity            Santander Jun 20 2025 5 Call
SX5E 06/20/25 C5000 Index            Eurostoxx 50 Jun 20 2025 5000 Call
DAX 06/20/25 P20000 Index            DAX Jun 20 2025 20000 Put
```

Notes:
- US equities use `MM/DD/YY`. European exchanges sometimes use the
  same; Bloomberg normalizes for you.
- Strikes can be decimal: `C3.5`, `P3.50`.
- For SPX, expiry is third-Friday standard (`SPX`), with weekly
  variants:
  - `SPX 12/19/25 C5000 Index` — standard monthly
  - `SPXW 12/19/25 C5000 Index` — weekly (PM-settled)
  - `SPXQ 12/19/25 C5000 Index` — quarterly
  - `XSP US 12/19/25 C500 Index` — Mini-SPX (1/10th)

### Option chain (bulk)

```python
req.append("securities", "AAPL US Equity")
req.append("fields",     "OPT_CHAIN")

ov = req.getElement("overrides").appendElement()
ov.setElement("fieldId", "OPTION_CHAIN_OVERRIDE")
ov.setElement("value",   "EXPIRATION")          # one row per expiry
# or "all" / "C" / "P" / specific expiry codes
```

`OPT_CHAIN` row schema: `Security Description` (back-fill into
`bdp` for greeks, IVOL, etc.).

### Option fields

Per-contract:

```
PX_LAST, PX_BID, PX_ASK, PX_VOLUME,
OPT_OPEN_INT
DELTA_MID, DELTA_BID, DELTA_ASK
GAMMA_MID
THETA_MID
VEGA_MID
RHO_MID
IVOL_MID, IVOL_BID, IVOL_ASK,
OPT_IMPLIED_VOLATILITY_MID,            # sometimes IVOL_LAST_RT
OPT_THEO_PRICE_MID
OPT_DAYS_EXPIRE
OPT_EXPIRE_DT
OPT_STRIKE_PX
OPT_PUT_CALL                             # P / C
OPT_EXER_TYP                             # AMERICAN / EUROPEAN
OPT_UNDL_PX, OPT_UNDL_TICKER
OPT_MULTIPLIER, OPT_CONT_SIZE
OPT_DIVIDEND_YIELD
OPT_RATE                                 # risk-free
```

### Implied vol surface (from the underlying)

Constructed surface fields query the underlying directly — Bloomberg
returns the model-fit interpolated value. Format:

```
<DAYS>DAY_IMPVOL_<MONEYNESS>%MNY_DF
```

Examples:

```
30DAY_IMPVOL_100.0%MNY_DF       30d ATM
30DAY_IMPVOL_90.0%MNY_DF        30d, strike = 90% spot
30DAY_IMPVOL_110.0%MNY_DF       30d, strike = 110% spot
60DAY_IMPVOL_100.0%MNY_DF
90DAY_IMPVOL_100.0%MNY_DF
180DAY_IMPVOL_100.0%MNY_DF
360DAY_IMPVOL_100.0%MNY_DF

30DAY_IMPVOL_25DELTA_RR         25-delta risk reversal
30DAY_IMPVOL_25DELTA_BF         25-delta butterfly
30DAY_IMPVOL_10DELTA_RR
```

Note `_DF` suffix = "default fit" (Bloomberg's calibration).

Single-name equity surfaces are typically 30/60/90/180/360 day, ±10%
moneyness; index surfaces (SPX, SX5E) extend to multi-year and finer
moneyness grids.

### Skew / smile shortcuts

```
IVOL_DELTA_NEUTRAL_30D, IVOL_DELTA_NEUTRAL_60D
IVOL_TENOR_DAYS_TO_EXPIRY
IVOL_25D_RR_30D / IVOL_25D_BF_30D
SKEW_INDEX                       Bloomberg's pre-computed skew metric
```

## Index options

Same grammar, yellow key `Index`:

```
SPX 12/19/25 C5000 Index
SX5E 06/20/25 C5000 Index
DAX 06/20/25 P20000 Index
NKY 12/12/25 C40000 Index
HSI 06/27/25 C20000 Index
KOSPI2 06/12/25 C300 Index
RTY US 06/20/25 P2000 Index
VIX 06/18/25 C20 Index            VIX options
```

VIX options have unusual underlying — they reference the **VIX
future** (not spot VIX). `OPT_UNDL_TICKER` returns the right one.

## Options on futures

Address by future ticker:

```
ESZ5C 5800 Index            ES Dec-25 5800 Call
TYZ5P 110 Comdty            TY Dec-25 110 Put
CLZ5C 80 Comdty             WTI Dec-25 80 Call
GCG6C 2300 Comdty           Gold Feb-26 2300 Call
RXM5P 130 Comdty            Bund Jun-25 130 Put
ZNZ5C 110 Comdty            Same TY (older code)
```

Same field set as equity options. `OPT_UNDL_TICKER` returns the
specific future (e.g. `CLZ5 Comdty`).

## FX options

OTC market — addressed by **vol tickers**, not strike-by-strike:

```
EURUSDV1M Curncy            ATM straddle, 1m
EURUSDV3M Curncy            ATM straddle, 3m
EURUSDV1Y Curncy            ATM straddle, 1y

EURUSD25R1M Curncy          25-delta risk reversal 1m
EURUSD25B1M Curncy          25-delta butterfly 1m
EURUSD10R1M Curncy
EURUSD10B1M Curncy

USDJPYV1M Curncy
GBPUSDV1M Curncy
AUDUSDV1M Curncy
```

For specific strikes you'd build a Black-Scholes from the ATM /
RR / BF triplet (the "smile interpolation" Bloomberg also exposes via
`OVDV <GO>`). Programmatically you can use the family of constructed
fields:

```
30DAY_IMPVOL_100.0%MNY_DF       on the spot ticker
... (same family as equities)
```

## Listed FX options (CME)

Strike-level CME FX options on FX futures:

```
ECM5C 1.10 Curncy           EUR/USD Jun-25 1.10 Call (CME)
JYM5P 0.0066 Curncy
```

## Bond options (swaptions, options on bond futures)

Swaption vol — see [swaps.md](swaps.md). Listed options on bond
futures parallel commodity options on futures.

```
RXM5C 130.5 Comdty          Bund Jun-25 130.5 Call (Eurex)
TYZ5P 110 Comdty            TY Dec-25 110 Put (CBOT)
```

## Vol indices

Pre-baked implied-vol indices:

```
VIX Index                   30d S&P 500
VIX9D Index                 9-day
VIX3M Index                 3-month
VIX6M Index                 6-month
VVIX Index                  vol-of-VIX
SKEW Index                  CBOE skew
V2X Index                   VSTOXX
V1X Index                   VDAX-NEW
VHSI Index                  HSI vol
VKOSPI Index                KOSPI vol
VFTSE Index                 FTSE 100 vol
JNIV Index                  Nikkei vol

MOVE Index                  Treasury implied vol (option-implied)
SRVIX Index                 swaption vol (former CME)
GVZ Index                   Gold vol
OVX Index                   Crude oil vol
EVZ Index                   EUR/USD vol (CBOE)
JYVIX Index                 USD/JPY vol
```

## Greeks at the underlying level (aggregated)

```
PX_OPTION_PUT_VOLUME, PX_OPTION_CALL_VOLUME
PUT_CALL_VOLUME_RATIO_CUR_DAY
PUT_CALL_OPEN_INTEREST_RATIO
OPT_PUT_CALL_RATIO_30D, OPT_PUT_CALL_RATIO_60D
OPT_OPEN_INT_AGGTE                     # all options OI
30DAY_GAMMA_EXPOSURE                   # market-makers' gamma estimate
```

## OPRA / pricing source

Some option fields require a specific source:

| Source | Coverage |
|---|---|
| `OPRA` | US listed options consolidated |
| `XCBO` | CBOE-only |
| `BVOL` | Bloomberg implied-vol surface (model) |
| `BVAL` | Evaluated price (illiquid contracts) |

Override the request's `pricingSource` element to switch.

## Common option research recipes

```python
# Full SPX option chain on a date
chain = bds("SPX Index", "OPT_CHAIN")          # all expiries
opts  = [r["Security Description"] for r in chain
         if "12/19/25" in r["Security Description"]]

snap  = bdp(opts, ["OPT_STRIKE_PX","OPT_PUT_CALL","DELTA_MID","IVOL_MID",
                   "OPT_OPEN_INT","PX_LAST","OPT_UNDL_PX"])

# 30-day ATM IVOL history for a basket
underlyings = ["AAPL US Equity","MSFT US Equity","NVDA US Equity"]
ivol = bdh(underlyings, ["30DAY_IMPVOL_100.0%MNY_DF"],
           "20240101","20251231")

# 25-delta skew (RR) history for FX
skew = bdh(["EURUSD25R1M Curncy","EURUSD25R3M Curncy",
            "EURUSD25R1Y Curncy"], ["PX_LAST"],
           "20140101","20251231")
```

## Pitfalls

- **Mid IVOL** is interpolated when bid/ask spreads are wide — for
  illiquid names use `IVOL_BID` and `IVOL_ASK` and inspect the spread.
- **Multipliers vary**: AAPL = 100, SPX = 100, ES futures option = 50.
  Always pull `OPT_MULTIPLIER` for PnL calculations.
- **American vs European**: same strike/expiry can have both for
  index options (e.g. `XSP` is European, `SPY` options are American).
- **Time-to-expiry day count**: Bloomberg uses calendar days for
  `OPT_DAYS_EXPIRE`. For trading-day vol you need to compute manually.
- **Listed vs OTC FX**: CME options use a futures underlying; OTC
  options use spot. The same delta/strike maps to different vols.
- **Settlement type**: cash-settled (SPX), AM-settled, PM-settled —
  check `OPT_SETTLE_TYPE`. SPXW (weekly) is PM, SPX (monthly) is AM
  (this affects pricing into expiry).
