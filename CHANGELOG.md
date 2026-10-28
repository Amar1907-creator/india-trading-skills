# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed
- `india-market-pulse`: fetch named sources for today's news (Google News, last 24 hours), FII/DII
  (Groww + Trendlyne, cross-checked) and GIFT Nifty (NiftyTrader + INDmoney) instead of broad web searches, which
  returned stale pages

### Added
- Every skill now forbids placing, modifying or cancelling orders, even when a broker connector is connected (enforced by a test)
- Contributor docs, code of conduct, security policy, issue and PR templates
- `docs/` folder: getting started, skills reference, architecture, FAQ
- `skills.json` machine-readable skills index
- `Makefile`, `.editorconfig`, ruff lint in CI, Dependabot for GitHub Actions

## [1.0.0] - 2026-10-28

### Added
- `india-trading-navigator`: start-here router, including the US tradermonty skills
- `india-market-pulse`: Nifty, Bank Nifty, Sensex, midcaps, smallcaps, India VIX and global cues with a HEALTHY / MIXED / WEAK mood
- `india-stock-explainer`: price snapshot vs Nifty plus sourced fundamentals research
- `india-position-sizer`: shares and lots with Indian charges, reward:risk and an ATR check
- `india-news-impact`: market-moving news ranked by impact with a sector playbook
- `india-sector-rotation`: 16 indices labelled LEADING / IMPROVING / WEAKENING / LAGGING
- `beginner-trading-coach`: glossary, 4-week learning path and safety lessons
- Standard-library-only data helper, offline tests, CI on Linux, macOS and Windows

[Unreleased]: https://github.com/Amar1907-creator/india-trading-skills/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Amar1907-creator/india-trading-skills/releases/tag/v1.0.0
