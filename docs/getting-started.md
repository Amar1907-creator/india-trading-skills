# Getting started

This guide takes about 10 minutes and assumes you've never used Claude Code skills before.

## 1. What you need

| Requirement | How to check | How to get it |
|-------------|--------------|---------------|
| Claude Code (desktop app or terminal) | Open it | [Claude Code docs](https://docs.claude.com/en/docs/claude-code) |
| Python 3.9 or newer | `python3 --version` (Windows: `python --version`) | macOS/Linux usually have it; Windows: [python.org](https://www.python.org/downloads/), and tick "Add to PATH" |
| Internet connection | | Needed for live prices and web search |

You **don't** need an API key, a broker account, or `pip install`.

## 2. Install the skills

**macOS / Linux**

```bash
git clone https://github.com/Amar1907-creator/india-trading-skills.git
cd india-trading-skills
./install.sh
```

**Windows**

1. On the GitHub page, click **Code → Download ZIP** and unzip it.
2. Open `C:\Users\<your-name>\.claude\skills\` (create the `skills` folder if it doesn't exist).
3. Copy every folder from the unzipped `skills\` folder into it.

## 3. First conversation

Open Claude Code and try these, one at a time:

1. `Where do I start with the Indian stock market?` (navigator)
2. `How is the market today?` (market pulse)
3. `Explain Infosys stock in simple words` (stock explainer)
4. `I have ₹50,000. Entry 500, stop-loss 480. How many shares?` (position sizer)
5. `Teach me trading from zero, start lesson 1` (beginner coach)

Claude may ask permission to run a Python script or search the web. Allow it. The scripts only read public prices.

## 4. Updating

```bash
cd india-trading-skills
git pull
./install.sh
```

## 5. Troubleshooting

| Problem | Fix |
|---------|-----|
| `python3: command not found` (Windows) | Use `python`, or reinstall Python with "Add to PATH" ticked |
| "No data for 'XYZ' on NSE or BSE" | Use the exact NSE trading symbol (e.g. `HDFCBANK`, not `HDFC Bank Ltd`). Renamed or demerged companies have new symbols |
| "Could not reach Yahoo Finance" | Check your internet, or try again in a minute |
| Numbers look old | Data can be ~15 minutes delayed. On holidays and weekends you see the last trading day |
| Claude doesn't use the skill | Mention it by name, e.g. "use india-market-pulse" |

Still stuck? [Open an issue](https://github.com/Amar1907-creator/india-trading-skills/issues/new/choose).
