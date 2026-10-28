#!/usr/bin/env python3
"""India Portfolio Review: health check of a stock portfolio (read-only).

Usage:
    python3 portfolio_review.py holdings.csv
    python3 portfolio_review.py holdings.json --json

Input: a CSV or JSON list of holdings with a symbol, quantity and average buy price.
Accepted column names (any case): symbol / tradingsymbol / ticker, quantity / qty / shares,
avg_price / average_price / average buy price / buy_price.

This script only reads prices. It never places, changes or cancels orders.
No API key needed. Data: Yahoo Finance (may be ~15 min delayed).
"""

import argparse
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if hasattr(sys.stdout, "reconfigure"):  # show ₹ correctly on Windows consoles
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from india_data import DataError, closes, fetch_history, fmt_num, fmt_pct, pct_change, sma, to_symbol  # noqa: E402

ALIASES = {
    "symbol": ("symbol", "tradingsymbol", "trading_symbol", "ticker", "nse_symbol", "stock_symbol"),
    "quantity": ("quantity", "qty", "shares", "quantity_available", "holding_quantity"),
    "avg_price": ("avg_price", "average_price", "averageprice", "average buy price", "avg buy price",
                  "buy_price", "avg_cost", "average_cost"),
}
SINGLE_STOCK_LIMIT = 20.0   # % of portfolio in one stock that triggers a warning
TOP3_LIMIT = 60.0           # % in the three largest holdings that triggers a warning
DEEP_LOSS = -20.0           # % below average price that triggers a review note


def _norm(key):
    return "_".join(str(key).strip().lower().replace("-", " ").split())


def _pick(row, field):
    lookup = {_norm(k): v for k, v in row.items() if k is not None}
    for name in ALIASES[field]:
        value = lookup.get(_norm(name))
        if value is not None and str(value).strip() != "":
            return value
    return None


def _number(value):
    return float(str(value).replace(",", "").replace("₹", "").strip())


def load_holdings(path):
    """Read holdings from CSV or JSON. Returns (holdings, problems)."""
    with open(path, encoding="utf-8-sig") as f:
        if path.lower().endswith(".json"):
            data = json.load(f)
            rows = data.get("holdings", data) if isinstance(data, dict) else data
        else:
            rows = list(csv.DictReader(f))
    holdings, problems = [], []
    for i, row in enumerate(rows, 1):
        sym, qty, avg = _pick(row, "symbol"), _pick(row, "quantity"), _pick(row, "avg_price")
        if not sym or qty is None or avg is None:
            problems.append(f"row {i}: needs symbol, quantity and average price ({dict(row)})")
            continue
        try:
            qty_n, avg_n = _number(qty), _number(avg)
        except ValueError:
            problems.append(f"row {i}: quantity or price isn't a number ({qty!r}, {avg!r})")
            continue
        if qty_n <= 0:
            continue
        holdings.append({"input": str(sym).strip(), "quantity": qty_n, "avg_price": avg_n})
    return holdings, problems


