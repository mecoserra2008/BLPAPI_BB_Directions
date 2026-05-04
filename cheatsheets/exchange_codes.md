# Exchange / Pricing-Source Codes

The 2-letter (sometimes 3-letter) suffix between the ticker and the
yellow key tells Bloomberg which exchange / venue you mean. For
research the **composite** is usually right; for execution you want
the specific venue.

## Americas

| Code | Country | Venue |
|---|---|---|
| `US` | USA | US composite (consolidated tape) |
| `UN` | USA | NYSE |
| `UQ` | USA | NASDAQ |
| `UW` | USA | NASDAQ Global Select |
| `UA` | USA | NYSE American (former AMEX) |
| `UR` | USA | NYSE Arca |
| `UV` | USA | OTC Markets / OTCBB |
| `UF` | USA | OTC Pink Sheets |
| `UB` | USA | BATS / Cboe BZX |
| `UP` | USA | NYSE National |
| `UD` | USA | NASDAQ ADR |
| `UU` | USA | NASDAQ Capital Market |
| `CN` | Canada | Canada composite |
| `CT` | Canada | TSX |
| `CV` | Canada | TSX Venture |
| `CF` | Canada | CSE (Canadian Securities Exchange) |
| `CC` | Canada | Cboe Canada (formerly NEO) |
| `BZ` | Brazil | B3 (São Paulo) |
| `BS` | Brazil | B3 (alt) |
| `MM` | Mexico | BMV (also a legacy Spanish code; check `COUNTRY`) |
| `MX` | Mexico | BMV (alt) |
| `MF` | Mexico | BIVA (newer) |
| `AR` | Argentina | BYMA / Buenos Aires |
| `CI` | Chile | Santiago |
| `CC` | Chile | Santiago (alt; conflict with Cboe Canada) |
| `CB` | Colombia | BVC |
| `PE` | Peru | Lima |
| `VE` | Venezuela | Caracas |
| `UY` | Uruguay | Montevideo |
| `JM` | Jamaica | Kingston |
| `BB` | Barbados | (also Belgium — check) |
| `TT` | Trinidad & Tobago | (also Taiwan — check) |

## Europe (EU + EEA + non-EU)

| Code | Country | Venue |
|---|---|---|
| `LN` | UK | London Stock Exchange |
| `LI` | UK | LSE International Order Book (DRs) |
| `EU` | pan-European | Composite multi-MTF |
| `IX` | pan-European | Cboe Europe (Chi-X / BATS) |
| `TQ` | UK | Turquoise |
| `GR` | Germany | Xetra |
| `GY` | Germany | Frankfurt floor |
| `GH` | Germany | Hamburg |
| `GS` | Germany | Stuttgart |
| `GM` | Germany | Munich |
| `GD` | Germany | Düsseldorf |
| `GB` | Germany | Berlin |
| `FP` | France | Euronext Paris |
| `NA` | Netherlands | Euronext Amsterdam |
| `BB` | Belgium | Euronext Brussels (also Barbados) |
| `PL` | Portugal | Euronext Lisbon |
| `IM` | Italy | Borsa Italiana / Euronext Milan |
| `SM` | Spain | BME (Madrid) |
| `MM` (legacy) | Spain | older secondary boards (now mostly `SM`) |
| `AT` | Austria | Wiener Börse |
| `SW` | Switzerland | SIX |
| `VX` | Switzerland | virt-x / older |
| `IR` | Ireland | Euronext Dublin |
| `LX` | Luxembourg | Bourse de Luxembourg |
| `MT` | Malta | MSE |
| `CY` | Cyprus | CSE |
| `GA` | Greece | ATHEX |
| `ID` | Iceland | Reykjavik |
| `IS` | Iceland (alt) / India BSE — context-dependent |
| `SS` | Sweden | Nasdaq Stockholm |
| `SE` | Sweden (alt) | older SSE |
| `DC` | Denmark | Nasdaq Copenhagen |
| `FH` | Finland | Nasdaq Helsinki |
| `OB` | Norway | Oslo Børs |
| `NO` | Norway | Oslo (alt) |
| `PW` | Poland | Warsaw GPW |
| `CP` | Czechia | Prague PSE |
| `HB` | Hungary | Budapest |
| `RO` | Romania | Bucharest |
| `BU` | Bulgaria | Sofia |
| `LR` | Latvia | Riga |
| `EE` | Estonia | Tallinn |
| `LT` | Lithuania | Vilnius |

## Middle East / Africa

