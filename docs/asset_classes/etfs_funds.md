# ETFs & Mutual Funds

ETFs use yellow key `Equity` (they trade on exchanges). Open-end
mutual funds use `Equity` too — Bloomberg distinguishes them via
`SECURITY_TYP2`.

## ETFs

### Identification

```
SPY US Equity                SPDR S&P 500
IVV US Equity                iShares S&P 500
VOO US Equity                Vanguard S&P 500
QQQ US Equity                Invesco NASDAQ-100
EZU US Equity                iShares MSCI Eurozone
VGK US Equity                Vanguard FTSE Europe
EWJ US Equity                iShares MSCI Japan
FXI US Equity                iShares China Large-Cap
INDA US Equity               iShares MSCI India
EEM US Equity                iShares MSCI EM
EMB US Equity                iShares JPM EM USD bonds

# European-listed UCITS:
CSPX LN Equity               iShares Core S&P 500 (UCITS)
VUSA LN Equity               Vanguard S&P 500 (UCITS)
EXSA GR Equity               iShares STOXX Europe 600 (Xetra)
SX5EEX GR Equity             Lyxor Eurostoxx 50

# Bond ETFs:
AGG US Equity                iShares Core US Aggregate Bond
LQD US Equity                iShares iBoxx IG Corp
HYG US Equity                iShares iBoxx HY Corp
TLT US Equity                iShares 20+ Year Treasury
IEF US Equity                7-10y Treasury
GOVT US Equity               US Treasury all maturities

# Commodity ETFs:
GLD US Equity                SPDR Gold
SLV US Equity                iShares Silver
USO US Equity                US Oil Fund
UNG US Equity                US Natural Gas Fund
```

### ETF-specific fields

```
FUND_NET_ASSET_VAL                     latest NAV
FUND_TOTAL_ASSETS                      AUM (USD by default)
FUND_EXPENSE_RATIO                     TER (%)
FUND_INCEPT_DT
FUND_OBJECTIVE_LONG, FUND_OBJECT
FUND_BENCHMARK_PROSPECTUS              prospectus benchmark
ETF_TRACKING_INDEX_TICKER              underlying index Bloomberg ticker
ETF_INAV                               ticker of intra-day NAV
ETF_PREMIUM_DISCOUNT                   px vs NAV %
FUND_DOMICILE                          IE, US, LU, ...
FUND_LEGAL_STRUCTURE                   ETF, OEF, SICAV, ...
FUND_GEO_FOCUS, FUND_INDUSTRY_FOCUS, FUND_STRATEGY
FUND_MGMT_COMPANY                      iShares, Vanguard, ...
FUND_BENCHMARK                         actual benchmark used
EQY_FUND_TICKER                        for share-class consolidation
TOTAL_RETURN_LAST_DAY                  1d total return (incl divs)
FUND_DISTR_FREQ                        Annual / Quarterly / ...
FUND_NET_FLOW                          fund flows (recent)
FUND_FLOW_1MO, FUND_FLOW_3MO, FUND_FLOW_YTD
ETF_SHARES_OUT                         shares outstanding
ETF_NUM_HOLDINGS                       number of holdings
```

### Holdings (bulk)

```python
req.append("securities", "SPY US Equity")
req.append("fields",     "FUND_HOLDINGS")
ov = req.getElement("overrides").appendElement()
ov.setElement("fieldId", "FUND_HOLDINGS_OVERRIDE")
ov.setElement("value",   "Y")           # full holdings (otherwise top 10)
ov2 = req.getElement("overrides").appendElement()
ov2.setElement("fieldId", "REFERENCE_DATE")
ov2.setElement("value",   "20250502")   # historical holdings
```

Row schema typically: `Holding`, `Position`, `Position Date`,
`% Net Assets`, `Market Value`, `Currency`, `Holding Ticker`.

Variant:

```
PORTFOLIO_DATA                         when the ETF is set up as PRTU
```

### Premium/discount, creation/redemption

```
PX_LAST                       last traded price
FUND_NET_ASSET_VAL            most recent NAV
PX_LAST_NAV                   end-of-day NAV
ETF_PREMIUM_DISCOUNT          (px - NAV) / NAV %
ETF_CREATION_UNIT_SIZE        50,000 typical for US
```

## Open-end mutual funds

Mutual funds quote NAV daily, not intra-day. `SECURITY_TYP2 = OEF`.

```
VFINX US Equity              Vanguard 500 Index Investor
VTSAX US Equity              Vanguard Total Stock Market Admiral
ANCFX US Equity              American Funds Capital Income
PIMIX US Equity              PIMCO Income Inst
```

### Fund fields specific to OEFs

