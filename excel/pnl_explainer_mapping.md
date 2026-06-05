# PnL Explainer × Bloomberg Excel — Field Map

A one-file mapping between every quantity in the PnL-explainer
worksheet and the exact Bloomberg Excel formula that fetches it,
given the inputs we usually have (**ISIN / CUSIP / FIGI, notional,
trade date, purchase price, number of contracts**).

Notation follows the handwritten notes:

```
r   = OIS rate at the bond's maturity tenor
g   = Gov yield − OIS                 (gov-OIS basis)
q   = Swap yield − Gov yield          (swap-gov basis)
i   = Bond yield − Swap yield         (i-spread, the credit piece)

Bond yield − r       = g + q + i
Gspread (vs gov)     = q + i
ZOIS  (vs OIS)       = g + q + i
ASW   (vs swap)      ≈ i

PV(y+Δy) ≈ PV(y) − PV·Dc·Δy + ½·PV·Cc·(Δy)²

Full PnL = Duration_PnL + Convexity_PnL + Hedge_PnL
         + Carry_PnL    + Roll_PnL     + FX_PnL
         + Credit_PnL   + Basis_PnL    + Residual

Carry = Coupon accrual + Roll-to-par + Funding cost
Hedge efficiency = 1 − |Residual bvol| / |Bond bvol|
```

All formulas below use comma separators; on continental Excel
(DE/FR/ES/PT-PT) replace `,` with `;`. Replace `A2`/`B2`/etc. with
the cell holding the relevant input.

---

## 0 · Layout assumption

Every formula assumes a row-per-trade panel:

| Col | Holds |
|---|---|
| `A` | ISIN (or other id) |
| `B` | Notional (face) |
| `C` | Trade date |
| `D` | Purchase price (clean, /100) |
| `E` | Side (`+1` long / `−1` short) |
| `F` | Hedge contracts (signed) |
| `G` | Hedge instrument ticker (e.g. `"TYZ5 Comdty"`) |

Then derived columns from H onwards use the mapping below.

Named ranges used throughout:

| Name | Refers to |
|---|---|
| `Today` | `=TEXT(TODAY(),"YYYYMMDD")` |
| `Yesterday` | `=TEXT(WORKDAY(TODAY(),-1),"YYYYMMDD")` |
| `Settle` | `=TEXT(WORKDAY(TODAY(),1),"YYYYMMDD")` (T+1; use +2 for EUR corp) |
| `OISCurveUSD` | `="S490"` |
| `OISCurveEUR` | `="S514"` |
| `OISCurveGBP` | `="S141"` |
| `OISCurveJPY` | `="S510"` |

---

## 1 · Identifier resolution (ISIN / CUSIP / FIGI → BBG ticker)

Bloomberg accepts identifiers with or without an explicit yellow
key. The empty-key form is the safest if you don't know whether the
bond is `Govt` / `Corp` / `Mtge`:

```excel
' Canonical Bloomberg ticker from any identifier
=BDP("/isin/"  & $A2, "PARSEKYABLE_DES")
=BDP("/cusip/" & $A2, "PARSEKYABLE_DES")
=BDP("/figi/"  & $A2, "PARSEKYABLE_DES")

' If you already know the yellow key:
=BDP("/isin/"  & $A2 & " Govt", "PARSEKYABLE_DES")
=BDP("/isin/"  & $A2 & " Corp", "PARSEKYABLE_DES")
=BDP("/isin/"  & $A2 & " Mtge", "PARSEKYABLE_DES")
```

Probe the yellow key automatically:

```excel
=IFERROR(BDP("/isin/" & $A2 & " Govt", "PARSEKYABLE_DES"),
  IFERROR(BDP("/isin/" & $A2 & " Corp", "PARSEKYABLE_DES"),
   IFERROR(BDP("/isin/" & $A2 & " Mtge", "PARSEKYABLE_DES"),
           "UNKNOWN")))
```

Once resolved, store the BBG ticker in column **H** and use `$H2`
everywhere below.

### Cross-id fields

```excel
=BDP($H2, "ID_BB_GLOBAL")     ' FIGI
=BDP($H2, "ID_ISIN")
=BDP($H2, "ID_CUSIP")
=BDP($H2, "ID_SEDOL1")
=BDP($H2, "ID_BB_UNIQUE")
=BDP($H2, "ID_BB_SEC_NUM_DES")
```

---

## 2 · Trade-level quantities (NOT from Bloomberg)

These come from your book / OMS / position file, not the API.

| Quantity | Excel cell | Source |
|---|---|---|
| Notional / face | `$B2` | book |
| Trade date | `$C2` | book |
| Purchase price (clean, /100) | `$D2` | book |
| Side | `$E2` (`+1`/`−1`) | book |
| Hedge contracts | `$F2` (signed) | book |
| Hedge ticker | `$G2` | book |

Derived MV-style:

```excel
' Purchase value (cash that left the desk)
I2: =$B2 * $D2 / 100 + $B2 * BDP($H2,"ACCRUED_INTEREST","SETTLE_DT",TEXT($C2,"YYYYMMDD"))/100

' Current clean market value
J2: =$B2 * BDP($H2,"PX_LAST") / 100

' Current dirty MV (the figure used for funding)
K2: =$B2 * (BDP($H2,"PX_LAST") + BDP($H2,"ACCRUED_INTEREST")) / 100

' Clean price P&L
L2: =$E2 * ( $B2 * (BDP($H2,"PX_LAST") - $D2) / 100 )
```

---

## 3 · Static bond reference (BDP)

