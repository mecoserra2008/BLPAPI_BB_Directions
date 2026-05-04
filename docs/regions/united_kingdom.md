# United Kingdom

## Equity exchange codes

| Code | Venue |
|---|---|
| `LN` | London Stock Exchange (default) |
| `LI` | LSE International Order Book (GDRs, Russian/EM names) |
| `LD` | Off-exchange |
| `EU` | Pan-European composite (when CBOE Europe trades the LN line) |
| `IX` | Cboe Europe (Chi-X / BATS) |

Use `LN` for UK domestic stocks. `LI` for the IOB (most ADRs and
foreign DRs trading in London).

## Indices

| Ticker | Index |
|---|---|
| `UKX Index` | FTSE 100 |
| `MCX Index` | FTSE 250 |
| `NMX Index` | FTSE 350 |
| `ASX Index` | FTSE All-Share (the broad index) |
| `AIM Index` | FTSE AIM All-Share |
| `FTNMX0001 Index` | FTSE 350 Oil & Gas (sector) |
| `RIY Index` | (US Russell 1000 — careful, easy to confuse) |
| `TXX Index` | FTSE 100 Total Return |
| `UKXSC Index` | UK 100 Spread Constituents |

## Sector decomposition (ICB-based for FTSE)

The FTSE family uses ICB classification, not GICS. Field is
`ICB_SECTOR_NAME`. For breakouts use FTSE-published indices like
`FTNMX*`.

## Gilts

Sovereign UK debt. Yellow key `Govt`.

```
T 4 ½ 06/07/34 Govt              treasury gilt (older "T" ticker family)
UKT 4 ½ 06/07/34 Govt            modern UK Treasury ticker
GTGBP2Y Govt, GTGBP5Y Govt, GTGBP10Y Govt, GTGBP30Y Govt
                                 active on-the-run benchmarks
GUKG10 Index                     UK 10y benchmark yield
GUKG2 Index, GUKG5 Index, GUKG30 Index
```

Index-linked gilts:

```
UKTI 0.125 03/22/34 Govt         Index-linked
GTGBII10Y Govt                   on-the-run linker
UKGGBE10 Index                   UK 10y breakeven inflation
UKGGT10Y Index                   10y real yield
```

## Corporate bonds (GBP)

```
ITRX MAIN CDSI S40 5Y Corp        iTraxx Main (pan-EU; UK names included)
LECCTREU Index                    Bloomberg EUR Aggregate Corp (broader)
LP01TRGB Index                    GBP Treasury TR
LP02TRGB Index                    GBP IG TR
LP04TRGB Index                    GBP HY TR
LF98TRGB Index                    GBP HY 100
G0BC Index                        ICE BofA Sterling Corp
HL00 Index                        ICE BofA Sterling HY
```

## Money market & short rates

```
SONIO/N Index                     SONIA (Sterling Overnight Index Average)
SONIO/N Index                     overnight
BOEAPM Index                      Bank of England Bank Rate (policy)
BP0001M Index ... BP0006M Index   BBA LIBOR (DEPRECATED post-2024)
LDNCASH Index                     UK Treasury Bill 1m
UKTBILLI Index                    UK 3m T-bill
```

Bank of England policy:

```
UKBRBASE Index                    Bank Rate
UKBRBASE Index                    Bank Rate (current level)
BOELP Index                       BOE QE balance
```

## Swaps & OIS

```
BPSO1 Curncy ... BPSO30 Curncy     SONIA OIS (post-LIBOR)
BPSWS1 Curncy ... BPSWS30 Curncy   Legacy GBP swaps (LIBOR-based)
BPSWIT1 Curncy ... BPSWIT30 Curncy GBP RPI inflation swaps
BPBSC1 Curncy ... BPBSC10 Curncy   GBP/USD basis (bps)
```

GBP swap conventions: post-LIBOR transition the **SONIA OIS** (`BPSO`)
is the benchmark. Pre-2022 use legacy `BPSWS`.

## FX

```
GBPUSD Curncy                     cable
EURGBP Curncy                     EUR/GBP cross
GBPJPY Curncy
GBPCHF Curncy
GBPSEK Curncy
GBPNOK Curncy
USDGBP Curncy                     inverse (rare; cable is the convention)

GBPUSDV1M Curncy                  ATM vol 1m
GBP1M Curncy                      forward points 1m
GBPUSD1M Curncy                   outright 1m
```

## Futures (UK)

| Class | Ticker |
|---|---|
| FTSE 100 | `Z 1 Index` (note the space) |
| FTSE 250 | `Z2 Index` (or `MCM1 Index`) |
| Gilt 10y | `G 1 Comdty` (note the space) |
| Short Sterling (DEPRECATED) | `L 1 Comdty` |
| SONIA 3m | `SO1 Comdty` |

## UK-specific economic data

```
UKRPCJYR Index                    UK CPI YoY
UKRPCH Index                      UK RPI
UKEUEMP Index                     ILO Unemployment Rate
UKHBR Index                       Bank Rate
UKGGAB Index                      UK Government 10y minus 2y
UKMPMI Index                      UK Manufacturing PMI
UKSPMI Index                      UK Services PMI
UKCSPI Index                      Construction PMI
UKRGAY Index                      UK Retail Sales YoY
UKAVE Index                       Average Earnings YoY
UKHPISG Index                     Halifax house price
GFKCC Index                       GfK consumer confidence
```

## ADRs / GDRs and dual listings

UK has a deep cross-listing market. Two patterns:

- **ADRs of UK companies** trade in NYC: `BCS US Equity` (Barclays
  ADR) → underlying is `BARC LN Equity`. Resolve with `ADR_UNDL_TICKER`.
- **Foreign GDRs in London** (IOB) trade with `LI` suffix. Most
  Russian / EM names had this format pre-2022 sanctions.
- **Dual primary listings**: `RIO LN Equity` and `RIO AT Equity` (Rio
  Tinto plc/Limited) both real, separate fundamentals — consolidate
  via `EQY_FUND_TICKER`.

## Trading sessions

- LSE 08:00–16:30 GMT/BST.
- Closing auction 16:30–16:35 with a price-discovery extension if
  imbalances trigger.
- LSE settlement T+1 since 2024.

## Pitfalls

- **Pence vs pounds**: UK equities are quoted in **pence** by default
  (e.g. `BARC LN Equity` PX_LAST = 250 means £2.50). Bloomberg fields
  often have `_GBP` vs `_GBp` distinctions. `CRNCY` returns `GBp` for
  pence.
- **Sterling LIBOR retired**: any series spanning Dec-2024 needs
  splicing to SONIA. `BPSO` for the new world.
- **Dividend treatment**: UK dividends are franked; net vs gross
  matters. `EQY_DVD_YLD_IND` is gross.
- **Stamp duty**: UK equities pay 0.5% stamp on purchases. Affects
  backtests of high-turnover strategies.
- **AIM vs Main**: AIM-listed micro-caps have lower data quality,
  intermittent BVAL, and may not appear in `INDX_MEMBERS` queries
  scoped to FTSE All-Share.
- **Legal-entity specific**: `BARC LN Equity` is Barclays plc, the
  holdco. Subsidiaries (e.g. Barclays Bank plc) appear under `Corp`
  for debt but not as `Equity`.
