---
name: india-market-pulse
description: Daily 5-minute health check of the Indian stock market (NSE/BSE). Shows Nifty 50, Bank Nifty, Sensex, midcaps, smallcaps, India VIX fear meter, global cues (US markets, USD/INR, crude) and an overall HEALTHY / MIXED / WEAK mood with reasons, then adds GIFT Nifty and FII/DII flows from the web. Use when the user asks "how is the market today", "Nifty kaisa hai", "should I be careful today", "market mood", "pre-market check", or wants a daily Indian market summary. No API key needed.
---

# India Market Pulse

A quick, honest read of the Indian market for beginners and experienced traders alike.

## Step 1: Run the data script

```bash
python3 <this-skill-folder>/scripts/market_pulse.py
```

(On Windows use `python` instead of `python3`.) Add `--json` if you want to compute more from the numbers.
The script needs only internet access, no installs and no API key. If it fails, tell the user plainly and
continue with Step 2 using web search, noting that the numbers came from the web.

## Step 2: Add what the script cannot see (web search)

Search for, and cite the source and date of, each of these:
1. **GIFT Nifty**: the latest level and the premium or discount to Nifty. It hints at the opening before 9:15 AM IST.
2. **FII / DII cash-market flows**: the latest provisional figures (₹ crore bought or sold). NSE publishes these after market close.
3. **The 1-3 biggest news items** moving Indian markets today (RBI, results, global events).

If you can't find a figure or it's older than 2 trading days, say so. Never guess a number.

## Step 3: Explain it simply

Use this structure and keep the whole thing short:

1. **Today's mood in one line**, e.g. "Market is WEAK: Nifty and Bank Nifty are below their long-term averages."
2. **The why**: 3 bullets from the script's reasons, in plain words.
3. **Fear meter**: the India VIX zone in one line. Explain that a higher VIX means bigger daily swings.
4. **Global cues**: one line each on the US markets, the rupee and crude, and what each means for India
   (a weak rupee helps IT exporters, high crude hurts oil marketing companies, paints and airlines).
5. **Money flow**: FII/DII from Step 2.
6. **What a careful trader might do**: general *process* guidance only, e.g. "in a WEAK market, many disciplined
   traders reduce position size and avoid new aggressive buys". Never say "buy X" or "sell X".
7. One-line disclaimer.

If the user writes in Hindi or Hinglish, reply in the same style.

## How the mood is calculated (so you can explain it)

- Each of Nifty and Bank Nifty: +1 if in an **uptrend** (price > 50-day avg > 200-day avg), -1 if in a **downtrend** (the reverse).
- India VIX: +1 if below 18 (normal or calm), -1 if 25 or above (high fear).
- Total ≥ 2 → HEALTHY, ≤ -1 → WEAK, otherwise MIXED.
- RSI above 70 or below 30 is shown as a caution note, not scored.

This is a simple trend-following rule, not a prediction. Markets can turn quickly.
See `references/reading-the-pulse.md` for what each number means.

## Rules

- Always show the data's "as of" time. Yahoo data can be about 15 minutes delayed, and the script doesn't know exchange holidays.
- Never give buy or sell calls, price targets or guarantees. This is education and research.
- For personal advice, point users to a SEBI-registered investment adviser.
