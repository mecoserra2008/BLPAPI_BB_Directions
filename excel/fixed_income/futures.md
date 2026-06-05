# Futures in Excel (fixed-income focus)

Yellow keys: `Comdty` for bond and short-rate futures, `Curncy` for
FX futures. For commodities and equity-index futures see
[docs/asset_classes/futures.md](../../docs/asset_classes/futures.md).

This file focuses on **fixed-income** futures: bond contracts
(`TY`, `RX`, `JB`, `OE`, etc.) and **short-rate / IR strips**
(`SR3`, `FF`, `ER`, `SO`, `JY`, `EI`).

## 1 · Generic vs specific tickers

Same model as commodities:

| Form | Example | Use |
|---|---|---|
| Generic active | `TY1 Comdty` | Time series, monitor |
| 2nd-month | `TY2 Comdty` | Term structure |
| Specific contract | `TYZ5 Comdty` | Term-structure snapshot, exact roll |

Generic = Bloomberg rolls underneath. Specific = pinned to that
contract.

```excel
=BDP("TY1 Comdty", "PX_LAST")            ' generic active
=BDP("TYZ5 Comdty", "PX_LAST")           ' Dec-25
=BDP("TYZ25 Comdty", "PX_LAST")          ' same, two-digit year
```

For stored data prefer two-digit-year (`Z25` not `Z5`) to avoid
ambiguity in archives.

## 2 · Bond futures

| Generic | Underlying | Exchange |
|---|---|---|
| `TU1 Comdty` | US 2Y Note | CBOT |
| `FV1 Comdty` | US 5Y Note | CBOT |
| `TY1 Comdty` | US 10Y Note | CBOT |
| `UXY1 Comdty` | US Ultra 10Y | CBOT |
| `US1 Comdty` | US Long Bond | CBOT |
| `WN1 Comdty` | US Ultra Long | CBOT |
| `RX1 Comdty` | German Bund 10Y | Eurex |
| `OE1 Comdty` | Bobl 5Y | Eurex |
| `DU1 Comdty` | Schatz 2Y | Eurex |
| `UB1 Comdty` | Buxl 30Y | Eurex |
| `IK1 Comdty` | BTP 10Y | Eurex |
| `OAT1 Comdty` | OAT 10Y | Eurex |
| `OEU1 Comdty` | BTAN 5Y | Eurex |
| `G 1 Comdty` (note space) | Gilt 10Y | ICE Europe |
| `JB1 Comdty` | JGB 10Y | OSE |

## 3 · Short-rate / IR futures

| Generic | Underlying |
|---|---|
| `SR3A Comdty` | SOFR 3M (white-pack A = front quarterly) |
| `SFR1 Comdty` | SOFR 3M alt naming |
| `FF1 Comdty` | Fed Funds 30D |
| `ED1 Comdty` | Eurodollar 3M (retired post-2023) |
| `ER1 Comdty` | EURIBOR 3M (transitioning) |
| `EI1 Comdty` | €STR 3M |
| `L 1 Comdty` | Short Sterling (retired) |
| `SO1 Comdty` | SONIA 3M |
| `JY1 Comdty` (Comdty, not Curncy!) | TONA 3M |

> `JY1 Comdty` is the JPY *rate* future. `JY1 Curncy` is the CME
> JPY/USD *FX* future. Yellow key disambiguates.

## 4 · Snapshot fields

```excel
=BDP("TY1 Comdty", "PX_LAST")
=BDP("TY1 Comdty", "PX_SETTLE")         ' prefer for daily total return
=BDP("TY1 Comdty", "PX_BID")
=BDP("TY1 Comdty", "PX_ASK")
=BDP("TY1 Comdty", "OPEN_INT")
=BDP("TY1 Comdty", "OPEN_INT_DATE")
=BDP("TY1 Comdty", "FUT_AGGTE_VOL")     ' aggregate volume
=BDP("TY1 Comdty", "FUT_AGGTE_OPEN_INT")
```

## 5 · Contract specs

```excel
=BDP("TYZ5 Comdty", "FUT_TICK_SIZE")          ' 1/64 in price terms
=BDP("TYZ5 Comdty", "FUT_TICK_VAL")           ' $ per tick
=BDP("TYZ5 Comdty", "FUT_VAL_PT")             ' $ per 1.00 price point
=BDP("TYZ5 Comdty", "FUT_CONT_SIZE")          ' notional
=BDP("TYZ5 Comdty", "FUT_TRADING_UNITS")
=BDP("TYZ5 Comdty", "FUT_FIRST_TRADE_DT")
=BDP("TYZ5 Comdty", "LAST_TRADEABLE_DT")
=BDP("TYZ5 Comdty", "FUT_NOTICE_FIRST")
=BDP("TYZ5 Comdty", "FUT_DLV_DT_FIRST")
=BDP("TYZ5 Comdty", "FUT_DLV_DT_LAST")
=BDP("TYZ5 Comdty", "FUT_CUR_GEN_TICKER")     ' the generic this currently pins
```

