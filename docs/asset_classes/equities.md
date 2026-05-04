# Equities

Yellow key: `Equity`. Single-stock listings, ETFs, REITs, ADRs, GDRs,
preferred shares, share classes — all share the same yellow key. The
exchange is encoded by the **2-letter pricing source** before `Equity`.

## Ticker grammar

```
<TICKER> <EXCH> Equity
```

Examples:

| Ticker | Reads as |
|---|---|
| `AAPL US Equity` | Apple, US composite (default routing) |
| `AAPL UW Equity` | Apple, NASDAQ National Market |
| `MSFT UQ Equity` | Microsoft, NASDAQ |
| `EDP PL Equity` | EDP, Lisbon |
| `SAN SM Equity` | Santander, BME (Spain) |
| `RIO LN Equity` | Rio Tinto plc, London |
| `RIO AT Equity` | Rio Tinto Limited, ASX (Australia) |
| `7203 JT Equity` | Toyota, Tokyo |
| `005930 KS Equity` | Samsung, KOSPI |
| `941 HK Equity` | China Mobile, HKEX |
| `600519 CH Equity` | Kweichow Moutai, Shanghai (A-share) |
| `000333 CG Equity` | Midea, Shenzhen (A-share) |

Rule of thumb: the 2-letter code is the **exchange / pricing source**,
not the country. See [cheatsheets/exchange_codes.md](../../cheatsheets/exchange_codes.md).

### Composite vs primary listing

`AAPL US Equity` is the **US composite** (consolidated tape). For a
specific venue:

- `AAPL UN Equity` — NYSE Composite
- `AAPL UQ Equity` — NASDAQ Composite (CTA)
- `AAPL UW Equity` — NASDAQ National Market
- `AAPL UR Equity` — NYSE Arca

Use composites for research; specific venues for execution analysis.

### Multi-class shares

Bloomberg uses `/A`, `/B` suffixes:

- `BRK/A US Equity`, `BRK/B US Equity`
- `GOOG US Equity` (class C, no vote), `GOOGL US Equity` (class A)

## Identifier resolution

Convert any external id to a Bloomberg ticker:

```python
# ISIN
req.append("securities", "/isin/US0378331005")
req.append("fields",     "PARSEKYABLE_DES_SOURCE")
# back-resolves to "AAPL US Equity"

# CUSIP
req.append("securities", "/cusip/037833100")
# SEDOL
req.append("securities", "/sedol/2046251")
# FIGI (Bloomberg Global Identifier)
req.append("securities", "/bbgid/BBG000B9XRY4")
```

Useful identifier fields:

| Field | Returns |
|---|---|
| `ID_BB_GLOBAL` | FIGI |
| `ID_BB_UNIQUE` | Bloomberg unique id |
| `ID_ISIN` | ISIN |
| `ID_CUSIP` | CUSIP |
| `ID_SEDOL1` | SEDOL |
| `ID_BB_SEC_NUM_DES` | Bloomberg ticker (parseable) |
| `PARSEKYABLE_DES` | Same, with yellow key |
| `EQY_FUND_TICKER` | Underlying issuer ticker (helps for share classes) |
| `EQY_FUND_CRNCY` | Reporting currency |

## Reference / static fields

The "describe a stock" set:

```
SECURITY_NAME, NAME, COMPANY_NAME, LONG_COMP_NAME,
SECURITY_TYP2, EQY_FUND_TICKER, ISSUER, COUNTRY,
COUNTRY_FULL_NAME, COUNTRY_OF_INCORPORATION, EXCH_CODE,
PRIMARY_EXCHANGE_NAME, CRNCY,
GICS_SECTOR_NAME, GICS_INDUSTRY_GROUP_NAME,
GICS_INDUSTRY_NAME, GICS_SUB_INDUSTRY_NAME,
BICS_LEVEL_1_SECTOR_NAME, BICS_LEVEL_2_INDUSTRY_GROUP_NAME, ...,
ICB_SECTOR_NAME, INDUSTRY_SECTOR, INDUSTRY_GROUP, INDUSTRY_SUBGROUP,
BLOOMBERG_PEERS, RELATIVE_INDEX,
EQY_FREE_FLOAT_PCT, EQY_SH_OUT, EQY_SH_OUT_REAL,
EQY_FLOAT, MARKET_STATUS,
HISTORICAL_VOLATILITY_30D, EQY_BETA_RAW
```