| Notation | Bloomberg field | Excel |
|---|---|---|
| Coupon rate | `CPN` | `=BDP($H2,"CPN")` |
| Coupon frequency | `CPN_FREQ` | `=BDP($H2,"CPN_FREQ")` |
| Coupon type | `CPN_TYP` | `=BDP($H2,"CPN_TYP")` |
| Day count | `DAY_CNT_DES` | `=BDP($H2,"DAY_CNT_DES")` |
| Issue date | `ISSUE_DT` | `=BDP($H2,"ISSUE_DT")` |
| Maturity | `MATURITY` | `=BDP($H2,"MATURITY")` |
| Currency | `CRNCY` | `=BDP($H2,"CRNCY")` |
| Country of risk | `COUNTRY_FULL_NAME` | `=BDP($H2,"COUNTRY_FULL_NAME")` |
| Issuer | `ISSUER` | `=BDP($H2,"ISSUER")` |
| Industry | `ISSUER_INDUSTRY` | `=BDP($H2,"ISSUER_INDUSTRY")` |
| Composite rating | `RTG_BB_COMPOSITE` | `=BDP($H2,"RTG_BB_COMPOSITE")` |
| Amount outstanding | `AMT_OUTSTANDING` | `=BDP($H2,"AMT_OUTSTANDING")` |
| Maturity type | `MTY_TYP` | `=BDP($H2,"MTY_TYP")` |
| Next call date | `NXT_CALL_DT` | `=BDP($H2,"NXT_CALL_DT")` |
| Next call price | `NXT_CALL_PX` | `=BDP($H2,"NXT_CALL_PX")` |
| FRN benchmark | `FLT_BENCHMARK_INDEX` | `=BDP($H2,"FLT_BENCHMARK_INDEX")` |
| FRN spread | `FLT_SPREAD` | `=BDP($H2,"FLT_SPREAD")` |

Tenor (years) — for picking the right curve node:

```excel
=YEARFRAC(TODAY(), BDP($H2,"MATURITY"), 1)
```

---

## 4 · Prices, yields & spreads (today)

These four quantities are the heart of the PnL explainer: yield
splits cleanly into `r + g + q + i` (OIS + gov-OIS basis +
swap-gov basis + i-spread).

```excel
' Yields and spreads today
=BDP($H2, "PX_LAST")                ' clean price
=BDP($H2, "PX_BID")
=BDP($H2, "PX_ASK")
=BDP($H2, "PX_MID")
=BDP($H2, "ACCRUED_INTEREST")
=BDP($H2, "YLD_YTM_MID")            ' = Bond yield (the y in the notes)
=BDP($H2, "YLD_YTM_BID")
=BDP($H2, "YLD_YTM_ASK")
=BDP($H2, "YLD_YTW_MID")
=BDP($H2, "YLD_YTC_MID")

=BDP($H2, "G_SPRD_MID")             ' = Gspread = q + i (vs gov benchmark)
=BDP($H2, "I_SPRD_MID")             ' ≈ i (vs interp swap)
=BDP($H2, "Z_SPRD_MID")             ' = ZOIS  ≈ g + q + i (zero-vol over swap)
=BDP($H2, "OAS_SPREAD_MID")
=BDP($H2, "ASSET_SWAP_SPD_MID")
=BDP($H2, "DISC_MARGIN")            ' floaters

=BDP($H2, "BENCHMARK_SECURITY")
=BDP($H2, "BENCHMARK_NAME")
=BDP($H2, "PRC_AS_OF_DT")
=BDP($H2, "PRICING_SOURCE")
=BDP($H2, "LAST_PX_DT")             ' for staleness check
```

> Bloomberg's `Z_SPRD_MID` is the zero-volatility spread over the
> **swap** curve, which is the cleanest empirical proxy for the
> notes' `Bond yield − OIS = g + q + i` once the discounting curve
> is the OIS. If your firm computes Z-spread over the OIS curve
> directly, use the YAS override path (§14) instead.

### Yesterday & period changes — for Δy decomposition

```excel
' Yield yesterday
=INDEX(BDH($H2,"YLD_YTM_MID",WORKDAY(TODAY(),-1),WORKDAY(TODAY(),-1),
            "Per=cdr","Days=W","Fill=P","Dts=H","Cols=N"),1,1)

' Δy = today − yesterday (in bps)
=(BDP($H2,"YLD_YTM_MID") - INDEX(BDH(...),1,1)) * 100
```

Same pattern for `G_SPRD_MID`, `I_SPRD_MID`, `Z_SPRD_MID`,
`ASSET_SWAP_SPD_MID`, `OAS_SPREAD_MID`.

---

## 5 · Risk metrics (Dc, Cc, DV01)

Bloomberg-published values match the notes' `Dc` and `Cc` to a
working approximation:

| Notation | Bloomberg field | Comment |
|---|---|---|
| `Dc` | `DUR_ADJ_MID` | Modified duration (yield-based) |
| `Dc` (OAS) | `DUR_ADJ_OAS_MID` | Better for callables |
| `Cc` | `CONVEXITY` | Standard convexity |
| `Cc` (OAS) | `CONVEXITY_OAS` |  |
| DV01 | `DV01` | $ per bp |
| Spread duration | `SPRD_DUR` | for `Δi` PnL |
| Z-spread duration | `ZSPRD_DUR` |  |
| Key-rate dur 2/5/10/30 | `KEY_RATE_DUR_2Y` etc. | For curve decomposition |
| Effective duration | `EFF_DUR` |  |
| WAL | `WAL` |  |
| Risky duration | `RISKY_DUR` | CDS |

