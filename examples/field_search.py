"""Field discovery: //blp/apiflds.

Two patterns:
1. FieldSearchRequest -- keyword search across the entire field universe.
2. FieldInfoRequest   -- describe known mnemonics (datatype, overrides, docs).
"""

from __future__ import annotations
import pandas as pd

from utils import bbg_session, drain_response


def search(keywords: str, max_results: int = 50) -> pd.DataFrame:
    rows: list[dict] = []
    with bbg_session(services=("//blp/apiflds",)) as sess:
        svc = sess.getService("//blp/apiflds")
        req = svc.createRequest("FieldSearchRequest")
        req.set("searchSpec", keywords)
        req.set("returnFieldDocumentation", True)
        req.set("includeProductType", True)
        req.set("includeFieldType", True)
        sess.sendRequest(req)

        for msg in drain_response(sess):
            if not msg.hasElement("fieldData"):
                continue
            fd_arr = msg.getElement("fieldData")
            for i in range(fd_arr.numValues()):
                if len(rows) >= max_results:
                    break
                fd = fd_arr.getValueAsElement(i)
                rec = {"id": fd.getElementAsString("id")}
                if fd.hasElement("fieldInfo"):
                    fi = fd.getElement("fieldInfo")
                    for k in ("mnemonic", "description", "datatype",
                              "categoryName", "documentation"):
                        if fi.hasElement(k):
                            rec[k] = fi.getElementAsString(k)
                rows.append(rec)
    return pd.DataFrame(rows)


def info(mnemonics: list[str]) -> pd.DataFrame:
    rows: list[dict] = []
    with bbg_session(services=("//blp/apiflds",)) as sess:
        svc = sess.getService("//blp/apiflds")
        req = svc.createRequest("FieldInfoRequest")
        for m in mnemonics:
            req.append("id", m)
        req.set("returnFieldDocumentation", True)
        sess.sendRequest(req)

        for msg in drain_response(sess):
            if not msg.hasElement("fieldData"):
                continue
            fd_arr = msg.getElement("fieldData")
            for i in range(fd_arr.numValues()):
                fd = fd_arr.getValueAsElement(i)
                rec = {"id": fd.getElementAsString("id")}
                if fd.hasElement("fieldInfo"):
                    fi = fd.getElement("fieldInfo")
                    for k in ("mnemonic", "description", "datatype",
                              "categoryName", "documentation"):
                        if fi.hasElement(k):
                            rec[k] = fi.getElementAsString(k)
                rows.append(rec)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print("=== search 'earnings announcement' ===")
    print(search("earnings announcement").head(10).to_string())

    print("\n=== info on canonical fields ===")
    print(info(["PX_LAST", "BEST_EPS", "EARN_ANN_DT_TIME_HIST_WITH_EPS",
                "Z_SPRD_MID"]).to_string())