## Price / volume

Snapshot:

```
PX_LAST, PX_OPEN, PX_HIGH, PX_LOW, PX_BID, PX_ASK, PX_MID,
PX_VOLUME, PX_VOLUME_AVG_30D, PX_VOLUME_AVG_1Y,
LAST_TRADE_TIME, LAST_TRADE_DATE,
PX_OFFICIAL_AUCTION_CLOSE, PX_OFFICIAL_AUCTION_OPEN,
HIGH_52WEEK, LOW_52WEEK,
PX_PREVIOUS_DAY_CLOSE, CHG_PCT_1D, CHG_PCT_5D, CHG_PCT_YTD
```

Total return (use this for backtests, not `PX_LAST`):

```
TOT_RETURN_INDEX_GROSS_DVDS,                # gross divs reinvested
TOT_RETURN_INDEX_NET_DVDS,                  # net divs (after WHT)
DAY_TO_DAY_TOT_RETURN_GROSS_DVDS            # 1-day return %
```

## Market cap and float

```
CUR_MKT_CAP                  current market capitalization (millions, see EQY_FUND_CRNCY)
HISTORICAL_MARKET_CAP        historical (with date overrides)
EQY_SH_OUT                   shares outstanding (diluted)
EQY_SH_OUT_REAL              actual basic shares
EQY_FLOAT                    free-float shares
EQY_FREE_FLOAT_PCT           free-float %
EQY_FLOAT_MKT_CAP            free-float adjusted mcap
```

## Fundamentals (income statement / balance sheet / cash flow)

Periodicity is controlled by **`FUND_PER`** override:
- `Q` = quarterly
- `S` = semi-annual
- `A` = annual
- `Y` = year-to-date
- `LTM` = trailing twelve months (use the `TRAIL_12M_*` fields directly)

Period selection by **`EQY_FUND_RELATIVE_PERIOD`** override:
- `0` = current/most recent
- `-1` = 1 period back
- `-1Q`, `-4Q`, `-1A`, ... combine direction + unit

Currency by **`EQY_FUND_CRNCY`** override (`USD`, `EUR`, ...).

### Income statement (`IS_*`)

```
IS_REVENUE                Sales / Revenue
IS_COGS                   Cost of goods sold
IS_GROSS_PROFIT
IS_OPERATING_EXPN
IS_OPERATING_INCOME
IS_EBITDA
IS_EBIT
IS_INT_EXPENSE
IS_PRETAX_INC
IS_INC_TAX_EXP
IS_NET_INCOME
IS_EARN_FOR_COMMON
IS_EPS                    EPS basic
IS_EPS_DILUTED            EPS diluted
IS_DIL_EPS_CONT_OPS       diluted EPS from continuing ops
IS_AVG_NUM_SH_FOR_EPS     weighted avg sh outstanding
IS_DPS                    Dividend per share, declared
IS_DEPRECATION_AMORTIZATION
```

### Balance sheet (`BS_*`)

```
BS_TOT_ASSET              Total assets
BS_CASH_NEAR_CASH_ITEM    Cash & equivalents
BS_TOT_LIAB2              Total liabilities
BS_LT_BORROW              Long-term debt
BS_ST_BORROW              Short-term debt
BS_TOT_DEBT               Total debt (LT + ST)
BS_TOTAL_EQUITY           Total equity
BS_SH_FOR_DILUTED_EPS     Shares outstanding for diluted EPS
BS_INVENTORIES
BS_ACCT_RCV
BS_ACCT_PAYABLE
BS_INTANGIBLES
BS_GOODWILL
BS_NET_FIX_ASSET          Net PP&E
BS_PFD_EQTY_HYBRID_CAP
BS_MIN_INTERESTS
NET_DEBT                  BS_TOT_DEBT − BS_CASH_NEAR_CASH_ITEM
```

### Cash flow (`CF_*`)

```
CF_CASH_FROM_OPER         CFO
CF_CASH_FROM_INV_ACT      CFI
CF_CASH_FROM_FNC_ACT      CFF
CF_CAP_EXPEND_PRPTY_ADD   CapEx
CF_FREE_CASH_FLOW         FCF (CFO − CapEx)
CF_FREE_CASH_FLOW_TO_FIRM
CF_DPS_PAID
CF_NET_CASH_DISCONT_OPS
```

