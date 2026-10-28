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

## Step 2: Add what the script cannot see (web)

General web searches often return old pages for these numbers. **Fetch these specific pages first** (with your
web-fetch tool), and use web search only as a fallback. Cite the source and its date or time for every figure.

### 2a. Today's news: fetch Google News search results for the last day

```
https://news.google.com/rss/search?q=Sensex+Nifty+when:1d&hl=en-IN&gl=IN&ceid=IN:en
```

Each item has a title, source and publish time (GMT; add 5:30 for IST). Pick the 1-3 items that explain the move,
preferring closing-bell or market-wrap stories from established outlets (Moneycontrol, Business Standard, Economic Times,
Zee Business, NDTV Profit, DSIJ). If a headline's index level matches the script's close, say so: it confirms the data.
Ignore headlines that contradict the script's numbers and the established outlets (for example "Sensex jumps 1,500 points"
on a day it closed lower). Small sites sometimes mislabel dates or republish old stories.
For a specific topic, change the query, e.g. `q=RBI+policy+when:1d` or `q=FII+selling+when:2d`.

### 2b. FII / DII cash-market flows: fetch two sources and compare

1. `https://groww.in/fii-dii-data` (shows several recent dates)
2. `https://trendlyne.com/macro-data/fii-dii/latest/cash-pastmonth/`

Report the latest date's net FII and DII figures in ₹ crore (positive = net buying). If both sources show the same
figure, say it's confirmed by two sources; if they differ, show both. Provisional figures come out in the evening
(around 4-6 PM IST), so before that the latest is the previous trading day. Say which day it is.

### 2c. GIFT Nifty: fetch two sources and compare

1. `https://www.niftytrader.in/sgx-nifty-live` (shows a timestamp)
2. `https://indmoney.com/indices/gift-nifty`

Report the level, the change, and its **difference from the Nifty close** in the script. A positive difference hints at a
higher open. Use it mainly **before 9:15 AM IST** (for today's open) or **after 3:30 PM** (as an early hint for
tomorrow). During market hours, Nifty's own price matters more. If the page shows no timestamp, say the time is unknown.

### If a source fails

Try the other source, then a web search with the exact date (e.g. "FII DII data 27 October 2026"). If nothing
is found, or the figure is more than 2 trading days old, say so plainly. **Never guess a number.**

## Step 3: Explain it simply

Use this structure and keep the whole thing short:

1. **Today's mood in one line**, e.g. "Market is WEAK: Nifty and Bank Nifty are below their long-term averages."
2. **The why**: 3 bullets from the script's reasons, in plain words.
3. **Fear meter**: the India VIX zone in one line. Explain that a higher VIX means bigger daily swings.
4. **Global cues**: one line each on the US markets, the rupee and crude, and what each means for India
   (a weak rupee helps IT exporters, high crude hurts oil marketing companies, paints and airlines).
5. **Money flow**: FII/DII from Step 2b, with the date and whether two sources agree.
   Add GIFT Nifty from Step 2c when it's useful for the time of day.
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

- **Never place, modify or cancel orders, and never move money**, even if a broker connector (such as Groww MCP) is connected and even if the user asks. Only read data. Tell the user to place trades themselves in their broker app.
- Always show the data's "as of" time. Yahoo data can be about 15 minutes delayed, and the script doesn't know exchange holidays.
- Never give buy or sell calls, price targets or guarantees. This is education and research.
- For personal advice, point users to a SEBI-registered investment adviser.
