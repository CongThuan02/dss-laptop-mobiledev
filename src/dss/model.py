"""Lõi mô hình: kiểm tra dữ liệu, hard filter, min-max và WSM."""

from __future__ import annotations

import csv
import io
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

CRITERIA = {
    "price_million_vnd": {"label": "Giá", "kind": "cost"},
    "cpu_score": {"label": "CPU", "kind": "benefit"},
    "gpu_score": {"label": "GPU", "kind": "benefit"},
    "ram_gb": {"label": "RAM", "kind": "benefit"},
    "ssd_gb": {"label": "SSD", "kind": "benefit"},
    "battery_hours": {"label": "Pin", "kind": "benefit"},
    "weight_kg": {"label": "Khối lượng", "kind": "cost"},
}

SCENARIOS = {
    "balanced": {
        "label": "Lập trình mobile cân bằng",
        "weights": dict(zip(CRITERIA, [0.20, 0.20, 0.08, 0.18, 0.10, 0.14, 0.10])),
    },
    "performance": {
        "label": "Ưu tiên hiệu năng",
        "weights": dict(zip(CRITERIA, [0.10, 0.28, 0.12, 0.25, 0.12, 0.08, 0.05])),
    },
    "budget": {
        "label": "Ưu tiên tiết kiệm",
        "weights": dict(zip(CRITERIA, [0.40, 0.15, 0.05, 0.15, 0.10, 0.08, 0.07])),
    },
    "mobility": {
        "label": "Ưu tiên di động",
        "weights": dict(zip(CRITERIA, [0.15, 0.15, 0.05, 0.10, 0.05, 0.30, 0.20])),
    },
}

NUMERIC_COLUMNS = tuple(CRITERIA)
REQUIRED_COLUMNS = ("laptop_id", "model", "os_platform", *NUMERIC_COLUMNS)
PLATFORMS = {"Windows", "macOS", "Linux"}
TARGETS = {"android", "ios", "cross_platform"}


@dataclass(frozen=True)
class Constraints:
    max_budget: float = 40.0
    min_ram: float = 16.0
    min_ssd: float = 512.0
    target: str = "android"

    def validate(self) -> None:
        if not all(math.isfinite(v) and v > 0 for v in (self.max_budget, self.min_ram, self.min_ssd)):
            raise ValueError("Ngân sách, RAM và SSD phải là số dương hữu hạn")
        if self.target not in TARGETS:
            raise ValueError(f"Mục tiêu không hợp lệ: {self.target}")


def _read_rows(reader: csv.DictReader) -> list[dict]:
    fields = reader.fieldnames or []
    missing = [column for column in REQUIRED_COLUMNS if column not in fields]
    if missing:
        raise ValueError(f"Thiếu cột dữ liệu: {', '.join(missing)}")
    raw_rows = list(reader)
    if not raw_rows:
        raise ValueError("Tập dữ liệu rỗng")

    rows: list[dict] = []
    ids: set[str] = set()
    for line_no, raw in enumerate(raw_rows, start=2):
        laptop_id = raw["laptop_id"].strip()
        if not laptop_id or laptop_id in ids:
            raise ValueError(f"ID rỗng hoặc trùng tại dòng {line_no}: {laptop_id!r}")
        if raw["os_platform"] not in PLATFORMS:
            raise ValueError(f"Nền tảng không hợp lệ tại dòng {line_no}")
        row = dict(raw)
        for column in NUMERIC_COLUMNS:
            try:
                row[column] = float(raw[column])
            except ValueError as exc:
                raise ValueError(f"Dữ liệu không phải số tại dòng {line_no}, cột {column}") from exc
            if not math.isfinite(row[column]) or row[column] <= 0:
                raise ValueError(f"Dữ liệu phải là số dương hữu hạn tại dòng {line_no}, cột {column}")
        ids.add(laptop_id)
        rows.append(row)
    return rows


