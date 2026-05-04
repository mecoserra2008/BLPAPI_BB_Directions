# Examples

Each script is self-contained -- run it from the `examples/` directory:

```bash
cd examples
python connect_dapi.py
python reference_data.py
python historical_data.py
python intraday_bars.py
python intraday_ticks.py
python beqs_universe.py
python subscription.py        # async, ctrl-C to stop
python bulk_fields.py
python futures_chain.py
python fx_forwards.py
python bond_analytics.py
python field_search.py
python overrides.py
python equity_universe.py
python xbbg_quickstart.py     # requires `pip install xbbg`
```

All examples assume DAPI on `localhost:8194` (default).  For SAPI /
B-PIPE adjust the `bbg_session(...)` call in `utils.py` (host, port,
auth options).

## utils.py

Shared helpers:

- `bbg_session(...)`: context manager for opening a session with the
  requested services.
- `drain_response(sess)`: yields messages until the final RESPONSE
  event.
- `append_overrides(req, dict)`: idiomatic way to add overrides.
- `el2py(element)`: recursive `Element` → Python conversion.

## requirements.txt

```
--index-url https://blpapi.bloomberg.com/repository/releases/python/simple/
--extra-index-url https://pypi.org/simple

blpapi==3.21.0
pandas>=2.0
xbbg==0.7.7        # optional, for xbbg_quickstart.py
pyarrow>=14        # optional, for parquet caching in recipes
```

Install with `pip install -r requirements.txt` from the repo root.
