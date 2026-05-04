"""Iterate bulk fields: index members, dividend history, earnings.

Bulk fields are fields whose value is a *table* (list of records).
Each record is a child Element with named sub-fields.
"""

from __future__ import annotations
import pandas as pd

from utils import bbg_session, drain_response, append_overrides


CASES = [
    ("SX5E Index",       "INDX_MEMBERS",                 {}),
    ("EDP PL Equity",    "DVD_HIST_ALL",                 {"EQY_INC_DVD_TYPES_FILTER": "All"}),
    ("AAPL US Equity",   "EARN_ANN_DT_TIME_HIST_WITH_EPS", {}),
    ("CL1 Comdty",       "FUT_CHAIN",                    {"INCLUDE_EXPIRED_CONTRACTS": "N",
                                                          "CHAIN_DATE":                "20250502"}),
]


def bulk_to_records(field_element):
    rows = []
    if not field_element.isArray():
        return rows
    for i in range(field_element.numValues()):
        row = field_element.getValueAsElement(i)
        rec = {}
        for j in range(row.numElements()):
            sub = row.getElement(j)
            try:
                rec[str(sub.name())] = None if sub.isNull() else sub.getValue()
            except Exception:
                rec[str(sub.name())] = None
        rows.append(rec)
    return rows


def fetch_one(security, field, overrides):
    with bbg_session() as sess:
        svc = sess.getService("//blp/refdata")
        req = svc.createRequest("ReferenceDataRequest")
        req.append("securities", security)
        req.append("fields",     field)
        append_overrides(req, overrides)
        sess.sendRequest(req)

        rows = []
        for msg in drain_response(sess):
            sd_arr = msg.getElement("securityData")
            for i in range(sd_arr.numValues()):
                sd = sd_arr.getValueAsElement(i)
                if sd.hasElement("securityError"):
                    continue
                fd = sd.getElement("fieldData")
                if not fd.hasElement(field):
                    continue
                rows = bulk_to_records(fd.getElement(field))
        return pd.DataFrame(rows)


if __name__ == "__main__":
    for security, field, overrides in CASES:
        print(f"\n### {security} / {field}  overrides={overrides}")
        df = fetch_one(security, field, overrides)
        print(df.head())
        print(f"({len(df)} rows)")
