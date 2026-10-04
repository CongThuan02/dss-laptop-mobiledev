#!/usr/bin/env python3
"""Sinh kết quả baseline và What-if dưới dạng CSV/JSON."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from dss import CRITERIA, SCENARIOS, Constraints, evaluate, load_laptops

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "laptops_simulated.csv"
RESULTS = ROOT / "results"


def write_ranking(path: Path, result: dict) -> None:
    fields = ["rank", "laptop_id", "model", "os_platform", "score", *CRITERIA]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in result["ranked"]:
            writer.writerow({key: f"{row[key]:.6f}" if key == "score" else row[key] for key in fields})


def main() -> None:
    rows = load_laptops(DATA)
    RESULTS.mkdir(parents=True, exist_ok=True)
    summary: dict[str, dict] = {}
    for key, scenario in SCENARIOS.items():
        result = evaluate(rows, Constraints(), scenario["weights"])
        write_ranking(RESULTS / f"ranking_{key}.csv", result)
        summary[key] = {
            "label": scenario["label"],
            "eligible_count": len(result["ranked"]),
            "rejected_count": len(result["rejected"]),
            "top5": [
                {"rank": row["rank"], "id": row["laptop_id"], "model": row["model"], "score": round(row["score"], 6)}
                for row in result["ranked"][:5]
            ],
        }

    for target in ("android", "ios", "cross_platform"):
        result = evaluate(rows, Constraints(target=target), SCENARIOS["balanced"]["weights"])
        summary[f"target_{target}"] = {
            "eligible_count": len(result["ranked"]),
            "rejected_count": len(result["rejected"]),
            "top5": [row["laptop_id"] for row in result["ranked"][:5]],
        }
    reduced = evaluate(rows, Constraints(max_budget=30), SCENARIOS["balanced"]["weights"])
    summary["budget_30"] = {
        "eligible_count": len(reduced["ranked"]),
        "rejected_count": len(reduced["rejected"]),
        "top5": [row["laptop_id"] for row in reduced["ranked"][:5]],
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Đã phân tích {len(rows)} laptop mô phỏng. Kết quả: {RESULTS}")


if __name__ == "__main__":
    main()