```excel
=BDP($H2, "DUR_ADJ_MID")
=BDP($H2, "DUR_ADJ_OAS_MID")
=BDP($H2, "CONVEXITY")
=BDP($H2, "CONVEXITY_OAS")
=BDP($H2, "DV01")                   ' dollar value of 1 bp per 1 unit of face
=BDP($H2, "SPRD_DUR")
=BDP($H2, "KEY_RATE_DUR_2Y")
=BDP($H2, "KEY_RATE_DUR_5Y")
=BDP($H2, "KEY_RATE_DUR_10Y")
=BDP($H2, "KEY_RATE_DUR_30Y")
```

`DV01` is per **unit of face**; for the full-position DV01 in
currency:

```excel
PositionDV01 = $E2 * $B2 * BDP($H2,"DV01") / 100
```

### Fisher-Weil (continuous-time) Dc/Cc from cash flows

If you want the *exact* `Dc = Σ tᵢ·CFᵢ·e^(−r·tᵢ) / Σ CFᵢ·e^(−r·tᵢ)`
from the notes:

1. Pull the cash-flow schedule (§7).
2. Spread cash-flow times in column X, amounts in Y.
3. Pull `r(tᵢ)` from the OIS curve (§8) — interpolate.
4. In a helper column: `=Y2 * EXP(-r_t * X2)`.
5. `PV = SUM(helper)`; `Dc = SUMPRODUCT(X, helper)/PV`;
   `Cc = SUMPRODUCT(X^2, helper)/PV`.

For most desks, `DUR_ADJ_MID` and `CONVEXITY` are accurate enough.

---

## 6 · OIS, Gov, Swap curves — extracting r, g, q

The decomposition needs the curve value at the bond's maturity
tenor (interpolated linearly between curve nodes). Build a tenor
table once:

```
Sheet "USD curves":
   A     B (OIS, USSO)          C (Gov, GT)          D (Swap, USSWAP)
1  yrs   PX_LAST                 PX_LAST              PX_LAST
2  1     =BDP("USSO1 Curncy","PX_LAST") =BDP("GT1 Govt","YLD_YTM_MID") =BDP("USSWAP1 Curncy","PX_LAST")
3  2     ... USSO2
4  3     USSO3                   GT3                   USSWAP3
5  5     USSO5                   GT5                   USSWAP5
6  7     USSO7                   GT7                   USSWAP7
7  10    USSO10                  GT10                  USSWAP10
8  20    USSO20                  GT20                  USSWAP20
9  30    USSO30                  GT30                  USSWAP30
```

(Repeat in EUR with `EESWE*` + `GTDEM*` + `EUSA*`, in GBP with
`BPSO*` + `GTGBP*Y` + `BPSWS*`, in JPY with `JYSO*` + `GTJPY*Y`
+ `JYSWAP*`.)

### Linear interpolation at the bond's tenor

Suppose the bond's maturity tenor is in cell `T2`:

```excel
T2: =YEARFRAC(TODAY(), BDP($H2,"MATURITY"), 1)

' r(T) — OIS at bond tenor
U2: =FORECAST(T2, USDCurves!B$2:B$9, USDCurves!A$2:A$9)

' Gov yield at bond tenor
V2: =FORECAST(T2, USDCurves!C$2:C$9, USDCurves!A$2:A$9)

' Swap yield at bond tenor
W2: =FORECAST(T2, USDCurves!D$2:D$9, USDCurves!A$2:A$9)

' r, g, q decomposition
X2: =U2                     ' r
Y2: =V2 - U2                ' g = Gov − OIS
Z2: =W2 - V2                ' q = Swap − Gov
AA2: =BDP($H2,"I_SPRD_MID")/100  ' i in same units (%)
```

Sanity check: `X2 + Y2 + Z2 + AA2` should approximately equal
`BDP($H2,"YLD_YTM_MID")` (within rounding from the i-spread
convention).

### Curve-component changes (Δr, Δg, Δq, Δi)

For the period [yesterday, today]:

```excel
' Today's curve values are in columns U,V,W as above.
' Yesterday's values: pull each curve node via BDH dated to WORKDAY(TODAY(),-1).

' Reusable formula for a single node at a single date:
=INDEX(BDH(<ticker>,"PX_LAST",WORKDAY(TODAY(),-1),WORKDAY(TODAY(),-1),
            "Per=cdr","Days=W","Fill=P","Dts=H","Cols=N"),1,1)

' Then:
Δr = r_today − r_yest
Δg = g_today − g_yest
Δq = q_today − q_yest
Δi = i_today − i_yest        ' = ΔI_SPRD_MID
Δy = Δr + Δg + Δq + Δi       ' (should match the bond's ΔYLD_YTM_MID)
```

In bps multiply by 10,000 if rates are in decimal, or by 100 if in
percent.

### Curves by currency — copy/paste table

| CCY | OIS (post-LIBOR) | Legacy IRS | Govt benchmarks |
|---|---|---|---|
| USD | `USSO[1..30] Curncy` | `USSWAP[1..30]` | `GT[1..30] Govt`, `USGG10YR Index` |
| EUR | `EESWE[1..30] Curncy` | `EUSA[1..30]`, `EUSW[1..30]` | `GTDEM[1/2/5/10/30]Y Govt`, `GTFRF[…]Y`, `GTITL[…]Y`, `GTESP[…]Y`, `GTPTE[…]Y` |
| GBP | `BPSO[1..30] Curncy` | `BPSWS[1..30]` | `GTGBP[1/2/5/10/30]Y Govt` |
| JPY | `JYSO[1..30] Curncy` | `JYSWAP[1..30]` | `GTJPY10Y Govt` (and other tenors) |
| CHF | `SFSARON[1..30] Curncy` | `SFSF[1..30]` | `GTCHF10Y Govt` |
| BRL | `BRLNDS[1..10] Curncy` (DI-swap) | — | `GTBRL10Y Govt` |
| MXN | `MXNNDS[1..10] Curncy` | — | `GTMXN10Y Govt` |
| CNY | `CNYNDS[1..10] Curncy` | — | `GTCNY10Y Govt` |

