"""xbbg quickstart: same calls as the raw-blpapi examples, much shorter.

Requires `pip install xbbg`.  xbbg internally uses blpapi, so DAPI/SAPI
must still be available.
"""

from __future__ import annotations
import pandas as pd

try:
    from xbbg import blp
except ImportError:
    raise SystemExit("Install xbbg first: pip install xbbg")


def reference_snapshot():
    """bdp = Bloomberg Data Point (single-value snapshot)."""
    df = blp.bdp(
        tickers=["EDP PL Equity", "GALP PL Equity", "JMT PL Equity",
                 "AAPL US Equity", "EURUSD Curncy", "SX5E Index"],
        flds=["PX_LAST", "CUR_MKT_CAP", "BEST_EPS", "BEST_PE_RATIO",
              "EQY_DVD_YLD_IND", "GICS_SECTOR_NAME", "ID_ISIN"],
        BEST_FPERIOD_OVERRIDE="1FY",
        EQY_FUND_CRNCY="EUR",
    )
    return df


def historical():
    """bdh = Bloomberg Data History (time series)."""
    df = blp.bdh(
        tickers=["SPX Index", "SX5E Index", "PSI20 Index"],
        flds=["TOT_RETURN_INDEX_GROSS_DVDS"],
        start_date="2014-01-01",
        end_date="2025-12-31",
        Per="D", Fill="P",
        currency="EUR",
        adjust="all",      # apply splits + divs
    )
    return df


def bulk_members():
    """bds = Bloomberg Data Set (bulk fields)."""
    return blp.bds("SX5E Index", "INDX_MEMBERS")


def intraday_bars():
    """bdib = Bloomberg Data Intra-day Bar."""
    return blp.bdib(
        ticker="EDP PL Equity",
        dt="2025-05-02",
        typ="TRADE",
        interval=1,
        session="allday",
    )


def screen():
    """beqs = Bloomberg Equity Screen (saved EQS)."""
    return blp.beqs("PSI20_Members", typ="PRIVATE")


if __name__ == "__main__":
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)

    print("\n=== bdp ===")
    print(reference_snapshot())

    print("\n=== bdh (tail) ===")
    print(historical().tail())

    print("\n=== bds INDX_MEMBERS ===")
    print(bulk_members().head())
