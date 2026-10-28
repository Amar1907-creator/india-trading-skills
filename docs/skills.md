# Skills reference

All skills need no API key. "Script" skills run a Python script for live numbers; "Web" skills use Claude's web search
and cite sources.

| Skill | Level | Script | Web |
|-------|-------|:------:|:---:|
| [india-trading-navigator](#india-trading-navigator) | All | | |
| [india-market-pulse](#india-market-pulse) | All | ✅ | ✅ |
| [india-stock-explainer](#india-stock-explainer) | All | ✅ | ✅ |
| [india-position-sizer](#india-position-sizer) | All | ✅ | |
| [india-news-impact](#india-news-impact) | All | | ✅ |
| [india-sector-rotation](#india-sector-rotation) | Intermediate | ✅ | ✅ |
| [india-portfolio-review](#india-portfolio-review) | All | ✅ | |
| [beginner-trading-coach](#beginner-trading-coach) | Beginner | | |

---

## india-trading-navigator

The starting point. Asks at most two questions (experience, market, goal) and routes to the right skill, including the
US tradermonty skills if installed. Suggests a daily routine and a beginner path.

**Try:** "Where do I start?" · "Which skill should I use?"

## india-market-pulse

Daily health check: Nifty 50, Bank Nifty, Sensex, Next 50, Midcap 150, Smallcap 250, India VIX, S&P 500, Nasdaq, USD/INR,
Brent crude. Gives a **HEALTHY / MIXED / WEAK** mood, then adds GIFT Nifty, FII/DII flows and top news from the web.

**Try:** "How is the market today?" · "Nifty kaisa hai?"

```bash
python3 skills/india-market-pulse/scripts/market_pulse.py [--json]
```

**Mood rule:** Nifty and Bank Nifty each score +1 in an uptrend (price > 50-day avg > 200-day avg) and -1 in a
downtrend; India VIX scores +1 below 18 and -1 at 25 or above. A total ≥ 2 is HEALTHY, ≤ -1 is WEAK, anything else is MIXED.

## india-stock-explainer

Explains any NSE/BSE stock: business, growth, ROE, debt, valuation vs peers, promoter holding and pledge, trend and
strength vs Nifty, bull and bear points, red flags, and what to watch next.

**Try:** "Explain HDFC Bank stock" · "Compare TCS and Infosys"

```bash
python3 skills/india-stock-explainer/scripts/stock_snapshot.py RELIANCE [--json]
```

## india-position-sizer

How many shares or lots to trade so one loss is a fixed % of capital. Includes STT, exchange fees, SEBI fee, stamp duty,
GST, DP charge and brokerage; reward:risk; profit after charges; and a stop-loss vs ATR check.

**Try:** "₹1 lakh capital, 1% risk, entry 1200, stop 1150, target 1320"

```bash
python3 skills/india-position-sizer/scripts/position_size.py --capital 100000 --risk-pct 1 \
  --entry 1200 --stop 1150 --target 1320 [--product delivery|intraday|futures|options] \
  [--lot-size N] [--symbol RELIANCE] [--json]
```

Run with `--help` for brokerage options.

## india-news-impact

Finds today's market-moving news (RBI, Budget, results, FII flows, crude, rupee, Fed), ranks it by impact, and explains
which sectors are helped or hurt and why. Verifies forwarded headlines and warns about tip scams.

**Try:** "Why did the market fall today?" · "How will the RBI decision affect stocks?"

## india-sector-rotation

Ranks 16 sector and market-cap indices by strength vs Nifty over 1 and 3 months, labels each LEADING / IMPROVING /
WEAKENING / LAGGING, and explains the drivers.

**Try:** "Which sector is strong?" · "Konsa sector chal raha hai?"

```bash
python3 skills/india-sector-rotation/scripts/sector_rotation.py [--json]
```

## india-portfolio-review

Read-only portfolio check-up: invested vs current value, P&L, weight of each stock, concentration (one stock above 20%,
top 3 above 60%), holdings 20%+ below average price, holdings below the 200-day average, sector mix, and 1- and
3-month performance vs Nifty.

Holdings come from a broker connector such as **Groww MCP** (read tools only) or from a CSV/JSON you export from
Groww, Zerodha or any broker. **It never places, modifies or cancels orders**, and holdings files are git-ignored.

**Try:** "Review my Groww portfolio" · "Mera portfolio kaisa hai?"

```bash
python3 skills/india-portfolio-review/scripts/portfolio_review.py holdings.csv [--json]
```

CSV columns: `symbol, quantity, avg_price` (common broker names such as `Trading Symbol`, `Qty` and `Average buy price` also work).

## beginner-trading-coach

A patient teacher: simple definitions with Indian examples, a 4-week learning path, quizzes, safety lessons
(1% rule, F&O risk, scams), in English, Hindi or Hinglish.

**Try:** "Teach me trading from zero" · "What is a stop-loss?" · "Start lesson 1"
