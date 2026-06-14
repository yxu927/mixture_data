#!/usr/bin/env python3
"""Append true tree height and tree length to simulation true-value logs."""

from __future__ import annotations

import argparse
from pathlib import Path

import dendropy


def calc_stats(tree_path: Path) -> dict[str, list[float]]:
    stats = {"treelength": [], "treeheight": []}
    for tree in dendropy.Tree.yield_from_files(files=[str(tree_path)], schema="nexus"):
        stats["treelength"].append(tree.length())
        stats["treeheight"].append(tree.max_distance_from_root())
    return stats


def append_tree_stats(tree_path: Path, true_log_path: Path, overwrite: bool) -> bool:
    if not tree_path.exists():
        raise FileNotFoundError(tree_path)
    if not true_log_path.exists():
        raise FileNotFoundError(true_log_path)

    backup_path = true_log_path.with_suffix(true_log_path.suffix + ".orig")
    if backup_path.exists() and not overwrite:
        return False

    original_text = true_log_path.read_text(encoding="utf-8")
    lines = original_text.splitlines()
    if not lines:
        return False

    header = lines[0].split("\t")
    add_height = "treeheight" not in header
    add_length = "treelength" not in header
    if not add_height and not add_length:
        return False

    stats = calc_stats(tree_path)
    if not stats["treeheight"] or not stats["treelength"]:
        raise ValueError(f"No trees parsed from {tree_path}")

    if not backup_path.exists():
        backup_path.write_text(original_text, encoding="utf-8")

    output_lines = []
    for line_no, line in enumerate(lines):
        parts = line.split("\t")
        if line_no == 0:
            if add_height:
                parts.append("treeheight")
            if add_length:
                parts.append("treelength")
        else:
            if add_height:
                parts.append(str(stats["treeheight"][0]))
            if add_length:
                parts.append(str(stats["treelength"][0]))
        output_lines.append("\t".join(parts))

    true_log_path.write_text("\n".join(output_lines) + "\n", encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("simulation_stratum", type=Path, help="Path such as simulation/short/auto")
    parser.add_argument("--start", type=int, default=0, help="First replicate index")
    parser.add_argument("--stop", type=int, default=100, help="One past the last replicate index")
    parser.add_argument("--overwrite", action="store_true", help="Rewrite even if .orig backups exist")
    args = parser.parse_args()

    data_dir = args.simulation_stratum / "data"
    changed = 0
    for rep in range(args.start, args.stop):
        tree_path = data_dir / f"mixture-{rep}_true_psi.trees"
        true_log_path = data_dir / f"mixture-{rep}_true.log"
        if append_tree_stats(tree_path, true_log_path, args.overwrite):
            changed += 1
    print(f"updated {changed} true-value logs in {data_dir}")


if __name__ == "__main__":
    main()
