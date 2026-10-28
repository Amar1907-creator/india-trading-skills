# Contributing to India Trading Skills

Thanks for helping make Indian market research easier and safer for everyone. 🙏
Bug reports, new skills, better explanations, translations and doc fixes are all welcome.

## Ways to contribute

- 🐛 **Report a bug**: [open a bug report](https://github.com/Amar1907-creator/india-trading-skills/issues/new?template=bug_report.yml)
- 💡 **Suggest a feature or skill**: [open a feature request](https://github.com/Amar1907-creator/india-trading-skills/issues/new?template=feature_request.yml)
- 📝 **Improve docs or explanations**: small PRs are great
- 🧩 **Build a new skill**: see "Adding a new skill" below. The [roadmap](README.md#roadmap) lists ideas

## Development setup

You only need Python 3.9+. There are no dependencies.

```bash
git clone https://github.com/Amar1907-creator/india-trading-skills.git
cd india-trading-skills
make test        # offline tests (or: python3 -m unittest discover tests)
make lint        # optional style check, needs ruff (pip install ruff)
make install     # copy skills into ~/.claude/skills to try them in Claude Code
```

## Project layout

```
skills/<skill-name>/
  SKILL.md          # instructions Claude follows (frontmatter: name + description)
  scripts/          # optional Python scripts (standard library only)
  references/       # optional reference docs the skill reads
shared/india_data.py  # canonical data helper, copied into each skill's scripts/
docs/               # user and contributor documentation
skills.json         # machine-readable index of all skills
tests/              # offline unit tests (no network)
```

See [docs/architecture.md](docs/architecture.md) for how the pieces fit together.

## Adding a new skill

1. Create `skills/<your-skill-name>/SKILL.md`. The frontmatter `name` must equal the folder name, and the
   `description` must be at most 1024 characters and say *when* Claude should use the skill.
2. If it needs data, add `scripts/<name>.py` that imports `india_data`, then run `make sync`.
3. Add an entry to `skills.json`, a row to the README skills table, and a section in `docs/skills.md`.
4. Add offline tests in `tests/` (mock or pure-function tests; CI has no market data).
5. Update `CHANGELOG.md` under **Unreleased**.

## Rules every skill must follow

These protect users. PRs that break them won't be merged.

- **No buy/sell calls, targets or guarantees.** Skills explain and educate.
- **Never invent numbers.** Data comes from scripts or cited web sources with dates.
- **No broker logins, order placement or credential handling.** Every SKILL.md must keep the "Never place, modify or cancel orders" rule (a test checks this).
- **No paid API required for the core path.** An optional key-based path is OK if it's clearly marked.
- **Standard library only** in scripts, so beginners never need `pip install`.
- Keep the disclaimer and point to SEBI-registered advisers for personal advice.

## Editing the shared data helper

Edit only `shared/india_data.py`, then run `make sync`. A test fails if the copies drift.

## Pull request checklist

- [ ] `make test` passes
- [ ] `make lint` passes (if you have ruff)
- [ ] Docs, `skills.json` and `CHANGELOG.md` updated if behaviour changed
- [ ] The safety rules above still hold

## Commit messages

Use short, present-tense summaries, e.g. `Add FII/DII flow tracker` or `Fix RSI for short history`.

By contributing you agree that your contributions are licensed under the [MIT License](LICENSE) and that you'll follow
our [Code of Conduct](CODE_OF_CONDUCT.md).
