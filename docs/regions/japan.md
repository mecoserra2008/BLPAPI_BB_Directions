# Japan

## Equity exchange codes

| Code | Venue |
|---|---|
| `JT` | Tokyo Stock Exchange (TSE) — default |
| `JE` | Osaka (Osaka Exchange — derivatives + Nikkei 225 futures) |
| `JN` | Nagoya |
| `JS` | Sapporo |
| `JF` | Fukuoka |
| `JP` | Japan composite (multi-venue) |
| `JQ` | JASDAQ (now part of TSE Growth) |
| `JU` | TSE Mothers (now Growth) |

Tickers are **4-digit numeric**:

```
7203 JT Equity                Toyota
6758 JT Equity                Sony
9432 JT Equity                NTT
6098 JT Equity                Recruit
9984 JT Equity                Softbank Group
8035 JT Equity                Tokyo Electron
6594 JT Equity                Nidec
7974 JT Equity                Nintendo
8306 JT Equity                Mitsubishi UFJ
9433 JT Equity                KDDI
4519 JT Equity                Chugai Pharmaceutical
4063 JT Equity                Shin-Etsu Chemical
9101 JT Equity                NYK Line
```

## Indices

| Ticker | Index |
|---|---|
| `NKY Index` | Nikkei 225 (price) |
| `NKYTR Index` | Nikkei 225 Total Return |
| `TPX Index` | Topix (price) |
| `TPXDDVD Index` | Topix Total Return |
| `TPX500 Index` | Topix 500 |
| `TPXSC Index` | Topix Small |
| `MOSE2 Index` | Mothers Composite (legacy) |
| `JN225 Index` | Nikkei 225 alt |
| `NKM Index` | Nikkei Mid Cap |
| `NKS Index` | Nikkei 300 (legacy) |
| `MXJP Index` | MSCI Japan |
| `MXJPSC Index` | MSCI Japan Small Cap |

Sector decomposition (Topix sectors, 33 industries):

```
TPXBANK Index                Banks
TPXAUTO Index                Auto
TPXELEC Index                Electric Appliances
TPXMACH Index                Machinery
TPXCHEM Index                Chemicals
TPXOTHER Index               Other
... (33 total in TSE classification)
```

Topix Sector ETF mapping is via `TSE_SECTOR_CODE` field.

## Government bonds (JGBs)

```
JB 0.6 03/20/35 Govt           specific JGB issue
GTJPY10Y Govt                  10y benchmark
GTJPY2Y, GTJPY5Y, GTJPY20Y, GTJPY30Y, GTJPY40Y Govt
GJGB10 Index                   composite 10y yield
JGBS10 Index                   JGB simple 10y
```

JGBi (inflation-linked):

```
JBII Govt                      generic linker
JPGGTBE10 Index                10y breakeven
GTJGBI10Y Govt                 active linker
```

## Money market / short rates

```
TONAR Index                    TONA (overnight call)
JBOJP Index                    BOJ policy rate (current)
JY0001M Index                  TIBOR 1m
JY0003M Index                  TIBOR 3m
MUTKCALM Index                 Tokyo Mutual Call Rate
JPY3M Curncy                   3m JPY forward points
```

## Swaps & OIS

```
JYSO1 Curncy ... JYSO30 Curncy   TONA OIS (post-LIBOR)
JYSWAP1 Curncy ... JYSWAP30 Curncy  Legacy
JYBSC1 Curncy ... JYBSC30 Curncy   JPY/USD cross-currency basis
JYSWIT1 Curncy ... JYSWIT30 Curncy JPY CPI inflation swaps
```

## FX

```
USDJPY Curncy
EURJPY Curncy
GBPJPY Curncy
AUDJPY Curncy

USDJPYV1M Curncy                  ATM vol 1m
USDJPY1M Curncy                   1m forward outright
JPY1M Curncy                      1m forward points (JPY-side)
```

## Futures (Japan)

