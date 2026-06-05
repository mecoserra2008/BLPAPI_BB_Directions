# 01 · Install & Excel Add-in Setup

The Bloomberg Excel Add-in is bundled with the Terminal install. You
do not download it from anywhere separate.

## Prerequisites

| Requirement | Notes |
|---|---|
| Windows | Mac is **not** supported for the COM add-in. Use Bloomberg Anywhere via Citrix, or drive Excel from Python via `blpapi` + `xlwings`. |
| Microsoft Excel 2016+ (32 or 64-bit) | The add-in ships with both bit-widths; the installer picks the right one for your Excel. |
| Bloomberg Terminal logged in | The add-in connects to the local `bbcomm` service. If the Terminal is locked / not logged in, formulas return `#N/A Requesting Data` indefinitely. |
| Bloomberg Anywhere desktop | Same as above. |
| .NET Framework 4.7.2+ | Pre-installed on supported Windows versions. |
| Visual C++ runtimes | Pre-installed by the BBG installer. |

## What the installer puts on disk

| Path | Contents |
|---|---|
| `C:\blp\API\` | Add-in DLLs, XLLs, registry entries |
| `C:\blp\API\Office Tools\` | `BLP API.xll` (the loader) |
| `C:\blp\API\Office Tools\BloombergUI.xla` | Ribbon / menu hookup |
| `C:\blp\DAPI\` | `bbcomm.exe` (the local API bridge) |
| `%APPDATA%\Bloomberg\` | User-level config |
| `%APPDATA%\Bloomberg\Office\` | Excel-specific options, default refresh behaviour |

The single most useful path is `C:\blp\API\Office Tools\` — when the
add-in disappears from the ribbon, this is where you go to re-add
it.

## Enabling the add-in

If the **Bloomberg** ribbon tab is missing:

1. Excel → **File → Options → Add-Ins**.
2. Bottom: **Manage:** drop-down → **Excel Add-ins** → **Go…**.
3. Tick **Bloomberg API** (or **BLP API**). If absent, click
   **Browse…** and pick `C:\blp\API\Office Tools\BLP API.xll`.
4. Repeat with **Manage:** **COM Add-ins** → tick **Bloomberg
   Excel Tools** if present.
5. Restart Excel.

When working you should see three ribbon tabs:

- **Bloomberg** — the main one. Refresh, function builders, FA, GP,
  template gallery.
- **BBG Data** — same family, the modern name on newer installs.
- **Real-Time** — if your entitlement includes streaming.

## First connection test

```
=BDP("AAPL US Equity", "PX_LAST")
```

Three possible outcomes:

| Cell shows | Meaning |
|---|---|
| A number | Add-in healthy. Done. |
| `#N/A Requesting Data` then a number | Normal — first call wakes the connection. |
| `#N/A Requesting Data` permanently | `bbcomm` not running / Terminal locked. See troubleshooting. |
| `#NAME?` | Add-in not loaded. Re-tick in Add-Ins. |
| `#N/A Invalid Security` | Yellow key wrong. Try `AAPL UQ Equity` or check via `DES <GO>`. |
| `#N/A Field Not Applicable` | Field exists but doesn't apply to this security type. |

## Bloomberg Anywhere vs Terminal vs SAPI

| Install type | Excel add-in works |
|---|---|
| Bloomberg Terminal (desktop) | Yes — connects to local `bbcomm` (`127.0.0.1:8194`). |
| Bloomberg Anywhere (biometric login) | Yes — same local `bbcomm`, but session is bound to the biometric login. |
| SAPI server | Yes — point `bbcomm` config at the SAPI server's IP. Set under **Bloomberg → Settings → Connection**. |
| B-PIPE | Yes — typically via SAPI-side gateway; users still use the local add-in. |

For **Citrix / Remote Desktop** users: Excel on the Citrix host
connects to the *Citrix-side* `bbcomm`, which talks to whichever
Terminal you're logged into in that session. Local Excel on your
laptop talks to your *local* Terminal. They are two separate
add-ins.

## 32-bit vs 64-bit gotchas

- **Excel bitness must match installed add-in bitness.** Office
  365 has been default-64-bit since 2019; if your Excel is 64-bit
  and the BBG installer only deployed the 32-bit add-in, the
  ribbon stays blank.
- Check Excel bitness: **File → Account → About Excel** → look at
  the very end of the version string.
- Re-run the BBG installer (`Software Install <GO>` on the
  Terminal, or `C:\blp\API\dapiinstall.exe`) to refresh the right
  bitness.

## Ribbon tour (Bloomberg tab)

