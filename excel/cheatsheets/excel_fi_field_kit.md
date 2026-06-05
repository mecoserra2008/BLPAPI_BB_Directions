# Fixed-Income Field Kit (Excel-grouped)

Hand-picked field list for FI workbooks, grouped by which function
returns useful results.

For the full mnemonic universe see
[../../cheatsheets/field_index.md](../../cheatsheets/field_index.md).
This file trims to FI + adds a column showing which Excel function
to use.

| Function | Use when |
|---|---|
| `BDP` | Single value / snapshot |
| `BDH` | Time series |
| `BDS` | Returns a table per security (bulk) |

## Bond identifiers

| Field | Function | Notes |
|---|---|---|
| `PARSEKYABLE_DES` | `BDP` | Canonical ticker; the back-resolver for `/isin/`, `/cusip/`, `/figi/` |
| `ID_BB_GLOBAL` | `BDP` | FIGI |
| `ID_ISIN` | `BDP` |  |
| `ID_CUSIP` | `BDP` |  |
| `ID_SEDOL1` | `BDP` |  |
| `ID_BB_UNIQUE` | `BDP` | BBG unique |
| `ID_BB_SEC_NUM_DES` | `BDP` |  |
| `EQY_TICKER_FROM_DEBT` | `BDP` | Issuer's listed equity |
| `ISSUER_PARENT_EQY_TICKER` | `BDP` |  |
| `ULT_PARENT_TICKER_EXCHANGE` | `BDP` |  |
| `NEAREST_LIQ_5Y_BOND` | `BDP` | Most-liquid 5y bond from same issuer |

## Bond reference / static

| Field | Function | Notes |
|---|---|---|
| `ISSUER`, `ISSUER_NAME`, `ISSUER_INDUSTRY` | `BDP` |  |
| `SECURITY_NAME`, `SECURITY_DES` | `BDP` |  |
| `ISSUE_DT`, `MATURITY` | `BDP` | Use `WORKDAY(...,1)` for trade settle |
| `FIRST_COUPON_DT`, `LAST_COUPON_DT` | `BDP` |  |
| `CPN`, `CPN_TYP`, `CPN_FREQ` | `BDP` | `CPN_TYP` = FIXED / FLOATING / ZERO / STEP |
| `DAY_CNT_DES`, `DAY_CNT` | `BDP` | ACT/ACT, 30/360, ACT/360 |
| `CALC_TYP_DES`, `CALC_TYP` | `BDP` |  |
| `AMT_ISSUED`, `AMT_OUTSTANDING` | `BDP` |  |
| `CRNCY` | `BDP` |  |
| `RANK`, `PAYMENT_RANK` | `BDP` |  |
| `COUNTRY_FULL_NAME`, `COUNTRY_OF_RISK` | `BDP` |  |
| `MARKET_OF_ISSUE` | `BDP` |  |
| `MTY_TYP` | `BDP` | AT MATURITY / CALLABLE / PUTTABLE |
| `NXT_CALL_DT`, `NXT_CALL_PX` | `BDP` |  |
| `NXT_PUT_DT` | `BDP` |  |
| `COVERED_FLAG`, `GREEN_BOND_FLAG`, `SOCIAL_BOND_FLAG`, `SUSTAINABILITY_BOND_FLAG`, `SUKUK_FLAG` | `BDP` |  |
| `USE_OF_PROCEEDS` | `BDP` |  |

## Floaters

| Field | Function | Notes |
|---|---|---|
| `FLT_BENCHMARK_INDEX` | `BDP` | SOFR / ESTR / EURIBOR / SONIA / TONA |
| `FLT_SPREAD` | `BDP` | bps over index |
| `FLT_RESET_DT`, `FLT_RESET_FREQ` | `BDP` |  |
| `FLT_CAP`, `FLT_FLOOR` | `BDP` |  |
| `NEXT_RESET_DT` | `BDP` |  |
| `DISC_MARGIN` | `BDP` |  |

