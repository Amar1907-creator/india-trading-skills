---
name: india-sector-rotation
description: Rank 16 NSE sector and market-cap indices (Bank, PSU Bank, IT, Auto, Pharma, FMCG, Metal, Realty, Energy, Infra, Midcap, Smallcap and more) by strength versus Nifty 50, and label each LEADING, IMPROVING, WEAKENING or LAGGING. Then explain why money may be moving between sectors using current news. Use when the user asks "which sector is strong", "sector rotation", "konsa sector chal raha hai", "where is money flowing", "best sectors this month", or wants to know which areas of the Indian market are leading. No API key needed.
---

# India Sector Rotation

Big money rarely moves the whole market at once. It rotates from one sector to another. This skill shows where.

## Step 1: Run

```bash
python3 <this-skill-folder>/scripts/sector_rotation.py
```

(On Windows use `python`.) It takes about 5-10 seconds. Use `--json` for raw numbers.

## Step 2: Find the "why" (web search)

For the top 2 LEADING or IMPROVING sectors and the bottom 2 LAGGING ones, search for recent news that explains the move
(e.g. "Nifty IT rally reason this week"). Cite the source and date. Common drivers in India:

| Driver | Sectors usually helped | Sectors usually hurt |
|--------|------------------------|----------------------|
| RBI rate cut / softer inflation | Banks, NBFCs, Realty, Auto | |
| Weaker rupee | IT, Pharma (exporters) | Oil marketing, importers |
| Higher crude oil | Upstream oil (ONGC, Oil India) | OMCs, Paints, Aviation, Tyres |
| Good monsoon | FMCG, Auto (tractors, 2-wheelers), Agri | |
| Govt capex push / Budget | Infra, Capital goods, PSE, Cement | |
| Strong US tech spending | IT | |
| Global metal prices up / China stimulus | Metal | |

## Step 3: Explain simply

1. **One-line summary**: "IT and Pharma are leading. FMCG, Realty and MNC stocks are lagging."
2. **What the four labels mean** (only the first time with a new user):
   - LEADING: stronger than Nifty for 3 months and still strong. The trend is in its favour.
   - IMPROVING: was weak, but strong this month. Possibly a new leader, not yet proven.
   - WEAKENING: was strong, now slowing. Watch carefully.
   - LAGGING: weaker than Nifty on both. Usually best avoided for new momentum trades.
3. **The why**: the news from Step 2 for the top and bottom sectors.
4. **Midcap and Smallcap**: whether the broader market is joining in (a healthy rally) or only large-caps are moving (a narrow one).
5. **How traders use this**: momentum traders often look for stocks in LEADING or IMPROVING sectors, and long-term
   investors sometimes study LAGGING sectors for value but expect patience. Process, not picks.
6. Disclaimer.

## Rules

- Rotation shows **past** relative strength. It doesn't promise the future.
- "vs Nifty" columns are simple percentage-point differences in returns.
- Don't name stocks to buy. If the user wants stocks within a sector, offer india-stock-explainer for a specific name they choose.
