# Bonds

Yellow keys: `Govt` (sovereigns + supranationals + agencies),
`Corp` (corporates, financials, covered, hybrids, CDS, supras), `Mtge`
(MBS / ABS / CMOs), `Muni` (US municipals), `Pfd` (preferred stock),
`M-Mkt` (commercial paper, T-bills, CDs).

## Identifying a bond

Five interchangeable forms:

```
T 4.625 02/15/35 Govt        # ticker + coupon + maturity (US Treasury)
DBR 2 ½ 08/15/54 Govt        # German Bund 2.5% Aug-2054
EDP 1 ⅞ 03/14/35 Corp        # EDP Energias 1.875% Mar-2035
/cusip/91282CHV9 Govt        # by CUSIP
/isin/DE0001102614 Govt      # by ISIN
/figi/BBG00FPNNVS3 Corp      # by FIGI
```

Spaces in the ticker form: separator between coupon and maturity is a
single space; coupon can be a fraction (`½`, `¼`, `⅜`, `⅝`, `¾`, `⅞`)
or decimal (`4.625`).

For research panels, prefer **ISIN-based** identification. It survives
restructurings and corporate name changes that mangle the ticker.

### Generic benchmarks (always-on-the-run)

```
GT2 Govt, GT5 Govt, GT10 Govt, GT30 Govt          # US actives
GTGBP2Y / 5Y / 10Y / 30Y Govt                     # UK gilts
GTDEM2Y / 5Y / 10Y / 30Y Govt                     # German bunds
GTJPY10Y Govt                                     # JGB 10Y
GTITL10Y / GTFRF10Y / GTESP10Y / GTPTE10Y Govt    # IT, FR, ES, PT
GTBRL10Y Govt, GTMXN10Y Govt, GTCNY10Y Govt       # EM
```

These are "constant-maturity" benchmarks — Bloomberg rolls them as the
underlying issue moves off-the-run.

## Static / reference fields

```
ISSUER, ISSUER_NAME, ISSUER_INDUSTRY,
SECURITY_NAME, SECURITY_DES,
ISSUE_DT, MATURITY, ISSUE_PX,
FIRST_COUPON_DT, LAST_COUPON_DT,
CPN, CPN_TYP                       # FIXED, FLOATING, ZERO, STEP
CPN_FREQ                           # 1, 2, 4, 12
DAY_CNT_DES, DAY_CNT,              # ACT/ACT, 30/360, ACT/360
CALC_TYP_DES, CALC_TYP,            # 1=Bond Yld, 2=Discount, ...
AMT_ISSUED, AMT_OUTSTANDING,
CRNCY, RANK, PAYMENT_RANK,
COUNTRY_FULL_NAME, COUNTRY_OF_RISK,
INDUSTRY_GROUP, INDUSTRY_SUBGROUP,
BICS_LEVEL_1_INDUSTRY_NAME, ...
COLLAT_TYP, MTG_AGENCY,            # MBS only
ID_BB_GLOBAL, ID_ISIN, ID_CUSIP, ID_SEDOL1,
SERIES, MARKET_OF_ISSUE,
MTY_TYP                            # AT MATURITY, CALLABLE, PUTTABLE
NXT_CALL_DT, NXT_CALL_PX, NXT_PUT_DT,
FIRST_CALL_DT_ISSUANCE
SUKUK_FLAG, COVERED_FLAG, GREEN_BOND_FLAG
```

Floaters:

```
FLT_BENCHMARK_INDEX                # SOFR, ESTR, EURIBOR, ...
FLT_SPREAD                         # spread to index, in bps
FLT_RESET_DT, FLT_RESET_FREQ
FLT_CAP, FLT_FLOOR
NEXT_RESET_DT
```

Convertibles:

```
CV_FLAG, CV_PARITY, CV_PREMIUM,
CV_CONVERSION_RATIO, CV_CONVERSION_PX,
CV_NEXT_CALL_DT
```

## Pricing fields

Bonds quote price *and* yield. Both are first-class.

```
PX_LAST, PX_BID, PX_ASK, PX_MID,        # clean price by default
PX_DIRTY_BID, PX_DIRTY_ASK,             # dirty (with accrued)
YLD_YTM_BID, YLD_YTM_ASK, YLD_YTM_MID,  # yield to maturity
YLD_YTC_MID,                            # yield to call
YLD_YTW_MID,                            # yield to worst
YLD_CNV_BID                             # for convertibles, conv yield

ACCRUED_INTEREST                        # at PX_LAST settle
ACCRUED_DAYS

NXT_CPN_PMT_DT
PRC_AS_OF_DT
PRICING_SOURCE                          # CBBT, BVAL, BGN, TRACE, ...
```