| Class | Ticker | Exchange |
|---|---|---|
| Nikkei 225 | `NK1 Index` | OSE |
| Nikkei 225 mini | `NM1 Index` | OSE |
| Nikkei 225 (SGX) | `NXA Index` | SGX |
| Topix | `TP1 Index` | OSE |
| Topix mini | `TPM1 Index` | OSE |
| JGB 10y | `JB1 Comdty` | OSE |
| JGB 5y | `JBM1 Comdty` | OSE |
| TONA 3m | `JY1 Comdty` | TFX |
| Yen futures (CME) | `JY1 Curncy` | CME |

> **The same `JY1` ticker means different things under different yellow
> keys.** `JY1 Comdty` = TONA short-rate future. `JY1 Curncy` = CME
> JPY/USD future. Be deliberate with the yellow key.

## Japan-specific economic data

```
JNCPIYOY Index                  Japan CPI YoY (national)
JCCPIYOY Index                  Japan Core CPI (ex-fresh food)
JNTGDP Index                    Japan GDP YoY
JNUE Index                      Unemployment rate
JNETLALR Index                  Labor cash earnings YoY
JNHCMEDM Index                  Tankan large manufacturers
JNHCMEDS Index                  Tankan large non-manufacturers
JNTBALEN Index                  Trade balance
JCBOJBP Index                   BOJ policy balance
BOJDTR Index                    BOJ depo rate
JNMA Index                      Manufacturing PMI
JNSA Index                      Services PMI
```

## TSE-specific fields

```
JCN_NUM                          legal entity number (Japan)
JFP_TICKER                       JapanFP ticker
TSE_INDUSTRY_CODE                33-sector code
TSE_INDUSTRY_NAME                Japanese sector name (Japanese in some locales)
TSE_TYPE                         Prime / Standard / Growth (post 2022 reclass)
TSE_SECTION                      old First/Second/Mothers/JASDAQ
DOMICILE_CODE                    JP
```

## Trading sessions

- TSE morning: 09:00–11:30 JST
- TSE afternoon: 12:30–15:00 JST
- OSE (futures): 16:30–06:00 JST overnight + 08:45–15:15 day
- Closing auction at 15:00; opening auction at 09:00

Settlement: T+1 (since 2019).

## Cross-listings

- US ADRs: `TM US Equity` (Toyota ADR) → underlying `7203 JT Equity`.
  Use `ADR_RATIO` to convert (TM ADR = 10 underlying shares).
- Tokyo PRO Market: foreign listings, low volume.
- HK Connect (Stock Connect Tokyo) — limited.

## Mutual funds & ETFs

```
1306 JT Equity                  TOPIX ETF (Nomura NEXT FUNDS)
1308 JT Equity                  Nikkei 225 ETF (Nomura)
1330 JT Equity                  Nikkei 225 ETF (Daiwa)
1321 JT Equity                  Nikkei 225 ETF (NEXT FUNDS)
1320 JT Equity                  Nikkei 225 ETF (Daiwa)
2516 JT Equity                  Topix Banks ETF
1546 JT Equity                  Dow Industrial ETF (Tokyo-listed)
1545 JT Equity                  NASDAQ-100 ETF
1655 JT Equity                  S&P 500 ETF
```

## Pitfalls

- **Numeric tickers padded to 4 digits**: `7203` not `7.203`. Some
  newer listings use 5 digits (Mothers/Growth). Always confirm via
  `DES <GO>`.
- **TSE 2022 restructuring**: First/Second sections + Mothers + JASDAQ
  consolidated into Prime / Standard / Growth. Pre-2022 panels use
  `TSE_SECTION`; post-2022 use `TSE_TYPE`.
- **Adjustment factors for splits**: Japan-listed companies do
  large stock splits (1-for-3, 1-for-10). Always set
  `adjustmentSplit=True` for backtests.
- **Currency**: most fields in JPY. `CUR_MKT_CAP` for Japanese names
  is in millions (¥M) by default — check `CUR_MKT_CAP_UNITS`.
- **TONA OIS history**: thin pre-2018, before TONA reform. For
  pre-2018 USD/JPY basis use the legacy `JYSO`/`JYSWAP` blend.
- **TSE Prime market reclass**: some former "First Section" names
  were dropped. Membership of `NKY Index` and `TPX Index` reshuffled
  in 2022 — backtests should respect `INDX_MEMBERS_HIST`.