---

## 7 · Cash flows (for continuous-time PV / Dc / Cc)

The future cash-flow stream of a bond is a bulk field — `CSHFLW`
or `CASH_FLOW` is the modern mnemonic, with the call schedule
overlay:

```excel
=BDS($H2, "CSHFLW",
     "START_DT", TEXT(WORKDAY(TODAY(),1),"YYYYMMDD"),
     "END_DT",   TEXT(BDP($H2,"MATURITY"),"YYYYMMDD"))

' Alternative bulk fields
=BDS($H2, "CALL_SCHEDULE")           ' Date / Price / Type
=BDS($H2, "PUT_SCHEDULE")
=BDS($H2, "AMORT_SCHEDULE")
=BDS($H2, "CPN_SCHEDULE")            ' for step-ups
=BDS($H2, "SINKING_FUND_SCHEDULE")
=BDS($H2, "INT_PMT_HIST")
=BDS($H2, "PAYMENT_HISTORY")
```

For a vanilla fixed-coupon bullet the equivalent reconstruction
matches the notes exactly:

```
Coupon CF per period   = Notional × CPN / CPN_FREQ
Final CF (maturity)    = Coupon CF + Notional
```

In Excel:

```
B2 : Notional
=BDP($H2,"CPN")
=BDP($H2,"CPN_FREQ")
CouponCF = $B2 * BDP($H2,"CPN")/100 / BDP($H2,"CPN_FREQ")
```

---

## 8 · Funding & repo (Carry component)

The notes' Carry = Coupon accrual + Roll-to-par + Funding cost.

```excel
' Coupon accrual over period (days/365)
=$E2 * $B2 * BDP($H2,"CPN")/100 * (TODAY() - PrevDate) / 365

' Funding cost (financing the dirty MV)
=-$E2 * K2 * <funding_rate>/100 * (TODAY() - PrevDate) / 365
```

Where `<funding_rate>` is one of:

| Currency | Pick | Bloomberg ticker | Excel |
|---|---|---|---|
| USD | SOFR overnight | `SOFRRATE Index` | `=BDP("SOFRRATE Index","PX_LAST")` |
| USD | GC repo | `BGCR Index` / `TGCR Index` | `=BDP("BGCR Index","PX_LAST")` |
| USD | Effective Fed Funds | `FEDL01 Index` / `EFFR Index` | `=BDP("FEDL01 Index","PX_LAST")` |
| EUR | €STR | `ESTRON Index` | `=BDP("ESTRON Index","PX_LAST")` |
| GBP | SONIA | `SONIO/N Index` | `=BDP("SONIO/N Index","PX_LAST")` |
| JPY | TONA | `TONAR Index` | `=BDP("TONAR Index","PX_LAST")` |
| CHF | SARON | `SARON Index` | `=BDP("SARON Index","PX_LAST")` |
| CAD | CORRA | `CORRAINDX Index` | `=BDP("CORRAINDX Index","PX_LAST")` |
| AUD | RBA cash | `AONIA Index` | `=BDP("AONIA Index","PX_LAST")` |
| BRL | DI 1d | `BRDIIN Index` | `=BDP("BRDIIN Index","PX_LAST")` |
| MXN | Banxico O/N | `MXTSETA Index` | `=BDP("MXTSETA Index","PX_LAST")` |
| INR | RBI repo | `RBIRPO Index` | `=BDP("RBIRPO Index","PX_LAST")` |

For term funding (e.g. 1m, 3m, weighting historic days):

```excel
=BDP("USSO1M Curncy","PX_LAST")     ' 1m OIS, USD
=BDP("USSO3M Curncy","PX_LAST")     ' 3m OIS
=BDP("EESWE1M Curncy","PX_LAST")
=BDP("BPSO3M Curncy","PX_LAST")
=BDP("JYSO3M Curncy","PX_LAST")
```

If you have a desk repo rate (specials), enter it manually as a
column input — it will not be in Bloomberg.

### Roll-to-par component

Captures the convergence of clean price to par over time. Per the
notes' approximation `Roll-to-par = (Notional − Market value) ×
days / 365 / time_to_maturity` — implemented as the rolldown along
the curve, computed by:

```excel
' Bond yield today at tenor T
y_T     = BDP($H2,"YLD_YTM_MID")

' Curve yield at tenor T − Δt (i.e. as if we "roll down" by Δt)
' Use the gov + swap curves you built in §6 with a slightly shorter tenor
y_Tminus = FORECAST(T2 - days/365, ..., ...)

' Roll PnL (per unit MV)
Roll_PnL_per_unit = -BDP($H2,"DUR_ADJ_MID") * (y_T - y_Tminus)
```

---

## 9 · Hedge instruments

### 9a · Bond futures (TY, RX, OE, DU, JB, G, etc.)

If the hedge is `TYZ5 Comdty`:

```excel
=BDP($G2, "PX_LAST")                          ' price
=BDP($G2, "PX_SETTLE")                        ' for daily mark
=BDP($G2, "FUT_VAL_PT")                       ' $ per 1.00 price point
=BDP($G2, "FUT_CONT_SIZE")                    ' notional per contract
=BDP($G2, "FUT_CTD_BOND")                     ' CTD ticker (string)
=BDP($G2, "CONV_FACTOR")                      ' CTD conversion factor
=BDP($G2, "CTD_FRWD_PX")                      ' forward CTD price
=BDP($G2, "IMPLIED_REPO_RATE")
=BDP($G2, "NET_BASIS")                        ' bps
=BDP($G2, "GROSS_BASIS")
=BDP($G2, "LAST_TRADEABLE_DT")
=BDP($G2, "FUT_DLV_DT_FIRST")
=BDP($G2, "FUT_NOTICE_FIRST")

