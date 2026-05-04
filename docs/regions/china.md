# China & Hong Kong

China is fragmented into **four** equity markets sharing many
underlying issuers:

1. **A-shares** — Shanghai (`CH`) and Shenzhen (`CG`), CNY-denominated,
   onshore, capital-controlled.
2. **B-shares** — Shanghai (`C1`) and Shenzhen (`C2`), USD/HKD-quoted,
   foreign-investor (legacy, mostly illiquid).
3. **H-shares** — Hong Kong (`HK`), HKD-denominated. Many A-share
   issuers also list as H.
4. **Red chips / P chips** — HK-listed with Mainland operations.
5. **US ADRs** — sometimes the cleanest US-investor access (`BABA US`,
   `JD US`, etc.).

Hong Kong is also home to non-China issuers (e.g. AIA, HKEX itself).

## Exchange codes

| Code | Venue |
|---|---|
| `CH` | Shanghai Stock Exchange (A) |
| `CG` | Shenzhen Stock Exchange (A) |
| `C1` | Shanghai B (USD) |
| `C2` | Shenzhen B (HKD) |
| `HK` | Hong Kong (HKEX) |
| `C5` | Beijing Stock Exchange (BSE / former NEEQ) |
| `S1` | STAR Market (SSE Sci-Tech) |
| `S2` | ChiNext (Shenzhen) |
| `CN` | China composite |

Examples:

```
600519 CH Equity              Kweichow Moutai (Shanghai)
601318 CH Equity              Ping An (A-share)
000333 CG Equity              Midea (Shenzhen)
300750 CG Equity              CATL (ChiNext)
2318 HK Equity                Ping An (H-share)
941 HK Equity                 China Mobile
700 HK Equity                 Tencent
9988 HK Equity                Alibaba (HK)
3690 HK Equity                Meituan
1810 HK Equity                Xiaomi
1024 HK Equity                Kuaishou
6862 HK Equity                Haidilao

BABA US Equity                Alibaba ADR
JD US Equity                  JD.com ADR
PDD US Equity                 Pinduoduo
NIO US Equity                 NIO
BIDU US Equity                Baidu

# Stock Connect–accessible (most large A-shares):
600519 CH Equity              available via Northbound Connect
000858 CG Equity              Wuliangye (Connect)
```

## Indices

China A:

```
SHCOMP Index                  Shanghai Composite
SZCOMP Index                  Shenzhen Composite
SHSZ300 Index                 CSI 300 (Shanghai+Shenzhen blue chips)
SH50 Index                    SSE 50
SH180 Index                   SSE 180
ChiNext Index = `CNIE Index` or `399006 CG Equity`-equivalent index
SZSE100 Index                 Shenzhen 100
STAR50 Index                  STAR 50

# MSCI China A:
MXCNA Index                   MSCI China A
M2CN Index                    MSCI China All-Shares
MXCN Index                    MSCI China (offshore-eligible)
```

Hong Kong:

```
HSI Index                     Hang Seng Index
HSCEI Index                   HSCEI (H-shares index)
HSTECH Index                  Hang Seng Tech
HSCI Index                    Hang Seng Composite
HSMSCI Index                  Hang Seng Mid-Cap
HSF Index                     Hang Seng Finance
HSP Index                     Hang Seng Property
HSU Index                     Hang Seng Utility
HSC Index                     Hang Seng Commerce
```

Stock Connect baskets:

```
HSCEI Index                   underlying for HSCEI futures (HC1)
HSI Index                     HSI futures (HI1)
SHSZ300 Index                 CSI 300 futures (IF1 traded in CN)
```

## Bonds

Sovereign:

```
GTCNY10Y Govt                 China 10y on-the-run
GTCNY5Y Govt
GTCNY1Y Govt
GTHKD10Y Govt                 HK govt bond 10y
GTHKD5Y Govt
GCNY10YR Index                CGB 10y benchmark yield
```

China onshore corporates:

```
ITRX ASIAXJ CDSI S40 5Y Corp  iTraxx Asia ex-Japan
CHINA CDS USD SR 5Y D14 Corp  China sovereign CDS
HK CDS USD SR 5Y D14 Corp     HK sovereign CDS
```

Onshore corp bonds use 6-digit ID + market suffix:

```
019547 CH Corp                generic format
```

Most foreign access uses Bond Connect, addressed normally via
ISIN/CUSIP.

## Money markets / short rates

Onshore CNY:

```
SHIBORON Index                Shibor overnight
SHIBOR1M Index, SHIBOR3M Index
DR007 Index                   7d depo repo rate (key onshore funding)
DR001 Index                   ON depo repo
CHBM7D Index                  PBoC 7d reverse repo
PBOCYHC Index                 PBoC LPR 1y
PBOC5Y Index                  PBoC LPR 5y
LPR1Y Index                   LPR 1y (alt)
```

Offshore CNH:

```
HIBORON Index                 Hibor overnight
CNHHIBOR Index                CNH HIBOR (TMA fix)
CNH1M Curncy                  1m CNH forward points
```

## FX