For a generic series, the *current* specific underlying:

```excel
=BDP("TY1 Comdty", "FUT_CUR_GEN_TICKER")      ' e.g. "TYU5 Comdty"
=BDP("TY1 Comdty", "FUT_GEN_FIRST_TRADE_DT")  ' when it started being TY1
```

## 6 · The futures chain (`FUT_CHAIN`)

```excel
=BDS("TY1 Comdty", "FUT_CHAIN")
=BDS("TY1 Comdty", "FUT_CHAIN",
     "INCLUDE_EXPIRED_CONTRACTS", "Y")
=BDS("TY1 Comdty", "FUT_CHAIN",
     "INCLUDE_EXPIRED_CONTRACTS", "N",
     "CHAIN_DATE", "20250502")
```

Output: one column, `Security Description` per row. Back-fill into
`BDP` for term-structure snapshots.

### Term-structure worksheet

```
Sheet "TY Curve":
   A                                                B
1  Chain (BDS spill)                                Settle
2  =BDS("TY1 Comdty","FUT_CHAIN","INCLUDE_EXPIRED_CONTRACTS","N","CHAIN_DATE",TEXT(TODAY(),"YYYYMMDD"))
3  (spills downward)
4  ...

   D                          E                              F
1  Contract                   Px settle                      Delivery
2  =A2                        =BDP(D2,"PX_SETTLE")           =BDP(D2,"FUT_DLV_DT_FIRST")
3  =A3                        =BDP(D3,"PX_SETTLE")           =BDP(D3,"FUT_DLV_DT_FIRST")
...
```

Then plot column E vs F for the term structure.

## 7 · Generic-series history with roll control

```excel
' Active-month roll (Bloomberg's default)
=BDH("TY1 Comdty", "PX_LAST",
     DATE(2014,1,1), TODAY(),
     "Per=cdr", "Days=T", "Fill=P", "Roll=A")

' Open-interest based roll
=BDH("TY1 Comdty", "PX_LAST",
     DATE(2014,1,1), TODAY(),
     "Per=cdr", "Days=T", "Fill=P", "Roll=O")

' Notice-based (T-N days before first notice)
=BDH("TY1 Comdty", "PX_LAST",
     DATE(2014,1,1), TODAY(),
     "Per=cdr", "Days=T", "Fill=P", "Roll=N")

' Front (no roll — gap at each expiry)
=BDH("TY1 Comdty", "PX_LAST",
     DATE(2014,1,1), TODAY(),
     "Per=cdr", "Days=T", "Fill=P", "Roll=F")
```

`Roll=A` (Active) is the most common backtest default.

## 8 · Cheapest-to-deliver, implied repo, basis

The CTD-related field family lives on the specific contract:

```excel
=BDP("TYZ5 Comdty", "FUT_CTD_BOND")          ' bond ticker of current CTD
=BDP("TYZ5 Comdty", "FUT_CTD_FRWD_PX")       ' CTD forward price
=BDP("TYZ5 Comdty", "IMPLIED_REPO_RATE")     ' implied repo (%)
=BDP("TYZ5 Comdty", "NET_BASIS")             ' basis (bps)
=BDP("TYZ5 Comdty", "GROSS_BASIS")
=BDP("TYZ5 Comdty", "NET_BASIS_BCT")         ' (alternative)
=BDP("TYZ5 Comdty", "CTD_FRWD_PX")
=BDP("TYZ5 Comdty", "DELIVERY_DAY_RATE")
=BDP("TYZ5 Comdty", "CONV_FACTOR")           ' conversion factor of CTD
```

You can also chain it: take the CTD ticker, pull its bond fields:

```
A2: =BDP("TYZ5 Comdty","FUT_CTD_BOND")       ' e.g. "T 4 ½ 11/15/33 Govt"
B2: =BDP(A2, "PX_LAST")
C2: =BDP(A2, "DUR_ADJ_MID")
D2: =BDP(A2, "MATURITY")
```

## 9 · Short-rate strips — the standard layout

A "white pack" / "red pack" SOFR strip in one column:

```
   A           B                C                  D                E
1  Code        Future            Px settle          Implied rate (%) Volume
2  SR3A        =A2 & " Comdty"   =BDP(B2,"PX_SETTLE") =100-D2          =BDP(B2,"PX_VOLUME")
3  SR3B        ...
4  SR3C
5  SR3D
6  SR3E
... up to SR3X (5+ years out)
```