' CTD's own DV01 (back-fill the CTD ticker into BDP)
CtdTicker = BDP($G2,"FUT_CTD_BOND")
CTD_DV01  = BDP(CtdTicker,"DV01")

' Futures DV01 per contract (approximation)
Fut_DV01_per_contract = CTD_DV01 / BDP($G2,"CONV_FACTOR") * BDP($G2,"FUT_VAL_PT")/100
```

### 9b · Swap as hedge (USSO10 Curncy etc.)

The hedge "instrument" is parametric — store its par rate and DV01:

```excel
=BDP("USSO10 Curncy","PX_LAST")       ' par rate now
' Swap DV01 per 1 mio notional (USD SOFR 10y), back-of-envelope:
'    Swap_DV01 ≈ Modified duration × Notional × 0.0001
'    (Bloomberg curve fields give modified duration via the curve)
```

For a precise swap-DV01 use the YAS-style override on a curve
ticker (some installs support it), or compute via `BCURVE` for
discount factors and rebuild the swap PV manually.

---

## 10 · FX (for FX PnL)

For non-base-currency trades:

```excel
=BDP("EURUSD WMCO Curncy","PX_LAST")        ' spot, WM 4pm London fix
=INDEX(BDH("EURUSD WMCO Curncy","PX_LAST",
            WORKDAY(TODAY(),-1), WORKDAY(TODAY(),-1),
            "Per=cdr","Days=W","Fill=P","Dts=H","Cols=N"),1,1)

' Forward outright if you funded the position via FX forward
=BDP("EURUSD3M Curncy","PX_LAST")
```

FX PnL on a foreign-currency position, in base currency:

```
FX_PnL = MV_foreign × (Spot_today − Spot_yesterday)
       = J2 × (EURUSD_today − EURUSD_yest)
```

---

## 11 · Putting it together — PnL components

Given the inputs above, each PnL component is a one-line Excel
formula.

Below, indices refer to the column letters used in §2 and the
helper cells in §4–§10. All in **base currency** assuming inputs
are in matching units (yields as decimals, MV in face).

### Helper cells (per row)

| Cell | What | Formula |
|---|---|---|
| `MV` | Current MV (dirty) | `=K2` |
| `Dc` | Modified duration | `=BDP($H2,"DUR_ADJ_MID")` |
| `Cc` | Convexity | `=BDP($H2,"CONVEXITY")` |
| `Δr` | ΔOIS at tenor (decimal) | `=(r_today − r_yest)` |
| `Δg` | Δ gov-OIS basis | `=(g_today − g_yest)` |
| `Δq` | Δ swap-gov basis | `=(q_today − q_yest)` |
| `Δi` | Δ i-spread | `=(BDP($H2,"I_SPRD_MID") − INDEX(BDH(...),1,1))/10000` |
| `Δy` | Total Δ yield | `=Δr + Δg + Δq + Δi` |
| `ΔSpot` | FX change | `=Spot_today − Spot_yest` |

### Component formulas

```excel
' 1. Duration PnL (rate ∂):  ΔPV ≈ -PV × Dc × Δy
Duration_PnL       = -$E2 * MV * Dc * Δy

' Decomposed by curve piece:
Duration_OIS       = -$E2 * MV * Dc * Δr
Duration_GovBasis  = -$E2 * MV * Dc * Δg
Duration_SwapBasis = -$E2 * MV * Dc * Δq
Duration_Ispread   = -$E2 * MV * Dc * Δi    ' "Credit PnL" (idiosyncratic)

' 2. Convexity PnL:   ½ × PV × Cc × (Δy)²
Convexity_PnL      = 0.5 * $E2 * MV * Cc * Δy^2

' 3. Carry: Coupon accrual + Funding + Roll-to-par
Coupon_PnL         = $E2 * $B2 * BDP($H2,"CPN")/100 * days/365
Funding_PnL        = -$E2 * MV * funding_rate/100 * days/365
Roll_PnL           = $E2 * MV * (-Dc) * (y_T − y_T_minus_dt)   ' rolldown approx
Carry_PnL          = Coupon_PnL + Funding_PnL + Roll_PnL

' 4. Hedge PnL (apply 1–3 to the hedge instrument)
Hedge_Duration_PnL = -F2_signed * Hedge_MV * Hedge_Dc * Hedge_Δy
Hedge_Convexity    = 0.5 * F2_signed * Hedge_MV * Hedge_Cc * Hedge_Δy^2
Hedge_Carry        = F2_signed * Hedge_MV * (carry rate at hedge funding) * days/365
Hedge_PnL          = Hedge_Duration_PnL + Hedge_Convexity + Hedge_Carry

' 5. FX PnL
FX_PnL             = MV_foreign × ΔSpot                ' direct base-CCY contribution

' 6. Credit / spread PnL (= the Δi piece above; isolate as needed)
Credit_PnL         = Duration_Ispread + ½·PV·SprdDur·Δi² (small)

' 7. Basis PnL (e.g. cash-CDS basis, futures-bond basis)
Basis_PnL          = ΔBasis × DV01-equivalent of basis exposure

' 8. Residual
Residual           = Realized_clean_PnL − (Duration_PnL + Convexity_PnL
                                          + Carry_PnL + Hedge_PnL
                                          + FX_PnL + Basis_PnL)

