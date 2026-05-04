"""Async subscription example -- streams real-time prices.

Run, watch ticks roll in, ctrl-C to stop.
"""

from __future__ import annotations
import threading

import blpapi


TOPICS = [
    ("EDP PL Equity",  ["LAST_PRICE", "BID", "ASK", "VOLUME"]),
    ("PSI20 Index",    ["LAST_PRICE"]),
    ("EURUSD Curncy",  ["LAST_PRICE", "BID", "ASK"]),
]


class Handler:
    def __init__(self):
        self.stopped = threading.Event()

    def __call__(self, event, sess):
        et = event.eventType()
        if et == blpapi.Event.SESSION_STATUS:
            for msg in event:
                print(f"[session ] {msg.messageType()}")
                if msg.messageType() == blpapi.Name("SessionStarted"):
                    sess.openServiceAsync("//blp/mktdata")
                elif msg.messageType() == blpapi.Name("SessionTerminated"):
                    self.stopped.set()

        elif et == blpapi.Event.SERVICE_STATUS:
            for msg in event:
                print(f"[service ] {msg.messageType()}")
                if msg.messageType() == blpapi.Name("ServiceOpened"):
                    self._subscribe(sess)

        elif et == blpapi.Event.SUBSCRIPTION_STATUS:
            for msg in event:
                print(f"[sub.stat] {msg.messageType()} cid="
                      f"{msg.correlationIds()[0].value()}")

        elif et == blpapi.Event.SUBSCRIPTION_DATA:
            for msg in event:
                cid = msg.correlationIds()[0].value()
                fields = []
                for fld in ("LAST_PRICE", "BID", "ASK", "VOLUME"):
                    if msg.hasElement(fld):
                        fields.append(f"{fld}={msg.getElementAsFloat(fld)}")
                if fields:
                    print(f"[tick    ] {cid:25s} | {' '.join(fields)}")

    def _subscribe(self, sess):
        sub = blpapi.SubscriptionList()
        for ticker, fields in TOPICS:
            sub.add(ticker, fields, "interval=1.0",
                    blpapi.CorrelationId(ticker))
        sess.subscribe(sub)


def main():
    handler = Handler()
    opts = blpapi.SessionOptions()
    opts.setServerHost("localhost")
    opts.setServerPort(8194)
    opts.setDefaultSubscriptionService("//blp/mktdata")
    opts.setMaxEventQueueSize(100_000)
    sess = blpapi.Session(opts, handler)
    sess.startAsync()
    try:
        handler.stopped.wait()
    except KeyboardInterrupt:
        pass
    finally:
        sess.stop()


if __name__ == "__main__":
    main()
