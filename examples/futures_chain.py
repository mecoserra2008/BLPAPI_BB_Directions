"""Futures chain term structure: WTI as a worked example.

1) Pull FUT_CHAIN at a given date.
2) Snap PX_LAST + delivery dates for each specific contract.
3) Print the term structure.
"""

from __future__ import annotations
import pandas as pd

from utils import bbg_session, drain_response, append_overrides
from bulk_fields import bulk_to_records


GENERIC = "CL1 Comdty"
ASOF    = "20250502"


def chain_at(generic: str, asof: str, include_expired: str = "N"):
    with bbg_session() as sess:
        svc = sess.getService("//blp/refdata")
        req = svc.createRequest("ReferenceDataRequest")
        req.append("securities", generic)
        req.append("fields",     "FUT_CHAIN")
        append_overrides(req, {"INCLUDE_EXPIRED_CONTRACTS": include_expired,
                               "CHAIN_DATE":                asof})
        sess.sendRequest(req)
        rows = []
        for msg in drain_response(sess):
            sd_arr = msg.getElement("securityData")
            for i in range(sd_arr.numValues()):
                sd = sd_arr.getValueAsElement(i)
                if sd.hasElement("securityError"):
                    continue
                fd = sd.getElement("fieldData")
                if fd.hasElement("FUT_CHAIN"):
                    rows.extend(bulk_to_records(fd.getElement("FUT_CHAIN")))
        return [r["Security Description"] for r in rows
                if "Security Description" in r]


def snap(contracts: list[str]):
    rows = []
    with bbg_session() as sess:
        svc = sess.getService("//blp/refdata")
        req = svc.createRequest("ReferenceDataRequest")
        for t in contracts:
            req.append("securities", t)
        for f in ["PX_LAST", "PX_SETTLE", "OPEN_INT",
                  "FUT_DLV_DT_FIRST", "LAST_TRADEABLE_DT",
                  "FUT_VAL_PT", "FUT_CONT_SIZE"]:
            req.append("fields", f)
        sess.sendRequest(req)

        for msg in drain_response(sess):
            sd_arr = msg.getElement("securityData")
            for i in range(sd_arr.numValues()):
                sd  = sd_arr.getValueAsElement(i)
                sec = sd.getElementAsString("security")
                if sd.hasElement("securityError"):
                    continue
                fd = sd.getElement("fieldData")
                row = {"contract": sec}
                for f in ["PX_LAST","PX_SETTLE","OPEN_INT",
                          "FUT_DLV_DT_FIRST","LAST_TRADEABLE_DT",
                          "FUT_VAL_PT","FUT_CONT_SIZE"]:
                    row[f] = fd.getElement(f).getValue() if fd.hasElement(f) else None
                rows.append(row)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    contracts = chain_at(GENERIC, ASOF)
    print(f"{len(contracts)} contracts in chain on {ASOF}:")
    df = snap(contracts).sort_values("FUT_DLV_DT_FIRST")
    print(df.head(15))
