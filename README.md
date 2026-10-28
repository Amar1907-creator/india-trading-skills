# 🇮🇳 India Trading Skills for Claude

[![tests](https://github.com/Amar1907-creator/india-trading-skills/actions/workflows/tests.yml/badge.svg)](https://github.com/Amar1907-creator/india-trading-skills/actions/workflows/tests.yml) ![No API key](https://img.shields.io/badge/API%20key-not%20needed-brightgreen) ![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue) [![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE) [![PRs welcome](https://img.shields.io/badge/PRs-welcome-orange)](CONTRIBUTING.md)

**Claude skills that understand the Indian stock market (NSE/BSE): for first-time Groww users and experienced traders.**

Ask Claude *"How is the market today?"*, *"Explain Infosys stock"*, *"Aaj market kyu gira?"* or
*"I have ₹50,000, how many shares should I buy?"*, and get a clear, sourced, honest answer.

- ✅ **No API key, no paid data, no installs.** It only needs Python 3.9+, with no extra packages.
- ✅ **Live data** for Nifty, Bank Nifty, Sensex, India VIX, 16 sector indices and any NSE/BSE stock
- ✅ **Real Indian charges** (STT, stamp duty, GST, DP charges) in position sizing
- ✅ **Beginner-friendly**, in English, Hindi or Hinglish
- ✅ **Safe by design**: it never places trades, never connects to your broker account, and never gives buy/sell tips
- ✅ Works alongside the popular US [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills)

> ⚠️ **For learning and research only. Not investment advice.** See the [disclaimer](#disclaimer).

**Contents:** [Skills](#the-skills) · [Install](#install-2-minutes) · [Daily routine](#a-10-minute-daily-routine) · [How it works](#how-it-works) · [Docs](#documentation) · [Roadmap](#roadmap) · [Contributing](#contributing) · [Disclaimer](#disclaimer)

---

## The skills

| Skill | Ask Claude... | What you get |
|-------|---------------|--------------|
| 🧭 **india-trading-navigator** | "Where do I start?" | Points you to the right skill, Indian or US |
| 📊 **india-market-pulse** | "How is the market today?" | Nifty, Bank Nifty, midcaps, smallcaps, India VIX, US cues, rupee, crude → **HEALTHY / MIXED / WEAK** mood with reasons, plus GIFT Nifty and FII/DII from the web |
| 🔍 **india-stock-explainer** | "Explain HDFC Bank stock" | Business, growth, debt, valuation, promoter pledge, trend vs Nifty, good points, risks and red flags, with sources |
| 🧮 **india-position-sizer** | "₹1 lakh capital, entry 1200, stop 1150" | Exact shares or lots, max loss including all charges, reward:risk, and a check that the stop isn't too tight |
| 📰 **india-news-impact** | "Why did the market fall today?" | Today's news ranked by impact, which sectors are affected and why, with sources |
| 🔄 **india-sector-rotation** | "Which sector is strong?" | 16 sectors ranked vs Nifty: LEADING / IMPROVING / WEAKENING / LAGGING |
| 💼 **india-portfolio-review** | "Review my Groww portfolio" | Value, P&L, weights, concentration, deep losses, downtrends and sector mix vs Nifty. **Read-only**: works with Groww MCP or a holdings CSV, and never places orders |
| 🎓 **beginner-trading-coach** | "Teach me trading from zero" | A 4-week course, simple glossary, quizzes, and scam warnings |

### Example: India Market Pulse

```text
INDIA MARKET PULSE   (data as of 2026-10-28 12:53 IST; NSE open)
==============================================================================
Overall mood: WEAK
  - Nifty 50 is in a downtrend
  - Bank Nifty is in a downtrend
  - India VIX 16.3 is normal

Index                      Price    1 day   1 week  1 month   RSI  Trend
Nifty 50               22,718.75   -0.14%   -0.41%   -1.82%    45  downtrend
Bank Nifty             54,260.70   +0.53%   -1.30%   -2.37%    39  downtrend
Nifty Midcap 150       21,089.25   +0.41%   -0.52%   -6.01%    37  sideways, below long-term average

India VIX (fear meter): 16.31 (+4.02% this week) -> normal
```

Claude then adds GIFT Nifty, FII/DII flows and the day's key news, and explains everything in plain words.

### Example: India Position Sizer

```text
Capital ₹100,000 | risk 1.0% = ₹1,000 max loss
Entry ₹1,200.00 | stop ₹1,150.00 | risk per unit ₹50.00

>> Quantity: 20   (limited by risk)
   Position value: ₹24,000
   Loss if stop hits: ₹1,000 + ~₹115 charges = ₹1,115
   Reward:risk = 2.40 | profit at target after charges ≈ ₹2,281
```

---

## Install (2 minutes)

You need [Claude Code](https://docs.claude.com/en/docs/claude-code) (desktop app or terminal) and Python 3.9+
(already on macOS and most Linux; on Windows install it from python.org).

**macOS / Linux**

```bash
git clone https://github.com/Amar1907-creator/india-trading-skills.git
cd india-trading-skills
./install.sh
```

**Windows**: download the ZIP from GitHub, unzip it, and copy every folder inside `skills/` into
`C:\Users\<you>\.claude\skills\`.

Then open Claude Code and ask: **"Where do I start with Indian stock market?"**

### Also want US market skills?

```bash
git clone https://github.com/tradermonty/claude-trading-skills.git
cp -R claude-trading-skills/skills/* ~/.claude/skills/
```

The navigator automatically sends US questions to those skills. Many of them need paid US data keys.

---

## A 10-minute daily routine

1. **india-market-pulse**: what's the mood?
2. **india-news-impact**: why?
3. **india-sector-rotation** (weekly): where is the strength?
4. Before any trade: **india-stock-explainer** + **india-position-sizer**
5. Monthly: **india-portfolio-review**

New to the market? Start with **beginner-trading-coach**: *"start lesson 1"*.

---

## How it works

- Price data comes from Yahoo Finance's public chart data, with no key, using only Python's standard library.
  Data may be delayed by about 15 minutes, and the scripts don't know exchange holidays.
- Fundamentals, news, GIFT Nifty, FII/DII and F&O lot sizes come from Claude's web search, **with every number cited**.
  Skills are told never to guess a number.
- Every rule (trend, mood score, sector labels) is simple and explained, so you can learn from it rather than trust a black box.

## Roadmap

- [ ] FII/DII flow tracker with history
- [ ] Nifty / Bank Nifty option-chain analyzer (PCR, max pain, OI build-up)
- [ ] Quarterly results calendar
- [ ] Bulk and block deal tracker
- [ ] Promoter holding and pledge tracker
- [ ] IPO analyzer (mainboard and SME)
- [ ] Mutual fund and SIP helper

Want one of these sooner? Open an issue. Pull requests are welcome.

## Documentation

| Guide | For |
|-------|-----|
| [Getting started](docs/getting-started.md) | Installing and your first conversation, plus troubleshooting |
| [Skills reference](docs/skills.md) | What every skill does, example prompts and script options |
| [Architecture](docs/architecture.md) | How skills, scripts and data sources fit together |
| [FAQ](docs/faq.md) | Cost, safety, accuracy and Hindi support |
| [Changelog](CHANGELOG.md) | What changed in each version |

## Contributing

Contributions are welcome: bug reports, new skills, better explanations and translations.
Read [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md), then:

```bash
make check     # sync helper copies, lint, and run offline tests
```

Found a security problem? Please follow [SECURITY.md](SECURITY.md) instead of opening a public issue.

## Credits

Inspired by [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) (MIT).
This project contains no copied code from it; it routes to those skills when they're installed.

## Disclaimer

This project is for **education and research only**. It is not investment advice, not a SEBI-registered
investment adviser or research analyst service, and not a tip or signal service. Market data may be delayed or wrong.
Trading involves risk of loss, and SEBI studies have found that most individual F&O traders lose money.
Check every number before you act, and consult a SEBI-registered adviser for personal advice. Provided under the MIT
License, AS IS, without warranty.
