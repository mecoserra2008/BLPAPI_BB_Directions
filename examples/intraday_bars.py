"""IntradayBarRequest -> DataFrame of OHLCV bars.

Single security, ~140-day window, bars at N-minute resolution.  Times
are UTC throughout the request and response.
"""

from __future__ import annotations
import datetime as dt
import pandas as pd

from utils import bbg_session, drain_response


SECURITY = "EDP PL Equity"
EVENT    = "TRADE"          # TRADE / BID / ASK / ...
INTERVAL = 1                # minutes
START    = dt.datetime(2025, 5, 1, 7, 0)   # UTC
END      = dt.datetime(2025, 5, 3, 16, 0)


def fetch():
    rows: list[dict] = []
    with bbg_session() as sess:
        svc = sess.getService("//blp/refdata")
        req = svc.createRequest("IntradayBarRequest")
        req.set("security",       SECURITY)
        req.set("eventType",      EVENT)
        req.set("interval",       INTERVAL)
        req.set("startDateTime",  START)
        req.set("endDateTime",    END)
        req.set("gapFillInitialBar", True)
        req.set("adjustmentSplit",  True)
        req.set("adjustmentNormal", False)
        req.set("adjustmentAbnormal", True)
        req.set("adjustmentFollowDPDF", False)
        sess.sendRequest(req)

        for msg in drain_response(sess):
            data = msg.getElement("barData").getElement("barTickData")
            for i in range(data.numValues()):
                bar = data.getValueAsElement(i)
                rows.append({
                    "time":      bar.getElementAsDatetime("time"),
                    "open":      bar.getElementAsFloat("open"),
                    "high":      bar.getElementAsFloat("high"),
                    "low":       bar.getElementAsFloat("low"),
                    "close":     bar.getElementAsFloat("close"),
                    "volume":    bar.getElementAsInteger("volume"),
                    "numEvents": bar.getElementAsInteger("numEvents"),
                    "value":     bar.getElementAsFloat("value"),
                })
    return pd.DataFrame(rows).set_index("time")


if __name__ == "__main__":
    df = fetch()
    print(df.head())
    print(f"\n{len(df)} bars across {df.index.min()} to {df.index.max()}")
