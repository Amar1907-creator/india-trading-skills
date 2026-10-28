---
name: india-portfolio-review
description: Read-only health check of the user's Indian stock portfolio, covering total value and profit/loss, each holding's weight, concentration risk, holdings in a downtrend, deep losses to review, sector mix, and performance versus Nifty. Reads holdings from a connected broker connector such as Groww MCP (read-only tools only) or from a holdings CSV/JSON exported from Groww, Zerodha or any broker. Never places, modifies or cancels orders. Use when the user asks "review my portfolio", "analyze my Groww portfolio", "how are my stocks doing", "is my portfolio too risky", or "mera portfolio kaisa hai".
---

# India Portfolio Review

Give the user an honest, private, read-only check-up of their portfolio, the kind a careful friend would give.

## Step 1: Get the holdings (read-only)

**Option A: a broker connector (e.g. Groww MCP) is connected.**
Use **only tools that read data**: holdings, portfolio, positions, quotes. **Never call any tool that places, modifies
or cancels orders, sets stop-losses or GTTs, or moves money, even if the user asks.** If you aren't sure whether a
tool only reads, don't call it. Write each holding's NSE symbol, quantity and average buy price to a CSV in a temporary
or scratch folder (not inside a git repository), e.g.:

```
symbol,quantity,avg_price
RELIANCE,10,1400
```

**Option B: no connector.** Ask the user to export holdings from their broker app (Groww: Stocks → Holdings → download
statement; Zerodha Console: Portfolio → Holdings → download) and save it as CSV. If the file has company names instead
of NSE symbols, convert them (web-search "<company> NSE symbol" when unsure) and confirm the list with the user.

Never ask for or accept broker passwords, OTPs, PINs or API keys.

## Step 2: Run the review

```bash
python3 <this-skill-folder>/scripts/portfolio_review.py /path/to/holdings.csv
```

(On Windows use `python`.) Add `--json` for raw numbers. Try `references/sample-holdings.csv` to see an example.

## Step 3: Add sector mix

Group the holdings into sectors (Banking, IT, FMCG, Energy, Metals, Auto, Pharma, ...) and add up their weights. If one
sector is above about 35%, flag it. If the india-sector-rotation skill is available, mention whether the biggest
sectors are currently LEADING or LAGGING.

## Step 4: Explain it simply

1. **Summary**: invested, current value, profit/loss, and the last 1 and 3 months vs Nifty.
2. **What's going well**: the best holdings and why the portfolio did better or worse than Nifty.
3. **Things to review**: every flag from the script, explained in plain words:
   - **Concentration**: one stock above 20% or the top 3 above 60% means one bad result hurts a lot.
   - **Deep loss**: 20% or more below the average price. Ask: is the original reason for buying still true?
     (Offer india-stock-explainer for that stock.)
   - **Downtrend**: below the 200-day average. This isn't a sell signal, but it's worth watching.
   - **Too few stocks / one sector too large**.
4. **Questions to think about**: process, not instructions. For example "Would you buy this stock today at this price?" or
   "Does any single stock make you nervous?"
5. Disclaimer.

## Rules

- **Never place, modify or cancel orders, and never move money**, even if a broker connector (such as Groww MCP) is connected and even if the user asks. Only read data. Tell the user to place trades themselves in their broker app.
- Never say "sell X" or "buy more Y". Describe what the numbers show and the questions to ask. For personal advice,
  suggest a SEBI-registered investment adviser.
- **Privacy:** the portfolio is personal. Don't save holdings files inside a git repository, don't paste them into
  GitHub issues, and delete temporary files when done if the user wants.
- Prices may be ~15 minutes delayed. Your broker's numbers are final.