### Trailing-twelve-months pre-baked

Avoid override gymnastics for LTM:

```
TRAIL_12M_NET_INC, TRAIL_12M_EPS, TRAIL_12M_REVENUE,
TRAIL_12M_EBITDA, TRAIL_12M_FREE_CASH_FLOW,
TRAIL_12M_DIL_PE_RATIO, TRAIL_12M_DVD_PER_SH
```

### Per-share book / common ratios

```
BOOK_VAL_PER_SH, TANG_BOOK_VAL_PER_SH,
SALES_REV_TURN_PER_SH, CASH_FLOW_PER_SH,
PE_RATIO, BEST_PE_RATIO, PX_TO_BOOK_RATIO,
PX_TO_SALES_RATIO, EV_TO_T12M_EBITDA,
EV_TO_T12M_SALES, EBITDA_TO_REVENUE,
RETURN_COM_EQY (ROE), RETURN_ON_ASSETS (ROA),
RETURN_ON_INV_CAPITAL (ROIC),
DVD_PAYOUT_RATIO, EQY_DVD_YLD_IND, EQY_DVD_YLD_12M
```

## Estimates (BEst consensus)

Mean / dispersion metrics:

```
BEST_EPS, BEST_EPS_NUMEST, BEST_EPS_HIGH, BEST_EPS_LOW,
BEST_EPS_STDEV, BEST_EPS_MEDIAN,
BEST_REVENUE, BEST_EBIT, BEST_EBITDA, BEST_NET_INCOME,
BEST_FREE_CASH_FLOW, BEST_DPS,
BEST_TARGET_PRICE, BEST_TARGET_PX_NUMEST, BEST_TARGET_PX_HIGH,
BEST_TARGET_PX_LOW,
ANALYST_RECS_HIGH_LOW_AVG_NUM, RECMD_BEST_REPRT_TYP_DET,
TOT_BUY_REC, TOT_HOLD_REC, TOT_SELL_REC,
ANALYST_RATING                 # Bloomberg rating model output
```

Period selection: **`BEST_FPERIOD_OVERRIDE`** with values:
- `1FY`, `2FY`, `3FY` — fiscal years out
- `1FQ`, `2FQ`, ... — fiscal quarters out
- `1BF` — blended forward (between `0FY` and `1FY`)
- `1FH` — fiscal half

Point-in-time consensus (avoid look-ahead bias):
**`BEST_DATA_RELEASE_DT=YYYYMMDD`**.

## Earnings dates and surprises

```
EARN_ANN_DT                       next earnings date (or last announced)
EARN_ANN_DT_TIME_HIST_WITH_EPS    BULK — full history with reported & est EPS
ECO_RELEASE_DT                    same as EARN_ANN_DT for some sources
ANNOUNCEMENT_DT                   most-recent
ANN_DT_NEXT_EARNINGS              prospective
ECO_RELEASE_TIME                  AMC / BMO / Time
EXPECTED_REPORT_DT                next expected (analyst-driven)
EARN_REL_DT_PRD_END_DT            period-end date for last reported
LAST_EARNINGS_SURPRISE            % surprise on EPS
```

## Dividends & corporate actions

```
DVD_HIST_ALL              BULK — full dividend history
EQY_DVD_HIST_GROSS        sum gross divs over a period (override START/END_DATE)
DVD_LAST                  most recent cash dividend amount
DVD_EX_DT                 next ex-date
DVD_PAYABLE_DT            next pay date
EQY_DVD_YLD_IND           indicated yield (annual / px)
EQY_DVD_YLD_12M           trailing 12m yield
DVD_PAYOUT_RATIO
NXT_DVD_AMT_GROSS / NXT_DVD_EX_DT
DVD_HIST_GROSS            history of gross divs
EQY_SPLIT_RATIO           latest split
EQY_SPLIT_DT              latest split date
CIE_DES                   corporate action description
EQY_DVD_ADJUST_FACT       cumulative split-adj factor
```

## Index / membership

