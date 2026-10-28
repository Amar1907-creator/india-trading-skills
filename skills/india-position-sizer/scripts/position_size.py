#!/usr/bin/env python3
"""India Position Sizer: how many shares or lots to trade so one loss stays small.

Examples:
    # Delivery: ₹1,00,000 capital, risk 1%, buy at 1200, stop-loss 1150, target 1320
    python3 position_size.py --capital 100000 --risk-pct 1 --entry 1200 --stop 1150 --target 1320

    # Intraday short (stop above entry)
    python3 position_size.py --capital 50000 --risk-pct 0.5 --entry 800 --stop 812 --product intraday

    # F&O: lot size is required because NSE revises lot sizes
    python3 position_size.py --capital 500000 --risk-pct 1 --entry 24500 --stop 24380 --product futures --lot-size 75

    # Check the stop against the stock's normal daily swing
    python3 position_size.py --capital 100000 --risk-pct 1 --entry 1200 --stop 1185 --symbol RELIANCE

Charges are estimates of common Indian statutory rates plus a typical discount-broker fee.
Always confirm with your broker's contract note.
"""

import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if hasattr(sys.stdout, "reconfigure"):  # show ₹ correctly on Windows consoles
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Approximate statutory rates (fraction of turnover). Rates change via Budget/SEBI/exchange
# circulars; keep RATES_AS_OF current when updating.
RATES_AS_OF = "2026 (approximate)"
RATES = {
    #            STT buy, STT sell, exchange txn, stamp (buy side)
    "delivery": (0.001, 0.001, 0.0000297, 0.00015),
    "intraday": (0.0, 0.00025, 0.0000297, 0.00003),
    "futures":  (0.0, 0.0002, 0.0000173, 0.00002),
    "options":  (0.0, 0.001, 0.0003503, 0.00003),  # on premium turnover
}
SEBI_FEE = 0.000001   # ₹10 per crore
GST = 0.18            # on brokerage + exchange + SEBI fee


def brokerage(order_value, flat, pct, minimum):
    """Common discount-broker pricing: lower of flat fee or pct of value, with a minimum."""
    fee = min(flat, order_value * pct / 100) if pct else flat
    return max(fee, minimum) if order_value > 0 else 0.0


