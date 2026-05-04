# Yellow Keys (market sectors)

The trailing word in every Bloomberg ticker. Determines schema,
fields, and how the security is interpreted.

| Yellow key | Sector | Examples |
|---|---|---|
| `Equity` | Listed equities, ETFs, REITs, ADRs/GDRs, preferred stock, single-stock futures | `AAPL US Equity`, `EDP PL Equity`, `7203 JT Equity`, `SPY US Equity`, `RIO LN Equity`, `CSPX LN Equity` |
| `Index` | Indices (price + total-return), index futures, index options | `SPX Index`, `SX5E Index`, `NKY Index`, `PSI20 Index`, `ES1 Index`, `SPX 12/19/25 C5000 Index` |
| `Curncy` | FX spot, FX forwards, NDFs, money-market rates, OIS rates, swap rates, FX vol, FX-listed-futures, precious-metal spot | `EURUSD Curncy`, `EURUSD3M Curncy`, `XAU Curncy`, `USSO10 Curncy`, `EUBSC10 Curncy`, `EC1 Curncy` |
| `Comdty` | Commodity futures + options on futures, bond futures, rate futures (CME/CBOT/ICE/Eurex/LME/etc.) | `CL1 Comdty`, `GC1 Comdty`, `TY1 Comdty`, `RX1 Comdty`, `SR3A Comdty`, `LMCADS03 LME Comdty` |
| `Govt` | Sovereign debt, supranationals, agencies, T-bills, generic on-the-run | `T 4.625 02/15/35 Govt`, `DBR 2 ½ 08/15/54 Govt`, `GT10 Govt`, `GTGBP10Y Govt`, `B 0 ⅛ 12/12/25 Govt` |
| `Corp` | Corporate debt (IG, HY, hybrids), covered bonds, supras (sometimes), CDS (single-name + indices) | `EDP 1 ⅞ 03/14/35 Corp`, `JPM 4 ½ 06/15/30 Corp`, `EDPPL CDS USD SR 5Y D14 Corp`, `CDX IG CDSI S42 5Y Corp` |
| `Mtge` | Mortgage-backed securities (US agency MBS, CMOs, ABS) | `FNCL 5.5 Mtge`, `GNCL 6 Mtge`, `FNCT 5 Mtge`, `FHLMC 5 02/15/55 Mtge` |
| `Muni` | US municipal bonds | `NYC 5 06/01/35 Muni` |
| `Pfd` | Preferred stock | `JPM-A US Pfd`, `BAC-Q US Pfd` |
| `M-Mkt` | Money-market instruments: CD, commercial paper, BAs, repo | `CP1M Index` style + actual CP/CD tickers |
| `LME` | LME-specific contracts (also under Comdty for LMEX-listed) | mostly addressed via Comdty |

## How to choose the right key

When in doubt:

1. Ask `DES <GO>` on the Terminal with your guess — Bloomberg shows
   the canonical ticker including yellow key.
2. Use `ID <GO>` to resolve any ISIN/CUSIP/SEDOL → Bloomberg ticker
   (with key).
3. Heuristic by purpose:
   - It's a stock → `Equity`
   - It's a national/regional benchmark → `Index`
   - It's an FX rate, money-market rate, or swap → `Curncy`
   - It's an oil / metal / ag future or a bond/rate future → `Comdty`
   - It's a government or supra bond → `Govt`
   - It's a company-issued bond or CDS → `Corp`
   - It's a mortgage-backed instrument → `Mtge`

## Yellow key & the schema

The schema returned by the API (which fields exist on a security) is
determined by the yellow key. A few examples of fields that are
*only* meaningful on certain keys:

| Key | Key-specific fields |
|---|---|
| `Equity` | `EQY_SH_OUT`, `EQY_FREE_FLOAT_PCT`, `BEST_EPS`, `DVD_HIST_ALL`, `EARN_ANN_DT`, `BICS_*`, `GICS_*` |
| `Index` | `INDX_MEMBERS`, `INDX_MWEIGHT_HIST`, `INDX_DIV_YIELD` |
| `Curncy` | `FWD_POINTS`, `IMPL_YIELD_PCT`, `SPOT_PRICE` |
| `Comdty` | `FUT_CHAIN`, `FUT_VAL_PT`, `FUT_CONT_SIZE`, `OPEN_INT`, `FUT_DLV_DT_FIRST` |
| `Govt` / `Corp` | `YLD_YTM_MID`, `OAS_SPREAD_MID`, `Z_SPRD_MID`, `MOD_DUR`, `RTG_*`, `MATURITY` |
| `Mtge` | `WAC`, `WAM`, `WALA`, `PSA_SPEED`, `CPR_3MO`, `OUT_BAL` |
| `Pfd` | many `Equity` fields plus `CV_*` for convertibles |

A field that doesn't apply on a given yellow key returns either an
empty `fieldData` or appears under `fieldExceptions` with category
`BAD_FLD`.

## Cross-listings and yellow keys

The same underlying entity can appear under different yellow keys:

- `BABA US Equity` (NYSE ADR, equity yellow key)
- `9988 HK Equity` (HK primary, equity)
- `BABA 4 ⅜ 11/14/29 Corp` (Alibaba bond)
- Alibaba CDS doesn't actively quote → check for `BABACN CDS USD SR 5Y D14 Corp`

The yellow key never changes for a single security; switching key
switches *what kind of object* you're looking at.

## Less-used but valid yellow keys

| Key | Use |
|---|---|
| `BVAL` | Bloomberg evaluated pricing service (model-derived) — usually as a `pricingSource` |
| `CMDTY` | Older variant of Comdty (rare in current data) |
| `Cmdty` | Same |
| `Crncy` | Older spelling of Curncy; both work |
| `Pref` | Older spelling of Pfd |
