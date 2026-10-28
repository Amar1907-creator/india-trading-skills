"""Shared market-data helper for india-trading-skills.

Standard library only, so users never need `pip install`. Prices come from
Yahoo Finance's public chart endpoint (no API key). Data can be delayed by
~15 minutes and is for research and learning, not for order execution.

Canonical copy lives in shared/india_data.py; scripts/sync_shared.py copies
it into every skill's scripts/ folder so each skill works on its own.
"""

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))
_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={rng}&interval={itv}"
_HEADERS = {"User-Agent": "Mozilla/5.0 (india-trading-skills)"}

# Friendly names -> Yahoo symbols, so users can type "nifty" or "bank nifty".
INDEX_ALIASES = {
    "NIFTY": "^NSEI", "NIFTY50": "^NSEI", "NIFTY 50": "^NSEI",
    "BANKNIFTY": "^NSEBANK", "BANK NIFTY": "^NSEBANK", "NIFTYBANK": "^NSEBANK",
    "SENSEX": "^BSESN", "INDIAVIX": "^INDIAVIX", "INDIA VIX": "^INDIAVIX", "VIX": "^INDIAVIX",
    "FINNIFTY": "NIFTY_FIN_SERVICE.NS", "NIFTYIT": "^CNXIT", "NIFTY IT": "^CNXIT",
}


class DataError(Exception):
    """Raised when market data cannot be fetched or is empty."""


def to_symbol(text):
    """Turn user input like 'reliance', 'nifty' or 'TCS.BO' into a Yahoo symbol."""
    t = text.strip().upper()
    if t in INDEX_ALIASES:
        return INDEX_ALIASES[t]
    if any(ch in t for ch in ".^=") or t.endswith("-USD"):
        return t
    return t.replace(" ", "") + ".NS"


def fetch_history(symbol, rng="1y", interval="1d", retries=2):
    """Return {'symbol', 'name', 'currency', 'bars': [...]} with bars oldest first.

    Each bar is {'date', 'open', 'high', 'low', 'close', 'volume'}; bars with a
    missing close are dropped (Yahoo leaves gaps on holidays and thin indices).
    An NSE symbol that fails is retried once on BSE.
    """
    url = _CHART_URL.format(sym=urllib.parse.quote(symbol), rng=rng, itv=interval)
    payload, last_err = None, None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=_HEADERS)
            with urllib.request.urlopen(req, timeout=15) as resp:
                payload = json.load(resp)
            break
        except urllib.error.HTTPError as exc:
            if exc.code == 404:  # unknown symbol: no point retrying
                payload = {"chart": {"result": None}}
                break
            last_err = exc
            time.sleep(1 + attempt)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_err = exc
            time.sleep(1 + attempt)
    if payload is None:
        raise DataError(f"Could not reach Yahoo Finance for {symbol}: {last_err}")

    result = (payload.get("chart") or {}).get("result")
    if not result:
        if symbol.endswith(".NS"):
            return fetch_history(symbol[:-3] + ".BO", rng, interval, retries)
        name = symbol[:-3] if symbol.endswith(".BO") else symbol
        raise DataError(f"No data for '{name}' on NSE or BSE. Check the exact trading symbol "
                        "(e.g. RELIANCE, TCS, HDFCBANK); companies that merged, split or renamed get new symbols.")

    res = result[0]
    meta = res.get("meta", {})
    quote = (res.get("indicators", {}).get("quote") or [{}])[0]
    bars = []
    for i, ts in enumerate(res.get("timestamp") or []):
        close = (quote.get("close") or [None])[i]
        if close is None:
            continue
        bars.append({
            "date": datetime.fromtimestamp(ts, IST).strftime("%Y-%m-%d"),
            "open": quote["open"][i], "high": quote["high"][i], "low": quote["low"][i],
            "close": close, "volume": (quote.get("volume") or [0])[i] or 0,
        })
    if not bars:
        raise DataError(f"'{symbol}' returned no price bars.")
    return {
        "symbol": meta.get("symbol", symbol),
        "name": meta.get("longName") or meta.get("shortName") or symbol,
        "currency": meta.get("currency", "INR"),
        "last_price": meta.get("regularMarketPrice", bars[-1]["close"]),
        "as_of": datetime.fromtimestamp(meta.get("regularMarketTime", time.time()), IST).strftime("%Y-%m-%d %H:%M IST"),
        "bars": bars,
    }


def closes(hist):
    return [b["close"] for b in hist["bars"]]


def sma(values, n):
    return sum(values[-n:]) / n if len(values) >= n else None


def ema(values, n):
    if len(values) < n:
        return None
    k, e = 2 / (n + 1), sum(values[:n]) / n
    for v in values[n:]:
        e = v * k + e * (1 - k)
    return e


def rsi(values, n=14):
    """Wilder's RSI. Returns None when there is not enough history."""
    if len(values) <= n:
        return None
    gains = [max(values[i] - values[i - 1], 0) for i in range(1, len(values))]
    losses = [max(values[i - 1] - values[i], 0) for i in range(1, len(values))]
    avg_g, avg_l = sum(gains[:n]) / n, sum(losses[:n]) / n
    for gain, loss in zip(gains[n:], losses[n:]):
        avg_g = (avg_g * (n - 1) + gain) / n
        avg_l = (avg_l * (n - 1) + loss) / n
    if avg_l == 0:
        return 100.0
    return 100 - 100 / (1 + avg_g / avg_l)


def atr(bars, n=14):
    """Average True Range (simple average of the last n true ranges)."""
    if len(bars) <= n:
        return None
    trs = []
    for prev, cur in zip(bars[-n - 1:-1], bars[-n:]):
        trs.append(max(cur["high"] - cur["low"], abs(cur["high"] - prev["close"]), abs(cur["low"] - prev["close"])))
    return sum(trs) / n


def pct_change(values, sessions):
    """Percent change over the last `sessions` trading days (None if too short)."""
    if len(values) <= sessions or values[-sessions - 1] == 0:
        return None
    return (values[-1] / values[-sessions - 1] - 1) * 100


def market_status(now=None):
    """Rough NSE session status. Does not know exchange holidays."""
    now = now or datetime.now(IST)
    if now.weekday() >= 5:
        return "closed (weekend)"
    minutes = now.hour * 60 + now.minute
    if minutes < 9 * 60:
        return "pre-open soon" if minutes >= 8 * 60 else "closed (before market)"
    if minutes < 9 * 60 + 15:
        return "pre-open session"
    if minutes <= 15 * 60 + 30:
        return "open (unless today is an exchange holiday)"
    return "closed (after market)"


def fmt_pct(v):
    return "n/a" if v is None else f"{v:+.2f}%"


def fmt_num(v, digits=2):
    return "n/a" if v is None else f"{v:,.{digits}f}"
