#!/usr/bin/env python3
"""
run.py
CLI entry point. Runs all 20 tasks, prints live progress,
saves results to results/results.json, and prints a summary table.

Usage:
    python run.py              # run all tasks
    python run.py --task t01   # run a single task by id
    python run.py --dry-run    # print tasks without calling the API
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from tasks import ALL_TASKS
from grader import grade_all, grade_task


CATEGORY_COLORS = {
    "shortcut_solution":    "\033[93m",  # yellow
    "wrong_abstraction":    "\033[94m",  # blue
    "hallucinated_constraint": "\033[95m",  # magenta
}
RESET = "\033[0m"
GREEN = "\033[92m"
RED   = "\033[91m"


def fmt_pass(passed: bool) -> str:
    if passed:
        return f"{GREEN}PASS{RESET}"
    return f"{RED}FAIL{RESET}"


def progress(i, total, result):
    surface = fmt_pass(result.surface_pass)
    invariant = fmt_pass(result.invariant_pass)
    cat_color = CATEGORY_COLORS.get(result.failure_category, "")
    cat = f"{cat_color}{result.failure_category}{RESET}"
    print(f"  [{result.id}] {result.title:<35} surface={surface}  invariant={invariant}  ({cat})")


def print_summary(results):
    total = len(results)
    surface_n = sum(r.surface_pass for r in results)
    invariant_n = sum(r.invariant_pass for r in results)
    gap_cases = [r for r in results if r.surface_pass and not r.invariant_pass]

    print()
    print("=" * 65)
    print("  SUMMARY")
    print("=" * 65)
    print(f"  Total tasks:            {total}")
    print(f"  Surface tests passed:   {surface_n}/{total}  ({100*surface_n//total}%)")
    print(f"  Invariant tests passed: {invariant_n}/{total}  ({100*invariant_n//total}%)")
    print(f"  Gap (surface✓, inv✗):   {len(gap_cases)} tasks")
    print()

    if gap_cases:
        by_cat: dict[str, list] = {}
        for r in gap_cases:
            by_cat.setdefault(r.failure_category, []).append(r)

        print("  Tasks that fooled surface tests but failed invariant checks:")
        for cat, items in sorted(by_cat.items()):
            color = CATEGORY_COLORS.get(cat, "")
            print(f"\n    {color}[{cat}]{RESET}")
            for r in items:
                print(f"      {r.id} — {r.title}")
                print(f"             {r.description}")

    print()


def save_results(results, path="results/results.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = []
    for r in results:
        data.append({
            "id": r.id,
            "title": r.title,
            "failure_category": r.failure_category,
            "description": r.description,
            "surface_pass": r.surface_pass,
            "invariant_pass": r.invariant_pass,
            "surface_error": r.surface_error,
            "invariant_error": r.invariant_error,
            "model_code": r.model_code,
        })
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  Results saved to {path}")


def dry_run():
    print(f"\n{len(ALL_TASKS)} tasks loaded:\n")
    for t in ALL_TASKS:
        cat_color = CATEGORY_COLORS.get(t.failure_category, "")
        print(f"  [{t.id}] {t.title}")
        print(f"         Category: {cat_color}{t.failure_category}{RESET}")
        print(f"         Trap:     {t.description}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Coding Task Grader with Shortcut Detection")
    parser.add_argument("--task", help="Run a single task by id (e.g. t01)")
    parser.add_argument("--dry-run", action="store_true", help="Print tasks without calling API")
    parser.add_argument("--output", default="results/results.json", help="Output path for results JSON")
    args = parser.parse_args()

    if args.dry_run:
        dry_run()
        return

    # if not os.environ.get("ANTHROPIC_API_KEY"):
    #     print("Error: ANTHROPIC_API_KEY environment variable not set.")
    #     sys.exit(1)
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)
    if args.task:
        tasks = [t for t in ALL_TASKS if t.id == args.task]
        if not tasks:
            print(f"Task '{args.task}' not found. Available: {[t.id for t in ALL_TASKS]}")
            sys.exit(1)
    else:
        tasks = ALL_TASKS

    # print(f"\nRunning {len(tasks)} task(s) against claude-sonnet-4-5\n")
    print(f"\nRunning {len(tasks)} task(s) against gemini-2.0-flash\n")
    start = time.time()

    results = grade_all(tasks, progress_callback=progress)

    elapsed = time.time() - start
    print(f"\n  Completed in {elapsed:.1f}s")

    print_summary(results)
    save_results(results, args.output)


if __name__ == "__main__":
    main()
