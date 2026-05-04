# Europe (EU + EEA + Switzerland)

A single market officially, dozens of venues in practice. The pricing
source is the country/exchange code; the index family is usually
country-specific with a Eurostoxx pan-European overlay.

The UK has its own [page](united_kingdom.md).

## Country / venue codes for equities

| Code | Country / venue |
|---|---|
| `GR` | Germany — Xetra (default for German names) |
| `GY` | Germany — Frankfurt floor |
| `GH`, `GS`, `GM` | Hamburg / Stuttgart / Munich (regional) |
| `FP` | France — Euronext Paris |
| `NA` | Netherlands — Euronext Amsterdam |
| `BB` | Belgium — Euronext Brussels |
| `PL` | Portugal — Euronext Lisbon |
| `IM` | Italy — Borsa Italiana / Euronext Milan |
| `SM` | Spain — BME (Madrid) |
| `MM` | Spain alt (legacy) — beware overlap with Mexico's `MM` |
| `AT` | Austria — Wiener Börse |
| `IR` | Ireland — Euronext Dublin |
| `GA` | Greece — ATHEX |
| `PW` | Poland — Warsaw |
| `CP` | Czechia — Prague |
| `HB` | Hungary — Budapest |
| `RO` | Romania — Bucharest |
| `BU` | Bulgaria — Sofia |
| `SS` | Sweden — Stockholm (Nasdaq Nordic) |
| `DC` | Denmark — Copenhagen (Nasdaq Nordic) |
| `FH` | Finland — Helsinki (Nasdaq Nordic) |
| `OB`, `NO` | Norway — Oslo |
| `IS` | Iceland — Reykjavik |
| `SE` | Sweden alt (legacy SSE) |
| `SW` | Switzerland — SIX |
| `VX` | Switzerland — virt-x / older |
| `LX` | Luxembourg |
| `MT` | Malta |
| `CY` | Cyprus |
| `EU` | pan-European composite (multi-MTF, e.g. CBOE Europe) |
| `IX` | Cboe Europe (Chi-X / BATS) |
| `TQ` | Turquoise |

When you don't know the venue, **use the country code from the
issuer's primary listing**, e.g. EDP = `EDP PL Equity`, Santander =
`SAN SM Equity`, BMW = `BMW GR Equity`. For multi-listings prefer the
primary; cross-listings have lower liquidity in BBG data.

## Pan-European indices

| Ticker | Index |
|---|---|
| `SX5E Index` | Euro Stoxx 50 (price) |
| `SX5T Index` | Euro Stoxx 50 Total Return (gross) |
| `SX5R Index` | Euro Stoxx 50 Net Return |
| `SXXP Index` | Stoxx Europe 600 |
| `SXXR Index` | Stoxx Europe 600 Net Return |
| `SXXGR Index` | Stoxx Europe 600 Gross Return |
| `MXEU Index` | MSCI Europe |
| `MXEM Index` | MSCI EM (broader, but EU EM included) |
| `MXEF Index` | MSCI Emerging Markets |
| `STOXX50E Index` | Stoxx 50 (incl. Switzerland & UK, the "broad" 50) |
| `BE500 Index` | Bloomberg European 500 |
| `MXEU0PV Index` | MSCI Europe Value |
| `MXEU0PG Index` | MSCI Europe Growth |
| `MXEU0SC Index` | MSCI Europe Small Cap |

Sector decomposition (Stoxx 600 supersectors):

```
SXAP Index    Auto & Parts
SXKP Index    Banks
SXIP Index    Industrials
SXNP Index    Insurance
SXFP Index    Financial Services
SXTP Index    Telecom
SXEP Index    Energy
SX86P Index   Real Estate
SX6P Index    Utilities
SX4P Index    Chemicals
SXDP Index    Health Care
SX3P Index    Food & Beverage
SXOP Index    Oil & Gas
SX7P Index    Banks (alt)
```

## Country-specific equity indices

