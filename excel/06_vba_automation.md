# 06 · VBA & Automation

When your workbook needs to do more than recompute on edit —
scheduled refreshes, batch pulls across hundreds of securities,
exporting to parquet, alerting on price moves — Excel-side
automation is the next step. The toolbox:

- **VBA** macros calling the Bloomberg add-in via `Application.Run`.
- **`BlpApi.dll` COM** for finer-grained control from VBA.
- **Python via `xlwings`** to drive workbooks programmatically.
- **Power Automate / Office Scripts** for cloud-based scheduling
  (limited Bloomberg compatibility — usually only delayed data).

## 6.1 Basic refresh from VBA

The add-in exposes named subs accessible via `Application.Run`.

```vba
Sub RefreshAll()
    Application.Run "BLP.RefreshAll"
End Sub

Sub RefreshSheet()
    Application.Run "BLPRefreshCurrentSelection"
End Sub

Sub RefreshWorkbook()
    Application.Run "BLPRefreshAllStatic"
End Sub
```

Names vary slightly between add-in versions:

| Newer | Older |
|---|---|
| `BLP.RefreshAll` | `BLPRefreshAll` |
| `BLPRefreshAllStatic` | `BLPDataRefresh` |
| `BLP.RefreshActiveSheet` | `BLPRefreshSheet` |

Check what's available: in VBA `Immediate` window type
`Application.Run "BLP."` then `Ctrl+Space`, or open the add-in's
`.xla` in the VBE.

## 6.2 Scheduled refresh

```vba
Public NextRun As Date

Sub ScheduleRefresh()
    NextRun = Now + TimeValue("00:05:00")    ' every 5 minutes
    Application.OnTime NextRun, "TimedRefresh"
End Sub

Sub TimedRefresh()
    Application.Run "BLP.RefreshAll"
    ScheduleRefresh
End Sub

Sub StopRefresh()
    On Error Resume Next
    Application.OnTime NextRun, "TimedRefresh", , False
End Sub
```

Trigger `ScheduleRefresh` from a button or from `Workbook_Open`.

## 6.3 Waiting for the data to arrive

`BLP.RefreshAll` returns *immediately* — the actual data arrives
asynchronously. If you need to act on the values:

```vba
Sub RefreshAndWait()
    Application.Run "BLP.RefreshAll"

    Dim t As Double
    t = Timer
    Do While Timer - t < 30   ' wait up to 30s
        DoEvents
        If Application.WorksheetFunction.CountIf(
              Range("MyDataRange"), "#N/A Requesting Data") = 0 Then
            Exit Do
        End If
    Loop

    ' now safe to read values
End Sub
```

`#N/A Requesting Data` is the in-flight marker. Polling `CountIf`
across a known range tells you when the wave has cleared.

Better practice: name the data range and poll only the named
range, not the whole sheet.

## 6.4 Exporting a refreshed range to CSV / parquet

```vba
Sub ExportNamedRangeToCsv()
    Dim rng As Range
    Set rng = ThisWorkbook.Names("BondPanel").RefersToRange

    Dim path As String
    path = ThisWorkbook.Path & "\bond_panel_" & _
           Format(Now, "yyyymmdd_hhnnss") & ".csv"

    Open path For Output As #1
    Dim r As Long, c As Long, line As String
    For r = 1 To rng.Rows.Count
        line = ""
        For c = 1 To rng.Columns.Count
            line = line & rng.Cells(r, c).Value
            If c < rng.Columns.Count Then line = line & ","
        Next c
        Print #1, line
    Next r
    Close #1
End Sub
```

For parquet output, drive from Python via `xlwings`:

```python
import xlwings as xw
import pandas as pd

wb = xw.Book("BondPanel.xlsm")
sheet = wb.sheets["Panel"]
sheet.api.Application.Run("BLP.RefreshAll")

# Wait
import time
for _ in range(60):
    if "#N/A Requesting Data" not in sheet.range("BondPanel").value:
        break
    time.sleep(1)

df = sheet.range("BondPanel").options(pd.DataFrame, header=1, index=0).value
df.to_parquet("bond_panel.parquet")
wb.close()
```

## 6.5 Catching `#N/A` in VBA

`#N/A` is a special error value in Excel; testing for it requires
care.

```vba
If IsError(Range("A2").Value) Then
    If Range("A2").Value = CVErr(xlErrNA) Then
        ' is an #N/A
    End If
End If
```

Or via `WorksheetFunction.IsNA`:

```vba
If Application.WorksheetFunction.IsNA(Range("A2").Value) Then
    ' was #N/A
End If
```

For the specific Bloomberg strings (`#N/A Requesting Data`,
`#N/A Invalid Security`, `#N/A Field Not Applicable`):

```vba
Dim v As Variant
v = Range("A2").Text          ' .Text gives the displayed string
If InStr(v, "Requesting Data") > 0 Then ...
If InStr(v, "Invalid Security") > 0 Then ...
If InStr(v, "Field Not Applicable") > 0 Then ...
```

`.Text` (not `.Value`) returns the displayed text including the
Bloomberg-specific extension.

## 6.6 Batch pulls via VBA

For pulling 500 bonds × 10 fields without manually wiring 5,000
formulas:

```vba
Sub BuildBondPanel()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("Panel")
    Dim bonds() As Variant
    bonds = ThisWorkbook.Names("BondTickers").RefersToRange.Value

    Dim fields() As Variant
    fields = Array("PX_LAST", "YLD_YTM_MID", "DUR_ADJ_MID", _
                   "Z_SPRD_MID", "OAS_SPREAD_MID", _
                   "RTG_BB_COMPOSITE", "MATURITY", "CRNCY", _
                   "AMT_OUTSTANDING", "ISSUER_INDUSTRY")

    Dim r As Long, c As Long
    For r = 1 To UBound(bonds, 1)
        ws.Cells(r + 1, 1).Value = bonds(r, 1)
        For c = 0 To UBound(fields)
            ws.Cells(r + 1, c + 2).Formula = _
                "=BDP(""" & bonds(r, 1) & """, """ & fields(c) & """)"
        Next c
    Next r

    Application.Run "BLP.RefreshAll"
End Sub
```

The macro builds the formulas; the add-in pulls. For very large
universes split into batches of 100 — the add-in handles back-
pressure better in chunks.

## 6.7 `BlpComObject` — direct API from VBA

For low-latency or schema-driven work, talk to the BBG COM library
directly. Requires `BloombergUI.tlb` / `blpapi3_64.dll` registered
(default on Bloomberg-installed machines).

```vba
Dim blpApi As Object
Set blpApi = CreateObject("Bloomberg.Data.1")

' Reference Data
Dim req As Object
Set req = blpApi.CreateReferenceDataRequest
req.AddSecurity "EDP PL Equity"
req.AddField "PX_LAST"
req.AddField "BEST_EPS"
req.AddOverride "BEST_FPERIOD_OVERRIDE", "1FY"
req.Send

Do While Not req.IsComplete
    DoEvents
Loop

Dim rows As Variant
rows = req.GetResult           ' 2D variant array

' Inspect
Dim r As Long
For r = 1 To UBound(rows, 1)
    Debug.Print rows(r, 1) & " | " & rows(r, 2)
Next r
```

Trade-offs vs `BDP` formulas:

| Aspect | `BDP` | COM (`Bloomberg.Data.1`) |
|---|---|---|
| Simplicity | Easy | Verbose |
| Latency | Round-trips per cell | One round-trip for the whole request |
| Schema access | Limited | Full `fieldExceptions`, `securityError`, etc. |
| Threading | Excel re-eval | Background thread, doesn't block UI |

For research workflows: stay with `BDP` / `BDH` / `BDS`. For
production extract pipelines: COM.

## 6.8 Workbook open / close hooks

In `ThisWorkbook` module:

```vba
Private Sub Workbook_Open()
    ' Don't trigger a refresh on open — leave that explicit.
    Application.DisplayAlerts = False
    Application.ScreenUpdating = True
    ' Set up scheduled refresh, banner, etc.
    Call ScheduleRefresh
End Sub

Private Sub Workbook_BeforeClose(Cancel As Boolean)
    Call StopRefresh
    ' Unsubscribe streaming
    Application.Run "BLPCancelSubscribe"
End Sub
```

## 6.9 Driving Excel from Python with `xlwings`

For analysts who prefer Python but need to deliver Excel deliverables
to a desk:

```python
import xlwings as xw

wb = xw.Book("YieldCurveMonitor.xlsx")

# Set the as-of date in the parameter cell, refresh, extract
wb.sheets["Params"].range("RefDate").value = "20250502"
wb.api.Application.Run("BLP.RefreshAll")

# Wait for the BBG range to clear
import time
target = wb.sheets["Curves"].range("USDCurve")
for _ in range(60):
    if all("#N/A" not in str(c) for c in target.value):
        break
    time.sleep(1)

# Read out
import pandas as pd
df = target.options(pd.DataFrame, header=1).value
df.to_parquet("usd_curve_20250502.parquet")
```

This pattern keeps the **definitive formula** in Excel (auditable,
share-able with the desk) while letting Python orchestrate refresh,
caching and downstream processing.

## 6.10 Anti-patterns

| Don't | Why |
|---|---|
| Trigger `Application.Run "BLP.RefreshAll"` on every cell change | Hits cap, causes Excel to freeze |
| Use `Application.Wait` to wait for refresh | Blocks Excel, doesn't pump messages |
| Poll `Range.Value` in a tight loop | Without `DoEvents`, no events fire and refresh stalls |
| Use `On Error Resume Next` globally to hide `#N/A` | Hides real entitlement / network issues |
| Mix real-time `BLPSubscribe` and scheduled `BLP.RefreshAll` | Refresh cancels and restarts subscriptions, increases churn |
| Embed Bloomberg formulas in conditional formatting | Recalc storm |
| Save workbook with `#N/A Requesting Data` cells | They serialize as errors; recipient sees nothing |

## 6.11 Reliability checklist for a scheduled pipeline

- [ ] Manual refresh only — no auto-refresh, no real-time mixed in.
- [ ] `RefreshAll` followed by a `#N/A`-clear poll with timeout.
- [ ] Status range with `=NOW()`, refresh-count counter, last error.
- [ ] Export step writes to a `_tmp` file and renames atomically.
- [ ] Logging to a sheet (date, count, elapsed).
- [ ] Graceful fail when `bbcomm` is down: skip the run, log, retry.
- [ ] Cancel any active subscriptions in `Workbook_BeforeClose`.

## 6.12 Why not just use `blpapi` from Python instead?

You should, for genuinely-batch workloads. Excel-side automation
shines when:

- The **definition of the report** is an Excel formula (auditable
  by a desk, modifiable by non-coders).
- The **consumer** is Excel — daily PDF / printed deliverable.
- The **firm's standard** is Excel with BBG.

For pipelines where the deliverable is a database row or a parquet
file, skip Excel — use Python and `blpapi` directly.