```
FUND_NET_ASSET_VAL                   NAV per share
FUND_NET_ASSET_VAL_DAY_BEFORE
FUND_TOTAL_ASSETS
FUND_EXPENSE_RATIO
FUND_PRIMARY_PROSPECTUS_BENCHMARK
FUND_RTG_CLASS_FOCUS                 class A/B/C/I etc
FUND_MGMT_FEE
FUND_LOAD                            front-end load %
FUND_REDEMP_FEE
FUND_TURNOVER_RATIO
FUND_INCEPT_DT
FUND_INVMT_OBJECTIVE
FUND_FAMILY_NAME
FUND_PORT_MGR                        portfolio manager(s)
FUND_PORT_MGR_TENURE
FUND_DISTR_LAST                      most recent distribution
```

## Performance metrics

```
TOT_RETURN_INDEX_GROSS_DVDS           gross-of-tax TR series (preferred)
TOT_RETURN_INDEX_NET_DVDS             net-of-tax TR
1MO_TOT_RETURN, 3MO_TOT_RETURN, 1YR_TOT_RETURN, 3YR_TOT_RETURN, 5YR_TOT_RETURN
YTD_TOT_RETURN
TOT_RETURN_SINCE_INCEP

ALPHA_3YR, BETA_3YR, R_SQUARED_3YR
SHARPE_RATIO_3YR, INFORMATION_RATIO_3YR,
TRACKING_ERROR_3YR, DOWNSIDE_DEVIATION_3YR
MAX_DRAWDOWN_3YR, MAX_DRAWDOWN_5YR
SORTINO_3YR
```

## Fund classification

```
FUND_RTG_CLASS_FOCUS               Equity / Fixed Income / Allocation / ...
FUND_GEO_FOCUS                     US / Europe / Global / EM / ...
FUND_OBJECTIVE                     Growth / Income / Blend / ...
FUND_STRATEGY
FUND_BBG_PROVIDER_FOCUS
FUND_INDUSTRY_FOCUS
FUND_MARKET_CAP_FOCUS              Large / Mid / Small / All
LIPPER_GLOBAL_CLASSIFICATION
MORNINGSTAR_CATEGORY
```

## ETF flows / creations / redemptions

```
ETF_FLOW_DAILY, ETF_FLOW_1WK, ETF_FLOW_1MO,
ETF_FLOW_3MO, ETF_FLOW_YTD, ETF_FLOW_1YR
ETF_NET_CREATION_REDEMPTION_DLY    dollar value
ETF_SHARES_OUT_DAY_OVER_DAY        change in shares outstanding
```

Use shares outstanding day-over-day for the cleanest flow proxy
(net creates/redeems × NAV).

## ETF lookup and screening

`ETF <GO>` on Terminal is the screening tool. Programmatic
equivalent:

```python
# Saved EQS screen exporting ETFs:
universe = bdp(blp.beqs("MyETFScreen", typ="PRIVATE").index.tolist(),
               ["FUND_TOTAL_ASSETS","FUND_EXPENSE_RATIO",
                "ETF_TRACKING_INDEX_TICKER","FUND_GEO_FOCUS"])
```

Or build a universe from a benchmark:

```python
# Listings tracking a specific benchmark
bdp(["..."], ["ETF_TRACKING_INDEX_TICKER"])
```

## Regional ETF families to know

| Region | Family | Yellow / suffix |
|---|---|---|
| US-listed UCITS-equivalents | iShares (`IV*`, `EFA`), Vanguard (`V*`) | `US Equity` |
| Europe UCITS Xetra | iShares (`EXS*`), Lyxor, Amundi, Xtrackers | `GR Equity` (Xetra), `LN Equity` (LSE), `IM Equity` (Milan), `FP Equity` (Paris) |
| Japan-listed | Nomura NEXT FUNDS (`13*`) | `JT Equity` |
| HK-listed | iShares China A-share (`2820`), Tracker Fund (`2800`) | `HK Equity` |
| Korea-listed | KODEX (`069500`), TIGER, ARIRANG | `KS Equity` |
| Brazil | iShares (BOVA11), iboves | `BS Equity` |
| Mexico | NAFTRAC | `MM Equity` |

Full list of pricing-source codes: see
[cheatsheets/exchange_codes.md](../../cheatsheets/exchange_codes.md).

## Pitfalls

- **NAV vs price**: ETFs trade at price; NAV is computed at close.
  For backtests, prefer `TOT_RETURN_INDEX_GROSS_DVDS` (built off price)
  unless you specifically want NAV-based.
- **Distribution treatment**: gross vs net divs differ for funds
  domiciled in withholding-tax jurisdictions (Ireland, Luxembourg).
  Pick one and document.
- **Cross-listing**: same ETF often trades on multiple European venues
  (`CSPX LN`, `CSPX SW`, `CSPX IM`) — they have separate liquidity but
  share NAV. For strategies that consume liquidity, address the venue
  explicitly.
- **Synthetic vs physical**: `SWAP_TYPE` (or examining
  `FUND_HOLDINGS`) tells you whether the ETF holds the underlyings or
  uses a swap. Affects tracking error and counterparty risk.
- **Securities lending revenue**: `FUND_SECLEND_INCOME_RATIO` exists
  but isn't always populated — check before using.
