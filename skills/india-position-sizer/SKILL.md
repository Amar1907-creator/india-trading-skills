---
name: india-position-sizer
description: Calculate how many shares or F&O lots to trade in Indian markets so that one losing trade costs only a small, fixed part of capital. Includes realistic Indian charges (brokerage, STT, exchange fees, stamp duty, GST, DP charge), reward:risk, profit at target after charges, and a check of the stop-loss against the stock's normal daily swing. Supports delivery, intraday (long/short), futures and options. Use when the user asks "how many shares should I buy", "kitne share lu", "position size", "risk per trade", "lot size calculation", or plans a trade with an entry and stop-loss.
---

# India Position Sizer

The single most important habit in trading is to decide **how much you can lose before you buy**. This skill does that math.

## Step 1: Collect the inputs (ask only for what's missing)

| Input | Example | If the user doesn't know |
|-------|---------|---------------------------|
| Capital (₹) | 100000 | Required. It's the money set aside for trading, not life savings |
| Risk % per trade | 1 | Suggest 0.5-1% for beginners and explain why (see below) |
| Entry price | 1200 | Required |
| Stop-loss price | 1150 | Help them choose: below a recent swing low or the 50-day average, or about 1.5x ATR. The india-stock-explainer skill can show these |
| Target (optional) | 1320 | Skip if unknown |
| Product | delivery / intraday / futures / options | Default delivery |
| Lot size (F&O only) | 75 | **Never assume it.** NSE revises lot sizes; web-search "NSE <symbol> lot size" and cite the source and date |

## Step 2: Run

```bash
python3 <this-skill-folder>/scripts/position_size.py --capital 100000 --risk-pct 1 --entry 1200 --stop 1150 --target 1320 --symbol RELIANCE
```

(On Windows use `python`.) `--symbol` is optional and checks whether the stop is too tight for the stock's normal swing.
Groww, Zerodha and others charge differently. If the user tells you their broker's brokerage, pass
`--brokerage-flat`, `--brokerage-pct` and `--brokerage-min`. Run `--help` for all options.

## Step 3: Explain

1. **The answer first**: "Buy up to 20 shares (₹24,000)."
2. **Why**: "If the stop-loss hits, you lose about ₹1,115 including charges, which is about 1.1% of your capital."
3. **Reward:risk** and profit at target after charges, if a target was given.
4. Every warning the script printed, in plain words.
5. One beginner lesson: **the 1% rule**. With 1% risk you can be wrong 10 times in a row and still have about 90% of
   your capital. Beginners usually lose money by having no stop-loss, or one that's too big, more than by picking bad stocks.

## Rules

- **Never place, modify or cancel orders, and never move money**, even if a broker connector (such as Groww MCP) is connected and even if the user asks. Only read data. Tell the user to place trades themselves in their broker app.
- Never increase size to "make it worth it". If the result is 0 shares, explain that the stop is too wide for the capital,
  and offer to try a closer logical stop or a smaller-priced stock.
- For F&O: always repeat that margin is set by the broker, losses can exceed the plan if price gaps, and
  that SEBI studies found about 9 in 10 individual F&O traders lose money. Never encourage F&O for beginners.
- Charges are estimates. Tell users to check their contract note.
- This is a calculation aid, not advice to trade.
