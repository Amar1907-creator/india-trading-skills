---
name: india-trading-navigator
description: Start here. Figures out what the user wants (learn basics, check today's Indian market, research an NSE/BSE stock, size a trade, understand news, find strong sectors, or analyse US markets) and routes them to the right skill in this toolkit, or to the tradermonty US trading skills if they're installed. Use when the user says "where do I start", "which skill should I use", "help me with trading", "I'm new to stocks", "kya karu", or asks a broad trading or investing question without naming a skill.
---

# India Trading Navigator

Pick the right tool for the user's goal and explain the next step simply.

## Step 1: Understand the user (ask at most 2 short questions if unclear)

- **Experience**: complete beginner / some experience / active trader
- **Market**: India (NSE/BSE) / US / both
- **Goal**: learn, check the market, research a stock, plan a trade, understand news, find sectors

## Step 2: Route

### Indian market (this toolkit)

| Goal | Skill | Example request |
|------|-------|-----------------|
| Learn from zero | `beginner-trading-coach` | "Teach me what Nifty is" / "start lesson 1" |
| How is the market today? | `india-market-pulse` | "How is the market today?" |
| Understand a stock | `india-stock-explainer` | "Explain Infosys stock" |
| How many shares to buy | `india-position-sizer` | "I have ₹50,000, entry 500, stop 480" |
| Why is the market moving? | `india-news-impact` | "Aaj market kyu gira?" |
| Which sectors are strong? | `india-sector-rotation` | "Which sector is leading?" |
| Check my own portfolio | `india-portfolio-review` | "Review my Groww portfolio" |

### Suggested daily routine (about 10 minutes)
1. `india-market-pulse` → is the mood HEALTHY, MIXED or WEAK?
2. `india-news-impact` → what's driving it?
3. `india-sector-rotation` (weekly is enough) → where is strength?
4. Before any trade: `india-stock-explainer` + `india-position-sizer`

### Complete beginner path
Start with `beginner-trading-coach` (4-week learning path). Encourage index funds / SIPs as the core and small,
careful steps in direct stocks. Steer them away from F&O and intraday until they have experience.

### US markets (tradermonty/claude-trading-skills)

If the user asks about US stocks, check whether those skills are installed (look for folders such as
`market-breadth-analyzer` or `trading-skills-navigator` in the skills directory). If they are, route to them, e.g.:

| Goal | tradermonty skill |
|------|-------------------|
| US market health (no API key) | `market-breadth-analyzer`, `uptrend-analyzer` |
| US stock research | `us-stock-analysis` |
| US news impact | `market-news-analyst` |
| Backtesting a strategy idea (any market) | `backtest-expert` |
| Options theory / Greeks (any market) | `options-strategy-advisor` |
| Trade journal and review | `trader-memory-core`, `signal-postmortem` |
| More US options | `trading-skills-navigator` (their navigator) |

If they aren't installed, say so and link https://github.com/tradermonty/claude-trading-skills.
Note that many of those skills need paid US data keys (FMP, FinViz), and some are built around US brokers such as Alpaca.

### Global link (India + US)
For "how will the US market affect India today", run `india-market-pulse` (it includes S&P 500, Nasdaq, USD/INR and crude)
and, if installed, tradermonty's `market-breadth-analyzer` for US breadth.

## Rules

- **Never place, modify or cancel orders, and never move money**, even if a broker connector (such as Groww MCP) is connected and even if the user asks. Only read data. Tell the user to place trades themselves in their broker app.
- These tools are for learning and research.
- No buy or sell calls. For personal advice, point to a SEBI-registered investment adviser.