A subtle point: `PX_LAST` for a bond is **clean** by Bloomberg
convention. To go dirty, add `ACCRUED_INTEREST`.

## Spreads & risk metrics

```
G_SPRD_MID                Spread to government benchmark, bps
I_SPRD_MID                Spread to interpolated swap, bps
Z_SPRD_MID                Z-spread (zero-volatility) to swap curve, bps
OAS_SPREAD_MID            OAS over the swap curve, bps
OAS_SPREAD_BID, OAS_SPREAD_ASK
ASSET_SWAP_SPD_MID        Asset-swap spread, bps
DISC_MARGIN               Discount margin (floaters)
SPREAD_TO_BENCHMARK       generic
BENCHMARK_NAME, BENCHMARK_SECURITY      what the spread is vs.

DUR_ADJ_MID               modified duration
DUR_ADJ_OAS_MID           OAS-adjusted duration
RISKY_DUR                 risky duration (CDS-style)
DUR_MID, MOD_DUR_MID,     same family
KEY_RATE_DUR_2Y, _5Y, _10Y, _30Y
CONVEXITY                 convexity
CONVEXITY_OAS
DV01                      dollar value of 1bp
WAL                       weighted average life
ZSPRD_DUR                 Z-spread duration
SPRD_DUR                  spread duration
EFF_DUR                   effective duration
```

## YAS — yield/spread analytics on demand

Most spread fields above use the *current* market price. For
**user-supplied** prices/yields use the YAS family with overrides:

```python
req.append("securities", "T 4.625 02/15/35 Govt")
req.append("fields", "YAS_BOND_YLD")
req.append("fields", "YAS_ISPREAD")
req.append("fields", "YAS_ZSPREAD")
req.append("fields", "YAS_ASW_SPREAD")
req.append("fields", "YAS_OAS_SPREAD")

ovs = req.getElement("overrides")
for k, v in [("YAS_BOND_PX",  "98.50"),
             ("YAS_RISK_DT",  "20250506"),       # settle
             ("YAS_CURVE",    "S490")]:           # SOFR curve
    o = ovs.appendElement()
    o.setElement("fieldId", k); o.setElement("value", v)
```

YAS overrides reference table:

| Override | Meaning |
|---|---|
| `YAS_BOND_PX` | Clean price (you supply, yield comes back) |
| `YAS_BOND_YLD` | Yield (you supply, price comes back) |
| `YAS_RISK_DT` | Settle date for analytics |
| `YAS_CURVE` | Curve number (S490 = SOFR, S514 = ESTR, S141 = SONIA, S510 = TONA OIS) |
| `YAS_ZSPREAD` | Manual z-spread |
| `YAS_OAS_SPREAD` | Manual OAS |
| `OAS_VOL_BASIS_BVOL` | Vol input for OAS (bp normal) |
| `YAS_BENCHMARK_BOND` | Use a specific benchmark |

## Ratings

Three majors plus Bloomberg composite, plus their action histories
(bulk):

```
RTG_MOODY, RTG_SP, RTG_FITCH, RTG_BB_COMPOSITE,
RTG_MOODY_OUTLOOK, RTG_SP_OUTLOOK, RTG_FITCH_OUTLOOK,
RTG_MOODY_LT_LC, RTG_SP_LT_LC,                    # local-currency LT
RTG_MOODY_AS_OF_DT, RTG_SP_AS_OF_DT,
RTG_FITCH_HIST, RTG_MOODY_HIST, RTG_SP_HIST,      # BULK
DEFAULT_PROBABILITY                              # Bloomberg model
```

Override `RTG_AS_OF_DT=YYYYMMDD` for a point-in-time rating.

## Cash-flow schedules (bulk)

```
CALL_SCHEDULE             Date, Price, Type
PUT_SCHEDULE              Date, Price
AMORT_SCHEDULE            Date, Amount, Factor
CPN_SCHEDULE              for step-ups
SINKING_FUND_SCHEDULE
INT_PMT_HIST              historical interest payments
PAYMENT_HISTORY
```

## Issuer / capital structure

`CAPITAL_STRUCTURE_DETAILED` is the goldmine — every bond and loan in
the issuer's stack with rank, amount, currency, maturity, coupon.

```
ISSUER, PARENT_COMP_TICKER, ULT_PARENT_TICKER_EXCHANGE,
ISSUER_PARENT_EQY_TICKER,
EQY_TICKER_FROM_DEBT,                 # the issuer's listed equity
DEFAULT_PROBABILITY                   # Bloomberg DRSK model
NEAREST_LIQ_5Y_BOND                   # most liquid 5y bond from the issuer
```

## Money-market / T-bill specifics (`M-Mkt`)

