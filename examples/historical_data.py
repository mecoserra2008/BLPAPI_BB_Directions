"""HistoricalDataRequest -> DataFrame.

Daily total-return history for an index basket.  Pinned adjustment
flags so the result is reproducible regardless of DPDF settings.
"""

from __future__ import annotations
import pandas as pd

from utils import bbg_session, drain_response


TICKERS = ["SPX Index", "SX5E Index", "PSI20 Index", "NKY Index"]
FIELDS  = ["PX_LAST", "TOT_RETURN_INDEX_GROSS_DVDS"]
START   = "20140101"
END     = "20251231"
CURRENCY = "EUR"


def fetch():
    frames = []
    with bbg_session() as sess:
        svc = sess.getService("//blp/refdata")
        req = svc.createRequest("HistoricalDataRequest")
        for t in TICKERS:
            req.append("securities", t)
        for f in FIELDS:
            req.append("fields", f)
        req.set("startDate",            START)
        req.set("endDate",              END)
        req.set("periodicityAdjustment","CALENDAR")
        req.set("periodicitySelection", "DAILY")
        req.set("currency",             CURRENCY)
        req.set("nonTradingDayFillOption","NON_TRADING_WEEKDAYS")
        req.set("nonTradingDayFillMethod","PREVIOUS_VALUE")
        req.set("adjustmentSplit",      True)
        req.set("adjustmentNormal",     False)
        req.set("adjustmentAbnormal",   True)
        req.set("adjustmentFollowDPDF", False)
        sess.sendRequest(req)

        for msg in drain_response(sess):
            sd  = msg.getElement("securityData")
            sec = sd.getElementAsString("security")
            fd  = sd.getElement("fieldData")
            rows = []
            for i in range(fd.numValues()):
                bar = fd.getValueAsElement(i)
                row = {"date": bar.getElementAsDatetime("date")}
                for f in FIELDS:
                    if bar.hasElement(f):
                        row[f] = bar.getElement(f).getValue()
                rows.append(row)
            df = pd.DataFrame(rows).set_index("date")
            df.columns = pd.MultiIndex.from_product([[sec], df.columns])
            frames.append(df)
    return pd.concat(frames, axis=1).sort_index()


if __name__ == "__main__":
    panel = fetch()
    print(panel.tail())
