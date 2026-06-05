# Rates & Money Market in Excel

The short end. Overnight rates, central-bank policy rates,
deposit/CP rates, T-bills, FRAs.

For the conceptual model see
[docs/asset_classes/swaps.md](../../docs/asset_classes/swaps.md)
(swap and money-market sections) and
[docs/regions/](../../docs/regions/).

## 1 · Overnight benchmarks (post-LIBOR)

```excel
=BDP("SOFRRATE Index", "PX_LAST")     ' USD SOFR
=BDP("ESTRON Index",   "PX_LAST")     ' EUR €STR
=BDP("SONIO/N Index",  "PX_LAST")     ' GBP SONIA
=BDP("TONAR Index",    "PX_LAST")     ' JPY TONA
=BDP("SARON Index",    "PX_LAST")     ' CHF SARON
=BDP("CORRAINDX Index","PX_LAST")     ' CAD CORRA (newer; pre-CORRA used "CDOR")
=BDP("SORA Index",     "PX_LAST")     ' SGD SORA
=BDP("AONIA Index",    "PX_LAST")     ' AUD overnight (RBA)
```

Compounded indices (a few days back, useful for derivative work):

```excel
=BDP("SOFR1MO Index", "PX_LAST")      ' 30d SOFR (compounded)
=BDP("SOFR3MO Index", "PX_LAST")
=BDP("SOFR6MO Index", "PX_LAST")
=BDP("ESTR1M Index",  "PX_LAST")
=BDP("ESTR3M Index",  "PX_LAST")
=BDP("SONIA1MIDX Index", "PX_LAST")
```

## 2 · Central-bank policy rates

```excel
=BDP("FDTR Index",     "PX_LAST")     ' Fed funds upper bound (target)
=BDP("FDTRMID Index",  "PX_LAST")     ' Fed funds midpoint
=BDP("FDTRLOW Index",  "PX_LAST")     ' Fed funds lower bound
=BDP("FDTROVER Index", "PX_LAST")     ' IORB
=BDP("RRPONTSY Index", "PX_LAST")     ' ON RRP

=BDP("EURR002W Index", "PX_LAST")     ' ECB MRO
=BDP("EUDRA Index",    "PX_LAST")     ' ECB Deposit Facility Rate
=BDP("EUDP Index",     "PX_LAST")     ' ECB Marginal Lending Facility

=BDP("UKBRBASE Index", "PX_LAST")     ' BoE Bank Rate
=BDP("BOJDTR Index",   "PX_LAST")     ' BoJ depo rate
=BDP("SNBN Index",     "PX_LAST")     ' SNB policy rate
=BDP("BCBPOLY Index",  "PX_LAST")     ' BoC overnight target
=BDP("RBATCTR Index",  "PX_LAST")     ' RBA cash rate
=BDP("MASOVRN Index",  "PX_LAST")     ' MAS overnight

=BDP("BZSTSETA Index", "PX_LAST")     ' Brazil Selic target
=BDP("MXTSETA Index",  "PX_LAST")     ' Mexico Banxico overnight
=BDP("COREPO Index",   "PX_LAST")     ' Colombia BanRep repo
=BDP("SAFOPRR Index",  "PX_LAST")     ' SA SARB repo
=BDP("TBSO1WK Index",  "PX_LAST")     ' Turkey 1w repo
=BDP("RBIRPO Index",   "PX_LAST")     ' India RBI repo
=BDP("INDOIN Index",   "PX_LAST")     ' Indonesia BI 7d reverse repo
=BDP("PLZNREF Index",  "PX_LAST")     ' Poland NBP reference
=BDP("HUFNB Index",    "PX_LAST")     ' Hungary base
=BDP("CZTRWREF Index", "PX_LAST")     ' Czech CNB 2W repo
```

## 3 · OIS-implied policy expectations

The most direct way to read market-implied future policy rates is
the OIS strip:

```excel
=BDP("USSOA Curncy", "PX_LAST")       ' SOFR overnight
=BDP("USSOC Curncy", "PX_LAST")       ' SOFR OIS spot-starting (~1m)
=BDP("USSO3M Curncy", "PX_LAST")      ' 3m
=BDP("USSO6M Curncy", "PX_LAST")      ' 6m
=BDP("USSO9M Curncy", "PX_LAST")      ' 9m
=BDP("USSO1 Curncy", "PX_LAST")       ' 1y
=BDP("USSO2 Curncy", "PX_LAST")       ' 2y
```

For "rate cuts priced by FOMC date" workflows, calendar tickers exist:

```excel
=BDP("USSOFM26 Curncy", "PX_LAST")    ' OIS through the Mar-26 FOMC
=BDP("USSOFA26 Curncy", "PX_LAST")    ' through Apr-26 FOMC
```

(Bloomberg builds dated OIS for each scheduled FOMC.) Same for ECB:
`EESWFM` family.

## 4 · LIBOR (retired) and EURIBOR (alive)