' 9. Hedge efficiency
Hedge_Eff          = 1 - ABS(Residual_bvol) / ABS(Bond_bvol)
```

Sanity-row to add at the end:

```excel
' Should equal P&L from MTM marks
Total_Explained = Duration_PnL + Convexity_PnL + Carry_PnL
                + Hedge_PnL + FX_PnL + Basis_PnL
Realized_PnL    = L2 + (Coupon paid this period) + Hedge realized
Residual        = Realized_PnL − Total_Explained
```

---

## 12 · Hedge sizing & risk aggregation

Directly from the notes:

```
Target Hedge DV01     = − Hedge ratio × Bond DV01
Required Notional     = DV01_target / DV01_per_dV (e.g. per 1 bp move)
Number of Futures     = DV01_target / DV01_per_contract
DV01 per contract     ≈ CTD DV01 / Conversion Factor
Hedge ratio (Bond)    = − Hedge DV01 / Bond DV01
Residual DV01         = Bond DV01 + Hedge DV01
Net DV01 portfolio    = Σᵢⱼ DV01ᵢⱼ
Hedge inefficiency    = (curr DV01_bond − init)/init − (curr DV01_hedge − init)/init
```

Excel realisation:

```excel
' Per-bond DV01 in $
Bond_DV01_pos    = $E2 * $B2 * BDP($H2,"DV01") / 100

' Per-future DV01 in $ (per contract)
Fut_DV01_pc      = BDP(BDP($G2,"FUT_CTD_BOND"),"DV01")
                 / BDP($G2,"CONV_FACTOR")
                 * BDP($G2,"FUT_VAL_PT")
                 / 100

' Number of contracts to hedge a Bond_DV01_pos exposure
N_contracts      = -Bond_DV01_pos / Fut_DV01_pc

' Net DV01 (should be ~0 if hedged perfectly)
Net_DV01         = Bond_DV01_pos + $F2 * Fut_DV01_pc

' Hedge ratio
Hedge_Ratio      = -($F2 * Fut_DV01_pc) / Bond_DV01_pos

' Hedge inefficiency between t0 and t1
Ineff            = (Curr_Bond_DV01 - Init_Bond_DV01) / Init_Bond_DV01
                 - (Curr_Hedge_DV01 - Init_Hedge_DV01) / Init_Hedge_DV01
```

---

## 13 · Bloomberg-side optionality: YAS overrides

Where you want analytics computed at a **user-supplied price**
(e.g. for what-if at a stressed price, or to pin to your firm's
official mark), use the YAS-family overrides:

```excel
' Yield implied by a clean price
=BDP($H2, "YAS_BOND_YLD",
      "YAS_BOND_PX",  TEXT($D2,"0.000000"),
      "YAS_RISK_DT",  TEXT(WORKDAY(TODAY(),1),"YYYYMMDD"),
      "YAS_CURVE",    OISCurveUSD)

' Z-spread at user price
=BDP($H2, "YAS_ZSPREAD",
      "YAS_BOND_PX",  TEXT($D2,"0.000000"),
      "YAS_RISK_DT",  TEXT(WORKDAY(TODAY(),1),"YYYYMMDD"),
      "YAS_CURVE",    OISCurveUSD)

' OAS at user price + user vol
=BDP($H2, "YAS_OAS_SPREAD",
      "YAS_BOND_PX",        TEXT($D2,"0.000000"),
      "YAS_RISK_DT",        TEXT(WORKDAY(TODAY(),1),"YYYYMMDD"),
      "YAS_CURVE",           OISCurveUSD,
      "OAS_VOL_BASIS_BVOL", "65")            ' 65 bp normal vol

' Modified duration at user price
=BDP($H2, "DUR_ADJ_MID",
      "YAS_BOND_PX", TEXT($D2,"0.000000"),
      "YAS_RISK_DT", TEXT(WORKDAY(TODAY(),1),"YYYYMMDD"),
      "YAS_CURVE",   OISCurveUSD)
