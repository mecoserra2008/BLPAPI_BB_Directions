# Futures (cross-asset)

Yellow keys: futures live where their *underlying* lives.
Equity-index → `Index` (sometimes `Comdty`); single-stock futures →
`Equity`; bond and rate futures → `Comdty`; FX futures → `Curncy`;
commodity futures → `Comdty`. The yellow key tells you the asset
class, not the instrument type.

## Generic vs specific

Same convention as commodities (see [commodities.md](commodities.md)):
- `<ROOT>1 ... Comdty` = active month
- `<ROOT>2`, `<ROOT>3`, … = N-th deferred
- `<ROOT><MONTH><YEAR> ... Comdty` = specific contract

Month codes: `F G H J K M N Q U V X Z` for Jan–Dec.

## Equity-index futures

| Generic | Underlying | Currency / Exchange |
|---|---|---|
| `ES1 Index` | S&P 500 E-mini | USD / CME |
| `MES1 Index` | S&P 500 micro E-mini | USD / CME |
| `NQ1 Index` | NASDAQ-100 E-mini | USD / CME |
| `RTY1 Index` | Russell 2000 E-mini | USD / CME |
| `YM1 Index` | Dow E-mini | USD / CBOT |
| `VIX1 Index` | VIX futures | USD / CFE |
| `VG1 Index` | Euro Stoxx 50 | EUR / Eurex |
| `GX1 Index` | DAX | EUR / Eurex |
| `CF1 Index` | CAC 40 | EUR / Euronext |
| `Z 1 Index` | FTSE 100 (note the space) | GBP / ICE |
| `SM1 Index` | SMI | CHF / Eurex |
| `IB1 Index` | FTSE MIB | EUR / IDEM |
| `IBE1 Index` | IBEX 35 | EUR / MEFF |
| `EO1 Index` | OMX Helsinki 25 | EUR |
| `OMX1 Index` | OMX Stockholm 30 | SEK |
| `AEX1 Index` | AEX | EUR / Euronext |
| `BEL1 Index` | BEL 20 | EUR / Euronext |
| `PSI1 Index` | PSI 20 | EUR / Euronext |
| `ATX1 Index` | ATX | EUR / Wiener Börse |
| `TP1 Index` | Topix | JPY / OSE |
| `NK1 Index` | Nikkei 225 | JPY / OSE |
| `NXA Index` | Nikkei 225 SGX-traded | JPY / SGX |
| `HI1 Index` | Hang Seng | HKD / HKEX |
| `HC1 Index` | HSCEI | HKD / HKEX |
| `XU1 Index` | China A50 (SGX) | USD / SGX |
| `KM1 Index` | KOSPI 200 | KRW / KRX |
| `XP1 Index` | ASX SPI 200 | AUD / ASX |
| `TW1 Index` | TAIEX | TWD / TAIFEX |

## Bond futures

| Generic | Underlying | Exchange |
|---|---|---|
| `TU1 Comdty` | US 2Y Note | CBOT |
| `FV1 Comdty` | US 5Y Note | CBOT |
| `TY1 Comdty` | US 10Y Note | CBOT |
| `UXY1 Comdty` | US Ultra 10Y Note | CBOT |
| `US1 Comdty` | US Long Bond | CBOT |
| `WN1 Comdty` | US Ultra Long Bond | CBOT |
| `RX1 Comdty` | German Bund 10Y | Eurex |
| `OE1 Comdty` | German Bobl 5Y | Eurex |
| `DU1 Comdty` | German Schatz 2Y | Eurex |
| `UB1 Comdty` | German Buxl 30Y | Eurex |
| `IK1 Comdty` | Italian BTP 10Y | Eurex |
| `OAT1 Comdty` | French OAT 10Y | Eurex |
| `OEU1 Comdty` | French BTAN 5Y | Eurex |
| `G 1 Comdty` (note space) | UK Gilt 10Y | ICE Europe |
| `JB1 Comdty` | JGB 10Y | OSE |

## Short-rate / IR futures