```
USDCNY Curncy                 Onshore yuan (PBoC fix-driven, +/- 2% band)
USDCNH Curncy                 Offshore yuan (HK)
EURCNY Curncy, EURCNH Curncy
USDHKD Curncy                 Pegged 7.75–7.85
USDCNY1M Curncy               NDF (CFETS fix)
USDCNH1M Curncy               Deliverable forward (HK market)
```

PBoC fix:

```
PBOCCNY Index                 PBoC USD/CNY mid-point fix (daily 09:15 SGT)
CFETS Index                   CFETS RMB Index (trade-weighted)
```

> CNY ≠ CNH. CNY is onshore (capital-controlled, PBoC-managed). CNH is
> the offshore market. Forwards/NDFs work differently. Most foreign
> investors use CNH.

## Swaps

```
CNYNDS1 Curncy ... CNYNDS10 Curncy   Onshore CNY IRS (NDIRS)
CNHNDS1 Curncy ...                   Offshore CNH IRS
CCS curve via XCCY: CNH/USD basis tickers (rare programmatically)
```

## Futures (China & HK)

| Class | Ticker | Exchange |
|---|---|---|
| HSI | `HI1 Index` | HKEX |
| HSCEI | `HC1 Index` | HKEX |
| HSTECH | `HTI1 Index` | HKEX |
| China A50 (SGX) | `XU1 Index` | SGX |
| CSI 300 (CN) | `IF1 Index` | CFFEX (onshore) |
| SSE 50 (CN) | `IH1 Index` | CFFEX |
| CSI 500 | `IC1 Index` | CFFEX |
| 10Y CGB | `T 1 Comdty` (note space) | CFFEX |
| Iron ore | `SCO1 Comdty` | DCE / SGX |
| Coking coal | (DCE locally) | |

USD-listed China futures (offshore-accessible):

```
XU1 Index                     SGX China A50
HSI futures HI1, HC1
ICE Iron Ore (SGX) SCO1 Comdty
```

## Stock Connect specifics

Field flags for Connect eligibility:

```
HKEX_NORTHBOUND_ELIGIBLE       Y/N — Mainland stock open to HK investors
HKEX_SOUTHBOUND_ELIGIBLE       Y/N — HK stock open to Mainland investors
HKEX_NORTHBOUND_HOLDINGS       holdings of Mainland investors in HK names
SHSC_FLOW                      Shanghai-HK Connect daily net flow
SZSC_FLOW                      Shenzhen-HK Connect daily net flow
```

## Macro / economic data

```
CHCPIYOY Index                China CPI YoY
CHEFPCY Index                 PPI YoY
CHGDPYOY Index                Real GDP YoY
CHIRGI Index                  Industrial production
CHFXGOLD Index                FX reserves
CHM2 Index                    M2 YoY
CHCAIXPM Index                Caixin Manufacturing PMI
CHPMINDX Index                NBS Manufacturing PMI
CHPMSVC Index                 NBS Services PMI
HKCPIYOY Index                HK CPI YoY
HKEXBAL Index                 HK trade balance
```

## Hong Kong specifics

| Field / ticker | Note |
|---|---|
| HKEX trading hours | 09:30–12:00, 13:00–16:00 HKT |
| Auctions | Pre-open 09:00–09:30, closing 16:00–16:10 |
| Settlement | T+2 (vs A-share T+1, T+0 trading) |
| Stamp duty | 0.13% (paid on both sides) |
| Lot sizes | Variable (often 100/500/1000) — check `LOT_SIZE` |

## A-share specifics

- Trading: 09:30–11:30, 13:00–15:00 CST.
- T+0 trading, **T+1 settlement** for cash-equivalent transactions.
- Daily price limits: ±10% (regular A), ±20% (ChiNext, STAR), ±30%
  (delistable / ST). Field: `LIMIT_UP`, `LIMIT_DOWN`.
- Lot size: 100 shares.
- Suspensions are common — check `MARKET_STATUS`.

## Pitfalls

- **Same issuer, multiple identifiers**: Ping An has `601318 CH Equity`
  (A-share), `2318 HK Equity` (H-share), `PNGAY US Equity` (ADR).
  Different prices, different liquidity, *same* fundamentals.
  Use `EQY_FUND_TICKER` to consolidate.
- **CNY vs CNH**: addressing FX as `USDCNY` vs `USDCNH` gives
  *different* prices and *different* curves. Choose deliberately.
- **Connect flow lag**: `SHSC_FLOW` and `SZSC_FLOW` are reported
  end-of-day with a 1–2 hour lag. Don't trade on intraday Connect
  flow.
- **Onshore data lag**: many onshore A-share fundamentals lag 1–2 days
  vs HK reporting. Don't compare a same-day H-share fundamental
  with the A-share equivalent.
- **Currency for indices**: `SHCOMP` is CNY-denominated;
  `HSI Index` is HKD; `MXCN Index` is USD (gross-of-tax). Ensure
  consistent currency when stacking.
- **STAR50 / ChiNext index identifiers** changed names in 2020 —
  stale code may reference defunct tickers.
- **HSI 2022 restructuring**: HSI added 33 → 80 components over
  2021–2024. Use `INDX_MEMBERS_HIST` for point-in-time membership.
