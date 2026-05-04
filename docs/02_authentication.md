# 02 · Authentication

The `Session` is what holds the network connection; **`Identity`** is what
tells Bloomberg who is asking. With DAPI on `localhost` you almost never
build an `Identity` explicitly — the Terminal user is implicit. With SAPI
or B-PIPE you do.

## Auth modes (`setAuthenticationOptions`)

| Mode string | Used by | Notes |
|---|---|---|
| `OS_LOGON` | DAPI default | Terminal login = the OS user. No Identity needed for `//blp/refdata`. |
| `OS_LOGON_AND_DIRECTORY_SERVICE,DirSvcProperty=...` | SAPI | OS user mapped to an Active Directory property (typically `cn`). |
| `DIRECTORY_SERVICE,DirSvcProperty=cn` | SAPI | Pure DS auth. |
| `APPLICATION_ONLY,AppName=...` | B-PIPE | Application certificate / EMRS-managed application name. |
| `USER_AND_APPLICATION,AuthenticationType=...,AppName=...` | B-PIPE multi-user | Combines a per-user OS_LOGON with an app cert. |
| `MANUAL` | Custom | You feed a token from `generateToken()`. |

Construct via:

```python
opts = blpapi.SessionOptions()
opts.setAuthenticationOptions("OS_LOGON")   # or one of the above
```

## DAPI — the trivial case

```python
import blpapi

opts = blpapi.SessionOptions()
opts.setServerHost("localhost")
opts.setServerPort(8194)
session = blpapi.Session(opts)
assert session.start()
assert session.openService("//blp/refdata")
```

No Identity, no TLS, no `sendAuthorizationRequest`. The Terminal user is
authenticated as soon as `bbcomm` accepts the loopback connection.

## SAPI — directory-service auth

```python
opts = blpapi.SessionOptions()
opts.setServerHost("sapi.example.intra")
opts.setServerPort(8194)
opts.setAuthenticationOptions(
    "AuthenticationType=OS_LOGON_AND_DIRECTORY_SERVICE;"
    "DirSvcPropertyName=cn"
)
session = blpapi.Session(opts)
session.start()

# Build an Identity tied to the OS user
identity = session.createIdentity()

auth_svc = "//blp/apiauth"
session.openService(auth_svc)
auth_req = session.getService(auth_svc).createAuthorizationRequest()
auth_req.set("authId", "your.username")            # the AD cn
auth_req.set("ipAddress", "10.0.0.42")             # client IP
session.sendAuthorizationRequest(auth_req, identity)

# Drain events until AUTHORIZATION_SUCCESS
while True:
    ev = session.nextEvent(5000)
    for msg in ev:
        if msg.messageType() == blpapi.Name("AuthorizationSuccess"):
            authorized = True
    if ev.eventType() == blpapi.Event.RESPONSE:
        break

# Now sendRequest(req, identity)
```

Pass the `identity` to **every** `sendRequest` and `subscribe` call.

## B-PIPE — application + TLS

The standard pattern:

```python
opts = blpapi.SessionOptions()
opts.setServerAddress("bpipe-pop1.bloomberg.com", 8194, 0)
opts.setServerAddress("bpipe-pop2.bloomberg.com", 8194, 1)   # failover
opts.setAuthenticationOptions(
    "AuthenticationMode=APPLICATION_ONLY;"
    "ApplicationAuthenticationType=APPNAME_AND_KEY;"
    "ApplicationName=YOURFIRM:YOURAPP"
)

# TLS material. PKCS#12 client cert + the CA bundle Bloomberg gave you.
tls = blpapi.TlsOptions.createFromBlobs(
    clientCredentials=open("client.p12", "rb").read(),
    clientCredentialsPassword="your-p12-password",
    trustedCertificates=open("rootCertificate.pk7", "rb").read(),
)
opts.setTlsOptions(tls)

# Optional zlib compression on the wire
opts.setSessionIdentityOptions(blpapi.AuthOptions.createWithApp("YOURFIRM:YOURAPP"))
opts.setMaxPendingRequests(1024)

session = blpapi.Session(opts)
session.start()
```

If the auth string + TLS is right, `session.start()` succeeds and you can
go directly to `openService` — the **session identity** is already the
application. Per-user (`USER_AND_APPLICATION`) needs an extra
`createIdentity()` + `sendAuthorizationRequest` cycle on top.

## Failover and redundancy

`SessionOptions.setServerAddress(host, port, index)` accepts multiple
endpoints. The session connects to the lowest-index reachable host and
fails over automatically. For B-PIPE always configure both PoPs.

```python
opts.setServerAddress("primary", 8194, 0)
opts.setServerAddress("backup",  8194, 1)
opts.setNumStartAttempts(3)
opts.setAutoRestartOnDisconnection(True)
opts.setKeepAliveEnabled(True)
```

## Token (MANUAL) auth

Mostly used by web/Excel add-ins. You can do it from Python too:

```python
opts.setAuthenticationOptions("AuthenticationType=MANUAL")
session.start()
session.openService("//blp/apiauth")

cid = session.generateToken()         # async
# wait for TOKEN_STATUS event with the token string
# then build an authorization request that contains "token" instead of authId
```

Useful when the user is authenticating via a browser (e.g. SSO flow) and
the resulting token must be relayed to the SDK.

## Multi-Identity (one session, many users)

A SAPI/B-PIPE process can serve N users by issuing N `Identity` objects.
Each request/subscription carries its own identity. Make sure each user's
entitlements include the requested data — Bloomberg will reject otherwise.

## Common auth errors and what they mean

| Error / message | Likely cause |
|---|---|
| `Session.start() returned False` | `bbcomm` not running, or TCP blocked, or wrong host/port |
| `AuthorizationFailure` with reason `Invalid authId` | AD `cn` doesn't match your Terminal's profile |
| `EntitlementChanged` during a subscription | Admin revoked or moved a market-data permission |
| `INVALID_REQUEST` immediately on `sendRequest` | Forgot to pass the Identity, or the Identity is from a stale session |
| Silence after `openService` succeeds | DAPI: Terminal locked screen → `bbcomm` paused. Unlock it. |

## When to actually need an `Identity` object

- Always for B-PIPE / SAPI requests.
- DAPI: only if you'll later move the same code path to SAPI/B-PIPE.
  Pre-creating `identity = session.createIdentity()` and passing it
  through is harmless on DAPI and saves a refactor later.
