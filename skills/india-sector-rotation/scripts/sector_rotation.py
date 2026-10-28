#!/usr/bin/env python3
"""India Sector Rotation: which NSE sectors are leading, improving, weakening or lagging vs Nifty.

Usage:
    python3 sector_rotation.py
    python3 sector_rotation.py --json

Each sector index is compared with Nifty 50 over 1 month and 3 months:
    LEADING    beating Nifty over 3 months and still beating it over 1 month
    WEAKENING  beating Nifty over 3 months but falling behind over 1 month
    IMPROVING  behind Nifty over 3 months but beating it over 1 month
    LAGGING    behind Nifty on both

No API key needed. Data: Yahoo Finance (may be ~15 min delayed).
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if hasattr(sys.stdout, "reconfigure"):  # show ₹ correctly on Windows consoles
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from india_data import DataError, closes, fetch_history, fmt_num, fmt_pct, pct_change, rsi, sma  # noqa: E402

# Sector indices with reliable daily history on Yahoo.
SECTORS = [
    ("Bank", "^NSEBANK"), ("PSU Bank", "^CNXPSUBANK"), ("Financial Services", "NIFTY_FIN_SERVICE.NS"),
    ("IT", "^CNXIT"), ("Auto", "^CNXAUTO"), ("Pharma", "^CNXPHARMA"), ("FMCG", "^CNXFMCG"),
    ("Metal", "^CNXMETAL"), ("Realty", "^CNXREALTY"), ("Energy", "^CNXENERGY"), ("Infra", "^CNXINFRA"),
    ("Consumption", "^CNXCONSUM"), ("PSE (Govt cos.)", "^CNXPSE"), ("MNC", "^CNXMNC"),
    ("Midcap 150", "NIFTYMIDCAP150.NS"), ("Smallcap 250", "NIFTYSMLCAP250.NS"),
]


def quadrant(rel_1m, rel_3m):
    if rel_3m >= 0:
        return "LEADING" if rel_1m >= 0 else "WEAKENING"
    return "IMPROVING" if rel_1m >= 0 else "LAGGING"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        nifty_hist = fetch_history("^NSEI", "1y")
    except DataError as exc:
        print(f"Error: could not fetch Nifty 50: {exc}")
        sys.exit(1)
    nifty = closes(nifty_hist)
    n1w, n1m, n3m = pct_change(nifty, 5), pct_change(nifty, 21), pct_change(nifty, 63)

    rows, skipped = [], []
    for name, sym in SECTORS:
        try:
            c = closes(fetch_history(sym, "1y"))
        except DataError:
            skipped.append(name)
            continue
        r1w, r1m, r3m = pct_change(c, 5), pct_change(c, 21), pct_change(c, 63)
        if None in (r1m, r3m):
            skipped.append(name)
            continue
        rel1m, rel3m = r1m - n1m, r3m - n3m
        s50 = sma(c, 50)
        rows.append({
            "sector": name, "symbol": sym, "change_1w": r1w, "change_1m": r1m, "change_3m": r3m,
            "vs_nifty_1m": rel1m, "vs_nifty_3m": rel3m, "rsi14": rsi(c),
            "above_50dma": c[-1] > s50 if s50 else None, "quadrant": quadrant(rel1m, rel3m),
            # blend favours recent momentum but keeps the 3-month picture
            "score": 0.6 * rel1m + 0.4 * rel3m,
        })
    rows.sort(key=lambda r: r["score"], reverse=True)

    out = {"as_of": nifty_hist["as_of"], "nifty": {"change_1w": n1w, "change_1m": n1m, "change_3m": n3m},
           "sectors": rows, "skipped": skipped}
    if args.json:
        print(json.dumps(out, indent=2))
        return

    print(f"INDIA SECTOR ROTATION   (as of {out['as_of']})")
    print(f"Nifty 50: 1 week {fmt_pct(n1w)} | 1 month {fmt_pct(n1m)} | 3 months {fmt_pct(n3m)}")
    print("=" * 92)
    print(f"{'#':>2} {'Sector':<20}{'1 week':>9}{'1 month':>9}{'3 months':>10}{'vs Nifty 1m':>13}"
          f"{'vs Nifty 3m':>13}{'RSI':>5}  Status")
    for i, r in enumerate(rows, 1):
        print(f"{i:>2} {r['sector']:<20}{fmt_pct(r['change_1w']):>9}{fmt_pct(r['change_1m']):>9}"
              f"{fmt_pct(r['change_3m']):>10}{fmt_pct(r['vs_nifty_1m']):>13}{fmt_pct(r['vs_nifty_3m']):>13}"
              f"{fmt_num(r['rsi14'], 0):>5}  {r['quadrant']}")
    for q in ("LEADING", "IMPROVING", "WEAKENING", "LAGGING"):
        names = [r["sector"] for r in rows if r["quadrant"] == q]
        print(f"\n{q:<10} {', '.join(names) if names else '-'}")
    if skipped:
        print(f"\nSkipped (not enough data): {', '.join(skipped)}")
    print("\nFor learning and research only. Not investment advice.")


if __name__ == "__main__":
    main()