## Bond pricing & yield

| Field | Function | Notes |
|---|---|---|
| `PX_LAST`, `PX_BID`, `PX_ASK`, `PX_MID` | `BDP` / `BDH` | Clean by default; for dirty use `Quote=D` in `BDH` |
| `PX_DIRTY_BID`, `PX_DIRTY_ASK`, `PX_DIRTY_MID` | `BDP` |  |
| `YLD_YTM_BID`, `YLD_YTM_ASK`, `YLD_YTM_MID` | `BDP` / `BDH` |  |
| `YLD_YTC_MID` | `BDP` / `BDH` | Yield to call |
| `YLD_YTW_MID` | `BDP` / `BDH` | Yield to worst |
| `ACCRUED_INTEREST`, `ACCRUED_DAYS` | `BDP` |  |
| `NXT_CPN_PMT_DT` | `BDP` |  |
| `PRC_AS_OF_DT`, `PRICING_SOURCE` | `BDP` |  |
| `LAST_PX_DT` | `BDP` | For staleness filtering |

## Bond spreads & risk

| Field | Function | Notes |
|---|---|---|
| `G_SPRD_MID` | `BDP` / `BDH` | vs govt |
| `I_SPRD_MID` | `BDP` / `BDH` | vs interp swap |
| `Z_SPRD_MID` | `BDP` / `BDH` | zero-vol |
| `OAS_SPREAD_MID` | `BDP` / `BDH` | OAS over swap |
| `ASSET_SWAP_SPD_MID` | `BDP` / `BDH` | ASW |
| `BENCHMARK_NAME`, `BENCHMARK_SECURITY` | `BDP` |  |
| `DUR_ADJ_MID`, `MOD_DUR_MID`, `DUR_MID` | `BDP` |  |
| `DUR_ADJ_OAS_MID` | `BDP` |  |
| `RISKY_DUR` | `BDP` |  |
| `KEY_RATE_DUR_2Y`, `_5Y`, `_10Y`, `_30Y` | `BDP` |  |
| `CONVEXITY`, `CONVEXITY_OAS` | `BDP` |  |
| `DV01` | `BDP` |  |
| `WAL` | `BDP` | Weighted average life |
| `EFF_DUR` | `BDP` |  |

## YAS (user-supplied price)

All `BDP` with paired overrides.

| Field |
|---|
| `YAS_BOND_YLD`, `YAS_BOND_PX` |
| `YAS_ZSPREAD`, `YAS_ISPREAD`, `YAS_ASW_SPREAD`, `YAS_OAS_SPREAD` |
| `YAS_RISK_DT` (override input only) |
| `YAS_CURVE` (override input only) |

## Bond bulk schedules (BDS only)

| Field |
|---|
| `CALL_SCHEDULE` |
| `PUT_SCHEDULE` |
| `AMORT_SCHEDULE` |
| `CPN_SCHEDULE` |
| `SINKING_FUND_SCHEDULE` |
| `INT_PMT_HIST` |
| `PAYMENT_HISTORY` |
| `CAPITAL_STRUCTURE_DETAILED` |

## Ratings

| Field | Function |
|---|---|
| `RTG_MOODY`, `RTG_SP`, `RTG_FITCH`, `RTG_BB_COMPOSITE` | `BDP` |
| `RTG_*_OUTLOOK` | `BDP` |
| `RTG_*_HIST` | `BDS` (history) |
| `RTG_AS_OF_DT` | override input |
| `DEFAULT_PROBABILITY`, `RTG_BB_DEFAULT_PROB` | `BDP` |
| `LIQUIDITY_LIQ_SCORE`, `LQA_LIQUIDITY_SCORE` | `BDP` |

## CDS