| Generic | Underlying | Exchange |
|---|---|---|
| `SFR1 Comdty` | SOFR 3M (white-pack active) | CME |
| `SR3A Comdty` | SOFR 3M, A=White, B=Red, ... | CME |
| `FF1 Comdty` | Fed Funds 30D | CBOT |
| `ED1 Comdty` | Eurodollar 3M (DEPRECATED post-LIBOR) | CME |
| `ER1 Comdty` | EURIBOR 3M (transitioning to ESTR-equivalent) | ICE |
| `EI1 Comdty` | €STR 3M | ICE |
| `L 1 Comdty` (note space) | Short Sterling (DEPRECATED) | ICE |
| `SO1 Comdty` | SONIA 3M | ICE |
| `JY1 Comdty` | TONA 3M | TFX |

The Eurodollar / LIBOR-based contracts are being retired — for
post-LIBOR (post-2024) work, use SOFR (`SFR`/`SR3`), SONIA (`SO`),
€STR (`EI`), TONA (`JY`).

## FX futures

| Generic | Underlying | Exchange |
|---|---|---|
| `EC1 Curncy` | EUR/USD | CME |
| `BP1 Curncy` | GBP/USD | CME |
| `JY1 Curncy` | JPY/USD (note: JPY-side base) | CME |
| `AD1 Curncy` | AUD/USD | CME |
| `NV1 Curncy` | NZD/USD | CME |
| `CD1 Curncy` | CAD/USD | CME |
| `SF1 Curncy` | CHF/USD | CME |
| `MP1 Curncy` | MXN/USD | CME |
| `BR1 Curncy` | BRL/USD | CME |
| `RU1 Curncy` | RUB/USD | CME |
| `CN1 Curncy` | CNH/USD | CME |
| `IR1 Curncy` | INR/USD | CME |
| `KR1 Curncy` | KRW/USD | CME |

> CME FX futures are quoted **inverted** vs the FX market (USD per unit
> of foreign), so `JY1` = JPY/USD = 1/USDJPY. Mind the direction.

## Single-stock futures (SSFs)

Many European exchanges offer SSFs. Same yellow key as the underlying:

```
SAP1 Equity                 SAP single-stock future, generic active
TOTB1 Equity                TotalEnergies SSF
```

## Specific contract addressing

Combine root + month + year:

```
ESM5 Index                  S&P 500 Jun-2025
ESU5 Index                  S&P 500 Sep-2025
ESZ5 Index                  S&P 500 Dec-2025

TYZ5 Comdty                 US 10Y Note Dec-25
RXM5 Comdty                 Bund Jun-25
ECM5 Curncy                 EUR/USD Jun-25 (CME)

CLZ5 Comdty                 WTI Dec-25
GCG6 Comdty                 Gold Feb-26
```

For 2-digit-year, Bloomberg accepts both single-digit (`Z5` = 2025) and
two-digit (`Z25`) since 2020. Prefer two-digit to disambiguate (`Z5`
could be 2015 in old archived data).

## Static / contract-spec fields

```
FUT_TICK_SIZE             tick size (e.g. 0.25 for ES)
FUT_TICK_VAL              tick value in currency (e.g. $12.50 for ES)
FUT_VAL_PT                point value (e.g. $50 for ES)
FUT_CONT_SIZE             multiplier × index level
FUT_TRADING_UNITS         description
FUT_FIRST_TRADE_DT, FUT_LAST_TRADE_DT, LAST_TRADEABLE_DT
FUT_NOTICE_FIRST          first notice for delivery
FUT_DLV_DT_FIRST, FUT_DLV_DT_LAST
FUT_CUR_GEN_TICKER        for a generic, the underlying specific
FUT_GEN_FIRST_TRADE_DT    for generic, when the current pin started
OPEN_INT, OPEN_INT_DATE
FUT_AGGTE_VOL, FUT_AGGTE_OPEN_INT
SETTLE_DT
EXCH_CODE
PX_SETTLE_LAST_DT, PX_SETTLE_LAST,
PX_SETTLE
FUT_MONTH_YR              "Z25"
DELIVERY_MONTH_LBL        "DEC 25"
```

## Roll handling

Generic series are auto-rolled by Bloomberg using the chosen method.
Override per request:

```python
ov = req.getElement("overrides").appendElement()
ov.setElement("fieldId", "ROLL_METHOD")
ov.setElement("value",   "ACTIVE")
# Methods: ACTIVE, OPEN_INT, RELATIVE_RELATIVE, FRONT,
#          RELATIVE_TO_FIRST_NOTICE, RELATIVE_TO_LAST_TRADE
```

For backtesting commodities/futures, the **active-OI roll** is most
realistic; for academic-style backtests, the **calendar-N-days-before-
expiry** roll is more reproducible.

`xbbg` exposes this via `roll='ACTIVE' | 'PRIOR' | 'NONE' | 'AON'`.

## Total return commodity / equity-future indices

Many strategy / total-return indices are pre-computed:

```
SPGSCITR Index            S&P GSCI total return (commodities, no rolls)
BCOMTR Index              Bloomberg Commodity total return
SPESSP Index              S&P 500 E-mini total return (excess return on roll)
ER10 Index                Goldman ES roll-down (legacy)
```

These remove the need to model the roll yourself.

## Calendar spreads & inter-product spreads

Direct addressing:

```
ESM5-ESU5 Index           Jun-Sep ES spread
TYM5-TYU5 Comdty          Jun-Sep TY spread
RXM5-OEM5 Comdty          Bund-Bobl curve trade
TYM5-RXM5 Comdty          US-Germany 10Y spread
CLM5-COM5 Comdty          WTI-Brent
```

`PX_LAST` returns leg1 − leg2.

## Options on futures

Append a strike + put/call code to the future ticker:

```
ESZ5C 5800 Index          ES Dec-25 5800 call
ESZ5P 5800 Index          ES Dec-25 5800 put

CLZ5C 80 Comdty           WTI Dec-25 80 call
TYZ5P 110 Comdty          TY Dec-25 110 put

GCG6C 2300 Comdty         Gold Feb-26 2300 call
```

Field set parallels equity options (see [options.md](options.md)).

## Volatility on the future

Same surface fields as equities:

```
30DAY_IMPVOL_100.0%MNY_DF
60DAY_IMPVOL_100.0%MNY_DF
... 90DAY, 180DAY, 360DAY
30DAY_IMPVOL_90.0%MNY_DF              # 10% OTM
30DAY_IMPVOL_110.0%MNY_DF             # 10% ITM (call) / 10% OTM (put)
30DAY_IMPVOL_25DELTA_RR
```

Plus the dedicated VIX-style indices:

```
VIX Index                 30d S&P 500 implied vol
V2X Index                 VSTOXX (Eurostoxx 50)
VHSI Index                HSI vol
VKOSPI Index              KOSPI vol
MOVE Index                Treasury vol
GVZ Index                 Gold vol
OVX Index                 Crude oil vol
```

## CFTC Commitment of Traders

```
COTSP Index                       speculative net length, all CFTC
CFTC NETSPEC <ticker>             field family on individual contracts
NET_NCMRC_POS                     non-commercial net position
COMM_LONG_POS, COMM_SHORT_POS,
NCOMM_LONG_POS, NCOMM_SHORT_POS,
NRPT_LONG_POS, NRPT_SHORT_POS,
COT_REPORT_DATE
```

Use overrides `COT_REPORT_DATE` for as-of-date snapshots.

## Common pitfalls

- **Generic ≠ continuous total return.** `CL1` is the front future,
  *not* a total-return series. Backtesting on `CL1` close-to-close
  mis-attributes the roll yield.
- **Two-digit year**: `Z5` is ambiguous (2015 or 2025). Use `Z25` to
  be safe in stored data, but `Z5` is fine for live front-month.
- **Settle vs last** for futures: prefer `PX_SETTLE` for daily total
  returns — `PX_LAST` can be a stale trade if the contract is illiquid
  at close.
- **Holiday gaps**: `nonTradingDayFillOption` doesn't always do the
  right thing for futures — set to `ACTIVE_DAYS_ONLY` and join calendars
  yourself if you're combining with equity data.
- **Multipliers change** (e.g. SOFR contract reform): always pin
  `FUT_VAL_PT` and `FUT_CONT_SIZE` from the same date as your prices.
