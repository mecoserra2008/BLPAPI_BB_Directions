"""Bond analytics with YAS overrides.

For a list of bonds, pull live quotes plus user-supplied-price
analytics (z-spread, OAS, asset-swap spread).
"""

from __future__ import annotations
import pandas as pd

from utils import bbg_session, drain_response, append_overrides


BONDS = [
    "T 4.625 02/15/35 Govt",       # US Treasury 10y
    "DBR 2 ½ 08/15/54 Govt",       # German Bund 30y
    "EDP 1 ⅞ 03/14/35 Corp",       # EDP corporate
]

# (price, settlement, swap curve)
USER_INPUTS = {
    "T 4.625 02/15/35 Govt":   {"YAS_BOND_PX": "98.50",  "YAS_RISK_DT": "20250506", "YAS_CURVE": "S490"},
    "DBR 2 ½ 08/15/54 Govt":   {"YAS_BOND_PX": "92.20",  "YAS_RISK_DT": "20250506", "YAS_CURVE": "S514"},
    "EDP 1 ⅞ 03/14/35 Corp":   {"YAS_BOND_PX": "94.50",  "YAS_RISK_DT": "20250506", "YAS_CURVE": "S514"},
}

LIVE_FIELDS = [
    "PX_LAST", "YLD_YTM_MID",
    "G_SPRD_MID", "I_SPRD_MID", "Z_SPRD_MID", "OAS_SPREAD_MID",
    "ASSET_SWAP_SPD_MID",
    "DUR_ADJ_MID", "MOD_DUR_MID", "CONVEXITY",
    "RTG_BB_COMPOSITE", "MATURITY", "CRNCY",
]
YAS_FIELDS = [
    "YAS_BOND_YLD",                  # implied YTM from your price
    "YAS_ZSPREAD",
    "YAS_ISPREAD",
    "YAS_ASW_SPREAD",
    "YAS_OAS_SPREAD",
    "DUR_ADJ_MID",
]


def pull(security: str, fields: list[str], overrides: dict[str, str]):
    with bbg_session() as sess:
        svc = sess.getService("//blp/refdata")
        req = svc.createRequest("ReferenceDataRequest")
        req.append("securities", security)
        for f in fields:
            req.append("fields", f)
        append_overrides(req, overrides)
        sess.sendRequest(req)

        out = {}
        for msg in drain_response(sess):
            sd_arr = msg.getElement("securityData")
            for i in range(sd_arr.numValues()):
                sd = sd_arr.getValueAsElement(i)
                if sd.hasElement("securityError"):
                    print("!! sec err", sd.getElement("securityError"))
                    continue
                fd = sd.getElement("fieldData")
                for f in fields:
                    if fd.hasElement(f):
                        try:
                            out[f] = fd.getElement(f).getValue()
                        except Exception:
                            out[f] = None
        return out


if __name__ == "__main__":
    live = []
    yas  = []
    for b in BONDS:
        live.append({**{"bond": b}, **pull(b, LIVE_FIELDS, {})})
        yas.append({**{"bond": b}, **pull(b, YAS_FIELDS, USER_INPUTS[b])})

    live_df = pd.DataFrame(live).set_index("bond")
    yas_df  = pd.DataFrame(yas).set_index("bond")
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)
    print("=== Live market analytics ===")
    print(live_df)
    print("\n=== User-supplied price (YAS) analytics ===")
    print(yas_df)
