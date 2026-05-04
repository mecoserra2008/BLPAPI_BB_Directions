"""FX spot, outright forwards, NDFs and implied yields.

Builds:
- G10 spot snapshot at a chosen fixing source (WMCO by default)
- 1m / 3m / 6m / 12m forward outrights
- NDF panel (USD vs major EM)
- Implied carry per pair
"""

from __future__ import annotations
import math
import pandas as pd

from utils import bbg_session, drain_response


G10_PAIRS = ["EURUSD", "USDJPY", "GBPUSD", "USDCHF",
             "AUDUSD", "NZDUSD", "USDCAD", "USDSEK", "USDNOK"]
EM_NDF    = ["USDBRL", "USDMXN", "USDCLP", "USDCOP",
             "USDZAR", "USDTRY", "USDPLN", "USDHUF",
             "USDKRW", "USDINR", "USDIDR", "USDPHP",
             "USDTWD", "USDTHB", "USDCNH"]
TENORS    = ["1M", "3M", "6M", "1Y"]
FIX       = "WMCO"


def fetch(tickers, fields=("PX_LAST",)):
    rows = []
    with bbg_session() as sess:
        svc = sess.getService("//blp/refdata")
        req = svc.createRequest("ReferenceDataRequest")
        for t in tickers:
            req.append("securities", t)
        for f in fields:
            req.append("fields", f)
        sess.sendRequest(req)

        for msg in drain_response(sess):
            sd_arr = msg.getElement("securityData")
            for i in range(sd_arr.numValues()):
                sd = sd_arr.getValueAsElement(i)
                sec = sd.getElementAsString("security")
                if sd.hasElement("securityError"):
                    continue
                fd = sd.getElement("fieldData")
                row = {"security": sec}
                for f in fields:
                    if fd.hasElement(f):
                        try:
                            row[f] = fd.getElement(f).getValue()
                        except Exception:
                            row[f] = None
                rows.append(row)
    return pd.DataFrame(rows).set_index("security")


def annualised_carry(spot: float, fwd: float, tenor: str) -> float:
    yrs = {"1M": 1/12, "3M": 0.25, "6M": 0.5, "9M": 0.75, "1Y": 1.0}[tenor]
    return -math.log(fwd / spot) / yrs


if __name__ == "__main__":
    spot_tkrs = [f"{p} {FIX} Curncy" for p in G10_PAIRS] + \
                [f"{p} Curncy"        for p in EM_NDF]
    spot = fetch(spot_tkrs).PX_LAST
    spot.index = [s.split()[0] for s in spot.index]

    print("\n=== Spot ===")
    print(spot)

    fwd_tkrs = [f"{p}{t} Curncy" for p in G10_PAIRS + EM_NDF for t in TENORS]
    fwds = fetch(fwd_tkrs).PX_LAST.unstack()                       # noqa
    fwd_df = fetch(fwd_tkrs, fields=("PX_LAST", "IMPL_YIELD_NDF_PCT"))
    print("\n=== Forwards (outright) ===")
    print(fwd_df.head(20))

    # Carry table
    rows = []
    for p in G10_PAIRS + EM_NDF:
        if p not in spot.index:
            continue
        s = spot[p]
        for t in TENORS:
            tkr = f"{p}{t} Curncy"
            if tkr in fwd_df.index:
                f = fwd_df.loc[tkr, "PX_LAST"]
                if pd.notna(f) and pd.notna(s):
                    rows.append({"pair": p, "tenor": t,
                                 "spot": s, "fwd": f,
                                 "carry_ann": annualised_carry(s, f, t)})
    carry = pd.DataFrame(rows)
    print("\n=== Annualised carry (CIP-implied) ===")
    print(carry.pivot(index="pair", columns="tenor", values="carry_ann"))
