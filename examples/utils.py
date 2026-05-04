"""Shared utilities for the example scripts.

A `bbg_session` context manager and an `el2py` parser are the two
things every other example reuses.
"""

from __future__ import annotations
from contextlib import contextmanager
from typing import Iterable, Optional

import blpapi


@contextmanager
def bbg_session(host: str = "localhost",
                port: int = 8194,
                services: Iterable[str] = ("//blp/refdata",),
                auth: Optional[str] = None):
    """Open a sync DAPI/SAPI session, open the requested services, and
    yield the session.  Closes everything on exit."""
    opts = blpapi.SessionOptions()
    opts.setServerHost(host)
    opts.setServerPort(port)
    if auth is not None:
        opts.setAuthenticationOptions(auth)
    opts.setAutoRestartOnDisconnection(True)
    opts.setNumStartAttempts(3)

    sess = blpapi.Session(opts)
    if not sess.start():
        raise RuntimeError(f"Session.start() failed (host={host}, port={port})")
    try:
        for svc in services:
            if not sess.openService(svc):
                raise RuntimeError(f"openService failed: {svc}")
        yield sess
    finally:
        sess.stop()


def el2py(el: blpapi.Element):
    """Recursively convert a blpapi.Element tree into native Python."""
    if el.isArray():
        return [el2py(el.getValueAsElement(i)) for i in range(el.numValues())]
    if el.numElements() > 0:
        return {str(el.getElement(i).name()): el2py(el.getElement(i))
                for i in range(el.numElements())}
    if el.isNull():
        return None
    try:
        return el.getValue()
    except Exception:
        return None


def drain_response(sess: blpapi.Session, timeout_ms: int = 10_000):
    """Yield messages from the event queue until a final RESPONSE arrives."""
    while True:
        ev = sess.nextEvent(timeout_ms)
        for msg in ev:
            yield msg
        if ev.eventType() == blpapi.Event.RESPONSE:
            return


def append_overrides(req: blpapi.Request, overrides: dict[str, str]) -> None:
    """Append (fieldId, value) override pairs to a request."""
    if not overrides:
        return
    ovs = req.getElement("overrides")
    for k, v in overrides.items():
        o = ovs.appendElement()
        o.setElement("fieldId", k)
        o.setElement("value", str(v))


def field_exceptions(security_data: blpapi.Element) -> list[dict]:
    """Return a list of {fieldId, message, category} for failed fields."""
    out = []
    if not security_data.hasElement("fieldExceptions"):
        return out
    fex = security_data.getElement("fieldExceptions")
    for i in range(fex.numValues()):
        fe = fex.getValueAsElement(i)
        ei = fe.getElement("errorInfo")
        out.append({
            "fieldId":  fe.getElementAsString("fieldId"),
            "category": ei.getElementAsString("category"),
            "message":  ei.getElementAsString("message"),
        })
    return out
