"""IntradayTickRequest -> DataFrame of trade & quote ticks.

Heavy on hits — only run on a single security and a short window.
"""

from __future__ import annotations
import datetime as dt
import pandas as pd

from utils import bbg_session, drain_response


SECURITY  = "EDP PL Equity"
EVENTS    = ["TRADE", "BID", "ASK"]
START     = dt.datetime(2025, 5, 2, 7, 0)        # UTC
END       = dt.datetime(2025, 5, 2, 16, 0)


def fetch():
    rows: list[dict] = []
    with bbg_session() as sess:
        svc = sess.getService("//blp/refdata")
        req = svc.createRequest("IntradayTickRequest")
        req.set("security", SECURITY)
        ev = req.getElement("eventTypes")
        for e in EVENTS:
            ev.appendValue(e)
        req.set("startDateTime", START)
        req.set("endDateTime",   END)
        req.set("includeConditionCodes",     True)
        req.set("includeNonPlottableEvents", True)
        req.set("includeExchangeCodes",      True)
        req.set("includeRpsCodes",           True)
        req.set("includeBicMicCodes",        True)
        req.set("includeTradeTime",          True)
        sess.sendRequest(req)

        for msg in drain_response(sess):
            tick_data = msg.getElement("tickData").getElement("tickData")
            for i in range(tick_data.numValues()):
                t = tick_data.getValueAsElement(i)
                row = {"time": t.getElementAsDatetime("time"),
                       "type": t.getElementAsString("type"),
                       "value":t.getElementAsFloat("value")}
                if t.hasElement("size"):
                    row["size"] = t.getElementAsInteger("size")
                if t.hasElement("conditionCodes"):
                    row["cond"] = t.getElementAsString("conditionCodes")
                if t.hasElement("exchangeCode"):
                    row["xch"] = t.getElementAsString("exchangeCode")
                rows.append(row)
    return pd.DataFrame(rows).set_index("time")


if __name__ == "__main__":
    df = fetch()
    print(df.head(20))
    print(f"\n{len(df)} ticks ({df.type.value_counts().to_dict()})")
