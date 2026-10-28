#!/usr/bin/env python3
"""India Stock Snapshot: price trend, momentum, risk and strength vs Nifty for one NSE/BSE stock.

Usage:
    python3 stock_snapshot.py RELIANCE
    python3 stock_snapshot.py TCS --json
    python3 stock_snapshot.py 500325.BO      # BSE code also works

No API key needed. Data: Yahoo Finance (may be ~15 min delayed).
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if hasattr(sys.stdout, "reconfigure"):  # show ₹ correctly on Windows consoles
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from india_data import (DataError, atr, closes, fetch_history, fmt_num, fmt_pct,  # noqa: E402
                        market_status, pct_change, rsi, sma, to_symbol)

PERIODS = [("1 week", 5), ("1 month", 21), ("3 months", 63), ("6 months", 126), ("1 year", 245)]


def analyse(symbol):
    hist = fetch_history(symbol, "2y")
    c, bars = closes(hist), hist["bars"]
    if len(c) < 30:
        raise DataError(f"Only {len(c)} days of history for {hist['symbol']}; it may be newly listed.")
    nifty = closes(fetch_history("^NSEI", "2y"))

    price = c[-1]
    s20, s50, s200 = sma(c, 20), sma(c, 50), sma(c, 200)
    last_year = c[-245:]
    hi, lo = max(last_year), min(last_year)
    a = atr(bars)
    vol20 = sum(b["volume"] for b in bars[-20:]) / 20
    vol_today = bars[-1]["volume"]

    returns = {}
    for label, n in PERIODS:
        stock_r, nifty_r = pct_change(c, n), pct_change(nifty, n)
        returns[label] = {"stock": stock_r, "nifty": nifty_r,
                          "vs_nifty": None if stock_r is None or nifty_r is None else stock_r - nifty_r}

    if s50 and s200:
        if price > s50 > s200:
            trend = "uptrend (price above 50-day and 200-day averages)"
        elif price < s50 < s200:
            trend = "downtrend (price below 50-day and 200-day averages)"
        else:
            trend = "sideways or changing (averages are mixed)"
    else:
        trend = "not enough history for a long-term trend"

    r6 = returns["6 months"]["vs_nifty"]
    strength = ("stronger than Nifty" if r6 is not None and r6 > 5 else
                "weaker than Nifty" if r6 is not None and r6 < -5 else "moving roughly with Nifty")

    return {
        "symbol": hist["symbol"], "name": hist["name"], "as_of": hist["as_of"], "price": price,
        "trend": trend, "relative_strength_6m": strength, "returns": returns,
        "rsi14": rsi(c), "sma20": s20, "sma50": s50, "sma200": s200,
        "week52_high": hi, "week52_low": lo,
        "pct_below_52w_high": (price / hi - 1) * 100, "pct_above_52w_low": (price / lo - 1) * 100,
        "atr14": a, "atr_pct": a / price * 100 if a else None,
        "volume_today": vol_today, "volume_avg20": vol20,
        "volume_ratio": vol_today / vol20 if vol20 else None,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("stock", help="NSE symbol like RELIANCE, or Yahoo symbol like TCS.BO")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        d = analyse(to_symbol(args.stock))
    except DataError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    if args.json:
        print(json.dumps(d, indent=2, default=str))
        return

    print(f"{d['name']} ({d['symbol']})   price ₹{fmt_num(d['price'])}   as of {d['as_of']}")
    print("=" * 78)
    print(f"Trend:            {d['trend']}")
    print(f"Strength (6m):    {d['relative_strength_6m']}")
    print(f"RSI (14):         {fmt_num(d['rsi14'], 0)}  (above 70 = ran up fast, below 30 = fell fast)")
    print(f"52-wk close range:₹{fmt_num(d['week52_low'])} - ₹{fmt_num(d['week52_high'])}   "
          f"({fmt_pct(d['pct_below_52w_high'])} from high)")
    print(f"Averages:         20d ₹{fmt_num(d['sma20'])} | 50d ₹{fmt_num(d['sma50'])} | 200d ₹{fmt_num(d['sma200'])}")
    print(f"Daily swing:      ATR ₹{fmt_num(d['atr14'])} ({fmt_num(d['atr_pct'])}% of price on a typical day)")
    vr = d["volume_ratio"]
    partial = " - market is open, so today's volume is still partial" if market_status().startswith("open") else ""
    print(f"Volume today:     {d['volume_today']:,} ({fmt_num(vr)}x the 20-day average{partial})" if vr else "Volume: n/a")
    print(f"\n{'Period':<10}{'Stock':>10}{'Nifty':>10}{'Difference':>12}")
    for label, r in d["returns"].items():
        print(f"{label:<10}{fmt_pct(r['stock']):>10}{fmt_pct(r['nifty']):>10}{fmt_pct(r['vs_nifty']):>12}")
    print("\nFor learning and research only. Not investment advice.")


if __name__ == "__main__":
    main()
