# BLPAPI / Bloomberg Directions

A working encyclopedia of Bloomberg's `blpapi` SDK and the Bloomberg data
universe, organised so you can land on any asset class or region and pull the
right tickers, fields and overrides without leaving the repo.

The text is opinionated for **research workflows** (panel construction,
factor work, PEAD, yield-curve and credit-spread monitoring) rather than
execution. Code samples assume DAPI on `localhost:8194` unless stated.

## How to navigate

| If you want… | Read first |
|---|---|
| Get a session running | [docs/01_install.md](docs/01_install.md), [docs/02_authentication.md](docs/02_authentication.md), [docs/03_session_services.md](docs/03_session_services.md) |
| Pull a snapshot, history, intraday bars or ticks | [docs/04_request_types.md](docs/04_request_types.md) |
| Stream live prices | [docs/05_subscriptions.md](docs/05_subscriptions.md) |
| Find the right field / override | [docs/06_fields_and_overrides.md](docs/06_fields_and_overrides.md), [cheatsheets/field_index.md](cheatsheets/field_index.md), [cheatsheets/overrides_index.md](cheatsheets/overrides_index.md) |
| Iterate a bulk field (members, dividends, holdings…) | [docs/07_bulk_fields.md](docs/07_bulk_fields.md) |
| Stay under the daily-hit cap | [docs/08_limits.md](docs/08_limits.md) |
| Skip the boilerplate (xbbg, pdblp) | [docs/09_wrappers.md](docs/09_wrappers.md) |
| Debug a silent / empty response | [docs/10_diagnostics.md](docs/10_diagnostics.md) |

### Asset-class deep dives
- [Equities](docs/asset_classes/equities.md) — listings, fundamentals, estimates, corporate actions
- [Bonds](docs/asset_classes/bonds.md) — sovereigns, corporates, ID conventions, YAS analytics
- [Commodities](docs/asset_classes/commodities.md) — energy, metals, ags, generic vs specific futures
- [Currencies (FX)](docs/asset_classes/currencies.md) — spot, forwards, NDFs, crosses, vol
- [Futures](docs/asset_classes/futures.md) — equity index, bond, rate, commodity contracts; rolls
- [Swaps](docs/asset_classes/swaps.md) — IRS / OIS, basis, CDS, asset-swap
- [Forwards & Spot](docs/asset_classes/forwards.md) — FX forwards, NDFs, deliverable forwards
- [Options & Vol](docs/asset_classes/options.md) — listed equity / index / FX options, IVOL surfaces
- [ETFs & Funds](docs/asset_classes/etfs_funds.md) — ETFs, mutual funds, holdings

### Regions
- [United States](docs/regions/united_states.md)
- [Europe (EU + Switzerland + Nordics)](docs/regions/europe.md)
- [United Kingdom](docs/regions/united_kingdom.md)
- [Japan](docs/regions/japan.md)
- [China & Hong Kong](docs/regions/china.md)
- [Emerging Markets (LatAm, EM-Asia, EM-EMEA)](docs/regions/emerging_markets.md)

### Recipes (end-to-end pipelines)
- [Earnings panel for PEAD](docs/recipes/earnings_panel.md)
- [Cross-sectional factor panel](docs/recipes/factor_panel.md)
- [Yield curves (govt + swap)](docs/recipes/yield_curve.md)
- [Credit spreads (CDS + cash)](docs/recipes/credit_spreads.md)
- [FX carry & basis](docs/recipes/fx_carry.md)
- [Futures curve & rolls](docs/recipes/futures_curve.md)

### Excel × Bloomberg (parallel to the Python guide)
A full encyclopedia of the Bloomberg Excel Add-in, biased toward
fixed-income workflows. Same tickers and overrides as the Python
guide, expressed as `=BDP(...)` / `=BDH(...)` / `=BDS(...)`.

- [Excel index — start here](excel/README.md)
- [Install & ribbon setup](excel/01_install_and_addin.md)
- [Function reference (BDP / BDH / BDS / BEQS / BCURVE / BSRCH / BQL)](excel/02_function_reference.md)
- [Tickers in cells, overrides, calendars](excel/03_tickers_overrides_calendars.md)
- [Curves in worksheets](excel/04_curves.md)
- [Real-time, RTD, BLPSubscribe](excel/05_realtime_rtd.md)
- [VBA, automation, xlwings](excel/06_vba_automation.md)
- Fixed-income deep dives: [bonds](excel/fixed_income/bonds.md) ·
  [futures](excel/fixed_income/futures.md) ·
  [swaps](excel/fixed_income/swaps.md) ·
  [currencies](excel/fixed_income/currencies.md) ·
  [rates & money market](excel/fixed_income/rates_money_market.md) ·
  [credit & CDS](excel/fixed_income/credit_cds.md)
