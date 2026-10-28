#!/usr/bin/env python3
"""India Market Pulse: a 5-minute health check of the Indian stock market.

Usage:
    python3 market_pulse.py           # readable report
    python3 market_pulse.py --json    # machine-readable output

No API key needed. Data: Yahoo Finance (may be ~15 min delayed).
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if hasattr(sys.stdout, "reconfigure"):  # show ₹ correctly on Windows consoles
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from india_data import (DataError, closes, fetch_history, fmt_num, fmt_pct,  # noqa: E402
                        market_status, pct_change, rsi, sma)

INDIA = [("Nifty 50", "^NSEI"), ("Bank Nifty", "^NSEBANK"), ("Sensex", "^BSESN"),
         ("Nifty Next 50", "^NSMIDCP"), ("Nifty Midcap 150", "NIFTYMIDCAP150.NS"),
         ("Nifty Smallcap 250", "NIFTYSMLCAP250.NS")]
GLOBAL = [("S&P 500 (US)", "^GSPC"), ("Nasdaq (US)", "^IXIC"),
          ("USD/INR", "USDINR=X"), ("Brent crude ($)", "BZ=F")]


def trend_of(values):
    """Classify trend from price vs 50/200-day averages."""
    price, s50, s200 = values[-1], sma(values, 50), sma(values, 200)
    if s50 is None or s200 is None:
        return "not enough history", s50, s200
    if price > s50 > s200:
        return "uptrend", s50, s200
    if price < s50 < s200:
        return "downtrend", s50, s200
    if price > s200:
        return "sideways, above long-term average", s50, s200
    return "sideways, below long-term average", s50, s200


def vix_zone(v):
    if v < 13:
        return "calm (low fear; complacency possible)"
    if v < 18:
        return "normal"
    if v < 25:
        return "nervous (bigger daily swings likely)"
    return "high fear (very large swings; extra caution)"


def snapshot(name, symbol):
    hist = fetch_history(symbol, "1y")
    c = closes(hist)
    trend, s50, s200 = trend_of(c)
    return {
        "name": name, "symbol": symbol, "price": c[-1], "as_of": hist["as_of"],
        "change_1d": pct_change(c, 1), "change_1w": pct_change(c, 5), "change_1m": pct_change(c, 21),
        "rsi14": rsi(c), "sma50": s50, "sma200": s200, "trend": trend,
        "from_52w_high": (c[-1] / max(c[-250:]) - 1) * 100,
    }


def posture(nifty, bank, vix):
    """Plain-language market mood from simple, transparent rules."""
    points, reasons = 0, []
    for idx in (nifty, bank):
        if idx["trend"] == "uptrend":
            points += 1
            reasons.append(f"{idx['name']} is in an uptrend")
        elif idx["trend"] == "downtrend":
            points -= 1
            reasons.append(f"{idx['name']} is in a downtrend")
    if vix is not None:
        if vix < 18:
            points += 1
            reasons.append(f"India VIX {vix:.1f} is {vix_zone(vix).split(' (')[0]}")
        elif vix >= 25:
            points -= 1
            reasons.append(f"India VIX {vix:.1f} shows high fear")
    r = nifty["rsi14"]
    if r is not None and r > 70:
        reasons.append(f"Nifty RSI {r:.0f} is overbought (rallies can pause)")
    elif r is not None and r < 30:
        reasons.append(f"Nifty RSI {r:.0f} is oversold (falls can pause)")
    mood = "HEALTHY" if points >= 2 else "WEAK" if points <= -1 else "MIXED"
    return mood, reasons


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true", help="print JSON instead of text")
    args = ap.parse_args()

    out = {"market_status": market_status(), "india": [], "global": [], "errors": []}
    for group, items in (("india", INDIA), ("global", GLOBAL)):
        for name, sym in items:
            try:
                out[group].append(snapshot(name, sym))
            except DataError as exc:
                out["errors"].append(str(exc))
    try:
        vix_hist = fetch_history("^INDIAVIX", "3mo")
        vc = closes(vix_hist)
        out["india_vix"] = {"value": vc[-1], "change_1w": pct_change(vc, 5), "zone": vix_zone(vc[-1])}
    except DataError as exc:
        out["india_vix"] = None
        out["errors"].append(str(exc))

    by_name = {x["name"]: x for x in out["india"]}
    if "Nifty 50" not in by_name or "Bank Nifty" not in by_name:
        print("Could not fetch Nifty / Bank Nifty data. Check your internet connection and try again.")
        if out["errors"]:
            print("Details:", "; ".join(out["errors"]))
        sys.exit(1)
    vix_val = out["india_vix"]["value"] if out["india_vix"] else None
    out["mood"], out["reasons"] = posture(by_name["Nifty 50"], by_name["Bank Nifty"], vix_val)

    if args.json:
        print(json.dumps(out, indent=2, default=str))
        return

    print(f"INDIA MARKET PULSE   (data as of {by_name['Nifty 50']['as_of']}; NSE {out['market_status']})")
    print("=" * 78)
    print(f"Overall mood: {out['mood']}")
    for r in out["reasons"]:
        print(f"  - {r}")
    print()
    print(f"{'Index':<20}{'Price':>12}{'1 day':>9}{'1 week':>9}{'1 month':>9}{'RSI':>6}  Trend")
    for x in out["india"]:
        print(f"{x['name']:<20}{fmt_num(x['price']):>12}{fmt_pct(x['change_1d']):>9}{fmt_pct(x['change_1w']):>9}"
              f"{fmt_pct(x['change_1m']):>9}{fmt_num(x['rsi14'], 0):>6}  {x['trend']}")
    if out["india_vix"]:
        v = out["india_vix"]
        print(f"\nIndia VIX (fear meter): {v['value']:.2f} ({fmt_pct(v['change_1w'])} this week) -> {v['zone']}")
    print("\nGlobal cues")
    for x in out["global"]:
        print(f"  {x['name']:<18}{fmt_num(x['price']):>12}  1 day {fmt_pct(x['change_1d']):>8}  1 week {fmt_pct(x['change_1w']):>8}")
    if out["errors"]:
        print("\nSkipped (data unavailable):", "; ".join(out["errors"]))
    print("\nFor learning and research only. Not investment advice.")


if __name__ == "__main__":
    main()
