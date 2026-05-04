# 01 · Install & Prerequisites

## What you need before any code

1. **An entitlement.** No entitlement, no data. Three flavours:
   - **DAPI** (Desktop API): bundled with a Bloomberg Terminal subscription.
     Requires the Terminal to be **logged in on the same machine** (Windows,
     macOS, or via Citrix/Remote Desktop). Server defaults to
     `localhost:8194`. Limits scale with your hit-cap (≈500K data
     points/day).
   - **SAPI** (Server API): named-user license that lets *one* Terminal
     identity be served from a server to remote clients on the same
     subnet. Cheaper than B-PIPE but bound to the user.
   - **B-PIPE** (Enterprise): application authentication, TLS, multi-user,
     no Terminal required. Higher caps, redundancy, and the only way to
     get >140 days of intraday history. Requires firewall rules to the
     two B-PIPE PoP gateways.

2. **A Python environment.** 3.10+ recommended. The `blpapi` wheel is a
   thin Python binding around a vendored C++ SDK; pip installs both at
   once on supported platforms.

3. **Network access** to Bloomberg's gateway:
   - DAPI: loopback (`127.0.0.1:8194`) — the local `bbcomm` service is the
     bridge to the Terminal.
   - SAPI: TCP to the SAPI server (commonly `8194`).
   - B-PIPE: TCP to two PoP IPs on `8194` and `8294` plus TLS.

## Installing the Python SDK

Bloomberg hosts wheels on a private index. Always install with
`--index-url`, not `-i pip install -i ... blpapi` from PyPI (PyPI's
`blpapi` is unrelated — different project).

```bash
python -m pip install \
  --index-url=https://blpapi.bloomberg.com/repository/releases/python/simple/ \
  blpapi
```

Pin a version if you're committing a `requirements.txt`:

```
--index-url https://blpapi.bloomberg.com/repository/releases/python/simple/
blpapi==3.21.0
```

### Verifying

```bash
python -c "import blpapi; print(blpapi.__version__)"
```

The wheel **bundles the C++ SDK** since v3.20. On older Pythons or
exotic platforms (Linux ARM, FreeBSD), pip won't find a wheel — install
the C++ SDK manually from
<https://www.bloomberg.com/professional/support/api-library/> and set:

```bash
export BLPAPI_ROOT=/opt/bloomberg/blpapi_cpp_3.21.0
export LD_LIBRARY_PATH=$BLPAPI_ROOT/Linux:$LD_LIBRARY_PATH
```

then re-install the Python wheel.

## Optional but strongly recommended for research

```bash
python -m pip install xbbg pdblp pandas pyarrow numpy
```

- `xbbg` — pandas-native wrapper over `blpapi`, on-disk caching.
- `pdblp` — older but very stable. Useful as a fallback.
- `pandas` / `pyarrow` — every recipe in this repo lands data in a
  DataFrame, often persisted as parquet for re-use.

## Where things live on disk

| Component | Linux | macOS | Windows |
|---|---|---|---|
| `bbcomm` (Terminal-API bridge) | n/a | `/Applications/Bloomberg/bbcomm` | `C:\blp\API\bbcomm` |
| C++ SDK headers | `$BLPAPI_ROOT/include` | same | same |
| Python wheel | site-packages | site-packages | site-packages |
| Default log dir | `$HOME/.blpapi/logs` | same | `%APPDATA%\Bloomberg\blpapi\logs` |

## Sanity-check the connection

The shortest end-to-end test is in
[`examples/connect_dapi.py`](../examples/connect_dapi.py):

```bash
python examples/connect_dapi.py
```

If it prints `session.start ok → opened //blp/refdata` you have a working
pipe. If it prints **session.start failed**:

1. Is the Terminal logged in? The Terminal session must be active, not
   "Connecting…", and you must be physically signed in.
2. Is `bbcomm` running? On Windows it's a tray service; on macOS it
   launches with the Terminal.
3. Try `nc -zv 127.0.0.1 8194` (or `Test-NetConnection` on Windows).
4. Are you running from the same OS user as the Terminal? `OS_LOGON`
   auth ties to the logged-in account.

## What the `blpapi` package gives you

```python
import blpapi
dir(blpapi)
# Core: Session, SessionOptions, EventDispatcher, Service, Request,
#       Subscription, SubscriptionList, Element, Event, Message,
#       Identity, AuthOptions, CorrelationId, Name, DataType, ...
```

The five things you'll touch 90% of the time: `SessionOptions`,
`Session`, `Service.createRequest`, `Element` (returned via
`message.getElement(...)`), and `Subscription`. Everything else is
plumbing.

## Reproducible environments

A minimum `requirements.txt` for this repo:

```
--index-url https://blpapi.bloomberg.com/repository/releases/python/simple/
--extra-index-url https://pypi.org/simple

blpapi==3.21.0
xbbg==0.7.7
pandas>=2.0
pyarrow>=14
numpy>=1.26
```

Note the **two index URLs**: Bloomberg's index is the *primary* (so
`blpapi` resolves there); PyPI is the extra (so everything else
resolves normally).
