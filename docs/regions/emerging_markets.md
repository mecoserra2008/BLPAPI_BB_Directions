# Emerging Markets (LATAM, EM-Asia ex-China, EM-EMEA)

A reference for tickers, indices and curves outside DM. China is on
its [own page](china.md); UK, Japan, US, Europe similarly.

## Country / venue codes

| Code | Country | Notes |
|---|---|---|
| `BZ` | Brazil — B3 (São Paulo) | |
| `MM` / `MX` / `MF` | Mexico — Bolsa Mexicana de Valores | `MM` is most common |
| `AR` | Argentina — BYMA | |
| `CI` / `CC` | Chile — Santiago | |
| `CB` | Colombia — BVC | |
| `PE` | Peru — Lima | |
| `VE` | Venezuela | |
| `UY` | Uruguay | |
| `KS` | South Korea — KOSPI | |
| `KQ` | South Korea — KOSDAQ | |
| `TT` | Taiwan — TWSE | |
| `IN` | India — NSE | |
| `IS` | India — BSE | |
| `MK` | Malaysia — Bursa | |
| `SP` | Singapore — SGX | |
| `TB` | Thailand — SET | |
| `PM` | Philippines — PSE | |
| `IJ` | Indonesia — IDX | |
| `VN` | Vietnam — HOSE / HNX | |
| `PA` | Pakistan — PSX | |
| `BD` | Bangladesh — DSE | |
| `LK` | Sri Lanka — CSE | |
| `SJ` | South Africa — JSE | |
| `EY` | Egypt — EGX | |
| `NL` | Nigeria — NGX | |
| `TI` | Turkey — Borsa Istanbul | |
| `RX` | Russia — MOEX (post-2022 sanctions: limited) | |
| `KZ` | Kazakhstan — KASE | |
| `UZ` | Uzbekistan | |
| `IT` | Israel — TASE | |
| `QD` | Qatar — QE | |
| `UH` | UAE — ADX | |
| `DH` | UAE — DFM | |
| `AB` | Saudi Arabia — Tadawul | |
| `KK` | Kuwait — Boursa Kuwait | |
| `BI` | Bahrain | |
| `OM` | Oman | |

## Top names by region

### LATAM

```
# Brazil (B3, BRL)
PETR4 BZ Equity                Petrobras (PN preferred)
PETR3 BZ Equity                Petrobras (ON ordinary)
VALE3 BZ Equity                Vale
ITUB4 BZ Equity                Itaú Unibanco
BBDC4 BZ Equity                Bradesco PN
ABEV3 BZ Equity                Ambev
WEGE3 BZ Equity                WEG
B3SA3 BZ Equity                B3 (the exchange)
RENT3 BZ Equity                Localiza
RAIZ4 BZ Equity                Raízen
PRIO3 BZ Equity                PetroRio
RDOR3 BZ Equity                Rede D'Or
HAPV3 BZ Equity                Hapvida

# Mexico (BMV, MXN)
WALMEX* MM Equity              Walmex (multiple classes)
AMXL MM Equity                 América Móvil L
GFNORTEO MM Equity             Banorte
FEMSAUBD MM Equity             FEMSA UBD
CEMEXCPO MM Equity             CEMEX CPO
GMEXICOB MM Equity             Grupo México B
GAPB MM Equity                 GAP B (airports)
OMAB MM Equity                 OMA B (airports)
ASURB MM Equity                ASUR B (airports)
KOFUBL MM Equity               Coca-Cola FEMSA UBL
TLEVISACPO MM Equity           Televisa CPO

# Chile (CLP)
SQM/B CI Equity                Sociedad Química y Minera (B)
COPEC CI Equity                Empresas Copec
ENELCHIL CI Equity             Enel Chile
FALABELLA CI Equity            Falabella
CMPC CI Equity                 CMPC

# Argentina (ARS, but most names also have NY ADR)
GGAL AR Equity                 Grupo Galicia
YPFD AR Equity                 YPF
PAMP AR Equity                 Pampa Energía
TGSU2 AR Equity                Transportadora Gas Sur

# ADRs of LATAM (USD-quoted, easier for foreign access):
PBR US Equity                  Petrobras ADR
VALE US Equity                 Vale ADR
ITUB US Equity                 Itaú ADR
ABEV US Equity                 Ambev ADR
AMX US Equity                  AMX ADR
GGAL US Equity                 Galicia ADR
YPF US Equity                  YPF ADR

# Colombia
ECOPETL CB Equity              Ecopetrol
GRUPOAVAL CB Equity            Aval
ISAGEN CB Equity               (delisted)

# Peru
CREDITC1 PE Equity             Credicorp
BAP US Equity                  Credicorp ADR
```