| Field | Function | Notes |
|---|---|---|
| `PX_LAST` | `BDP` / `BDH` | Spread (bps) or upfront (%) — check `CDS_QUOTE_TYPE` |
| `CDS_QUOTE_TYPE` | `BDP` |  |
| `CDS_FAIR_SPREAD`, `CDS_FLAT_SPREAD` | `BDP` |  |
| `CDS_RUNNING_CPN` | `BDP` |  |
| `CDS_RECOVERY_RATE` | `BDP` | Default 0.40 SR / 0.25 SUB |
| `CDS_RECOVERY_RATE_OVERRIDE` | override input |  |
| `CDS_DV01`, `RISKY_DUR` | `BDP` |  |
| `CDS_IMPLIED_DEFAULT_PROB` | `BDP` |  |
| `UPFRONT_PMT`, `ACCRUED_INTEREST`, `ACCRUED_DAYS` | `BDP` |  |
| `ISDA_DEFINITION_VERSION` | `BDP` | D03 / D14 |
| `INDX_MEMBERS` (CDS indices) | `BDS` |  |

## Futures (`Comdty`)

| Field | Function | Notes |
|---|---|---|
| `PX_LAST`, `PX_SETTLE`, `PX_BID`, `PX_ASK` | `BDP` / `BDH` | Prefer `PX_SETTLE` for daily TR |
| `OPEN_INT`, `OPEN_INT_DATE` | `BDP` |  |
| `FUT_AGGTE_VOL`, `FUT_AGGTE_OPEN_INT` | `BDP` |  |
| `FUT_TICK_SIZE`, `FUT_TICK_VAL`, `FUT_VAL_PT`, `FUT_CONT_SIZE`, `FUT_TRADING_UNITS` | `BDP` |  |
| `FUT_FIRST_TRADE_DT`, `LAST_TRADEABLE_DT`, `FUT_NOTICE_FIRST` | `BDP` |  |
| `FUT_DLV_DT_FIRST`, `FUT_DLV_DT_LAST` | `BDP` |  |
| `FUT_CUR_GEN_TICKER`, `FUT_GEN_FIRST_TRADE_DT` | `BDP` |  |
| `FUT_CTD_BOND`, `FUT_CTD_FRWD_PX`, `CTD_FRWD_PX` | `BDP` |  |
| `IMPLIED_REPO_RATE`, `NET_BASIS`, `GROSS_BASIS` | `BDP` |  |
| `CONV_FACTOR` | `BDP` |  |
| `FUT_CHAIN` | `BDS` |  |
| `NCOMM_LONG_POS`, `NCOMM_SHORT_POS`, `COMM_LONG_POS`, `COMM_SHORT_POS`, `OI_AGG` | `BDH` (weekly) | CFTC COT |

## Swaps (`Curncy`)

| Field | Function | Notes |
|---|---|---|
| `PX_LAST` | `BDP` / `BDH` | Par rate (%) |
| Curve nodes: `USSO1..30 Curncy`, `EESWE1..30 Curncy`, `BPSO1..30 Curncy`, `JYSO1..30 Curncy`, `SFSARON1..30 Curncy` |  |  |
| XCCY basis: `EUBSC1..30`, `JYBSC1..30`, `BPBSC1..30`, etc. (bps) | `BDP` / `BDH` |  |
| Forward swaps: `USFS0102`, `USFS0510`, etc. | `BDP` / `BDH` |  |
| Inflation swaps: `USSWITP*`, `EUSWIT*`, `BPSWIT*`, `JYSWIT*` | `BDP` / `BDH` |  |
| Swaption vol: `USSV0110`, `USSV0510`, `EUSV0110`, etc. | `BDP` |  |

## FX (`Curncy`)

