"""BeqsRequest -> universe of tickers from a saved EQS screen.

Set up the screen on the Terminal in EQS <GO>, save it under a name,
and pass that name here.
"""

from __future__ import annotations
import pandas as pd

from utils import bbg_session, drain_response


SCREEN_NAME = "PSI20_Members"      # change to your saved screen
SCREEN_TYPE = "PRIVATE"            # or "GLOBAL"


def fetch(screen_name: str = SCREEN_NAME, screen_type: str = SCREEN_TYPE):
    rows: list[dict] = []
    with bbg_session() as sess:
        svc = sess.getService("//blp/refdata")
        req = svc.createRequest("BeqsRequest")
        req.set("screenName", screen_name)
        req.set("screenType", screen_type)
        sess.sendRequest(req)

        for msg in drain_response(sess):
            if not msg.hasElement("data"):
                continue
            sd_arr = msg.getElement("data").getElement("securityData")
            for i in range(sd_arr.numValues()):
                sd = sd_arr.getValueAsElement(i)
                row = {"security": sd.getElementAsString("security")}
                fd = sd.getElement("fieldData")
                for j in range(fd.numElements()):
                    f = fd.getElement(j)
                    try:
                        row[str(f.name())] = f.getValue()
                    except Exception:
                        pass
                rows.append(row)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = fetch()
    print(df.head())
    print(f"\n{len(df)} names in '{SCREEN_NAME}'")