```
T 0 12/05/25 Govt                     # T-bill (zero coupon)
PX_DISCOUNT, YLD_BANK_DISC,
YLD_DISC, YLD_MMKT_BOND_EQUIV
```

## MBS specifics (`Mtge`)

```
FNCL 5.5 Mtge                         # FNMA conventional 30y, 5.5% coupon TBA
WAC, WAM, WALA,                       # weighted avg coupon / maturity / age
ORIG_AMT, OUT_BAL,
PSA_SPEED, CPR_1MO, CPR_3MO, CPR_6MO,
PREPAY_SPEED_RANGE
COLLAT_TYP, AGENCY,
MTG_TBA_PRICING                       # for TBA settle
```

## Sovereign / supranational sources

For the same German 10y bund you can hit different sources:

| Pricing source | What it shows |
|---|---|
| `BGN` | Bloomberg Generic (composite) |
| `CBBT` | Composite Bloomberg Bond Trader (executable) |
| `BVAL` | Bloomberg evaluated price (model-based, 24h) |
| `TRAX` | TRAX (now MarketAxess) |
| `TRACE` | FINRA TRACE (US corporates) |
| `EXCH` | Exchange (e.g. MOT for Italian retail bonds) |
| `MSRB` | US munis |

Override on a request: append `pricingSource` element, or change the
ticker (some sources are baked in).

## Curves (the //blp/curve-style identifiers)

| Curve id | Description |
|---|---|
| `S490` | USD SOFR OIS |
| `S514` | EUR €STR OIS |
| `S141` | GBP SONIA OIS |
| `S510` | JPY TONA OIS |
| `I0001` | US Treasury active |
| `I0009` | German bund active |
| `I0022` | UK Gilt active |
| `I025` | Japanese govt |
| `S0023` | EUR swap (legacy 6M EURIBOR) |

Use them directly: `req.append("securities", "S490 Curncy")` returns
metadata for the curve, but the more common path is to list the swap
nodes directly (`USSO1 Curncy`, `USSO2 Curncy`, …; see
[swaps.md](swaps.md)).

## CDS

CDS lives under `Corp` yellow key but its grammar is different:

```
EDPPL CDS USD SR 5Y D14 Corp           # EDP Portugal 5Y senior CDS
ITRX MAIN CDSI S40 5Y Corp             # iTraxx Main S40 5Y index
CDX IG CDSI S42 5Y Corp                # CDX IG S42 5Y index
ITRX XOVER CDSI S40 5Y Corp            # iTraxx Crossover
```

Fields:

```
PX_LAST                  par-spread or upfront, depending on convention
CDS_QUOTE_TYPE           PAR_SPREAD or UPFRONT
CDS_FAIR_SPREAD          model-implied
CDS_FLAT_SPREAD
CDS_RUNNING_CPN          standard 100bp / 500bp coupon
CDS_RECOVERY_RATE
CDS_DV01
```

CDS curves: each issuer has 1Y, 2Y, 3Y, 4Y, 5Y, 7Y, 10Y, 20Y, 30Y. The
ticker pattern keeps the issuer prefix and only changes the tenor.

See [swaps.md](swaps.md) for full CDS detail.

## Liquidity / market activity

```
TRACE_TRD_VOL_TODAY, TRACE_TRD_VOL_5D,
TRACE_NUM_OF_TRD_TODAY,
LAST_PX_DT, PX_LAST_DT,
DAYS_SINCE_LAST_TRD,
LIQUIDITY_LIQ_SCORE              # Bloomberg LQA
LQA_LIQUIDITY_SCORE              # newer mnemonic
```

## ESG flags (where present)

```
GREEN_BOND_FLAG, SOCIAL_BOND_FLAG, SUSTAINABILITY_BOND_FLAG,
USE_OF_PROCEEDS, ICMA_PRINCIPLE
ESG_DISCLOSURE_SCORE             # equity-side, but issuer-level
```

## Common pitfalls

- **Yield curve vs spread direction**: `Z_SPRD_MID` and friends are bps
  *over* the (swap) curve. Higher = riskier. `BENCHMARK_NAME` tells you
  which curve.
- **OAS for callables**: requires a vol input. Bloomberg uses the
  Terminal user's `OAS1` setting unless you set
  `OAS_VOL_BASIS_BVOL`. Pin it to be reproducible.
- **Settle date**: many analytics depend on `YAS_RISK_DT`. T+1 / T+2
  conventions vary by market. Don't trust the default if you care
  about exact numbers.
- **Holiday calendars**: `CALENDAR_CODE` override drives accrual /
  settle. Default is the security's market.
- **Quote type**: a corporate CDS may quote in *upfront* (US conv) or
  *par-spread* (older). Always read `CDS_QUOTE_TYPE` before trusting
  `PX_LAST`.