def review(holdings):
    nifty = closes(fetch_history("^NSEI", "1y"))
    rows, errors = [], []
    for h in holdings:
        try:
            hist = fetch_history(to_symbol(h["input"]), "1y")
        except DataError as exc:
            errors.append(str(exc))
            continue
        c = closes(hist)
        price, s200 = c[-1], sma(c, 200)
        invested, value = h["quantity"] * h["avg_price"], h["quantity"] * price
        rows.append({
            "symbol": hist["symbol"], "name": hist["name"], "quantity": h["quantity"],
            "avg_price": h["avg_price"], "price": price, "invested": invested, "value": value,
            "pnl": value - invested, "pnl_pct": (value / invested - 1) * 100 if invested else None,
            "change_1m": pct_change(c, 21), "change_3m": pct_change(c, 63),
            "above_200dma": price > s200 if s200 else None,
        })
    total_value = sum(r["value"] for r in rows)
    total_invested = sum(r["invested"] for r in rows)
    for r in rows:
        r["weight"] = r["value"] / total_value * 100 if total_value else 0
    rows.sort(key=lambda r: r["value"], reverse=True)

    def weighted(key):
        pairs = [(r[key], r["weight"]) for r in rows if r[key] is not None]
        w = sum(wt for _, wt in pairs)
        return sum(v * wt for v, wt in pairs) / w if w else None

    flags = []
    for r in rows:
        if r["weight"] > SINGLE_STOCK_LIMIT:
            flags.append(f"{r['symbol']} is {r['weight']:.1f}% of the portfolio (above {SINGLE_STOCK_LIMIT:.0f}%)")
        if r["pnl_pct"] is not None and r["pnl_pct"] <= DEEP_LOSS:
            flags.append(f"{r['symbol']} is {abs(r['pnl_pct']):.1f}% below your average price; "
                         "review the original reason for holding it")
    top3 = sum(r["weight"] for r in rows[:3])
    if len(rows) > 3 and top3 > TOP3_LIMIT:
        flags.append(f"top 3 holdings are {top3:.1f}% of the portfolio (above {TOP3_LIMIT:.0f}%)")
    if 0 < len(rows) < 5:
        flags.append(f"only {len(rows)} stocks; a few bad results can hurt the whole portfolio")
    downtrend = [r["symbol"] for r in rows if r["above_200dma"] is False]
    if rows and len(downtrend) / len(rows) >= 0.5:
        flags.append(f"{len(downtrend)} of {len(rows)} holdings are below their 200-day average")

    return {
        "holdings": rows, "errors": errors, "flags": flags,
        "total_invested": total_invested, "total_value": total_value,
        "total_pnl": total_value - total_invested,
        "total_pnl_pct": (total_value / total_invested - 1) * 100 if total_invested else None,
        "portfolio_1m": weighted("change_1m"), "portfolio_3m": weighted("change_3m"),
        "nifty_1m": pct_change(nifty, 21), "nifty_3m": pct_change(nifty, 63),
        "top3_weight": top3, "below_200dma": downtrend,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file", help="holdings CSV or JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        holdings, problems = load_holdings(args.file)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: could not read {args.file}: {exc}")
        sys.exit(1)
    if not holdings:
        print("Error: no valid holdings found. " + "; ".join(problems[:3]))
        sys.exit(1)
    try:
        out = review(holdings)
    except DataError as exc:
        print(f"Error: {exc}")
        sys.exit(1)
    out["input_problems"] = problems

    if args.json:
        print(json.dumps(out, indent=2))
        return

    print("INDIA PORTFOLIO REVIEW   (read-only; prices may be ~15 min delayed)")
    print("=" * 96)
    print(f"Invested ₹{fmt_num(out['total_invested'], 0)} | Value ₹{fmt_num(out['total_value'], 0)} | "
          f"P&L ₹{fmt_num(out['total_pnl'], 0)} ({fmt_pct(out['total_pnl_pct'])})")
    print(f"Last 1 month: portfolio {fmt_pct(out['portfolio_1m'])} vs Nifty {fmt_pct(out['nifty_1m'])} | "
          f"Last 3 months: portfolio {fmt_pct(out['portfolio_3m'])} vs Nifty {fmt_pct(out['nifty_3m'])}")
    print("(Portfolio periods use today's weights, so they're an estimate.)")
    print(f"\n{'Stock':<16}{'Qty':>8}{'Avg ₹':>11}{'Now ₹':>11}{'Value ₹':>13}{'Weight':>8}{'P&L':>9}{'3 months':>10}  200-day avg")
    for r in out["holdings"]:
        trend = "above" if r["above_200dma"] else "below" if r["above_200dma"] is False else "n/a"
        print(f"{r['symbol'][:15]:<16}{r['quantity']:>8,.0f}{fmt_num(r['avg_price']):>11}{fmt_num(r['price']):>11}"
              f"{fmt_num(r['value'], 0):>13}{r['weight']:>7.1f}%{fmt_pct(r['pnl_pct']):>9}{fmt_pct(r['change_3m']):>10}  {trend}")
    if out["flags"]:
        print("\nThings to review:")
        for f in out["flags"]:
            print(f"  ! {f}")
    if out["errors"] or problems:
        print("\nSkipped:", "; ".join(out["errors"] + problems))
    print("\nFor learning and research only. Not investment advice. This tool never places orders.")


if __name__ == "__main__":
    main()