```excel
=BDP("US0001M Index", "PX_LAST")      ' USD LIBOR 1m (retired 2023)
=BDP("US0003M Index", "PX_LAST")      ' USD LIBOR 3m (retired)
=BDP("US0006M Index", "PX_LAST")      ' USD LIBOR 6m

=BDP("EUR001M Index", "PX_LAST")      ' EURIBOR 1m (alive)
=BDP("EUR003M Index", "PX_LAST")      ' EURIBOR 3m (the benchmark)
=BDP("EUR006M Index", "PX_LAST")      ' EURIBOR 6m

=BDP("BP0003M Index", "PX_LAST")      ' GBP LIBOR (retired)
=BDP("JY0003M Index", "PX_LAST")      ' JPY LIBOR (retired)
```

For pre-2023 splices use LIBOR; post-2023 USD/GBP use OIS.

## 5 · T-bills

US:

```excel
=BDP("USB1M Index",  "PX_LAST")       ' 1m T-bill yield (secondary)
=BDP("USB3M Index",  "PX_LAST")
=BDP("USB6M Index",  "PX_LAST")
=BDP("USB1Y Index",  "PX_LAST")
=BDP("USGG3M Index", "PX_LAST")       ' Fed H.15 3m yield
=BDP("USGG6M Index", "PX_LAST")
=BDP("USGG12M Index","PX_LAST")

' Specific bill (yield from ticker)
=BDP("B 0 12/05/25 Govt", "YLD_BANK_DISC")
=BDP("B 0 12/05/25 Govt", "YLD_DISC")
=BDP("B 0 12/05/25 Govt", "YLD_MMKT_BOND_EQUIV")
```

UK:

```excel
=BDP("UKTBILLI Index", "PX_LAST")      ' UK 3m T-bill
=BDP("UKTB1M Index",   "PX_LAST")      ' (if entitled)
```

EUR sovereign bills via specific ISIN / ticker.

## 6 · Commercial paper / depo

```excel
=BDP("DCPB30 Index", "PX_LAST")       ' US 30d AA financial CP
=BDP("DCPN30 Index", "PX_LAST")       ' US 30d AA non-financial CP
=BDP("DCPB90 Index", "PX_LAST")       ' US 90d financial CP
=BDP("ECPA90 Index", "PX_LAST")       ' Euro 90d CP (where entitled)
=BDP("USBA3M Index", "PX_LAST")       ' US 3m banker's acceptance
```

## 7 · FRA points

Pattern: `<CCY>FRA<expiry>x<expiry+tail>`. Less standardised; check
`DES <GO>` if uncertain.

```excel
=BDP("USDFRA 3X6 Curncy",   "PX_LAST")   ' USD 3x6 FRA
=BDP("USDFRA 6X9 Curncy",   "PX_LAST")
=BDP("EURFRA 3X6 Curncy",   "PX_LAST")
=BDP("EURFRA 6X9 Curncy",   "PX_LAST")
```

For SOFR/€STR-strip-style FRA equivalents, prefer the OIS strip
(USSO3M, USSO6M, etc.) — cleaner, more liquid in the post-LIBOR
world.

## 8 · Repo & funding

```excel
=BDP("RRPONTSY Index", "PX_LAST")     ' Fed ON RRP rate
=BDP("RREPO TR Index", "PX_LAST")     ' GC repo (alt)
=BDP("USGGRR1Y Index", "PX_LAST")     ' US Treasury repo 1y
=BDP("BGCR Index",     "PX_LAST")     ' Broad General Collateral Rate
=BDP("TGCR Index",     "PX_LAST")     ' Tri-party GCR
=BDP("FEDL01 Index",   "PX_LAST")     ' Fed Effective rate (effective fed funds)
=BDP("EFFR Index",     "PX_LAST")     ' (alternative ticker)

=BDP("EUREPO Index",   "PX_LAST")     ' EUREPO (where published)
=BDP("ESTRBALN Index", "PX_LAST")     ' €STR balances
```

## 9 · Auction results / new issues

Bloomberg publishes auction stop-out yields as `auction tickers`,
referenced via the upcoming or just-completed bond. The cleanest
discovery path is `AUCH <GO>` on the Terminal.

Once you have a ticker:

```excel
=BDP("T 4.625 02/15/35 Govt", "AUCTION_HIGH_YIELD")
=BDP("T 4.625 02/15/35 Govt", "AUCTION_LOW_YIELD")
=BDP("T 4.625 02/15/35 Govt", "AUCTION_AVG_YIELD")
=BDP("T 4.625 02/15/35 Govt", "AUCTION_DT")
=BDP("T 4.625 02/15/35 Govt", "AUCTION_BID_COVER")
=BDP("T 4.625 02/15/35 Govt", "AUCTION_AMT_ACCEPTED")
=BDP("T 4.625 02/15/35 Govt", "AUCTION_INDIRECT_PCT")
=BDP("T 4.625 02/15/35 Govt", "AUCTION_DIRECT_PCT")
=BDP("T 4.625 02/15/35 Govt", "AUCTION_DEALER_PCT")
```