def load_laptops(path: str | Path) -> list[dict]:
    """Đọc và kiểm tra CSV từ file; trả về giá trị số đã chuyển kiểu."""
    path = Path(path)
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return _read_rows(csv.DictReader(handle))


def load_laptops_from_text(text: str) -> list[dict]:
    """Đọc và kiểm tra CSV từ nội dung text, ví dụ file người dùng tải lên."""
    if text.startswith("\ufeff"):
        text = text[1:]
    return _read_rows(csv.DictReader(io.StringIO(text)))


def validate_weights(weights: dict[str, float]) -> None:
    if set(weights) != set(CRITERIA):
        raise ValueError("Bộ trọng số phải chứa đúng bảy tiêu chí")
    if any(not math.isfinite(value) or value < 0 for value in weights.values()):
        raise ValueError("Trọng số phải hữu hạn và không âm")
    if not math.isclose(sum(weights.values()), 1.0, rel_tol=0.0, abs_tol=1e-9):
        raise ValueError("Tổng trọng số phải bằng 1")


def filter_reasons(row: dict, constraints: Constraints) -> list[str]:
    reasons: list[str] = []
    if row["price_million_vnd"] > constraints.max_budget:
        reasons.append(f"giá {row['price_million_vnd']:g} > {constraints.max_budget:g} triệu")
    if row["ram_gb"] < constraints.min_ram:
        reasons.append(f"RAM {row['ram_gb']:g} < {constraints.min_ram:g} GB")
    if row["ssd_gb"] < constraints.min_ssd:
        reasons.append(f"SSD {row['ssd_gb']:g} < {constraints.min_ssd:g} GB")
    if constraints.target in {"ios", "cross_platform"} and row["os_platform"] != "macOS":
        reasons.append("iOS/Xcode cục bộ yêu cầu macOS")
    return reasons


def _ranges(rows: Iterable[dict]) -> dict[str, tuple[float, float]]:
    row_list = list(rows)
    return {
        criterion: (
            min(row[criterion] for row in row_list),
            max(row[criterion] for row in row_list),
        )
        for criterion in CRITERIA
    }


def evaluate(rows: list[dict], constraints: Constraints, weights: dict[str, float]) -> dict:
    """Chạy toàn bộ pipeline và trả về kết quả có thể tuần tự hóa JSON."""
    constraints.validate()
    validate_weights(weights)

    eligible: list[dict] = []
    rejected: list[dict] = []
    for source in rows:
        reasons = filter_reasons(source, constraints)
        if reasons:
            rejected.append({"laptop_id": source["laptop_id"], "model": source["model"], "reasons": reasons})
        else:
            eligible.append(dict(source))
    if not eligible:
        return {"ranked": [], "rejected": rejected, "ranges": {}, "constraints": constraints.__dict__}

    ranges = _ranges(eligible)
    for row in eligible:
        normalized: dict[str, float] = {}
        contributions: dict[str, float] = {}
        for criterion, meta in CRITERIA.items():
            low, high = ranges[criterion]
            if math.isclose(low, high, rel_tol=0.0, abs_tol=1e-15):
                value = 1.0
            elif meta["kind"] == "benefit":
                value = (row[criterion] - low) / (high - low)
            else:
                value = (high - row[criterion]) / (high - low)
            normalized[criterion] = value
            contributions[criterion] = weights[criterion] * value
        row["normalized"] = normalized
        row["contributions"] = contributions
        row["score"] = sum(contributions.values())

    eligible.sort(key=lambda row: (-row["score"], row["price_million_vnd"], -row["cpu_score"], row["laptop_id"]))
    for rank, row in enumerate(eligible, start=1):
        row["rank"] = rank
    serializable_ranges = {key: {"min": low, "max": high} for key, (low, high) in ranges.items()}
    return {
        "ranked": eligible,
        "rejected": rejected,
        "ranges": serializable_ranges,
        "constraints": constraints.__dict__,
        "weights": weights,
    }