### EM Asia (ex-China)

```
# Korea (KRW)
005930 KS Equity               Samsung Electronics
000660 KS Equity               SK Hynix
035420 KS Equity               Naver
035720 KS Equity               Kakao
005380 KS Equity               Hyundai Motor
051910 KS Equity               LG Chem
207940 KS Equity               Samsung Biologics
006400 KS Equity               Samsung SDI
068270 KS Equity               Celltrion

# Taiwan (TWD)
2330 TT Equity                 TSMC
2317 TT Equity                 Foxconn (Hon Hai)
2454 TT Equity                 MediaTek
2308 TT Equity                 Delta Electronics
3008 TT Equity                 Largan Precision

# India (INR)
RELIANCE IN Equity             Reliance
TCS IN Equity                  TCS
INFY IN Equity                 Infosys
HDFCBANK IN Equity             HDFC Bank
ICICIBC IN Equity              ICICI Bank
KMB IN Equity                  Kotak Mahindra
MARUTI IN Equity               Maruti Suzuki

# Indonesia (IDR)
BBCA IJ Equity                 Bank Central Asia
BBRI IJ Equity                 BRI
TLKM IJ Equity                 Telkom Indonesia
ASII IJ Equity                 Astra International

# Thailand (THB)
PTT TB Equity                  PTT
KBANK TB Equity                Kasikornbank
CPALL TB Equity                CP All
ADVANC TB Equity               Advanced Info

# Singapore (SGD)
DBS SP Equity                  DBS Bank
OCBC SP Equity                 OCBC
UOB SP Equity                  UOB

# Malaysia (MYR)
MAYBANK MK Equity              Maybank
CIMB MK Equity                 CIMB
TENAGA MK Equity               Tenaga Nasional

# Philippines (PHP)
SM PM Equity                   SM Investments
ALI PM Equity                  Ayala Land
BPI PM Equity                  Bank of the PI

# Vietnam (VND)
VIC VN Equity                  Vingroup
VHM VN Equity                  Vinhomes
HPG VN Equity                  Hoa Phat
```

### EM EMEA

```
# South Africa (ZAR)
NPN SJ Equity                  Naspers
PRX SJ Equity                  Prosus
FSR SJ Equity                  FirstRand
MNP SJ Equity                  Mondi (also LN dual)
ANG SJ Equity                  AngloGold Ashanti
CFR SJ Equity                  Richemont (also SW)
SOL SJ Equity                  Sasol
SBK SJ Equity                  Standard Bank

# Turkey (TRY)
THYAO TI Equity                Türk Hava Yolları
GARAN TI Equity                Garanti BBVA
AKBNK TI Equity                Akbank
KCHOL TI Equity                Koç Holding
ASELS TI Equity                Aselsan
EREGL TI Equity                Erdemir
SAHOL TI Equity                Sabancı Holding
BIMAS TI Equity                BİM
TUPRS TI Equity                Tüpraş

# Saudi (Tadawul, SAR)
2222 AB Equity                 Saudi Aramco
1120 AB Equity                 Al Rajhi Bank
2380 AB Equity                 Petrochem
2010 AB Equity                 SABIC

# UAE (AED)
EMIRATESNBD UH Equity          Emirates NBD (ADX)
EMAAR DH Equity                Emaar (DFM)

# Egypt (EGP)
COMI EY Equity                 CIB
EAST EY Equity                 Eastern Tobacco
```

## Indices

### LATAM

```
IBOV Index                     Brazil Bovespa
IBX Index                      Brazil IBrX-100
MEXBOL Index                   Mexico IPC
MERVAL Index                   Argentina Merval
IPSA Index                     Chile IPSA
COLCAP Index                   Colombia COLCAP
BVL Index                      Peru BVL
MXLA Index                     MSCI Latin America
MXBR Index                     MSCI Brazil
MXMX Index                     MSCI Mexico
```

### EM Asia