## 10 · Economic data — interest-rate-relevant

```excel
=BDP("CPI YOY Index", "PX_LAST")       ' US CPI YoY headline
=BDP("CPI XYOY Index","PX_LAST")       ' US CPI core
=BDP("PCE DEFY Index","PX_LAST")       ' US PCE deflator YoY
=BDP("PCEC YOY Index","PX_LAST")       ' core PCE YoY
=BDP("GDP CYOY Index","PX_LAST")       ' US GDP YoY
=BDP("NFP T Index",   "PX_LAST")       ' Non-farm payrolls
=BDP("USURTOT Index", "PX_LAST")       ' US unemployment rate

=BDP("ECCPEMUY Index","PX_LAST")       ' Euro Area HICP YoY
=BDP("ECCPESTY Index","PX_LAST")       ' Euro Area HICP estimate

=BDP("UKRPCJYR Index","PX_LAST")       ' UK CPI YoY
=BDP("UKRPCH Index",  "PX_LAST")       ' UK RPI

=BDP("JNCPIYOY Index","PX_LAST")       ' JP CPI YoY
=BDP("JCCPIYOY Index","PX_LAST")       ' JP core CPI
```

For "release date" and surprise:

```excel
=BDP("CPI YOY Index", "ECO_RELEASE_DT")
=BDP("CPI YOY Index", "ECO_RELEASE_TIME")
=BDP("CPI YOY Index", "BN_SURVEY_MEDIAN")    ' consensus
=BDP("CPI YOY Index", "LAST_PRICE_DATE")
```

## 11 · OIS-implied policy expectations sheet

```
Sheet "Fed expectations":
   A             B                          C                 D
1  FOMC date     OIS-to-date ticker         Implied rate     Cut/Hike from current
2  2025-03-19    USSOFH25 Curncy            =BDP(B2,"PX_LAST") =C2 - $G$1
3  2025-04-30    USSOFJ25 Curncy            ...                ...
4  2025-06-17    USSOFM25 Curncy            ...                ...
5  2025-07-29    USSOFN25 Curncy            ...                ...
6  ...

G1: =BDP("FDTRMID Index","PX_LAST")  (current fed funds)
```

## 12 · Historical policy-rate path

```excel
=BDH("FDTR Index", "PX_LAST",
     DATE(2010,1,1), TODAY(),
     "Per=cdr", "Days=A", "Fill=P")    ' step-function: A days + Fill=P
```

For step-function rates `Days=A / Fill=P` is *exactly* what you
want — the rate persists across days until the next decision.

## 13 · FRA / OIS comparison sheet

```
Sheet "FRA vs OIS":
   A     B               C               D                  E
1  Tenor FRA rate         OIS-implied    Spread (bps)        Notes
2  3M    =BDP("USDFRA 0X3 Curncy","PX_LAST")
                          =BDP("USSO3M Curncy","PX_LAST")
                                          =B2-C2 * 100
3  6M    ...
```

## 14 · Worked monitor — global O/N rates

```
Sheet "Overnight rates":
   A       B (ticker)              C (rate)        D (yesterday)   E (1mo ago)
1  USD SOFR SOFRRATE Index         =BDP(B2,"PX_LAST") =BDH(B2,"PX_LAST",WORKDAY(TODAY(),-1)) =BDH(...)
2  EUR €STR ESTRON Index
3  GBP SONIA SONIO/N Index
4  JPY TONA  TONAR Index
5  CHF SARON SARON Index
6  CAD CORRA CORRAINDX Index
7  AUD ON    AONIA Index
8  SGD SORA  SORA Index
```

## 15 · Pitfalls

- **Step-function rates**: policy rates only change at decisions.
  `Days=W / Fill=P` smooths across non-trading days; `Days=A /
  Fill=P` is the right choice for a stair-step rate plot.
- **LIBOR splicing**: post-Jun-2023 (USD) and post-Jan-2024 (GBP /
  JPY), LIBOR ceased. Splicing legacy series with OIS needs an
  adjustment (Bloomberg's official cessation spreads, available
  via `IBOR <GO>`).
- **Compounded vs term rates**: a 3m SOFR compounded index
  (`SOFR3MO Index`) is *historical* — looking back 3m. The 3m SOFR
  OIS (`USSO3M Curncy`) is *forward-looking* — implied for the next
  3m. They are not the same number.
- **EURIBOR is alive but reformed**: methodology changed in 2019
  (hybrid). Pre-2019 EURIBOR data has slightly different
  statistical properties.
- **Repo rates fragmentation**: SOFR > BGCR > TGCR > GCF — each is
  a slightly different collateral universe. Match the one your
  trade uses.
- **`#N/A Field Not Applicable`** on ECO_* fields: only applies on
  the index "ticker" representing the release, not on derivatives
  of it.
- **Auction tickers** for unissued bonds resolve to the *most
  recent* auction of that maturity tenor; for pre-auction
  estimates you need the WI (when-issued) ticker.