- Excel cheatsheets: [quick reference](excel/cheatsheets/excel_quick_reference.md) ·
  [FI field kit](excel/cheatsheets/excel_fi_field_kit.md) ·
  [overrides syntax](excel/cheatsheets/excel_overrides_syntax.md)

### Cheatsheets
- [Yellow keys (market sectors)](cheatsheets/yellow_keys.md)
- [Exchange / pricing-source codes](cheatsheets/exchange_codes.md)
- [Field mnemonic index](cheatsheets/field_index.md)
- [Overrides index](cheatsheets/overrides_index.md)
- [Futures month codes](cheatsheets/month_codes.md)

### Runnable examples (`examples/`)
| File | What it shows |
|---|---|
| `connect_dapi.py` | Minimal sync DAPI session |
| `reference_data.py` | `ReferenceDataRequest` + parsing into a DataFrame |
| `historical_data.py` | EOD time series with overrides |
| `intraday_bars.py` | `IntradayBarRequest` (1-min bars) |
| `intraday_ticks.py` | Tick-by-tick with condition codes |
| `beqs_universe.py` | Saved EQS screen → universe |
| `subscription.py` | Async `mktdata` subscription |
| `bulk_fields.py` | `INDX_MEMBERS`, `DVD_HIST_ALL`, earnings history |
| `futures_chain.py` | `FUT_CHAIN`, generic series, rolls |
| `fx_forwards.py` | Spot, forward points, NDFs |
| `bond_analytics.py` | YAS overrides, OAS / Z-spread |
| `field_search.py` | `//blp/apiflds` discovery |
| `xbbg_quickstart.py` | Same data via `xbbg` wrapper |
| `utils.py` | Shared session helpers + Element → dict |

## Conventions used in this repo

- **Tickers** are written exactly as Bloomberg expects them, including the
  trailing yellow key. e.g. `EDP PL Equity`, `T 4.625 02/15/35 Govt`,
  `CL1 Comdty`, `EURUSD Curncy`, `SPX Index`. Whitespace and case matter.
- **Fields** are uppercase mnemonics (`PX_LAST`, `CUR_MKT_CAP`).
- **Overrides** appear as `(fieldId, value)` pairs appended to the request's
  `overrides` element. Values are strings even when the underlying datum is
  numeric or a date (`YYYYMMDD`).
- **Dates** in requests: `YYYYMMDD` for day-level, `datetime` (UTC) for
  intraday bars / ticks.
- All examples assume Python 3.10+.

## Quick install (recap)

```bash
python -m pip install \
  --index-url=https://blpapi.bloomberg.com/repository/releases/python/simple/ \
  blpapi
# Optional but strongly recommended for research:
python -m pip install xbbg pandas pyarrow
```

You need an active entitlement (DAPI / SAPI / B-PIPE). DAPI is the simplest:
log in to a Bloomberg Terminal on the same machine, leave it running, and the
SDK connects to `localhost:8194` automatically.

## Yellow-key glance

| Suffix | Sector | Examples |
|---|---|---|
| `Equity` | Listed equity (and ETFs, REITs) | `AAPL US Equity`, `EDP PL Equity`, `7203 JT Equity` |
| `Index` | Indices, index futures via generic | `SPX Index`, `SX5E Index`, `PSI20 Index` |
| `Curncy` | FX spot, forwards, NDFs, money-market rates, OIS | `EURUSD Curncy`, `EURUSD3M Curncy`, `USSO10 Curncy` |
| `Comdty` | Commodities (futures, options on futures) | `CL1 Comdty`, `GC1 Comdty`, `TY1 Comdty` |
| `Govt` | Sovereign / supranational debt | `T 4.625 02/15/35 Govt`, `GT10 Govt`, `DBR 2 ½ 08/15/54 Govt` |
| `Corp` | Corporate, agency, supra debt; CDS | `EDP 1 ⅞ 03/14/35 Corp`, `CDX IG CDSI S42 5Y Corp` |
| `Mtge` | MBS, ABS, CMOs | `FNCL 5.5 Mtge` |
| `Muni` | US municipals | |
| `Pfd` | Preferred stock | |
| `M-Mkt` | Money market instruments | |

Full list with ticker patterns lives in
[cheatsheets/yellow_keys.md](cheatsheets/yellow_keys.md).
