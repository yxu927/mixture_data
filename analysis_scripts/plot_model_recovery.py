#!/usr/bin/env python3
"""Plot clock-model credible-set size and true-model coverage."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


MODEL_COLUMNS = {
    "strict": "D.hierSVS.pStrict",
    "relaxUC": "D.hierSVS.pRelaxUC",
    "relaxAC": "D.hierSVS.pRelaxAC",
}

STRATA = {
    "Strict": ("strict", "strict"),
    "UCLN": ("ucln", "relaxUC"),
    "Autocorrelated": ("auto", "relaxAC"),
}


def parse_stats_log(path: Path) -> dict[str, dict[str, float | str]]:
    rows: dict[str, dict[str, float | str]] = {}
    with path.open(encoding="utf-8") as handle:
        headers = handle.readline().strip().split("\t")[1:]
        for line in handle:
            line = line.strip()
            if not line:
                continue
            items = line.split("\t")
            row_name = items[0]
            parsed: dict[str, float | str] = {}
            for header, value in zip(headers, items[1:]):
                try:
                    parsed[header] = float(value)
                except ValueError:
                    parsed[header] = value
            rows[row_name] = parsed
    return rows


def model_probabilities(stats_path: Path) -> dict[str, float]:
    mean = parse_stats_log(stats_path)["mean"]
    probs = {name: float(mean.get(column, 0.0)) for name, column in MODEL_COLUMNS.items()}
    total = sum(probs.values())
    return {name: value / total for name, value in probs.items()} if total else probs


def credible_set(probs: dict[str, float], alpha: float) -> set[str]:
    ordered = sorted(probs.items(), key=lambda item: item[1], reverse=True)
    selected: set[str] = set()
    cumulative = 0.0
    for name, prob in ordered:
        selected.add(name)
        cumulative += prob
        if cumulative >= alpha:
            break
    return selected


def summarize(simulation_condition: Path, start: int, stop: int, alpha: float):
    coverage_rows = []
    size_rows = []
    for label, (folder_name, true_model) in STRATA.items():
        stats_dir = simulation_condition / folder_name / "stats"
        covered = 0
        total = 0
        size_counts = {1: 0, 2: 0, 3: 0}
        missing = []

        for rep in range(start, stop):
            stats_path = stats_dir / f"mixture-{rep}_stats.log"
            if not stats_path.exists():
                missing.append(rep)
                continue
            probs = model_probabilities(stats_path)
            selected = credible_set(probs, alpha)
            size_counts[len(selected)] += 1
            covered += int(true_model in selected)
            total += 1

        if total == 0:
            raise FileNotFoundError(f"No stats files found in {stats_dir}")

        coverage_rows.append((label, covered / total * 100.0, covered, total, missing))
        size_rows.append((label, size_counts, total))
    return coverage_rows, size_rows


def plot_coverage(rows, output_dir: Path) -> None:
    labels = [row[0] for row in rows]
    pcts = [row[1] for row in rows]
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.clf()
    ax = plt.subplot(111)
    x = np.arange(len(labels))
    ax.vlines(x, 90, pcts, colors="k", lw=1.2, zorder=1)
    ax.plot(x, pcts, "ko", ms=8, zorder=2)
    ax.axhline(95, color="r", linestyle="--", lw=1.2, label="Nominal 95%")
    for xi, pct in zip(x, pcts):
        ax.text(xi, pct + 0.4, f"{pct:.0f}%", ha="center", va="bottom", fontsize=11, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Coverage (%)")
    ax.set_ylim([90, 101])
    ax.set_xlim([-0.5, len(labels) - 0.5])
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    plt.tight_layout()
    output_path = output_dir / "model_coverage_summary.pdf"
    plt.savefig(output_path, bbox_inches="tight")
    print(f"figure saved: {output_path}")


def plot_size_distribution(rows, output_dir: Path) -> None:
    labels = [row[0] for row in rows]
    pct1 = np.array([row[1][1] / row[2] * 100.0 for row in rows])
    pct2 = np.array([row[1][2] / row[2] * 100.0 for row in rows])
    pct3 = np.array([row[1][3] / row[2] * 100.0 for row in rows])

    plt.clf()
    ax = plt.subplot(111)
    x = np.arange(len(labels))
    bar_width = 0.6
    ax.bar(x, pct1, bar_width, label="Size = 1", color="#1f77b4")
    ax.bar(x, pct2, bar_width, bottom=pct1, label="Size = 2", color="#ff7f0e")
    ax.bar(x, pct3, bar_width, bottom=pct1 + pct2, label="Size = 3", color="#b0b0b0")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Replicates (%)")
    ax.set_ylim([0, 100])
    ax.set_yticks(range(0, 101, 25))
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False)
    plt.tight_layout()
    output_path = output_dir / "credible_set_size_distribution.pdf"
    plt.savefig(output_path, bbox_inches="tight")
    print(f"figure saved: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("simulation_condition", type=Path, help="Path such as simulation/short or simulation/long")
    parser.add_argument("--start", type=int, default=0, help="First replicate index")
    parser.add_argument("--stop", type=int, default=100, help="One past the last replicate index")
    parser.add_argument("--alpha", type=float, default=0.95, help="Credible-set mass")
    parser.add_argument("--output-dir", type=Path, default=None, help="Default: <simulation_condition>/figures")
    args = parser.parse_args()

    output_dir = args.output_dir or (args.simulation_condition / "figures")
    plt.rcParams["font.family"] = "Helvetica"
    plt.rc("font", size=12)
    plt.rc("axes", titlesize=12)
    plt.rcParams["figure.dpi"] = 300

    coverage_rows, size_rows = summarize(args.simulation_condition, args.start, args.stop, args.alpha)
    for label, pct, covered, total, missing in coverage_rows:
        print(f"{label}: coverage {pct:.0f}% ({covered}/{total}); missing reps={missing}")

    plt.rcParams["figure.figsize"] = (4, 4)
    plot_coverage(coverage_rows, output_dir)
    plt.rcParams["figure.figsize"] = (5, 4)
    plot_size_distribution(size_rows, output_dir)


if __name__ == "__main__":
    main()