| Field | Function | Notes |
|---|---|---|
| `PX_LAST` (spot) | `BDP` / `BDH` | Pick fix source (`WMCO`, `CMPL`, `BFIX`) |
| `PX_BID`, `PX_ASK` | `BDP` |  |
| `PX_LAST` (outright forward, e.g. `EURUSD3M`) | `BDP` / `BDH` |  |
| `PX_LAST` (points, e.g. `EUR3M`) | `BDP` / `BDH` |  |
| `FWD_POINTS`, `FWD_BID`, `FWD_ASK`, `FWD_RATE` | `BDP` |  |
| `SPOT_PRICE` | `BDP` |  |
| `IMPL_YIELD_PCT`, `IMPL_DEPOSIT_RATE` | `BDP` |  |
| `IMPL_YIELD_NDF_PCT` | `BDP` | NDFs |
| `NDF_FIX_DATE`, `NDF_FIX_RATE`, `NDF_VAL_DT`, `NDF_FIX_SOURCE` | `BDP` |  |
| `30DAY_IMPVOL_100.0%MNY_DF`, …`360DAY_IMPVOL_*` | `BDP` |  |
| `30DAY_IMPVOL_25DELTA_RR`, `_25DELTA_BF` | `BDP` |  |
| ATM-vol tickers `EURUSDV1M`, `USDJPYV3M`, etc. | `BDP` / `BDH` |  |
| RR / BF tickers `EURUSD25R1M`, `EURUSD25B1M`, etc. | `BDP` / `BDH` |  |

## Rates / money market

| Field / ticker family | Function | Notes |
|---|---|---|
| Overnight indices: `SOFRRATE Index`, `ESTRON Index`, `SONIO/N Index`, `TONAR Index`, `SARON Index` | `BDP` / `BDH` |  |
| Compounded: `SOFR1MO`, `SOFR3MO`, `ESTR3M`, `SONIA1MIDX` | `BDP` / `BDH` |  |
| Policy rates: `FDTR Index`, `EURR002W Index`, `UKBRBASE Index`, `BOJDTR Index` | `BDP` / `BDH` |  |
| T-bills: `USB1M`, `USB3M`, `USB6M`, `USB1Y Index` | `BDP` |  |
| LIBOR / EURIBOR: `US0001M Index`, `EUR003M Index` | `BDP` / `BDH` | LIBOR retired |
| Commercial paper: `DCPB30 Index`, etc. | `BDP` |  |
| Repo: `RRPONTSY Index`, `BGCR Index`, `TGCR Index`, `FEDL01 Index` | `BDP` |  |
| Auction: `AUCTION_HIGH_YIELD`, `AUCTION_AVG_YIELD`, `AUCTION_BID_COVER`, `AUCTION_INDIRECT_PCT`, `AUCTION_DEALER_PCT`, `AUCTION_DT` | `BDP` |  |

## Sovereign yields

| Family | Notes |
|---|---|
| `GT2`, `GT5`, `GT10`, `GT30 Govt` | US benchmark actives |
| `GTGBP10Y Govt`, `GTDEM10Y Govt`, `GTITL10Y Govt`, `GTESP10Y Govt`, `GTPTE10Y Govt`, `GTFRF10Y Govt`, `GTJPY10Y Govt`, `GTBRL10Y Govt`, `GTMXN10Y Govt`, `GTCNY10Y Govt` | Country actives |
| `USGG3M Index`, `USGG10YR Index`, `USGGT10Y Index`, `USGGBE10 Index` | Fed H.15 |

## Index-level total-return + OAS

| Ticker | What | Use |
|---|---|---|
| `LBUSTRUU Index` | US Aggregate TR | `BDP` / `BDH` for return; also `OAS_SPREAD_MID` |
| `LUACTRUU Index` | US Corporate IG TR | same |
| `LUH9TRUU Index` | US HY TR | same |
| `LECCTREU Index` | Euro Corp IG TR | same |
| `LF98TREU Index` | Euro HY TR | same |
| `ER00`, `HE00 Index` | ICE BofA Euro Corp / HY | same |
| `G0Q0`, `H0A0 Index` | ICE BofA US Corp / HY | same |
| `LP01TRGB Index` | GBP Treasury TR | same |
| `LEMBTRUU Index` | EM USD Bond TR | same |
| `JPEIDIVR Index` | EMBI Global Diversified | same |
| `JCEMCM Index` | CEMBI Composite | same |