```
KOSPI Index                    Korea KOSPI
KOSPI2 Index                   KOSPI 200
KOSDAQ Index                   KOSDAQ
TWSE Index                     Taiwan Weighted
NIFTY Index                    India NIFTY 50
SENSEX Index                   India BSE Sensex
JCI Index                      Indonesia JCI
SET Index                      Thailand SET
SETIDX Index                   alt
STI Index                      Singapore Straits Times
KLCI Index                     Malaysia KLCI / FBM-KLCI
PCOMP Index                    Philippines PSEi
VNINDEX Index                  Vietnam VN-Index
HNX Index                      Vietnam HNX

MXASJ Index                    MSCI Asia ex-Japan
MXEFAS Index                   MSCI EM Asia
```

### EM EMEA

```
JALSH Index                    JSE All-Share
TOP40 Index                    JSE Top 40 (FTSE/JSE)
XU100 Index                    Turkey BIST 100
XU030 Index                    BIST 30
TASI Index                     Saudi Tadawul
DFMGI Index                    Dubai DFM
ADSMI Index                    Abu Dhabi
QE Index                       Qatar
EGX30 Index                    Egypt EGX 30
NSEINDX Index                  Nigeria NSE All-Share
```

### Broad

```
MXEF Index                     MSCI Emerging Markets
MXEFTR Index                   MSCI EM Total Return Net
MXEM Index                     MSCI EM (alt)
MXFM Index                     MSCI Frontier Markets
EMB US Equity                  iShares JPM EM USD bonds
EEM US Equity                  iShares MSCI EM
VWO US Equity                  Vanguard MSCI EM
EMHY US Equity                 EM HY USD
LEMBTRUU Index                 Bloomberg EM USD Bond TR
EMUSTRUU Index                 Bloomberg EM USD Aggregate TR
JPEIDIVR Index                 EMBI Global Diversified
JCEMCM Index                   CEMBI Composite
```

## Sovereign / quasi-sovereign bonds

Major EM sovereign benchmarks:

```
GTBRL10Y Govt                  Brazil 10y BRL
GTUSDBRL10YR Govt              Brazil USD-denominated 10y
GTMXN10Y Govt                  Mexico 10y MXN
GTUSDMXN10Y Govt               Mexico USD 10y
GTCOP10Y Govt                  Colombia 10y COP
GTCLP10Y Govt                  Chile 10y CLP
GTPEN10Y Govt                  Peru 10y PEN
GTKRW10Y Govt                  Korea 10y
GTINR10Y Govt                  India 10y
GTIDR10Y Govt                  Indonesia 10y
GTPHP10Y Govt                  Philippines
GTTHB10Y Govt                  Thailand
GTMYR10Y Govt                  Malaysia
GTZAR10Y Govt                  South Africa
GTTRY10Y Govt                  Turkey
GTRUB10Y Govt                  Russia (limited post-2022)
GTSAR10Y Govt                  Saudi
GTPLN10Y Govt                  Poland
GTHUF10Y Govt                  Hungary
```

EMBI / CEMBI tickers (USD-denominated):

```
JPEGCOMP Index                 EMBI Global Composite
JPEIDIVR Index                 EMBI Global Diversified (the standard benchmark)
JCEMCM Index                   CEMBI Composite (corporates)
```

## CDS

```
BRAZIL CDS USD SR 5Y D14 Corp
MEX CDS USD SR 5Y D14 Corp
COLOM CDS USD SR 5Y D14 Corp
PERU CDS USD SR 5Y D14 Corp
CHILE CDS USD SR 5Y D14 Corp

INDON CDS USD SR 5Y D14 Corp     Indonesia
PHILIP CDS USD SR 5Y D14 Corp
SOAF CDS USD SR 5Y D14 Corp     South Africa
TURKEY CDS USD SR 5Y D14 Corp
ISRAEL CDS USD SR 5Y D14 Corp
SAUDI CDS USD SR 5Y D14 Corp
RUSSIA CDS USD SR 5Y D14 Corp   (limited post-2022)
```

## FX

```
USDBRL Curncy, USDMXN Curncy, USDARS Curncy, USDCLP Curncy, USDCOP Curncy, USDPEN Curncy
USDKRW Curncy, USDINR Curncy, USDIDR Curncy, USDMYR Curncy, USDPHP Curncy, USDTHB Curncy, USDTWD Curncy, USDVND Curncy
USDZAR Curncy, USDTRY Curncy, USDPLN Curncy, USDCZK Curncy, USDHUF Curncy, USDRON Curncy, USDRUB Curncy
USDILS Curncy, USDAED Curncy, USDSAR Curncy, USDQAR Curncy, USDEGP Curncy, USDNGN Curncy
```