```

YAS curve IDs (CCY ↔ curve):

| CCY | YAS_CURVE |
|---|---|
| USD | `S490` (SOFR), `S023` (legacy 3M LIBOR) |
| EUR | `S514` (€STR), `S045` (6M EURIBOR), `S030` (3M EURIBOR) |
| GBP | `S141` (SONIA), `S022` (LIBOR legacy) |
| JPY | `S510` (TONA), `S025` (LIBOR legacy) |
| CHF | `S234` (SARON) |

---

## 14 · Complete mapping table — quick lookup

| PnL leg | Quantity needed | Bloomberg field | Excel formula |
|---|---|---|---|
| Duration | `PV` (MV dirty) | `PX_LAST`+`ACCRUED_INTEREST` | `=$B2*(BDP($H2,"PX_LAST")+BDP($H2,"ACCRUED_INTEREST"))/100` |
| Duration | `Dc` (mod dur) | `DUR_ADJ_MID` | `=BDP($H2,"DUR_ADJ_MID")` |
| Duration | `Δy` | YTM today vs YTM yesterday | `=(BDP($H2,"YLD_YTM_MID") − INDEX(BDH(...,Yesterday,Yesterday,…),1,1))/100` |
| Duration | `Δr` | OIS @ bond tenor | interpolate `USSO*`/`EESWE*` etc. |
| Duration | `Δg` | Gov − OIS @ tenor | gov yield − interpolated OIS |
| Duration | `Δq` | Swap − Gov @ tenor | swap yield − gov yield |
| Duration | `Δi` | i-spread | `I_SPRD_MID` change |
| Convexity | `Cc` | `CONVEXITY` | `=BDP($H2,"CONVEXITY")` |
| Carry | Coupon rate | `CPN` | `=BDP($H2,"CPN")` |
| Carry | Coupon freq | `CPN_FREQ` | `=BDP($H2,"CPN_FREQ")` |
| Carry | Funding rate | overnight rate ticker | `=BDP("SOFRRATE Index","PX_LAST")` (etc.) |
| Carry | Days | calendar | `=TODAY() − PrevDate` |
| Roll | Tenor today T | `MATURITY` − today | `=YEARFRAC(TODAY(),BDP($H2,"MATURITY"),1)` |
| Roll | Yield at T − Δt | interp curve | `FORECAST(T−Δt, curve_y, curve_x)` |
| FX | Spot | `<PAIR> WMCO Curncy` | `=BDP("EURUSD WMCO Curncy","PX_LAST")` |
| FX | Spot yesterday | same, BDH | `=INDEX(BDH(...),1,1)` |
| Hedge | Future price | `PX_SETTLE` | `=BDP($G2,"PX_SETTLE")` |
| Hedge | Future point value | `FUT_VAL_PT` | `=BDP($G2,"FUT_VAL_PT")` |
| Hedge | Contract size | `FUT_CONT_SIZE` | `=BDP($G2,"FUT_CONT_SIZE")` |
| Hedge | CTD ticker | `FUT_CTD_BOND` | `=BDP($G2,"FUT_CTD_BOND")` |
| Hedge | CTD DV01 | DV01 on CTD | `=BDP(BDP($G2,"FUT_CTD_BOND"),"DV01")` |
| Hedge | Conversion factor | `CONV_FACTOR` | `=BDP($G2,"CONV_FACTOR")` |
| Hedge | Implied repo | `IMPLIED_REPO_RATE` | `=BDP($G2,"IMPLIED_REPO_RATE")` |
| Hedge | Net basis | `NET_BASIS` | `=BDP($G2,"NET_BASIS")` |
| Hedge | Swap par rate | `PX_LAST` on `<CCY>SO<tenor> Curncy` | `=BDP("USSO10 Curncy","PX_LAST")` |
| Basis | Cash-CDS basis | Z-spread − CDS spread | `=BDP($H2,"Z_SPRD_MID") − BDP($CDStkr,"PX_LAST")` |
| Spread | Z-spread | `Z_SPRD_MID` | `=BDP($H2,"Z_SPRD_MID")` |
| Spread | I-spread | `I_SPRD_MID` | `=BDP($H2,"I_SPRD_MID")` |
| Spread | G-spread | `G_SPRD_MID` | `=BDP($H2,"G_SPRD_MID")` |
| Spread | OAS | `OAS_SPREAD_MID` | `=BDP($H2,"OAS_SPREAD_MID")` |
| Spread | ASW | `ASSET_SWAP_SPD_MID` | `=BDP($H2,"ASSET_SWAP_SPD_MID")` |
| Risk | DV01 / unit | `DV01` | `=BDP($H2,"DV01")` |
| Risk | Spread duration | `SPRD_DUR` | `=BDP($H2,"SPRD_DUR")` |
| Risk | Key-rate dur 10y | `KEY_RATE_DUR_10Y` | `=BDP($H2,"KEY_RATE_DUR_10Y")` |
| Cash flows | Future CFs | `CSHFLW` (bulk) | `=BDS($H2,"CSHFLW","START_DT",…,"END_DT",…)` |
| Ratings | Composite | `RTG_BB_COMPOSITE` | `=BDP($H2,"RTG_BB_COMPOSITE")` |
| Default prob | Issuer-level | `DEFAULT_PROBABILITY` | `=BDP($H2,"DEFAULT_PROBABILITY")` |

---

## 15 · Identifier → everything else workflow

The single template that handles the entire pipeline. Given just
an ISIN (or CUSIP / FIGI) and the trade-level inputs in columns
B–G, fill the rest:

```excel
H2:  =BDP("/isin/" & $A2,"PARSEKYABLE_DES")    ' BBG ticker (with yellow key)

' Static
I2:  =BDP($H2,"CRNCY")
J2:  =BDP($H2,"MATURITY")
K2:  =BDP($H2,"CPN")
L2:  =BDP($H2,"CPN_FREQ")
M2:  =BDP($H2,"DAY_CNT_DES")
N2:  =BDP($H2,"RTG_BB_COMPOSITE")

' MV today
O2:  =BDP($H2,"PX_LAST")                       ' clean
P2:  =BDP($H2,"ACCRUED_INTEREST")
Q2:  =$B2*(O2+P2)/100                          ' dirty MV in face CCY

' Yield + spreads today
R2:  =BDP($H2,"YLD_YTM_MID")
S2:  =BDP($H2,"G_SPRD_MID")
T2:  =BDP($H2,"I_SPRD_MID")
U2:  =BDP($H2,"Z_SPRD_MID")
V2:  =BDP($H2,"ASSET_SWAP_SPD_MID")
W2:  =BDP($H2,"OAS_SPREAD_MID")

' Risk
X2:  =BDP($H2,"DUR_ADJ_MID")                   ' Dc
Y2:  =BDP($H2,"CONVEXITY")                     ' Cc
Z2:  =BDP($H2,"DV01")
AA2: =BDP($H2,"SPRD_DUR")

' Tenor (years) for curve interpolation
AB2: =YEARFRAC(TODAY(), J2, 1)

' Curve OIS @ tenor (e.g. USD)
AC2: =FORECAST(AB2, USDCurves!B$2:B$11, USDCurves!A$2:A$11)

' Yesterday's yield (for Δy)
AD2: =INDEX(BDH($H2,"YLD_YTM_MID",WORKDAY(TODAY(),-1),WORKDAY(TODAY(),-1),
                "Per=cdr","Days=W","Fill=P","Dts=H","Cols=N"),1,1)
