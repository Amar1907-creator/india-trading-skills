---
name: india-stock-explainer
description: Explain any Indian stock (NSE/BSE) in simple language, covering what the company does, whether its numbers are healthy, its price trend and strength versus Nifty, valuation, key risks and what to watch next. Combines a live price/technical snapshot (no API key) with sourced web research on fundamentals (Screener.in, company filings, NSE/BSE announcements). Use when the user asks "tell me about RELIANCE", "is TCS a good company", "explain HDFC Bank stock", "Zomato share analysis", or compares two Indian stocks. Never gives buy/sell calls.
---

# India Stock Explainer

Turn a stock name into a clear, sourced, balanced explanation that a beginner understands and an
experienced trader respects.

## Step 1: Get the right symbol

Users type names like "tata steel" or "hdfc bank". The script accepts the NSE symbol (`TATASTEEL`, `HDFCBANK`).
If the script says there's no data, web-search "<company> NSE symbol" to find the current symbol (companies get
new symbols after mergers, demergers and renames), tell the user, and retry.

## Step 2: Price snapshot

```bash
python3 <this-skill-folder>/scripts/stock_snapshot.py SYMBOL
```

(On Windows use `python`.) It reports the trend, RSI, 52-week closing range, typical daily swing (ATR),
volume vs average, and returns vs Nifty over 1 week to 1 year. To compare two stocks, run it once for each.

## Step 3: Fundamentals research (web)

Search and **cite every number with its source and period** (e.g. "FY26, Screener.in"). Good sources are
Screener.in, the company's investor-relations page, NSE/BSE corporate announcements, and annual reports.
Collect:
- What the business does and how it earns money (one or two sentences)
- Market cap and sector
- Revenue and net profit over the last 3-5 years (growing, flat or falling?)
- ROE / ROCE, debt-to-equity
- P/E compared with its own history and with 2-3 peers
- Promoter holding and any **pledged shares**, and the FII/DII holding trend
- Latest quarterly result highlights and any big recent news

If a figure isn't found, write "not found". Never invent numbers.

## Step 4: Write the explanation

Use `references/report-template.md`. Keep it scannable:
1. **In one line**: what the company is.
2. **Business health**: a green/yellow/red table for growth, profitability, debt and valuation, with one plain reason each.
3. **Price trend**: from Step 2, explained simply ("the stock is 26% below its 1-year high and weaker than Nifty").
4. **Good things** (bull points) and **risks** (bear points), at least 2-3 of each. Always include both.
5. **What to watch next**: the next results date, key levels (the 50-day and 200-day averages), and news triggers.
6. **For beginners**: one teaching line about a term used (e.g. what P/E means).
7. Disclaimer.

## Red flags to always mention if found

High or rising promoter pledge, falling promoter holding, auditor resignation, SEBI action, repeated losses,
debt-to-equity above ~1.5 (for non-financial companies), very thin trading volume, or an ASM/GSM surveillance listing.

## Rules

- Balanced, not hype. Never say "buy", "sell", "multibagger" or give price targets.
- If asked "should I buy?", explain what the data shows, then explain how to decide (budget, time horizon, stop-loss,
  diversification) and suggest a SEBI-registered investment adviser for personal advice.
- Match the user's language (English, Hindi, Hinglish).