def charges(product, qty, buy_price, sell_price, b_flat, b_pct, b_min, dp_charge):
    stt_b, stt_s, txn, stamp = RATES[product]
    buy_val, sell_val = qty * buy_price, qty * sell_price
    brk = brokerage(buy_val, b_flat, b_pct, b_min) + brokerage(sell_val, b_flat, b_pct, b_min)
    exch = (buy_val + sell_val) * txn
    sebi = (buy_val + sell_val) * SEBI_FEE
    parts = {
        "brokerage": brk,
        "stt": buy_val * stt_b + sell_val * stt_s,
        "exchange": exch,
        "sebi": sebi,
        "stamp_duty": buy_val * stamp,
        "gst": (brk + exch + sebi) * GST,
        "dp_charge": dp_charge if product == "delivery" else 0.0,
    }
    parts["total"] = sum(parts.values())
    return parts


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    ap.add_argument("--capital", type=float, required=True, help="total trading capital in ₹")
    ap.add_argument("--risk-pct", type=float, default=1.0, help="max %% of capital to lose on this trade (default 1)")
    ap.add_argument("--entry", type=float, required=True, help="planned entry price (premium for options)")
    ap.add_argument("--stop", type=float, required=True, help="stop-loss price; above entry means a short trade")
    ap.add_argument("--target", type=float, help="optional target price for reward:risk")
    ap.add_argument("--product", choices=list(RATES), default="delivery")
    ap.add_argument("--lot-size", type=int, help="F&O lot size (required for futures/options)")
    ap.add_argument("--max-position-pct", type=float, default=100.0,
                    help="cap one position at this %% of capital (default 100 = no cap)")
    ap.add_argument("--brokerage-flat", type=float, default=20.0, help="₹ per order (default 20)")
    ap.add_argument("--brokerage-pct", type=float, default=0.1,
                    help="%% of order value if lower than flat fee (default 0.1; 0 = always flat)")
    ap.add_argument("--brokerage-min", type=float, default=5.0, help="minimum ₹ per order (default 5)")
    ap.add_argument("--dp-charge", type=float, default=15.93, help="₹ depository charge on delivery sell (default ~15.93)")
    ap.add_argument("--symbol", help="optional NSE symbol to compare stop distance with typical daily swing (ATR)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    errors = []
    if a.capital <= 0 or a.entry <= 0 or a.stop <= 0:
        errors.append("capital, entry and stop must be positive numbers")
    if a.entry == a.stop:
        errors.append("stop-loss cannot equal entry")
    if not 0 < a.risk_pct <= 100:
        errors.append("risk-pct must be between 0 and 100")
    if a.product in ("futures", "options") and not a.lot_size:
        errors.append("--lot-size is required for futures/options (check NSE's current lot size)")
    if errors:
        print("Error: " + "; ".join(errors))
        sys.exit(1)

    side = "long (buy first)" if a.stop < a.entry else "short (sell first)"
    if a.stop > a.entry and a.product == "delivery":
        print("Error: a stop above entry means a short trade, which isn't possible for delivery. Use --product intraday.")
        sys.exit(1)
    risk_per_unit = abs(a.entry - a.stop)
    risk_budget = a.capital * a.risk_pct / 100
    unit = a.lot_size or 1

    units_by_risk = math.floor(risk_budget / (risk_per_unit * unit))
    # Notional cap applies to cash products; F&O exposure is limited by margin, which only the broker knows.
    if a.product in ("delivery", "intraday", "options"):
        cash_cap = a.capital * a.max_position_pct / 100
        units_by_cash = math.floor(cash_cap / (a.entry * unit))
    else:
        units_by_cash = units_by_risk
    units = max(min(units_by_risk, units_by_cash), 0)
    qty = units * unit

    buy_px, sell_px = (a.entry, a.stop) if a.stop < a.entry else (a.stop, a.entry)
    loss_charges = charges(a.product, qty, buy_px, sell_px, a.brokerage_flat, a.brokerage_pct,
                           a.brokerage_min, a.dp_charge) if qty else {"total": 0.0}
    out = {
        "side": side, "product": a.product, "risk_budget": risk_budget, "risk_per_unit": risk_per_unit,
        "quantity": qty, "lots": units if a.lot_size else None, "position_value": qty * a.entry,
        "loss_at_stop_before_charges": qty * risk_per_unit,
        "loss_at_stop_with_charges": qty * risk_per_unit + loss_charges["total"],
        "charges_if_stopped": loss_charges, "limited_by": "cash" if units_by_cash < units_by_risk else "risk",
        "rates_as_of": RATES_AS_OF, "warnings": [],
    }

    if a.target and qty:
        reward = abs(a.target - a.entry)
        win_buy, win_sell = (a.entry, a.target) if a.stop < a.entry else (a.target, a.entry)
        win_charges = charges(a.product, qty, win_buy, win_sell, a.brokerage_flat, a.brokerage_pct,
                              a.brokerage_min, a.dp_charge)
        out["reward_risk"] = reward / risk_per_unit
        out["profit_at_target_after_charges"] = qty * reward - win_charges["total"]
        if (a.stop < a.entry) != (a.target > a.entry):
            out["warnings"].append("target is on the wrong side of entry")
        if out["reward_risk"] < 1.5:
            out["warnings"].append(f"reward:risk is only {out['reward_risk']:.1f}; many traders want at least 2")

    if qty == 0:
        need = risk_per_unit * unit / (a.risk_pct / 100)
        out["warnings"].append(f"risk budget is too small for even 1 {'lot' if a.lot_size else 'share'} "
                               f"with this stop; you'd need about ₹{need:,.0f} capital at {a.risk_pct}% risk")
    if a.risk_pct > 2:
        out["warnings"].append(f"risking {a.risk_pct}% per trade is aggressive; 0.5-1% is common for beginners")
    if qty and loss_charges["total"] > 0.2 * out["loss_at_stop_before_charges"]:
        out["warnings"].append("charges are over 20% of the planned loss; the trade size may be too small to be efficient")
    if a.product in ("futures", "options"):
        out["warnings"].append("SEBI studies found about 9 in 10 individual F&O traders lost money; "
                               "margin needed is set by your broker, so check it before trading")
        if a.product == "futures":
            out["warnings"].append("futures can gap past your stop-loss overnight; real losses can exceed the plan")

    if a.symbol:
        try:
            from india_data import atr, fetch_history, to_symbol
            hist = fetch_history(to_symbol(a.symbol), "6mo")
            day_swing = atr(hist["bars"])
            if day_swing:
                out["atr14"] = day_swing
                ratio = risk_per_unit / day_swing
                out["stop_vs_atr"] = ratio
                if ratio < 0.5:
                    out["warnings"].append(f"stop is only {ratio:.2f}x the normal daily swing (ATR ₹{day_swing:.2f}); "
                                           "normal noise may hit it")
                elif ratio > 3:
                    out["warnings"].append(f"stop is {ratio:.1f}x the daily swing; it's wide, so the position is small")
        except Exception as exc:  # optional check: never block the sizing result
            out["warnings"].append(f"could not check ATR for {a.symbol}: {exc}")

    if a.json:
        print(json.dumps(out, indent=2))
        return

    lot_txt = f" ({units} lots x {unit})" if a.lot_size else ""
    print(f"POSITION SIZE: {side}, {a.product}")
    print("=" * 60)
    print(f"Capital ₹{a.capital:,.0f} | risk {a.risk_pct}% = ₹{risk_budget:,.0f} max loss")
    print(f"Entry ₹{a.entry:,.2f} | stop ₹{a.stop:,.2f} | risk per unit ₹{risk_per_unit:,.2f}")
    print(f"\n>> Quantity: {qty:,}{lot_txt}   (limited by {out['limited_by']})")
    print(f"   Position value: ₹{out['position_value']:,.0f}" +
          ("  (notional; margin is less, set by broker)" if a.product == "futures" else ""))
    print(f"   Loss if stop hits: ₹{out['loss_at_stop_before_charges']:,.0f} + ~₹{loss_charges['total']:,.0f} charges"
          f" = ₹{out['loss_at_stop_with_charges']:,.0f}")
    if "reward_risk" in out:
        print(f"   Reward:risk = {out['reward_risk']:.2f} | profit at target after charges ≈ ₹{out['profit_at_target_after_charges']:,.0f}")
    if "atr14" in out:
        print(f"   Stop distance = {out['stop_vs_atr']:.2f}x the typical daily swing (ATR ₹{out['atr14']:.2f})")
    if out["warnings"]:
        print("\nWarnings:")
        for w in out["warnings"]:
            print(f"  ! {w}")
    print(f"\nCharges are estimates using rates as of {RATES_AS_OF}; check your broker's contract note.")
    print("For learning and research only. Not investment advice.")


if __name__ == "__main__":
    main()