| Group | Items | What they do |
|---|---|---|
| Refresh | **Refresh Worksheet**, **Refresh All**, **Refresh Selection** | Force re-pull. Tied to `Application.Run "BLP.RefreshAll"` (see [06_vba_automation.md](06_vba_automation.md)). |
| Templates | **Templates**, **Spreadsheet Builder**, **Worksheet Library** | Pre-built workbooks (FA, GIP, EQS, OAS1, FIRC, etc.). |
| Charts | **Spreadsheet Builder Chart** | Interactive chart on top of BBG data. |
| Data | **Import Data**, **Field Search**, **Find Securities** | `FIBO` / `FLDS` / `SECF` style search inside Excel. |
| Real-Time | **Subscribe**, **Cancel Subscriptions** | Stream control. |
| Settings | **Options**, **Diagnostics** | Connection mode (DAPI / SAPI / B-PIPE), refresh defaults, logging level. |
| Help | **About**, **Bloomberg Help (`WAPI <GO>`)** | API Help inside Terminal. |

The **Spreadsheet Builder** is a code-free dialog that emits `BDP` /
`BDH` / `BDS` formulas for you — useful for discovery, less useful
once you know the syntax.

## Co-existence with `blpapi` Python

Excel and Python both go through the same local `bbcomm`. No
conflict in normal use. Two things to know:

- **Hit counter is shared.** Pulls from Excel count against the
  same ~500K data-point daily cap as Python pulls. `API <GO>`
  on the Terminal shows combined consumption.
- **`xlwings`** lets Python orchestrate Excel formulas: you can
  write `BDH` calls into cells from Python, refresh them, then
  read the values back. See
  [06_vba_automation.md](06_vba_automation.md).

## Connection settings

**Bloomberg → Options** (or right-click any BBG ribbon button →
**Settings**):

| Setting | Meaning |
|---|---|
| **Connection** | Local DAPI / Remote SAPI / B-PIPE |
| **Refresh** | Manual, On Workbook Open, On Cell Edit, Scheduled |
| **Default fill** | `PREVIOUS_VALUE` vs `NIL_VALUE` for non-trading days |
| **DPDF override** | Use Terminal's `DPDF <GO>` defaults — turn OFF for reproducibility |
| **Logging** | `Trace` / `Info` / `Error`; logs live in `%APPDATA%\Bloomberg\Office\` |

For research-grade workbooks: **DPDF override OFF**, **Manual
refresh**, **Default fill** explicit per formula.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `#NAME?` | Add-in not loaded | File → Options → Add-Ins → tick BLP API |
| `#N/A Requesting Data` forever | `bbcomm` not running | Terminal locked / not logged in; restart `bbcomm` from `C:\blp\API\dde\bbcomm.exe` |
| `#N/A N/A` after refresh | Entitlement not active for the security | Check `EUNI <GO>` for exchange entitlements |
| `#N/A Field Not Applicable` | Wrong field for this asset class | Try the field in `<security> FLDS <GO>` first |
| Ribbon tab missing on every open | XLL not auto-loading | Move `BLP API.xll` to `%APPDATA%\Microsoft\Excel\XLSTART\` |
| Slow workbook on open | All formulas refreshing at once | Set **Refresh on Open: OFF**, then refresh sections via VBA |
| Workbook crashes Excel | Too many simultaneous subscriptions | Cap concurrent subs <500, drop `interval=` higher |
| Excel hangs ~30s after refresh | Network timeout to gateway | Lower `Refresh Timeout` in Options |
| Different value vs Terminal | DPDF / pricing source mismatch | Pin `UseDPDF=N` and explicit `Quote=C` |

`bbcomm` diagnostics:

```cmd
:: in cmd.exe
C:\blp\API\dde\bbcomm.exe -dl              :: print connection log
netstat -ano | findstr :8194               :: confirm port is listening
tasklist | findstr bbcomm                  :: confirm process is up
```

If `bbcomm` is dead: kill any orphaned `bbcomm.exe` process, then
launch a new Terminal session (it auto-spawns `bbcomm`).

## Where logs live

| Log | Path |
|---|---|
| Add-in trace | `%APPDATA%\Bloomberg\Office\<date>.log` |
| `bbcomm` | `%APPDATA%\Bloomberg\Office\bbcomm.log` |
| API trace | `%APPDATA%\Bloomberg\API\logs\*.log` |

Set log level via **Bloomberg → Options → Diagnostics → Trace**.

## Recommended Excel-side defaults for research

In **Bloomberg → Options**:

- **Refresh: Manual**
- **Refresh on Open: OFF**
- **Use DPDF: OFF** (forces explicit `cshAdj*` flags)
- **Default Calendar: NTM** (next trading-month or your local
  market — depends on your work)
- **Default Period: D** (daily, the safe default)
- **Logging: Info**

Then in the workbook itself:

- Always pin `Per=`, `Fill=`, `Days=` on every `BDH`.
- Always pin overrides explicitly — never rely on DPDF.
- For point-in-time consensus pin `BEST_DATA_RELEASE_DT`.
