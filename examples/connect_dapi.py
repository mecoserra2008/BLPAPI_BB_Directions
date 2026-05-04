"""Smallest possible working example: open DAPI session, ping refdata.

Run:  python examples/connect_dapi.py
Expect:  session.start ok -> opened //blp/refdata
"""

from utils import bbg_session


def main():
    with bbg_session(services=("//blp/refdata",)) as sess:
        print("session.start ok -> opened //blp/refdata")


if __name__ == "__main__":
    main()
