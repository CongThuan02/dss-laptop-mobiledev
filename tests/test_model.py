import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dss import SCENARIOS, Constraints, evaluate, load_laptops, load_laptops_from_text


class ModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_laptops(ROOT / "data" / "raw" / "laptops_simulated.csv")

    def test_simulated_dataset_has_24_unique_rows(self):
        self.assertEqual(len(self.rows), 24)
        self.assertEqual(len({row["laptop_id"] for row in self.rows}), 24)

    def test_weights_sum_to_one(self):
        for scenario in SCENARIOS.values():
            self.assertAlmostEqual(sum(scenario["weights"].values()), 1.0)

    def test_default_filter_and_ranking(self):
        result = evaluate(self.rows, Constraints(), SCENARIOS["balanced"]["weights"])
        self.assertTrue(result["ranked"])
        self.assertEqual([row["rank"] for row in result["ranked"]], list(range(1, len(result["ranked"]) + 1)))
        self.assertTrue(all(0 <= row["score"] <= 1 for row in result["ranked"]))
        self.assertTrue(all(row["price_million_vnd"] <= 40 for row in result["ranked"]))

    def test_ios_requires_macos(self):
        result = evaluate(self.rows, Constraints(target="ios"), SCENARIOS["balanced"]["weights"])
        self.assertTrue(result["ranked"])
        self.assertTrue(all(row["os_platform"] == "macOS" for row in result["ranked"]))

    def test_no_eligible_options_is_handled(self):
        result = evaluate(self.rows, Constraints(max_budget=1), SCENARIOS["balanced"]["weights"])
        self.assertEqual(result["ranked"], [])
        self.assertEqual(len(result["rejected"]), 24)


    def test_load_laptops_from_text_matches_file(self):
        text = (ROOT / "data" / "raw" / "laptops_simulated.csv").read_text(encoding="utf-8-sig")
        rows = load_laptops_from_text(text)
        self.assertEqual(len(rows), len(self.rows))
        self.assertEqual({row["laptop_id"] for row in rows}, {row["laptop_id"] for row in self.rows})

    def test_load_laptops_from_text_rejects_missing_columns(self):
        text = "laptop_id,model,os_platform,price_million_vnd\nX01,Bad,Windows,20\n"
        with self.assertRaises(ValueError):
            load_laptops_from_text(text)

    def test_uploaded_dataset_can_be_ranked(self):
        text = (
            "laptop_id,model,os_platform,price_million_vnd,cpu_score,gpu_score,"
            "ram_gb,ssd_gb,battery_hours,weight_kg\n"
            "U01,MyBook Air,macOS,28.0,7800,4900,16,512,12.0,1.24\n"
            "U02,Gamer Rig,Windows,33.0,9200,8800,32,1024,4.5,2.30\n"
        )
        rows = load_laptops_from_text(text)
        result = evaluate(rows, Constraints(), SCENARIOS["mobility"]["weights"])
        self.assertEqual([row["laptop_id"] for row in result["ranked"]], ["U01", "U02"])


if __name__ == "__main__":
    unittest.main()
