"""Overrides demonstrated end-to-end.

Each call shows a different override pattern:
- LTM fundamentals in a non-default currency
- Point-in-time consensus EPS for a past date
- Historical index members at a past date
- ROE for a specific quarter relative period
- Asset-swap spread for a bond at user-supplied price
"""

from __future__ import annotations
import pandas as pd

from utils import bbg_session, drain_response, append_overrides


def _pull(securities, fields, overrides):
    rows = []
    with bbg_session() as sess:
        svc = sess.getService("//blp/refdata")
        req = svc.createRequest("ReferenceDataRequest")
        for t in securities:
            req.append("securities", t)
        for f in fields:
            req.append("fields", f)
        append_overrides(req, overrides)
        sess.sendRequest(req)

        for msg in drain_response(sess):
            sd_arr = msg.getElement("securityData")
            for i in range(sd_arr.numValues()):
                sd = sd_arr.getValueAsElement(i)
                if sd.hasElement("securityError"):
                    continue
                fd = sd.getElement("fieldData")
                row = {"security": sd.getElementAsString("security")}
                for f in fields:
                    if fd.hasElement(f):
                        try:
                            row[f] = fd.getElement(f).getValue()
                        except Exception:
                            row[f] = None
                rows.append(row)
    return pd.DataFrame(rows).set_index("security")


def ltm_fundamentals_in_eur():
    return _pull(
        ["AAPL US Equity", "MSFT US Equity"],
        ["TRAIL_12M_REVENUE", "TRAIL_12M_EBITDA", "TRAIL_12M_NET_INC"],
        {"FUND_PER": "LTM", "EQY_FUND_CRNCY": "EUR"},
    )


def pit_consensus_eps():
    return _pull(
        ["AAPL US Equity", "EDP PL Equity"],
        ["BEST_EPS", "BEST_EPS_STDEV", "BEST_EPS_NUMEST"],
        {"BEST_FPERIOD_OVERRIDE": "1FQ",
         "BEST_DATA_RELEASE_DT":  "20240131"},
    )


def historical_index_members():
    return _pull(
        ["SX5E Index"],
        ["INDX_MWEIGHT_HIST"],
        {"END_DATE_OVERRIDE": "20231229"},
    )


def quarterly_roe_minus_2():
    return _pull(
        ["AAPL US Equity"],
        ["RETURN_COM_EQY"],
        {"FUND_PER": "Q", "EQY_FUND_RELATIVE_PERIOD": "-2Q"},
    )


def yas_zspread_at_user_price():
    return _pull(
        ["EDP 1 ⅞ 03/14/35 Corp"],
        ["YAS_ZSPREAD", "YAS_ASW_SPREAD", "YAS_BOND_YLD"],
        {"YAS_BOND_PX": "94.50",
         "YAS_RISK_DT": "20250506",
         "YAS_CURVE":   "S514"},
    )


if __name__ == "__main__":
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)
    print("\n--- LTM fundamentals in EUR ---")
    print(ltm_fundamentals_in_eur())
    print("\n--- PIT consensus EPS as of Jan 31 2024 ---")
    print(pit_consensus_eps())
    print("\n--- SX5E members at end-2023 ---")
    print(historical_index_members())
    print("\n--- AAPL ROE 2 quarters ago ---")
    print(quarterly_roe_minus_2())
    print("\n--- EDP bond YAS analytics @ 94.50 ---")
    print(yas_zspread_at_user_price())
