# 07 · Bulk Fields

Most fields return a scalar (or a value per date for historical). Some
return a **table per security** — index members, dividend history,
option chains, holders, etc. These are *bulk fields*. The element
parsing is different.

## Detecting a bulk field

In `fieldData`, a bulk field's element has `numValues() > 0` and each
value is itself an Element with named sub-elements. Programmatically:

```python
fd = sd.getElement("fieldData")
el = fd.getElement("INDX_MEMBERS")
if el.isArray():
    rows = []
    for i in range(el.numValues()):
        row = el.getValueAsElement(i)
        rows.append({
            str(row.getElement(j).name()): row.getElement(j).getValue()
            for j in range(row.numElements())
        })
```

In the `apiflds` documentation they're labelled `Bulk Format` — in
`FLDS <GO>` you'll see "Bulk Data" in the field's metadata.

## The bulk fields you'll keep using

### Equity index membership

```python
req.append("securities", "SPX Index")
req.append("fields",     "INDX_MEMBERS")          # current members
# or:
req.append("fields",     "INDX_MWEIGHT_HIST")     # historical weights
ov = req.getElement("overrides").appendElement()
ov.setElement("fieldId", "END_DATE_OVERRIDE")
ov.setElement("value",   "20250430")
```

`INDX_MEMBERS` row schema: `Member Ticker and Exchange Code`.
`INDX_MWEIGHT_HIST` rows: `Index Member`, `Percent Weight`.
`INDX_MEMBERS_WEIGHTS` rows: `Member`, `Weight`, `Weight Method`.

> **Tickers in `INDX_MEMBERS` are returned without the yellow key.**
> You'll get e.g. `EDP PL`. Append ` Equity` (with a leading space) before
> using them as a security id elsewhere.

### Dividend history

```python
req.append("securities", "EDP PL Equity")
req.append("fields",     "DVD_HIST_ALL")
```

Row schema: `Declared Date`, `Ex-Date`, `Record Date`, `Payable Date`,
`Dividend Amount`, `Dividend Frequency`, `Dividend Type` (`Regular`,
`Special`, `Stock`, `Spinoff`), `Dividend Currency`.

Filter: override `EQY_INC_DVD_TYPES_FILTER` with `Regular` (default
`All`).

### Earnings history with reported / estimated EPS

This is the field that anchors a PEAD pipeline:

```python
req.append("fields", "EARN_ANN_DT_TIME_HIST_WITH_EPS")
```

Row schema: `Announcement Date`, `Announcement Time` (`AMC`/`BMO`),
`Period`, `Reported EPS`, `Estimated EPS`, `Surprise (%)`, `Comparable
EPS`, `Sales Reported`, `Sales Estimate`. Combined with
`BEST_EPS_STDEV` you get a SUE in three lines of pandas.

Related: `EARN_ANN_DT_TIME_HIST` (same without EPS),
`EARN_HIST_TYPE_FILTER` override (`First Call`, `Comparable`, …).

### Option chain

```python
req.append("securities", "AAPL US Equity")
req.append("fields",     "OPT_CHAIN")
```

Row schema: `Security Description` (Bloomberg ticker for the option).
You then back-fill that into `ReferenceDataRequest` to get strikes,
deltas, IVOL, etc.

Filter: `OPTION_CHAIN_OVERRIDE` with values like `EXPIRATION` (one
record per expiry) or specific expiry codes.

### Futures chain

```python
req.append("securities", "CL1 Comdty")            # active WTI
req.append("fields",     "FUT_CHAIN")
ov = req.getElement("overrides").appendElement()
ov.setElement("fieldId", "INCLUDE_EXPIRED_CONTRACTS")
ov.setElement("value",   "Y")
ov = req.getElement("overrides").appendElement()
ov.setElement("fieldId", "CHAIN_DATE")
ov.setElement("value",   "20250502")
```

Rows: `Security Description` (e.g. `CLM5 Comdty`).

### Top holders

`TOP_20_HOLDERS_PUBLIC_FILINGS` — `Holder Name`, `Holder ID`, `Position`,
`% Out`, `File Date`, `Source`. Variants: `AGGREGATE_HOLDINGS`,
`ALL_HOLDERS_PUBLIC_FILINGS`.

### Bloomberg peers

`BLOOMBERG_PEERS` — `Peer Ticker` (with no yellow key, append `Equity`).
Useful for industry-relative metrics; complements `GICS_*`.

### Bond cash flows

`CALL_SCHEDULE` — `Call Date`, `Call Price`, `Call Type`.
`PUT_SCHEDULE` — same shape.
`AMORT_SCHEDULE` — `Date`, `Amount`, `Factor`.

### Corporate actions

`CORP_ACTIONS_PRC_HISTORY` — `Effective Date`, `Action Type`, `Action`,
`Description`. For modelling adjustments outside DPDF.

### Capital structure

`CAPITAL_STRUCTURE_DETAILED` — `Type`, `Description`, `Amount Out`,
`Currency`, `Maturity`, `Coupon`, `Rank`. The cleanest way to get a
firm's full debt stack.

### Credit ratings history

`RTG_FITCH_HIST`, `RTG_MOODY_HIST`, `RTG_SP_HIST`, `RTG_BB_COMP_HIST`.
Rows: `Date`, `Rating`, `Outlook`, `Action`.

### Insider transactions

`INSIDER_TRANSACTIONS` — `Filing Date`, `Trade Date`, `Type`, `Insider`,
`Title`, `Shares`, `Price`, `Value`, `Beneficial Owner`.

## Iteration helper

A small reusable function:

```python
def bulk_to_records(field_element):
    """Bloomberg bulk field Element → list[dict]."""
    if not field_element.isArray():
        return []
    out = []
    for i in range(field_element.numValues()):
        row = field_element.getValueAsElement(i)
        rec = {}
        for j in range(row.numElements()):
            sub = row.getElement(j)
            rec[str(sub.name())] = None if sub.isNull() else sub.getValue()
        out.append(rec)
    return out
```

A complete example using this is in
[`examples/bulk_fields.py`](../examples/bulk_fields.py).

## A subtle gotcha — schema is per-field, not per-API

Bulk-field row schemas are **not declared** in any meta endpoint. The
column names are whatever Bloomberg decided (`Ex-Date` with a hyphen,
`% Out` with spaces and a percent sign). Treat the schema as runtime;
slugify the keys before using them in pandas.

```python
import re
def slug(s): return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
```
