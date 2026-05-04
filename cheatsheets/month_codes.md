# Futures Month Codes

The single-letter code for each delivery month, used in every
futures ticker (commodities, equity-index, bond, rate, FX).

| Letter | Month |
|---|---|
| `F` | January |
| `G` | February |
| `H` | March |
| `J` | April |
| `K` | May |
| `M` | June |
| `N` | July |
| `Q` | August |
| `U` | September |
| `V` | October |
| `X` | November |
| `Z` | December |

## Year encoding

- **Single digit** (e.g. `Z5`): last digit of the year. Ambiguous
  beyond 10 years; Bloomberg interprets as the *next* year ending in
  that digit. Fine for live tickers.
- **Two digits** (e.g. `Z25`): explicit. Use for stored / historical
  panels.

## Examples

```
ESM5   = ES (S&P E-mini), M = June, 5 = 2025
ESM25  = same, two-digit year (preferred for stored data)
CLZ5   = WTI Dec-2025
CLG6   = WTI Feb-2026
TYZ5   = US 10Y Note Dec-2025
RXM5   = Bund Jun-2025
GCG6   = Gold Feb-2026
NKZ5   = Nikkei 225 Dec-2025

# Bloomberg generic (active rolling):
ES1 Index    = front-month ES
ES2 Index    = 2nd-month
TY1 Comdty   = front-month TY
CL1 Comdty   = front-month WTI
```

## Common contract-month patterns

### Quarterly cycles (Mar / Jun / Sep / Dec) — `H M U Z`

Equity-index futures (ES, NQ, RTY, VG, GX, CF, NK, HI, KM, etc.)
trade quarterly. So the chain is `ESH5, ESM5, ESU5, ESZ5, ESH6, ...`.

Bond futures (TY, FV, TU, US, RX, OE, DU, etc.) also quarterly.

### Monthly — energy, metals, FX

Most energy, metals, and FX futures trade every month. WTI: `CLF6,
CLG6, CLH6, CLJ6, CLK6, CLM6, ...`.

### Specific cycles for some ag products

- Corn: `H K N U Z` (March, May, July, September, December)
- Soybeans: `F H K N Q U X` (Jan, Mar, May, Jul, Aug, Sep, Nov)
- Wheat: `H K N U Z`
- Sugar #11: `H K N V` (March, May, July, October)
- Coffee C: `H K N U Z`
- Cocoa: `H K N U Z`
- Cotton: `H K N V Z`
- Live cattle: `G J M Q V Z` (Feb, Apr, Jun, Aug, Oct, Dec)
- Lean hogs: `G J K M N Q V Z`

### IR / short-rate strips

- SOFR (`SR3*` / `SFR*`): white pack = first 4 quarterly contracts;
  red, green, blue packs = next 4 each. Pack codes (`SR3A` = 1st white,
  `SR3B` = 2nd, etc.) identify the position.
- Fed Funds (`FF*`): every month. `FFM5` = June 2025.
- Old Eurodollar (`ED*`): quarterly. Retired effective 2024.
- SONIA (`SO*`): quarterly. €STR (`EI*`): quarterly.

## Memory tricks

The codes go **F G H J K** (5 in a row, no I), then **M N**, then
**Q U V X Z** (5 more). Avoid the letters `A`, `B`, `C`, `D`, `E`,
`I`, `L`, `O`, `P`, `R`, `S`, `T`, `W`, `Y` to prevent confusion with
common ticker letters.

## Programmatic helpers

```python
MONTH_CODES = {
    1: "F", 2: "G", 3: "H", 4: "J", 5: "K", 6: "M",
    7: "N", 8: "Q", 9: "U", 10: "V", 11: "X", 12: "Z"
}
CODE_TO_MONTH = {v: k for k, v in MONTH_CODES.items()}

def to_ticker(root, month, year, yk):
    return f"{root}{MONTH_CODES[month]}{year % 100:02d} {yk}"

def parse_ticker(t):
    # e.g. "CLZ5 Comdty" or "ESH25 Index"
    import re
    m = re.match(r"([A-Z]+)\s*([FGHJKMNQUVXZ])(\d{1,2})\s+(\w+)", t)
    if not m: return None
    root, mc, yy, yk = m.groups()
    yy = int(yy)
    yy = 2000 + yy if yy < 50 else 1900 + yy   # disambiguate single-digit
    return dict(root=root, month=CODE_TO_MONTH[mc], year=yy, yk=yk)
```

## Pitfalls

- Some commodities skip months in their official cycle; addressing
  a non-cycle month returns `securityError`.
- `CLZ5 Comdty` vs `CLZ25 Comdty` both work today (Z5 maps to 2025
  while we're still in the 2020s); after 2030, prefer two-digit.
- Spaces matter: `C 1 Comdty` for corn (single-letter root needs the
  space). Same for `S `, `W `, `G `, `Z ` (some equity index futures).
- For pre-2000 historical data, `Z9` could be 1999 or 2009. Always
  use four-digit year in stored panels.
