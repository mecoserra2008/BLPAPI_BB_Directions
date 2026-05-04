"""ReferenceDataRequest -> DataFrame.

Pulls a snapshot of fields for a list of tickers and prints a tidy
table.  Demonstrates:
- securities + fields
- overrides
- securityError / fieldExceptions handling
"""

from __future__ import annotations
import pandas as pd

from utils import bbg_session, drain_response, append_overrides, field_exceptions


TICKERS = [
    "EDP PL Equity",
    "GALP PL Equity",
    "JMT PL Equity",
    "AAPL US Equity",
    "MSFT US Equity",
    "EURUSD Curncy",
    "SX5E Index",
]
FIELDS = [
    "PX_LAST",
    "CRNCY",
    "CUR_MKT_CAP",
    "BEST_EPS",
    "BEST_PE_RATIO",
    "EQY_DVD_YLD_IND",
    "GICS_SECTOR_NAME",
    "ID_ISIN",
]
OVERRIDES = {
    "BEST_FPERIOD_OVERRIDE": "1FY",
    "EQY_FUND_CRNCY":        "EUR",
}


def fetch():
    rows: list[dict] = []
    with bbg_session() as sess:
        svc = sess.getService("//blp/refdata")
        req = svc.createRequest("ReferenceDataRequest")
        for t in TICKERS:
            req.append("securities", t)
        for f in FIELDS:
            req.append("fields", f)
        append_overrides(req, OVERRIDES)
        sess.sendRequest(req)

        for msg in drain_response(sess):
            if not msg.hasElement("securityData"):
                continue
            sd_arr = msg.getElement("securityData")
            for i in range(sd_arr.numValues()):
                sd  = sd_arr.getValueAsElement(i)
                sec = sd.getElementAsString("security")

                if sd.hasElement("securityError"):
                    err = sd.getElement("securityError")
                    print(f"!! security error {sec}: "
                          f"{err.getElementAsString('message')}")
                    continue

                for fe in field_exceptions(sd):
                    print(f"!! field err {sec}/{fe['fieldId']}: {fe['message']}")

                fd = sd.getElement("fieldData")
                row = {"security": sec}
                for f in FIELDS:
                    if fd.hasElement(f):
                        try:
                            row[f] = fd.getElement(f).getValue()
                        except Exception:
                            row[f] = None
                    else:
                        row[f] = None
                rows.append(row)
    return pd.DataFrame(rows).set_index("security")


if __name__ == "__main__":
    df = fetch()
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)
    print(df)
