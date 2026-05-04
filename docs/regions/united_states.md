# United States

## Equities — exchange codes

| Code | Venue |
|---|---|
| `US` | US composite (default; consolidated tape) |
| `UN` | NYSE |
| `UQ` | NASDAQ |
| `UW` | NASDAQ National Market (Global Select) |
| `UA` | NYSE American (formerly AMEX) |
| `UR` | NYSE Arca |
| `UV` | OTC Bulletin Board / OTC Markets |
| `UF` | OTC Pink (Pink Sheets) |
| `UU` | NASDAQ Capital Market |
| `UD` | NASDAQ ADR |
| `UP` | NYSE National (formerly NSX) |
| `UB` | BATS |
| `US` | composite (most useful for research) |

Use `US` (composite) for research, the venue-specific code for execution
analysis or NBBO microstructure work.

## Equity indices

| Ticker | Index |
|---|---|
| `SPX Index` | S&P 500 (price) |
| `SPXT Index` | S&P 500 Total Return |
| `INDU Index` | Dow Jones Industrial Average |
| `CCMP Index` | NASDAQ Composite |
| `NDX Index` | NASDAQ-100 |
| `RTY Index` | Russell 2000 |
| `RAY Index` | Russell 3000 |
| `RIY Index` | Russell 1000 |
| `MID Index` | S&P 400 MidCap |
| `SML Index` | S&P 600 SmallCap |
| `SPLRC*` | S&P 500 sector indices (e.g. `S5INFT Index` = info tech) |
| `S5*` | S&P sector / sub-industry GICS indices |

Sector decomposition (S&P 500):

```
S5INFT Index   Information Technology
S5HLTH Index   Health Care
S5FINL Index   Financials
S5COND Index   Consumer Discretionary
S5CONS Index   Consumer Staples
S5INDU Index   Industrials
S5UTIL Index   Utilities
S5RLST Index   Real Estate
S5MATR Index   Materials
S5ENRS Index   Energy
S5TELS Index   Communication Services
```

## Equity microstructure conventions

- Trading hours: 9:30–16:00 ET (extended 4:00–9:30 pre, 16:00–20:00
  post). Bloomberg returns post/pre prints with `IS_EXT_HOURS=Y` in
  ticks if you ask for them via `includeNonPlottableEvents=True`.
- Settlement: T+1 since May 2024.
- Tick rules: SEC Rule 612 minimums (1 cent above $1, 1/100 cent
  below).
- Halts: type encoded in `MKTDATA_EVENT_TYPE` / condition codes.
- Auctions: opening `O`, closing `M` / `MOC`, halt `H`.

## Treasuries

```
T 4.625 02/15/35 Govt              actual issue (UST 10Y new active)
GT2 Govt, GT3 Govt, GT5 Govt, GT7 Govt, GT10 Govt, GT20 Govt, GT30 Govt
                                   on-the-run actives
H15T2Y Index ... H15T30Y Index     Fed H.15 daily yield (no settlement)
USGG10YR Index                     10Y benchmark yield (composite)
USYC2Y10 Index                     2y-10y curve (bps)
USYC2Y30 Index                     2y-30y
USGGT10Y Index                     10y TIPS yield
USGGBE10 Index                     10y breakeven inflation
TIPS LADDER                        TIPS strip via OTR / specific CUSIPs
```

T-bills:

```
B 0 ⅛ 12/12/25 Govt                Bloomberg ticker for a T-bill
USB1M Index ... USB1Y Index        secondary-market bill yields
USGG3M Index, USGG6M Index         actives
```

## Corporate bonds

Cash:

```
CDXIG Index                        CDX Investment Grade Index level
CDXHY Index                        CDX High Yield
LUACTRUU Index                     Bloomberg US Corporate Total Return
LUH9TRUU Index                     Bloomberg US Corp HY Total Return
LBUSTRUU Index                     Bloomberg US Aggregate Total Return
G0Q0 Index                         ICE BofA US Corporate
H0A0 Index                         ICE BofA US HY
LF98TRUU Index                     Bloomberg HY 100 Index
```

CDS:

```
CDX IG CDSI S42 5Y Corp            current series
CDX HY CDSI S42 5Y Corp
CDX EM CDSI S38 5Y Corp
```

## Mortgages (TBA)

```
FNCL 5.5 Mtge                      Fannie Mae conventional 30y, 5.5%
FNCL 6 Mtge, FNCL 6.5 Mtge
GNCL 5.5 Mtge                      Ginnie Mae 30y
FNCI 5.5 Mtge                      Fannie 15y
FNCT 5.5 Mtge                      Fannie 20y
GNCI 5.5 Mtge                      Ginnie 15y
MBSCURRENT Index                   on-the-run TBA aggregate
```

## Munis

Yellow key `Muni`. Address by CUSIP for specifics; bulk munis are
typically accessed via screens / indices:

```
LMBITR Index                       Bloomberg Muni Total Return
MAXIMA Index                       Muni AAA yield curve points
MMD Index                          MMD AAA yield (subscription)
```

## Money markets / short rates

```
SOFRRATE Index                     SOFR
FEDL01 Index                       Fed Effective rate
FDTR Index                         Fed funds target upper bound (FOMC)
FDTROVER Index                     IORB
SOFR1MO Index                      30d SOFR (compounded)
SOFR3MO Index                      90d SOFR (compounded)
RRPONTSY Index                     ON RRP take-up
EFFR Index                         Fed effective rate (alt)
USB1M Index, USB3M Index, USB6M Index    T-bill yields
```

## Swaps & OIS

```
USSO1 Curncy ... USSO30 Curncy     SOFR OIS
USSWAP1 Curncy ... USSWAP30 Curncy legacy LIBOR-based fixed/3M
EUBSC1 Curncy ... EUBSC10 Curncy   EUR/USD basis (bps)
USDOIS Curncy                      composite
```

## Futures (US)

| Class | Tickers |
|---|---|
| Equity-index | `ES1`, `MES1`, `NQ1`, `RTY1`, `YM1`, `VIX1` |
| Bond | `TU1`, `FV1`, `TY1`, `UXY1`, `US1`, `WN1` |
| Short rate | `SR3A` (SOFR), `FF1` (Fed Funds) |
| FX | `EC1`, `BP1`, `JY1`, `AD1`, `CD1`, `SF1` |
| Energy | `CL1`, `NG1`, `RB1`, `HO1` |
| Metals | `GC1`, `SI1`, `HG1`, `PL1`, `PA1` |
| Ags | `C 1`, `S 1`, `W 1`, `KC1`, `SB1`, `CT1`, `LH1`, `LC1` |

## US-specific data points & calendars

```
ECO_RELEASE_DT                     economic release date
ECO_RELEASE_TIME                   release time
USCABAL Index                      current account balance
NAPMPMI Index                      ISM Manufacturing PMI
NAPMNMI Index                      ISM Services PMI
USURTOT Index                      unemployment rate
CPI YOY Index                      CPI YoY headline
CPI XYOY Index                     CPI YoY core
PCE DEFY Index                     PCE deflator YoY
PCEC YOY Index                     core PCE YoY
GDP CYOY Index                     GDP YoY
NFP T Index                        non-farm payrolls
INJCJC Index                       initial jobless claims
USPHCI Index                       U Mich Consumer Sentiment
USRINDEX Index                     Conference Board CCI
RECMBR Index                       FRED-style recession indicator (constructed)
```

## Holidays / sessions

`CALENDAR_CODE` for US: `US` (NYSE/NYSE-Arca/NASDAQ); for futures
`CME` calendar; for bonds `SIFMA` (early closes on certain days).

```
CALENDAR_CODE                      "US" / "CME" / "SIFMA"
```

## Useful pre-built indices for research

```
SPX Index, SPXT Index             S&P 500 px / TR
RAY Index                          Russell 3000 (broad market)
USTRACK Index                      Bloomberg US Treasury TR
LBUSTRUU Index                     Bloomberg US Aggregate
BAML US HY (H0A0 Index)
USTM Index                         US 5-year breakeven
DXY Curncy                         Dollar Index
BBDXY Index                        Bloomberg Dollar Index
EFFRSV1Y Index                     1y Fed funds expectation (OIS-implied)
USYC2Y10 Index                     2y-10y Treasury slope
SOFR3M01YR Index                   1y forward SOFR (constructed)
```

## Common ID patterns

- US equity ISINs start with `US`. CUSIPs are 9-character. SEDOLs
  are 7-character (uniform global).
- US Treasury CUSIPs always start with `91282` (notes/bonds) or
  `912796` (bills) — useful for filtering bulk bond panels.
- ADRs identified via `ADR_UNDL_TICKER`.

## Pitfalls specific to US data

- **Composite vs venue**: `AAPL US Equity` consolidates all US trading;
  `AAPL UW Equity` is NASDAQ only. Volumes differ by an order of
  magnitude.
- **Adjusted close**: `PX_LAST` on `AAPL US Equity` is unadjusted.
  Use `TOT_RETURN_INDEX_GROSS_DVDS` for adjusted total-return series,
  or set `adjustmentSplit=True, adjustmentNormal=True` in the
  request.
- **US Treasury yield calculation**: Bloomberg uses ACT/ACT for
  notes/bonds, ACT/360 (banker's) for bills. `YLD_BANK_DISC` vs
  `YLD_MMKT_BOND_EQUIV` matters.
- **TIPS**: `INFLATION_INDEX_PUBLISH_DATE` controls indexed-principal
  reset. Fields on TIPS are real-yield by default.
- **Settlement**: equities T+1 (post May 2024); USTs T+1; corporates
  T+1; munis T+2.
