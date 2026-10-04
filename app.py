#!/usr/bin/env python3
"""Giao diện web Flask cho DSS lựa chọn laptop."""

from pathlib import Path
import sys

from flask import Flask, render_template, request, send_file, session

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from dss import (  # noqa: E402
    CRITERIA,
    SCENARIOS,
    Constraints,
    evaluate,
    load_laptops,
    load_laptops_from_text,
)

app = Flask(__name__)
# Dùng cho local/demo: giữ dữ liệu người dùng tải lên trong session (không có thông tin nhạy cảm).
app.secret_key = "dss-laptop-hoang-cong-thuan-dev"
DATA_PATH = ROOT / "data" / "raw" / "laptops_simulated.csv"
TEMPLATE_PATH = ROOT / "data" / "template" / "mau_du_lieu_dau_vao.csv"


def number(name: str, default: float) -> float:
    raw = request.form.get(name, str(default)).strip().replace(",", ".")
    return float(raw)


@app.route("/mau-du-lieu")
def download_template():
    return send_file(
        TEMPLATE_PATH,
        as_attachment=True,
        download_name="mau_du_lieu_laptop.csv",
        mimetype="text/csv",
    )


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    scenario_key = request.form.get("scenario", "balanced")
    if scenario_key not in SCENARIOS:
        scenario_key = "balanced"
    target = request.form.get("target", "android")

    if request.method == "POST" and request.form.get("reset_dataset"):
        session.pop("dataset_csv", None)
        session.pop("dataset_name", None)

    dataset_source = session.get("dataset_name")
    uploaded = request.files.get("dataset_file") if request.method == "POST" else None

    try:
        if uploaded and uploaded.filename:
            content = uploaded.stream.read().decode("utf-8-sig")
            rows = load_laptops_from_text(content)
            session["dataset_csv"] = content
            session["dataset_name"] = uploaded.filename
            dataset_source = uploaded.filename
        elif session.get("dataset_csv"):
            rows = load_laptops_from_text(session["dataset_csv"])
        else:
            rows = load_laptops(DATA_PATH)
            dataset_source = None

        constraints = Constraints(
            max_budget=number("max_budget", 40),
            min_ram=number("min_ram", 16),
            min_ssd=number("min_ssd", 512),
            target=target,
        )
        result = evaluate(rows, constraints, SCENARIOS[scenario_key]["weights"])
    except (OSError, ValueError, UnicodeDecodeError) as exc:
        error = str(exc)
        constraints = Constraints()
        result = {"ranked": [], "rejected": [], "ranges": {}}

    return render_template(
        "index.html",
        criteria=CRITERIA,
        scenarios=SCENARIOS,
        selected_scenario=scenario_key,
        target=target,
        constraints=constraints,
        result=result,
        error=error,
        dataset_source=dataset_source,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