| Country | Index | Total return | Members |
|---|---|---|---|
| Germany | `DAX Index` | `DAXTR Index` (gross) | DAX-40 |
| Germany | `MDAX Index` | `MDAXTR Index` | MDAX 50 |
| France | `CAC Index` | `CACR Index` | CAC 40 |
| France | `SBF120 Index` |  | SBF 120 |
| Netherlands | `AEX Index` | `AEXNR Index` | AEX 25 |
| Netherlands | `AMX Index` |  | AMX (mid-cap) |
| Belgium | `BEL20 Index` | `BEL20NR Index` | BEL 20 |
| Italy | `FTSEMIB Index` |  | FTSE MIB |
| Italy | `ITSTAR Index` |  | FTSE Italia STAR |
| Spain | `IBEX Index` | `IBEXTR Index` | IBEX 35 |
| Portugal | `PSI20 Index` | `PSI20TR Index` | PSI 20 |
| Austria | `ATX Index` | `ATXTR Index` | ATX |
| Switzerland | `SMI Index` | `SMIC Index` | SMI 20 |
| Switzerland | `SLI Index` |  | SLI Swiss Leaders |
| Sweden | `OMX Index` |  | OMXS30 |
| Sweden | `OMXSPI Index` |  | All-share |
| Denmark | `KFX Index` | `OMXC25CAP Index` | OMXC25 |
| Norway | `OBX Index` | `OBXP Index` | OBX25 |
| Finland | `HEX25 Index` |  | OMX Helsinki 25 |
| Iceland | `ICEXI Index` |  | OMX Iceland |
| Greece | `ASE Index` |  | Athex Composite |
| Poland | `WIG20 Index` | `WIG Index` (broad) | WIG20 |
| Hungary | `BUX Index` |  | BUX |
| Czechia | `PX Index` |  | PX |
| Romania | `BET Index` |  | BET |
| Ireland | `ISEQ Index` |  | ISEQ Overall |
| Turkey | `XU100 Index` |  | BIST 100 |

Total-return index where price index has a `*TR` / `*NR` sibling — use
the total-return version for backtests.

## Government bonds (sovereign debt)

Generic on-the-run actives:

```
GTDEM2Y Govt, GTDEM5Y Govt, GTDEM10Y Govt, GTDEM30Y Govt   Germany (Bunds)
GTFRF2Y, GTFRF5Y, GTFRF10Y, GTFRF30Y Govt                  France (OATs)
GTITL10Y, GTITL30Y Govt                                    Italy (BTPs)
GTESP10Y Govt                                              Spain
GTPTE10Y Govt                                              Portugal
GTNLG10Y Govt                                              Netherlands
GTBEF10Y Govt                                              Belgium
GTGRD10Y Govt                                              Greece
GTATS10Y Govt                                              Austria
GTSEK10Y Govt                                              Sweden
GTNOK10Y Govt                                              Norway
GTDKK10Y Govt                                              Denmark
GTFIM10Y Govt                                              Finland
GTCHF10Y Govt                                              Switzerland
GTPLN10Y Govt                                              Poland
GTHUF10Y Govt                                              Hungary
GTCZK10Y Govt                                              Czechia
GTRON10Y Govt                                              Romania
```

Spread tickers (vs Bunds):

```
.GBSPDE10Y Index                   Germany 10y yield
.IBSPDE10Y Index                   IT-DE 10y spread
.SBSPDE10Y Index                   ES-DE 10y spread
.PBSPDE10Y Index                   PT-DE 10y spread
GTITL10YR Govt Index – GTDEM10Y Govt Index    custom (compute manually)
```

Sovereign indices (Bloomberg families):

```
SPGBE Index                         S&P Eurozone Sovereign Bond
LUACTRUU Index                      US Aggregate (for context)
LECPTREU Index                      Bloomberg Pan-European Aggregate
LP01TREU Index                      Bloomberg EUR Treasury
LECCTREU Index                      Bloomberg Euro Corporate
LP05TREU Index                      Bloomberg EUR Aggregate
```

## Corporate bonds (EUR)

```
ITRX MAIN CDSI S40 5Y Corp          iTraxx Main 5Y (IG)
ITRX XOVER CDSI S40 5Y Corp         iTraxx Crossover 5Y (HY)
ITRX SNRFIN CDSI S40 5Y Corp        Senior financials
ITRX SUBFIN CDSI S40 5Y Corp        Sub financials
LECCTREU Index                       Euro Corporate Total Return
LF98TREU Index                       Euro HY Total Return
LP06TREU Index                       Euro Corp IG (alt)
SPEUCT Index                         S&P Eurozone Corp
ER00 Index                           ICE BofA Euro Corporate
HE00 Index                           ICE BofA Euro HY
```

## Money market / short rates

```
ESTRON Index                         €STR overnight
EONIA Index                          (DEFUNCT — replaced by €STR Oct 2022)
EUR001M Index ... EUR012M Index      EURIBOR (1m – 12m)
EUR003M Index                        EURIBOR 3m (the benchmark)
EUSWE3M Curncy                       3m €STR OIS
USSWE3M Curncy                       (no — that's USD; just naming pattern)
```

ECB main rate decisions:

```
EURR002W Index                       ECB MRO
EUDRA Index                          ECB Deposit Facility Rate
EUDP Index                           Bank Lending Facility Rate
ECB depo via "ECB MAIN REFINANCING OPERATIONS" function
```

## Swaps (EUR)

See [swaps.md](../asset_classes/swaps.md). Quick reference:

```
EESWE1 Curncy ... EESWE30 Curncy     €STR OIS
EUSA1 Curncy ... EUSA30 Curncy       Legacy (vs 6M EURIBOR)
EUSW1 Curncy ... EUSW30 Curncy       Legacy (vs 3M EURIBOR)
EUBSC1 Curncy ... EUBSC30 Curncy     EUR/USD basis (bps over USD)
USSWITP*  Curncy                     inflation
EUSWIT*  Curncy                      EUR HICPx inflation swaps
```

## FX

```
EURUSD Curncy, GBPUSD Curncy
EURJPY Curncy, EURGBP Curncy, EURCHF Curncy
EURPLN Curncy, EURHUF Curncy, EURCZK Curncy, EURRON Curncy
EURTRY Curncy, EURNOK Curncy, EURSEK Curncy
EURDKK Curncy                         pegged via ERM-II
EURISK Curncy                         Iceland (deliverable but illiquid)
```

## Futures (Europe)

| Class | Ticker |
|---|---|
| Eurostoxx 50 | `VG1 Index` |
| DAX | `GX1 Index` |
| CAC | `CF1 Index` |
| AEX | `EO1 Index` |
| BEL 20 | `BEL1 Index` |
| FTSE MIB | `IB1 Index` |
| IBEX 35 | `IBE1 Index` |
| SMI | `SM1 Index` |
| OMX Stockholm | `OMX1 Index` |
| ATX | `ATX1 Index` |
| PSI 20 | `PSI1 Index` |
| Bunds 10y | `RX1 Comdty` |
| Bobl 5y | `OE1 Comdty` |
| Schatz 2y | `DU1 Comdty` |
| Buxl 30y | `UB1 Comdty` |
| BTPs 10y | `IK1 Comdty` |
| OATs 10y | `OAT1 Comdty` |
| €STR 3m | `EI1 Comdty` |
| EURIBOR 3m | `ER1 Comdty` |

## Eurozone economic data

```
GRGDPCYY Index                       Germany GDP YoY
GRZECURR Index                       ZEW current
GRZEW Index                          ZEW expectations
GRIFPBUS Index                       Ifo business climate
GRCP20YY Index                       Germany CPI YoY
EUR003M Index                        EURIBOR 3m
ECCPEMUY Index                       Euro Area CPI YoY
ECCPESTY Index                       Euro Area CPI Estimate YoY
EMUMUNF Index                        Manufacturing PMI Eurozone
EMUMSEC Index                        Services PMI Eurozone
EMUMCOM Index                        Composite PMI Eurozone
UMRTEMU Index                        Eurozone unemployment rate
ECINUS Index                         consumer confidence
ECMSEUR Index                        M3 money supply YoY
EUWAGE Index                         negotiated wage tracker
ECRPESEC Index                       ECB MRO history
```

## Country-specific (selection)

```
# France
FRGDPCYY Index, FRCPCYOY Index, FRPMICOM Index
# Italy
ITPRMINF Index, ITGSGS Index, ITPRWAOR Index
# Spain
SPCPI YoY Index, SPGSEM Index, SPECF Index
# Portugal
PTCPNICY Index, PTGDP Index, PTUNFR Index
```

## Trading sessions

- **Equities**: typically 09:00–17:30 CET (Xetra, Euronext, Borsa
  Italiana, BME). LSE 08:00–16:30 GMT/BST. Closing auction lasts
  3–5 minutes.
- **Bonds (cash)**: 08:00–17:30 CET; off-hours pricing via BVAL.
- **Futures (Eurex)**: extended ~01:00–22:00 CET on the main
  contracts.

## Eurozone settlement

Most cash equities and bonds settle T+1 since Q4 2024 (some venues
moved earlier). Bond reps still quote T+2 for intra-day calc — confirm
via `SETTLE_DT` field on the request.

## Pitfalls

- **Country code overlap**: `MM` is used by Mexico (LATAM) and was
  historically used for Spanish secondary boards. Always sanity-check
  via `COUNTRY_FULL_NAME` field.
- **Multiple listings**: Roche has two share classes traded in
  Switzerland, plus a US ADR. Use `EQY_FUND_TICKER` to consolidate.
- **DR vs primary**: many EM names are easier to access via European
  GDR (e.g. `LKOD LI Equity` for Lukoil). The fundamentals fields
  return the same values; only price/volume differ.
- **Currency mixing**: Stoxx 600 has GBP, CHF, NOK, SEK, DKK, EUR
  components. `bdh` with `currency='EUR'` re-currencies all of them
  for you.
- **Holidays**: pan-European calendar `EU` covers ECB holidays. For
  exchange-specific use the local code (`GR`, `FP`, `IM`, etc.).
- **EONIA → €STR**: anything pre-Oct-2022 in your panel uses EONIA;
  post that, €STR. Splice manually if you need a continuous series.
