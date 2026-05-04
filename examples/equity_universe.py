"""Build a regional equity universe from index membership + factor pull.

This is a slim version of the factor-panel recipe -- one rebalance,
no caching.
"""

from __future__ import annotations
import pandas as pd

from utils import bbg_session, drain_response, append_overrides
from bulk_fields import bulk_to_records


INDEX  = "SX5E Index"
ASOF   = "20250502"
FIELDS = [
    "PX_LAST", "CUR_MKT_CAP", "EQY_FUND_CRNCY",
    "BEST_PE_RATIO", "PX_TO_BOOK_RATIO", "EV_TO_T12M_EBITDA",
    "RETURN_COM_EQY", "RETURN_ON_INV_CAPITAL",
    "TRAIL_12M_NET_INC", "TRAIL_12M_FREE_CASH_FLOW",
    "EQY_DVD_YLD_12M",
    "HISTORICAL_VOLATILITY_260D",
    "GICS_SECTOR_NAME", "GICS_INDUSTRY_NAME",
]
OVERRIDES = {
    "BEST_FPERIOD_OVERRIDE": "1BF",
    "BEST_DATA_RELEASE_DT":  ASOF,
    "EQY_FUND_CRNCY":        "EUR",
}


def members(index_ticker, asof):
    with bbg_session() as sess:
        svc = sess.getService("//blp/refdata")
        req = svc.createRequest("ReferenceDataRequest")
        req.append("securities", index_ticker)
        req.append("fields",     "INDX_MWEIGHT_HIST")
        append_overrides(req, {"END_DATE_OVERRIDE": asof})
        sess.sendRequest(req)
        rows = []
        for msg in drain_response(sess):
            sd_arr = msg.getElement("securityData")
            for i in range(sd_arr.numValues()):
                sd = sd_arr.getValueAsElement(i)
                if sd.hasElement("securityError"):
                    continue
                fd = sd.getElement("fieldData")
                if fd.hasElement("INDX_MWEIGHT_HIST"):
                    rows.extend(
                        bulk_to_records(fd.getElement("INDX_MWEIGHT_HIST")))
        return rows


def panel(tickers, asof):
    rows = []
    # Bloomberg likes batches of <=100
    for i in range(0, len(tickers), 100):
        batch = tickers[i:i+100]
        with bbg_session() as sess:
            svc = sess.getService("//blp/refdata")
            req = svc.createRequest("ReferenceDataRequest")
            for t in batch:
                req.append("securities", t)
            for f in FIELDS:
                req.append("fields", f)
            append_overrides(req, OVERRIDES)
            sess.sendRequest(req)

            for msg in drain_response(sess):
                sd_arr = msg.getElement("securityData")
                for j in range(sd_arr.numValues()):
                    sd = sd_arr.getValueAsElement(j)
                    if sd.hasElement("securityError"):
                        continue
                    fd = sd.getElement("fieldData")
                    row = {"security": sd.getElementAsString("security")}
                    for f in FIELDS:
                        if fd.hasElement(f):
                            try:
                                row[f] = fd.getElement(f).getValue()
                            except Exception:
                                row[f] = None
                    rows.append(row)
    return pd.DataFrame(rows).set_index("security")


if __name__ == "__main__":
    mem = members(INDEX, ASOF)
    tickers = [m["Index Member"] + " Equity" for m in mem
               if "Index Member" in m]
    print(f"{len(tickers)} members in {INDEX} as of {ASOF}")
    df = panel(tickers, ASOF)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 220)
    print(df.head(10))