| Code | Country | Venue |
|---|---|---|
| `IT` | Israel | TASE (Tel Aviv) |
| `TI` | Turkey | Borsa Istanbul |
| `AB` | Saudi Arabia | Tadawul |
| `UH` | UAE | ADX (Abu Dhabi) |
| `DH` | UAE | DFM (Dubai) |
| `DU` | UAE | NASDAQ Dubai |
| `KK` | Kuwait | Boursa Kuwait |
| `BI` | Bahrain | Bahrain Bourse |
| `OM` | Oman | MSM |
| `QD` | Qatar | QE (Qatar Exchange) |
| `JR` | Jordan | ASE |
| `EY` | Egypt | EGX |
| `LE` | Lebanon | BSE Beirut |
| `MR` | Morocco | Casablanca |
| `NL` | Nigeria | NGX |
| `KN` | Kenya | Nairobi |
| `SJ` | South Africa | JSE |
| `BG` | Botswana | BSE |

## Asia-Pacific

| Code | Country | Venue |
|---|---|---|
| `JT` | Japan | Tokyo Stock Exchange |
| `JE` | Japan | Osaka Exchange |
| `JN` | Japan | Nagoya |
| `JS` | Japan | Sapporo |
| `JF` | Japan | Fukuoka |
| `JP` | Japan | composite |
| `JQ` | Japan | JASDAQ (legacy) |
| `JU` | Japan | Mothers (legacy) |
| `HK` | Hong Kong | HKEX |
| `CH` | China | Shanghai (A) |
| `CG` | China | Shenzhen (A) |
| `C1` | China | Shanghai B (USD) |
| `C2` | China | Shenzhen B (HKD) |
| `C5` | China | Beijing Stock Exchange |
| `CN` | China | composite |
| `KS` | Korea | KRX (KOSPI) |
| `KQ` | Korea | KOSDAQ |
| `KN` | Korea (alt) | (conflict with Kenya — check) |
| `TT` | Taiwan | TWSE |
| `TF` | Taiwan | TPEx (formerly OTC) |
| `IN` | India | NSE (National Stock Exchange) |
| `IS` | India | BSE (Bombay) |
| `MK` | Malaysia | Bursa Malaysia |
| `SP` | Singapore | SGX |
| `TB` | Thailand | SET |
| `IJ` | Indonesia | IDX |
| `PM` | Philippines | PSE |
| `VN` | Vietnam | HOSE (Ho Chi Minh) |
| `VH` | Vietnam | HNX (Hanoi) |
| `AU` | Australia | ASX |
| `AT` | Australia (alt) | Cboe Australia (also Austria — context) |
| `NZ` | New Zealand | NZX |
| `PA` | Pakistan | PSX |
| `BD` | Bangladesh | DSE |
| `LK` | Sri Lanka | CSE |
| `KZ` | Kazakhstan | KASE |
| `AS` | Australia (alt) | (conflict — many uses) |
| `RX` | Russia | MOEX (post-2022 sanctioned) |

## Pricing-source codes (FX, bonds, generics)

Used as a third "ticker word" for FX or bonds:

```
EURUSD CMPL Curncy            Composite London close
EURUSD CMPN Curncy            Composite NY close
EURUSD WMCO Curncy            WM/Reuters 4pm London
EURUSD BFIX Curncy            Bloomberg FX fix
EURUSD ECB37 Curncy           ECB reference rate

T 4.625 02/15/35 Govt @CBBT   Composite Bond Trader
T 4.625 02/15/35 Govt @TRACE  TRACE
T 4.625 02/15/35 Govt @BVAL   Bloomberg evaluated
```

| Code | Source |
|---|---|
| `BGN` | Bloomberg Generic Composite (default) |
| `BVAL` | Bloomberg Valuation evaluated price |
| `CBBT` | Composite Bloomberg Bond Trader (executable) |
| `TRAX` | TRAX (MarketAxess) |
| `TRACE` | FINRA TRACE (US corporates) |
| `MSRB` | US Munis |
| `WMCO` | WM/Reuters 4pm London fix |
| `CMPL` | Composite London close |
| `CMPN` | Composite NY close |
| `BFIX` | Bloomberg FX fix |
| `ECB37` | ECB reference rate |
| `EBS` | EBS interbank |
| `MUTL` | Multilateral electronic platforms |
| `SPGB` | Spanish gov pricing |
| `BMA` | French bond pricing |

## Resolving ambiguity

When two contexts share a code (`MM` = Mexico or legacy Spain;
`AT` = Austria or Australia Cboe; `IS` = India BSE or Iceland), let
the security disambiguate:

```python
# Always confirm with COUNTRY field on a sample
blp.bdp(["MAYBANK MK Equity"], ["COUNTRY","COUNTRY_FULL_NAME","EXCH_CODE"])
```

For new tickers always do one quick `bdp` for `COUNTRY_FULL_NAME` and
`PRIMARY_EXCHANGE_NAME` before stitching them into a panel.