AE2: =R2 - AD2                                 ' Δy (in % units; ×100 for bps)

' Component PnL ($)
AF2: =-$E2 * Q2 * X2 * AE2/100                 ' Duration PnL
AG2: =0.5 * $E2 * Q2 * Y2 * (AE2/100)^2        ' Convexity PnL
AH2: =$E2 * $B2 * K2/100 * (TODAY()-$C2)/365   ' Coupon accrual (since trade)
AI2: =-$E2 * Q2 * BDP("SOFRRATE Index","PX_LAST")/100 * 1/365   ' overnight funding
AJ2: =BDP($G2,"PX_SETTLE")*$F2*BDP($G2,"FUT_VAL_PT")            ' hedge MV
' ... continue for hedge components, FX, basis, residual
```

---

## 16 · Notation glossary (notes ↔ Bloomberg)

| Notes notation | Meaning | Bloomberg field | Excel |
|---|---|---|---|
| `Notional` | Face value | — (book input) |  |
| `Purchase price` | Trade clean price (/100) | — (book input) |  |
| `Current price` | Today's clean | `PX_LAST` | `=BDP($H2,"PX_LAST")` |
| `Market value` (dirty) | Notional × (PX_LAST+Accr)/100 | derived | `=$B2*(BDP($H2,"PX_LAST")+BDP($H2,"ACCRUED_INTEREST"))/100` |
| `Coupon rate` | Annual % | `CPN` | `=BDP($H2,"CPN")` |
| `Coupon CF` | per period | derived | `=$B2*BDP($H2,"CPN")/100/BDP($H2,"CPN_FREQ")` |
| `DF(continuous)` | `e^(−r·t)` | derived from OIS curve | `=EXP(-r*t)` |
| `PV(c)` | discounted CF sum | derived | `=SUMPRODUCT(CF_range,EXP(-r_range*t_range))` |
| `Dc` | continuous duration | ≈ `DUR_ADJ_MID` | `=BDP($H2,"DUR_ADJ_MID")` |
| `Cc` | continuous convexity | ≈ `CONVEXITY` | `=BDP($H2,"CONVEXITY")` |
| `DV01` | bond DV01 per unit face | `DV01` | `=BDP($H2,"DV01")` |
| `Bond yield` | y | `YLD_YTM_MID` | `=BDP($H2,"YLD_YTM_MID")` |
| `OIS rate (r)` | OIS @ tenor | OIS curve | interpolate `USSO*`/`EESWE*`/`BPSO*`/`JYSO*` |
| `Gov yield` | sov benchmark @ tenor | gov curve | interpolate `GT*`/`GTGBP*Y`/`GTDEM*Y` etc. |
| `Swap yield` | par swap @ tenor | swap curve | interpolate `USSWAP*`/`EUSA*`/`BPSWS*`/`JYSWAP*` |
| `g (gov-OIS)` | gov − OIS | derived |  |
| `q (swap-gov)` | swap − gov | derived |  |
| `i (i-spread)` | bond − swap | `I_SPRD_MID` | `=BDP($H2,"I_SPRD_MID")` |
| `ZOIS` | bond − OIS | `Z_SPRD_MID` (vs swap, ~ZOIS) | `=BDP($H2,"Z_SPRD_MID")` |
| `Gspread` | bond − gov | `G_SPRD_MID` | `=BDP($H2,"G_SPRD_MID")` |
| `Hedge DV01` | $ per bp from hedge | derived | see §9 / §12 |
| `Conversion factor` | CBOT delivery factor | `CONV_FACTOR` | `=BDP($G2,"CONV_FACTOR")` |
| `CTD` | cheapest-to-deliver bond | `FUT_CTD_BOND` | `=BDP($G2,"FUT_CTD_BOND")` |
| `Implied repo` | future-implied financing | `IMPLIED_REPO_RATE` | `=BDP($G2,"IMPLIED_REPO_RATE")` |
| `Net basis` | bps | `NET_BASIS` | `=BDP($G2,"NET_BASIS")` |
| `Funding rate` | overnight or term | `SOFRRATE`/`ESTRON`/`SONIO/N`/`TONAR` Index | `=BDP("SOFRRATE Index","PX_LAST")` |
| `Hedge ratio` | −Hedge DV01 / Bond DV01 | derived |  |
| `Residual DV01` | sum | derived |  |
| `Bond bvol` | bond DV01 × yield σ | derived |  |
| `Hedge efficiency` | 1 − \|residual\| / \|bond\| | derived |  |
| `FX spot` | base → quote | `PX_LAST` | `=BDP("EURUSD WMCO Curncy","PX_LAST")` |

---

## 17 · Reproducibility / refresh discipline

For the workbook to produce auditable PnL each day:

- **Bloomberg → Options → Manual refresh; Refresh on Open: OFF;
  Use DPDF: OFF.**
- Every `BDH` carries `"Per=cdr","Days=W","Fill=P","UseDPDF=N"`.
- Every YAS call pins `YAS_RISK_DT`, `YAS_CURVE`.
- Every fundamentals/estimate override pins
  `BEST_DATA_RELEASE_DT` (not used here, but applies for credit
  fields driven by issuer fundamentals).
- The curve sheets (§6) are populated fresh each morning, then
  a hard "snapshot" column is copy-paste-value-d for that day's
  PnL run.
- Funding rate is captured at a fixed time (e.g. 16:00 local) and
  pinned.
- Residual is logged daily; persistent drift > 1 bp/day is a
  signal that one of the above is mis-pinned.

This single file is the contract between the notes and the
spreadsheet. Reference it whenever a PnL component is unclear or a
sign convention drifts.