For a continuous calendar layout (one row per quarter), pre-list
specific contracts `SFRH5`, `SFRM5`, `SFRU5`, `SFRZ5`, `SFRH6`, …

```excel
=BDP("SFRZ5 Comdty", "PX_SETTLE")
=BDP("SFRZ5 Comdty", "FUT_DLV_DT_FIRST")
```

Implied rate from a SOFR future price = `100 − price`.

For FRA-style strip rates, compare against the OIS curve from
[04_curves.md](../04_curves.md).

## 10 · €STR and SONIA strips

Same layout, different tickers:

```excel
=BDP("EI1 Comdty",  "PX_SETTLE")        ' €STR 3m active
=BDP("EIH6 Comdty", "PX_SETTLE")        ' €STR Mar-26
=BDP("SO1 Comdty",  "PX_SETTLE")        ' SONIA 3m active
=BDP("SOZ5 Comdty", "PX_SETTLE")        ' SONIA Dec-25
```

For TONA: `JY1 Comdty` family.

## 11 · Calendar spreads as a single instrument

Bloomberg supports direct spread addressing:

```excel
=BDP("TYZ5-TYM5 Comdty", "PX_LAST")      ' Z5 minus M5
=BDP("RXM5-OEM5 Comdty", "PX_LAST")      ' Bund-Bobl
=BDP("TYM5-RXM5 Comdty", "PX_LAST")      ' US-DE 10y bond future spread
```

`PX_LAST` is `leg1 − leg2`.

## 12 · CFTC Commitment of Traders

Available as fields on the front contract / generic series:

```excel
=BDH("TY1 Comdty",
     {"NCOMM_LONG_POS","NCOMM_SHORT_POS","COMM_LONG_POS","COMM_SHORT_POS","OI_AGG"},
     DATE(2014,1,1), TODAY(), "Per=cw", "Days=W", "Fill=P")
```

Then compute `spec_net = NCOMM_LONG − NCOMM_SHORT` and
`spec_pct = spec_net / OI_AGG`.

Weekly cycle: Tuesday positions released Friday 15:30 ET — refresh
overnight.

## 13 · Total-return (futures-rolled) series

For asset-allocation backtests on bond / rate futures, avoid the
gap-at-roll problem with pre-built TR indices:

```
SPESSP Index            S&P US 10Y Note futures TR
BBUSBOND Index          Bloomberg US Treasury futures (alt)
```

Or use the Bloomberg-rolled generic (`Roll=A`) with `BDH`.

## 14 · Worked sheet — bond future basis monitor

```
Sheet "TY Basis":
   A                  B                 C                D              E
1  Contract            CTD ticker        CTD px           Implied repo   Net basis (bps)
2  TYU5 Comdty         =BDP(A2,"FUT_CTD_BOND")
                                          =BDP(B2,"PX_LAST")
                                                           =BDP(A2,"IMPLIED_REPO_RATE")
                                                                          =BDP(A2,"NET_BASIS")
3  TYZ5 Comdty         ...
4  TYH6 Comdty         ...
```

Alongside it, term repo from `BSWP <GO>` (manual entry) or
`USRG3M Index` style funding tickers.

## 15 · Pitfalls

- **Multi-letter month codes don't exist.** Single letter only —
  `F G H J K M N Q U V X Z`. See
  [cheatsheets/month_codes.md](../../cheatsheets/month_codes.md).
- **`Z5` vs `Z25`**: single-digit year is fine for live front-month
  but ambiguous for archives spanning a decade.
- **Generic series ≠ TR series.** `TY1 Comdty` close-to-close has
  step changes on each roll day. For backtests use `Roll=A` in
  `BDH`, or one of the SPESSP / BBUSBOND TR indices.
- **Settle vs last**: prefer `PX_SETTLE` over `PX_LAST` for the
  short-rate strip. Front-month is liquid but back-month settles
  print at the exchange's official mark — far more reliable.
- **CTD switches between contracts.** When two bonds are very close
  on yield, the CTD can flip. Models that assume a stable CTD
  produce wrong basis. Pull `FUT_CTD_BOND` per-contract per-day.
- **`OPEN_INT` lags 1 day.** Exchange reports OI for the previous
  session. Same for COT — refresh logic must respect the lag.
- **Holiday calendars vary.** ICE Europe, CBOT, Eurex, OSE, TFX —
  all different. Use `Calendar=CME` / `Calendar=Eurex` etc. in
  `BDH`.
- **SOFR vs Eurodollar splice.** Pre-2024 series under `ED*` (3M
  LIBOR future). Post-2024 under `SR3*` / `SFR*`. Splice manually
  if you need a continuous IR-future series; the conversion factor
  is approximate (3M LIBOR → 3M SOFR adjusted by the CME conversion
  schedule).
