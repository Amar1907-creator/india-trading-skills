"""Offline tests: no network needed. Run with:  python3 -m unittest discover tests"""

import filecmp
import importlib.util
import json
import pathlib
import re
import subprocess
import sys
import unittest
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "shared"))
import india_data as d  # noqa: E402


def load(skill, script):
    path = ROOT / "skills" / skill / "scripts" / script
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(script[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class IndicatorTests(unittest.TestCase):
    def test_sma_and_pct_change(self):
        self.assertEqual(d.sma([1, 2, 3, 4], 2), 3.5)
        self.assertIsNone(d.sma([1, 2], 3))
        self.assertAlmostEqual(d.pct_change([100, 110], 1), 10.0)
        self.assertIsNone(d.pct_change([100], 1))

    def test_rsi_bounds(self):
        self.assertEqual(d.rsi(list(range(1, 30))), 100.0)       # only gains
        self.assertLess(d.rsi(list(range(30, 1, -1))), 1)        # only losses
        flat_up_down = [100 + (1 if i % 2 else -1) for i in range(40)]
        self.assertAlmostEqual(d.rsi(flat_up_down), 50, delta=5)

    def test_atr(self):
        bars = [{"high": 11, "low": 9, "close": 10} for _ in range(20)]
        self.assertAlmostEqual(d.atr(bars), 2.0)

    def test_symbol_mapping(self):
        self.assertEqual(d.to_symbol("reliance"), "RELIANCE.NS")
        self.assertEqual(d.to_symbol("Bank Nifty"), "^NSEBANK")
        self.assertEqual(d.to_symbol("TCS.BO"), "TCS.BO")
        self.assertEqual(d.to_symbol("tata steel"), "TATASTEEL.NS")

    def test_market_status(self):
        ist = d.IST
        self.assertIn("weekend", d.market_status(datetime(2026, 10, 31, 11, 0, tzinfo=ist)))  # Saturday
        self.assertTrue(d.market_status(datetime(2026, 10, 28, 11, 0, tzinfo=ist)).startswith("open"))
        self.assertIn("after", d.market_status(datetime(2026, 10, 28, 16, 0, tzinfo=ist)))


class PositionSizerTests(unittest.TestCase):
    SCRIPT = ROOT / "skills/india-position-sizer/scripts/position_size.py"

    def run_sizer(self, *args):
        res = subprocess.run([sys.executable, str(self.SCRIPT), *args, "--json"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        return json.loads(res.stdout)

    def test_basic_delivery(self):
        out = self.run_sizer("--capital", "100000", "--risk-pct", "1", "--entry", "1200", "--stop", "1150")
        self.assertEqual(out["quantity"], 20)
        self.assertAlmostEqual(out["loss_at_stop_before_charges"], 1000)
        self.assertGreater(out["charges_if_stopped"]["total"], 50)   # STT alone is ₹47

    def test_cash_cap(self):
        out = self.run_sizer("--capital", "10000", "--risk-pct", "2", "--entry", "100", "--stop", "99")
        self.assertEqual(out["quantity"], 100)            # risk allows 200, cash allows 100
        self.assertEqual(out["limited_by"], "cash")

    def test_futures_lots(self):
        out = self.run_sizer("--capital", "2000000", "--entry", "24500", "--stop", "24380",
                             "--product", "futures", "--lot-size", "75")
        self.assertEqual(out["lots"], 2)                  # ₹20,000 / (120 x 75)
        self.assertTrue(any("9 in 10" in w for w in out["warnings"]))

    def test_rejects_bad_input(self):
        res = subprocess.run([sys.executable, str(self.SCRIPT), "--capital", "1000", "--entry", "100", "--stop", "110"],
                             capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)            # short on delivery
        res = subprocess.run([sys.executable, str(self.SCRIPT), "--capital", "1000", "--entry", "100", "--stop", "90",
                              "--product", "options"], capture_output=True, text=True)
        self.assertIn("lot-size", res.stdout)


class SectorTests(unittest.TestCase):
    def test_quadrants(self):
        q = load("india-sector-rotation", "sector_rotation.py").quadrant
        self.assertEqual(q(1, 1), "LEADING")
        self.assertEqual(q(-1, 1), "WEAKENING")
        self.assertEqual(q(1, -1), "IMPROVING")
        self.assertEqual(q(-1, -1), "LAGGING")


class PortfolioTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.mod = load("india-portfolio-review", "portfolio_review.py")
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text):
        path = pathlib.Path(self.tmp.name) / name
        path.write_text(text, encoding="utf-8")
        return str(path)

    def test_loads_broker_style_columns(self):
        path = self.write("h.csv", "Trading Symbol,Qty,Average Price\nTCS,5,\"3,200.50\"\nINFY,0,1500\nBAD,x,1\n")
        # header names with spaces normalise to underscores
        path2 = self.write("z.csv", "tradingsymbol,quantity,average_price\nRELIANCE,10,1400\n")
        h, problems = self.mod.load_holdings(path)
        self.assertEqual([x["input"] for x in h], ["TCS"])      # zero qty dropped, bad number reported
        self.assertAlmostEqual(h[0]["avg_price"], 3200.5)
        self.assertEqual(len(problems), 1)
        self.assertEqual(self.mod.load_holdings(path2)[0][0]["quantity"], 10)

    def test_loads_json(self):
        path = self.write("h.json", json.dumps({"holdings": [{"symbol": "ITC", "qty": 50, "avg_price": 420}]}))
        self.assertEqual(self.mod.load_holdings(path)[0][0]["input"], "ITC")

    def test_review_flags(self):
        def fake_history(symbol, rng="1y", interval="1d"):
            price = {"^NSEI": 100, "BIG.NS": 100, "LOSER.NS": 50}.get(symbol, 100)
            bars = [{"date": str(i), "open": price, "high": price, "low": price, "close": price, "volume": 1}
                    for i in range(250)]
            return {"symbol": symbol, "name": symbol, "bars": bars}
        self.mod.fetch_history = fake_history
        out = self.mod.review([
            {"input": "BIG", "quantity": 100, "avg_price": 100},
            {"input": "LOSER", "quantity": 10, "avg_price": 100},
        ])
        self.assertAlmostEqual(out["total_value"], 10500)
        self.assertAlmostEqual(out["total_pnl"], -500)
        joined = " ".join(out["flags"])
        self.assertIn("BIG.NS is 95.2%", joined)
        self.assertIn("LOSER.NS is 50.0% below", joined)
        self.assertIn("only 2 stocks", joined)

    def test_script_has_no_order_code(self):
        text = (ROOT / "skills/india-portfolio-review/scripts/portfolio_review.py").read_text(encoding="utf-8").lower()
        for word in ("place_order", "placeorder", "cancel_order", "modify_order", "/orders"):
            self.assertNotIn(word, text)


class PulseTests(unittest.TestCase):
    def test_trend_rules(self):
        trend_of = load("india-market-pulse", "market_pulse.py").trend_of
        self.assertEqual(trend_of(list(range(1, 260)))[0], "uptrend")
        self.assertEqual(trend_of(list(range(260, 1, -1)))[0], "downtrend")
        self.assertEqual(trend_of([1] * 10)[0], "not enough history")


class RepoHygieneTests(unittest.TestCase):
    def test_helper_copies_in_sync(self):
        for copy in ROOT.glob("skills/*/scripts/india_data.py"):
            self.assertTrue(filecmp.cmp(ROOT / "shared/india_data.py", copy, shallow=False),
                            f"{copy} is out of date: run python3 scripts/sync_shared.py")

    def test_skill_frontmatter(self):
        skills = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
        self.assertGreaterEqual(len(skills), 7)
        for skill in skills:
            text = (skill / "SKILL.md").read_text(encoding="utf-8")
            m = re.match(r"^---\nname: (.+)\ndescription: (.+)\n---\n", text)
            self.assertIsNotNone(m, f"{skill.name}: bad frontmatter")
            self.assertEqual(m.group(1).strip(), skill.name)
            self.assertLessEqual(len(m.group(2)), 1024, f"{skill.name}: description too long")

    def test_every_skill_forbids_trading(self):
        for skill in (ROOT / "skills").iterdir():
            text = (skill / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("Never place, modify or cancel orders", text,
                          f"{skill.name}: the Rules section must forbid placing orders")

    def test_skills_index_matches_folders(self):
        index = json.loads((ROOT / "skills.json").read_text(encoding="utf-8"))
        names = {s["name"] for s in index["skills"]}
        folders = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}
        self.assertEqual(names, folders, "skills.json is out of date")
        for s in index["skills"]:
            if s["script"]:
                self.assertTrue((ROOT / "skills" / s["name"] / s["script"]).exists(), s)

    def test_referenced_files_exist(self):
        for skill in (ROOT / "skills").iterdir():
            text = (skill / "SKILL.md").read_text(encoding="utf-8")
            for ref in re.findall(r"`((?:references|scripts)/[\w./-]+)`", text):
                self.assertTrue((skill / ref).exists(), f"{skill.name} mentions missing {ref}")
            for ref in re.findall(r"<this-skill-folder>/(scripts/[\w.]+)", text):
                self.assertTrue((skill / ref).exists(), f"{skill.name} mentions missing {ref}")


if __name__ == "__main__":
    unittest.main()