```
INDX_MEMBERS                  BULK — current members of an index
INDX_MWEIGHT                  BULK — current weights (member, weight)
INDX_MWEIGHT_HIST             BULK — historical weights with END_DATE_OVERRIDE
INDX_MEMBERS_WEIGHTS          BULK — members with method
INDEX_RATIO_ADJ_TYPE          which weight method
RELATIVE_INDEX                the security's primary index
EQY_REL_INDEX                 default benchmark
INDEX_TICKER                  index ticker for an index member
```

## Trading / market microstructure

```
VOLUME_AVG_30D, VOLUME_AVG_3M,
TOT_BUY_VOL_TODAY, TOT_SELL_VOL_TODAY,
SHORT_INT, SHORT_INT_RATIO, EQY_SHORT_RATIO_DAYS,
PX_VOLUME_AVG_3M, EQY_TURNOVER_PCT,
LAST_TRADE_PRICE_TIME_TODAY_REALTIME (RT field),
SPREAD_BID_ASK
```

## Volatility / risk

```
HISTORICAL_VOLATILITY_30D, HISTORICAL_VOLATILITY_60D,
HISTORICAL_VOLATILITY_90D, HISTORICAL_VOLATILITY_260D,
EQY_BETA_RAW (1Y), EQY_BETA_ADJ_OVERRIDABLE,
30DAY_IMPVOL_100.0%MNY_DF (ATM 30d implied vol),
60DAY_IMPVOL_100.0%MNY_DF
```

## ETFs, REITs, funds (special equity types)

ETF-specific fields:

```
FUND_NET_ASSET_VAL                 latest NAV
FUND_TOTAL_ASSETS                  AUM
FUND_EXPENSE_RATIO
FUND_OBJECT_LONG, FUND_BENCHMARK_PROSPECTUS
FUND_INCEPT_DT
FUND_HOLDINGS                      BULK — holdings (security, weight, position)
ETF_TRACKING_INDEX_TICKER          underlying index
FUND_NET_FLOW                      flows
ETF_INAV                           intra-day NAV ticker
ETF_PREMIUM_DISCOUNT
```

REIT-specific:

```
FFO_PER_SHARE                      Funds From Operations per share
AFFO_PER_SHARE
REIT_INVESTMENT_PROP_GROSS
REIT_DEBT_TO_GROSS_PROP
```

## Common research recipes (sketch)

```python
# Universe = current SX5E members
members = bds("SX5E Index", "INDX_MEMBERS")
tickers = [m["Member Ticker and Exchange Code"] + " Equity" for m in members]

# Latest fundamentals + estimates panel
panel = bdp(tickers,
            ["PX_LAST","CUR_MKT_CAP","TRAIL_12M_NET_INC",
             "BEST_EPS","BEST_PE_RATIO","EQY_DVD_YLD_IND",
             "RETURN_COM_EQY","NET_DEBT","BS_TOT_ASSET",
             "GICS_SECTOR_NAME"],
            BEST_FPERIOD_OVERRIDE="1FY",
            EQY_FUND_CRNCY="EUR")

# Quarterly EPS history for a PEAD panel
quarterly = []
for t in tickers:
    df = bds(t, "EARN_ANN_DT_TIME_HIST_WITH_EPS")
    df["ticker"] = t
    quarterly.append(df)
panel_q = pd.concat(quarterly)
```

See [docs/recipes/earnings_panel.md](../recipes/earnings_panel.md) for the
full version.

## Specific traps

- **Total return**, not price, for backtests. `TOT_RETURN_INDEX_GROSS_DVDS`
  is the right field. Don't reinvent the wheel adjusting `PX_LAST`.
- **Survivor bias**: `INDX_MEMBERS` is point-in-time at request, not
  historical. Use `INDX_MWEIGHT_HIST` with `END_DATE_OVERRIDE` to get
  composition at a past date — and remember that delisted constituents
  still exist in Bloomberg under their original ticker (their
  `MARKET_STATUS` flips to `DELISTED`).
- **Currency**: `CUR_MKT_CAP` is in `EQY_FUND_CRNCY`, not always USD.
  Re-currency with the override.
- **Cross-listed equities**: `EQY_FUND_TICKER` is the canonical primary
  listing — useful for de-duplicating panels.
- **ADR / GDR depth**: `ADR_UNDL_TICKER` / `ADR_RATIO` link a depositary
  receipt back to its underlying.
