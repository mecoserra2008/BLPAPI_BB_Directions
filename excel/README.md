# Excel × Bloomberg

The Bloomberg Excel Add-in is a different surface from `blpapi` (the
Python SDK) — same data, different formula language and very
different ergonomics. This section covers it end-to-end with a bias
toward **fixed income**: bonds, swaps, futures, rates, currencies,
credit/CDS.

## How to navigate

| If you want… | Read first |
|---|---|
| Get the add-in installed and the ribbon working | [01_install_and_addin.md](01_install_and_addin.md) |
| Master `BDP` / `BDH` / `BDS` (+ `BEQS`, `BCURVE`, `BSRCH`, `BQL`) | [02_function_reference.md](02_function_reference.md) |
| Write tickers as cell formulas, pass overrides, control calendars | [03_tickers_overrides_calendars.md](03_tickers_overrides_calendars.md) |
| Build a yield/swap curve in a worksheet | [04_curves.md](04_curves.md) |
| Stream real-time prices and quotes | [05_realtime_rtd.md](05_realtime_rtd.md) |
| Automate refresh, build batch sheets in VBA / `xlwings` | [06_vba_automation.md](06_vba_automation.md) |

### Fixed-income deep dives
- [Bonds](fixed_income/bonds.md) — Govt / Corp / Mtge / Muni, ID lookup, YAS in Excel
- [Futures](fixed_income/futures.md) — bond + IR futures, generic vs specific, CTD, implied repo
- [Swaps](fixed_income/swaps.md) — IRS / OIS / inflation / XCCY basis curves
- [Currencies](fixed_income/currencies.md) — spot, forwards, NDFs, vol grids
- [Rates & money market](fixed_income/rates_money_market.md) — SOFR / ESTR / SONIA / TONA, FRAs, policy rates
- [Credit & CDS](fixed_income/credit_cds.md) — single-name + index CDS, ASW vs Z-spread

### Cheatsheets
- [Excel quick reference](cheatsheets/excel_quick_reference.md) — one page, every formula
- [FI field kit](cheatsheets/excel_fi_field_kit.md) — `BDP` / `BDH` / `BDS` field lists for fixed income
- [Overrides syntax](cheatsheets/excel_overrides_syntax.md) — paired-argument overrides, common gotchas

## What's where vs the Python side

The Excel guide and the `blpapi` guide use **the same tickers, fields
and overrides**. If you've already read the Python side, you can
think of the Excel section as a translation layer: same data, but
expressed as `=BDP(...)` / `=BDH(...)` / `=BDS(...)` instead of
`session.sendRequest(...)`.

| Concept | Python | Excel |
|---|---|---|
| Snapshot | `ReferenceDataRequest` | `=BDP(security, field, [ovr1, val1], …)` |
| History | `HistoricalDataRequest` | `=BDH(security, field, start, end, [options])` |
| Bulk / table | `ReferenceDataRequest` (bulk field) | `=BDS(security, field, [overrides])` |
| Equity screen | `BeqsRequest` | `=BEQS(screen, screenType, …)` |
| Curve | `//blp/refdata` curve queries | `=BCURVE(curve_id, date, points)` |
| Security search | `//blp/instruments` | `=BSRCH(domain)` |
| Modern DSL | n/a | `=BQL(universe, expression)` |
| Real-time | `Subscription` | `=BDP(…)` with real-time refresh, or `BLPSubscribe` |

If a ticker / field / override works in one, it works in the other.
The two guides are kept in sync.

## Default assumptions in this section

- **Excel 2016 or later on Windows.** The COM add-in only works on
  Windows. Mac users use Bloomberg Terminal in a Citrix session or
  drive Excel from Python via the Python SDK.
- **Bloomberg Anywhere or Terminal** logged in on the same machine
  (Excel calls `bbcomm` over loopback, same as DAPI).
- **`BLP API.xll`** registered as an add-in (this is installed by
  Bloomberg's installer in `C:\blp\API`).
- Functions / examples use UK/Portuguese English-locale Excel —
  comma argument separator. On semicolon-locale Excel (DE, FR, ES,
  PT-PT default), replace `,` with `;`.

## Quick first formula

Once the add-in is loaded, in any cell:

```
=BDP("EDP PL Equity", "PX_LAST")
```

You should see the last traded price. If you see `#N/A Requesting
Data` and it never resolves, see
[01_install_and_addin.md](01_install_and_addin.md#troubleshooting).

## Reading order

If you've never touched the BBG Excel add-in:

1. Install + ribbon ([01](01_install_and_addin.md))
2. The three core functions ([02](02_function_reference.md))
3. Tickers from cells + overrides ([03](03_tickers_overrides_calendars.md))
4. One FI deep dive that matches what you do most ([fixed_income/](fixed_income/))
5. Refresh control + VBA when you start automating ([06](06_vba_automation.md))
