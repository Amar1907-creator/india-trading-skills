---
name: india-news-impact
description: Find today's or this week's market-moving news for India (RBI policy, Union Budget, inflation/GDP data, quarterly results, FII flows, crude oil, rupee, US Fed, government policy, SEBI rules, geopolitics) and explain in simple words which sectors and stocks are affected and why, ranked by impact. Also explains a specific news item the user shares. Use when the user asks "what is the news today", "why is the market falling/rising", "aaj market kyu gira", "how will the RBI decision affect stocks", "budget impact on stocks", or pastes a headline and asks what it means.
---

# India News Impact

News moves prices, but beginners struggle to connect a headline with its effect. This skill makes that link clear and
honest.

## Mode A: "What's the news today?"

1. **Search** for the latest Indian market news (today, or the last 2-3 trading days if it's a weekend or holiday). Use several
   queries, e.g. "Sensex Nifty today", "stock market news India today", "RBI", "FII DII data", "results today NSE".
   Prefer Economic Times, Moneycontrol, Business Standard, Mint, BloombergQuint/NDTV Profit, NSE/BSE/RBI/SEBI
   official sites. **Every item must have a source and date.** Skip anything you can't date.
2. **Check the reaction**: if the india-market-pulse skill is available, run its script to see how indices actually moved.
3. **Rank** the 3-6 items by likely market impact using `references/event-playbook.md`:
   - 🔴 High: moves the whole market (RBI rate decision, Budget, big global shock, major FII selling)
   - 🟠 Medium: moves a sector (crude spike, sector policy, results of a sector leader)
   - 🟡 Low: moves one stock or is mostly noise
4. **Explain each item** in this format:
   - **What happened** (one line, plain words)
   - **Who is affected**: sectors and well-known example companies, with direction (helped / hurt)
   - **Why** (the cause-and-effect chain, e.g. "crude up → OMC costs up → margins down")
   - **Already priced in?** (did the market already react, using Step 2)
5. **Big picture**: 2 lines on what it adds up to for the market mood.
6. Disclaimer.

## Mode B: user shares a headline or article

Do steps 3-4 for that item. If it's from social media or WhatsApp, first **verify it** with a reliable source. If you
can't confirm it, say so clearly. Fake "tips" and rumours are common in Indian trading groups.

## Rules

- Separate **facts** (what happened) from **interpretation** (what it may mean). Use "may", "tends to" and "historically".
- Never claim to know what the market will do next. Never give buy or sell calls.
- Warn about common scams when relevant: "guaranteed return" tips, Telegram or WhatsApp "operators", and fake apps impersonating
  brokers. Only SEBI-registered advisers (check sebi.gov.in) can give paid stock advice.
- Match the user's language (English, Hindi, Hinglish).