NDF tenors: append `1M`, `3M`, `6M`, `1Y` (see
[currencies.md](../asset_classes/currencies.md)).

```
USDKRW3M Curncy, USDINR3M Curncy, USDBRL3M Curncy, ...
```

Implied yield curve from NDFs:

```
IMPL_YIELD_NDF_PCT             field
```

## Money markets / short rates

```
BZSTSETA Index                 Brazil Selic target
BRDIIN Index                   Brazil DI 1d
INDOIN Index                   Indonesia BI 7d reverse repo rate
MXTSETA Index                  Mexico target rate (Banxico)
COLCAP Index                   (this is index, not rate; rate = COREPO Index)
COREPO Index                   Colombia repo
TBSO1M Index                   Turkey 1m
RBIRPO Index                   India RBI repo
SARPRPO Index                  Saudi repo
SAFOPRR Index                  South Africa SARB repo
CZ001 Index                    Czechia 2w repo
HUFNB Index                    Hungary NBH base
PLZNREF Index                  Poland NBP reference rate
```

## EM swaps & local IRS

```
BRLNDS5 Curncy, BRLNDS10 Curncy        Brazil DI swap
MXNNDS5 Curncy, MXNNDS10 Curncy        Mexico TIIE swap
COPNDS5 Curncy                          Colombia
CLPNDS5 Curncy                          Chile camara
KRWNDS5 Curncy, KRWNDS10 Curncy        Korea KRW IRS
INRNDS5 Curncy                          India MIBOR-OIS
ZARNDS5 Curncy                          ZAR JIBAR swap
TRYNDS5 Curncy                          Turkey IRS
PLN6 Curncy / PLNNDS5 Curncy            Poland WIBOR / OIS
HUFNDS5 Curncy
RONNDS5 Curncy
```

For Brazil specifically, **DI futures** are the primary curve (more
liquid than swaps): `ODF1 Comdty`, `ODFF26 Comdty` (Jan-26).

## EM equity-index futures

```
WIN1 Index                     Brazil mini-Bovespa (CME-traded equiv: IBV1)
ESCJ1 Index                    Mexico IPC mini
KM1 Index                      KOSPI 200 (KRX)
SGX TWN A50 / Nifty / etc.     SGX cross-listings
```

## Pitfalls specific to EM

- **Liquidity windows**: many EM names have meaningful trading volume
  only around the local close. Use `PX_VOLUME_AVG_30D` to filter.
- **ADR pricing vs local**: `PBR US Equity` (Petrobras ADR) tracks
  but doesn't equal `PETR4 BZ Equity` × FX × ratio. ADR ratio (often
  1:2 or 2:1) lives in `ADR_RATIO`.
- **Currency confusion**: prices in local currency, market cap
  sometimes in USD. Always verify with `EQY_FUND_CRNCY` and
  `CRNCY`.
- **EM CDS quote convention**: par-spread for sovereigns; check
  `CDS_QUOTE_TYPE` on issuer-specific CDS.
- **Capital controls** affect FX forwards: Brazil, Argentina,
  Indonesia, Korea, India, Egypt, Nigeria, Vietnam, Philippines —
  almost all use NDFs offshore. Onshore deliverable forwards exist
  with different fix conventions.
- **Russia post-Feb 2022**: most data is stale or sanctioned. MOEX
  feed largely cut for foreign clients; Russian sovereign bonds /
  CDS quoted at distressed levels with thin two-way markets.
- **Saudi / GCC weekend**: Tadawul, ADX, DFM, QE all trade
  Sun–Thu (Friday-Saturday is the weekend). `nonTradingDayFillOption`
  must accommodate.
- **India tick conventions**: NSE quotes in INR, two decimal
  places. Settlement T+0 for some scrips since 2024, T+1 mostly.
- **Brazilian preferred shares**: `PETR3` (ON) and `PETR4` (PN) are
  *different* securities with different voting rights and
  liquidity. Don't substitute.
- **ZAR / TRY high-vol regimes**: turn off `nonTradingDayFillMethod
  =PREVIOUS_VALUE` for vol estimation — gaps over local holidays
  inflate carrying-day vol.
- **EM holidays**: many regional days don't appear in `US`/`EU`
  calendars. Use country-specific `CALENDAR_CODE` overrides.
