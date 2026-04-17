# Coding Task Grader with Shortcut Detection

Evaluates frontier coding models (Claude Sonnet) on tasks specifically designed to expose
the gap between **surface correctness** and **actual correctness**.

Each task has two layers:
- **Surface tests** — visible unit tests the model can optimize for
- **Invariant tests** — hidden checks the grader runs after, testing edge cases,
  performance, mutation safety, and semantic correctness

The core finding: Claude Sonnet passes ~80% of tasks on surface tests and drops
to ~45% on invariant checks. In the majority of failures the model produces
confident, wrong output with no uncertainty signal.

---

## Project Structure

```
shortcut-detector/
├── run.py              # CLI entry point
├── tasks/
│   └── __init__.py     # 20 task definitions with surface + invariant tests
├── grader/
│   └── __init__.py     # Model calls, code extraction, test runner
├── dashboard/
│   └── index.html      # Portfolio dashboard (loads results/results.json)
└── results/
    └── results.json    # Generated after running — loaded by dashboard
```

---

## Setup

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your_key_here
```

---

## Usage

**Run all 20 tasks:**
```bash
python run.py
```

**Run a single task:**
```bash
python run.py --task t01
```

**Preview all tasks without calling the API:**
```bash
python run.py --dry-run
```

**Results are saved to** `results/results.json` automatically.

---

## View the Dashboard

After running, open the dashboard in a browser:

```bash
cd dashboard
python -m http.server 8080
# then open http://localhost:8080
```

The dashboard loads `results/results.json` from the parent directory.
If no results file is found, it shows demo data so you can preview the UI.

---

## Failure Categories

| Category | Description |
|---|---|
| `shortcut_solution` | Model satisfies tests by pattern-matching rather than solving the problem |
| `wrong_abstraction` | Model applies a related but incorrect algorithm |
| `hallucinated_constraint` | Model invents requirements not stated in the prompt |

---

## Tasks

| ID | Title | Category | Trap |
|---|---|---|---|
| t01 | Sum of Even Numbers | shortcut_solution | Negative numbers and performance |
| t02 | First Non-Repeating Character | wrong_abstraction | Alphabetical vs positional order |
| t03 | Flatten Nested List | wrong_abstraction | String flattening and input mutation |
| t04 | Valid Parentheses | shortcut_solution | Mixed bracket types and non-bracket chars |
| t05 | Most Frequent Element | hallucinated_constraint | Tie-breaking by smallest not first-seen |
| t06 | Two Sum Indices | shortcut_solution | O(n) requirement on large input |
| t07 | Run-Length Encoding | wrong_abstraction | Round-trip decodability |
| t08 | Binary Search | shortcut_solution | True O(log n) performance check |
| t09 | Count Islands | wrong_abstraction | Diagonal adjacency and grid mutation |
| t10 | Anagram Check | shortcut_solution | Spaces, case, numbers as characters |
| t11 | Longest Common Prefix | wrong_abstraction | Case sensitivity and empty strings |
| t12 | Rotate List K Steps | hallucinated_constraint | k > len and input mutation |
| t13 | Pascal's Triangle Row | shortcut_solution | Symmetry and sum invariants |
| t14 | Decode Ways | wrong_abstraction | Leading zeros and 10/20 edge cases |
| t15 | Merge Intervals | hallucinated_constraint | Unsorted input and mutation |
| t16 | Reverse Words in Sentence | shortcut_solution | Character order within words |
| t17 | Power Function | shortcut_solution | Fast exponentiation requirement |
| t18 | Spiral Matrix | wrong_abstraction | Single-row, single-column, non-square |
| t19 | Longest Increasing Subsequence | wrong_abstraction | Strictly increasing vs non-decreasing |
| t20 | Group Anagrams | hallucinated_constraint | Empty strings and case sensitivity |

---

## Key Finding

The gap between surface and invariant pass rate is largest on tasks with
**underspecified requirements** — cases where the model fills ambiguity
confidently and incorrectly, producing no uncertainty signal.
