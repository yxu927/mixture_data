#!/usr/bin/env python3
"""Plot posterior coverage for shared continuous simulation parameters."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


PARAMETER_MAP = {
    "psi.height": "treeheight",
    "psi.treeLength": "treelength",
    "clockRate": "clockRate",
}

DISPLAY_NAME = {
    "psi.height": "Tree height",
    "psi.treeLength": "Tree length",
    "clockRate": "Clock rate",
}


def parse_table(path: Path, skip_first_column: bool = False) -> dict[str, dict[str, float | str]]:
    rows: dict[str, dict[str, float | str]] = {}
    with path.open(encoding="utf-8") as handle:
        headers = handle.readline().strip().split("\t")
        if skip_first_column:
            headers = headers[1:]
        for line in handle:
            line = line.strip()
            if not line:
                continue
            items = line.split("\t")
            row_name = items[0]
            values = items[1:] if skip_first_column else items
            parsed: dict[str, float | str] = {}
            for header, value in zip(headers, values):
                try:
                    parsed[header] = float(value)
                except ValueError:
                    parsed[header] = value
            rows[row_name] = parsed
    return rows


def parse_true_values(path: Path) -> dict[str, float | str]:
    with path.open(encoding="utf-8") as handle:
        headers = handle.readline().strip().split("\t")
        values = handle.readline().strip().split("\t")
    result: dict[str, float | str] = {}
    for header, value in zip(headers, values):
        try:
            result[header] = float(value)
        except ValueError:
            result[header] = value
    return result


def plot_figures(stratum_dir: Path, start: int, stop: int, output_dir: Path) -> None:
    stats_dir = stratum_dir / "stats"
    data_dir = stratum_dir / "data"
    output_dir.mkdir(parents=True, exist_ok=True)

    true_rows = []
    mean_rows = []
    lower_rows = []
    upper_rows = []
    ess_rows = []

    for rep in range(start, stop):
        stats_path = stats_dir / f"mixture-{rep}_stats.log"
        true_path = data_dir / f"mixture-{rep}_true.log"
        if not stats_path.exists() or not true_path.exists():
            continue
        stats = parse_table(stats_path, skip_first_column=True)
        true_rows.append(parse_true_values(true_path))
        mean_rows.append(stats["mean"])
        lower_rows.append(stats["HPD95.lower"])
        upper_rows.append(stats["HPD95.upper"])
        ess_rows.append(stats["ESS"])

    if not true_rows:
        raise FileNotFoundError(f"No replicate stats found under {stratum_dir}")

    plt.rcParams["font.family"] = "Helvetica"
    plt.rc("font", size=12)
    plt.rc("axes", titlesize=12)
    plt.rcParams["figure.figsize"] = (3.375, 3.375)
    plt.rcParams["figure.dpi"] = 300

    for estimated_name, true_name in PARAMETER_MAP.items():
        true_values = [float(row[true_name]) for row in true_rows]
        mean_values = [float(row[estimated_name]) for row in mean_rows]
        lowers = [float(row[estimated_name]) for row in lower_rows]
        uppers = [float(row[estimated_name]) for row in upper_rows]
        ess_values = [float(row[estimated_name]) for row in ess_rows]

        covered = [lo <= truth <= up for truth, lo, up in zip(true_values, lowers, uppers)]
        colors = ["c" if value else "r" for value in covered]
        mean_ess = float(np.mean(ess_values))
        coverage_percent = sum(covered) / len(covered) * 100.0

        plt.clf()
        ax = plt.subplot(111)
        ax.plot(true_values, mean_values, "k.", ms=2, zorder=2)
        ax.vlines(true_values, ymin=lowers, ymax=uppers, colors=colors, alpha=0.2, lw=3, zorder=1)

        lo = min(min(true_values), min(lowers))
        hi = max(max(true_values), max(uppers))
        pad = (hi - lo) * 0.05 if hi > lo else 1.0
        ax.plot([lo - pad, hi + pad], [lo - pad, hi + pad], "k-", lw=0.5, zorder=10)
        ax.set_xlim([lo - pad, hi + pad])
        ax.set_ylim([lo - pad, hi + pad])

        label = DISPLAY_NAME.get(estimated_name, estimated_name)
        ax.set_xlabel("True " + label)
        ax.set_ylabel("Estimated " + label)
        ax.set_title(label)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.text(
            0.05,
            0.95,
            f"covg. = {coverage_percent:.0f} %\nmean ESS = {mean_ess:.0f}",
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment="top",
            horizontalalignment="left",
            bbox={"facecolor": "white", "alpha": 0.5},
        )
        plt.tight_layout()

        output_path = output_dir / (estimated_name.lower().replace(".", "_") + ".pdf")
        plt.savefig(output_path)
        print(f"figure saved: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("simulation_stratum", type=Path, help="Path such as simulation/short/auto")
    parser.add_argument("--start", type=int, default=0, help="First replicate index")
    parser.add_argument("--stop", type=int, default=100, help="One past the last replicate index")
    parser.add_argument("--output-dir", type=Path, default=None, help="Default: <simulation_stratum>/figures")
    args = parser.parse_args()

    output_dir = args.output_dir or (args.simulation_stratum / "figures")
    plot_figures(args.simulation_stratum, args.start, args.stop, output_dir)


if __name__ == "__main__":
    main()
