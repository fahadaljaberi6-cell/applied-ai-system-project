"""
test_suite.py — Reliability Test Harness for Game Glitch Investigator
Runs predefined inputs through core logic and prints a structured pass/fail report.
This satisfies the "Test Harness / Evaluation Script" stretch feature requirement.
"""

import sys
import os
# Ensure UTF-8 output on Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty

RESET  = "\033[0m"
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"

results = []

def run_test(name, actual, expected, field=None):
    """Run a single assertion and record the result."""
    value = actual[field] if field is not None else actual
    passed = value == expected
    results.append({"name": name, "passed": passed, "got": value, "expected": expected})
    status = f"{GREEN}PASS{RESET}" if passed else f"{RED}FAIL{RESET}"
    print(f"  [{status}] {name}")
    if not passed:
        print(f"         Expected: {expected!r}  |  Got: {value!r}")
    return passed


# ── SECTION 1: check_guess ────────────────────────────────────────────────────
print(f"\n{BOLD}─── check_guess ───{RESET}")

cases = [
    ("Exact match returns Win",          (50, 50),  "Win",      0),
    ("Guess above secret → Too High",    (60, 50),  "Too High", 0),
    ("Guess below secret → Too Low",     (40, 50),  "Too Low",  0),
    ("Boundary: guess == high → Win",    (100,100), "Win",      0),
    ("Boundary: guess 1 below → Too Low",(49, 50),  "Too Low",  0),
]
for name, args, expected, idx in cases:
    outcome, _ = check_guess(*args)
    run_test(name, (outcome, _), expected, field=0)


# ── SECTION 2: parse_guess ────────────────────────────────────────────────────
print(f"\n{BOLD}─── parse_guess ───{RESET}")

parse_cases = [
    # (name, raw, low, high, expected_ok, expected_value, expected_err_fragment)
    ("Valid integer in range",      "50",  1, 100, True,  50,   None),
    ("Valid lower boundary",        "1",   1, 100, True,  1,    None),
    ("Valid upper boundary",        "100", 1, 100, True,  100,  None),
    ("Float rounds to int",         "3.7", 1, 100, True,  3,    None),
    ("Empty string rejected",       "",    1, 100, False, None, "Enter a guess."),
    ("Letters rejected",            "abc", 1, 100, False, None, "That is not a number."),
    ("Negative out of range",       "-5",  1, 100, False, None, "out of range"),
    ("Too high out of range",       "150", 1, 100, False, None, "out of range"),
    ("Boundary+1 rejected",         "101", 1, 100, False, None, "out of range"),
    ("Easy mode valid guess",       "15",  1, 20,  True,  15,   None),
    ("Easy mode out of range",      "25",  1, 20,  False, None, "out of range"),
]
for name, raw, low, high, exp_ok, exp_val, exp_err in parse_cases:
    ok, val, err = parse_guess(raw, low, high)
    run_test(f"{name} — ok={exp_ok}", ok, exp_ok)
    if exp_ok:
        run_test(f"{name} — value={exp_val}", val, exp_val)
    else:
        got_err = (err or "").lower()
        passed = exp_err.lower() in got_err
        results.append({"name": f"{name} — error msg", "passed": passed, "got": err, "expected": f"contains '{exp_err}'"})
        status = f"{GREEN}PASS{RESET}" if passed else f"{RED}FAIL{RESET}"
        print(f"  [{status}] {name} — error msg")
        if not passed:
            print(f"         Expected to contain: {exp_err!r}  |  Got: {err!r}")


# ── SECTION 3: update_score ───────────────────────────────────────────────────
print(f"\n{BOLD}─── update_score ───{RESET}")

score_cases = [
    ("Win on attempt 1 adds points",   (0,  "Win",      1), lambda s: s > 0,   "> 0"),
    ("Win on attempt 1 <= 100",        (0,  "Win",      1), lambda s: s <= 100,"<= 100"),
    ("Too High loses 5 points",        (50, "Too High", 3), lambda s: s == 45, "== 45"),
    ("Too Low loses 5 points",         (50, "Too Low",  3), lambda s: s == 45, "== 45"),
    ("Wrong guess deducts 5 from low score", (3, "Too High", 3), lambda s: s == -2, "== -2"),
    ("Win late game floor is 10",      (0,  "Win",     10), lambda s: s >= 10, ">= 10"),
]
for name, args, check_fn, desc in score_cases:
    score = update_score(*args)
    passed = check_fn(score)
    results.append({"name": name, "passed": passed, "got": score, "expected": desc})
    status = f"{GREEN}PASS{RESET}" if passed else f"{RED}FAIL{RESET}"
    print(f"  [{status}] {name}  (got {score}, expected {desc})")


# ── SECTION 4: get_range_for_difficulty ──────────────────────────────────────
print(f"\n{BOLD}─── get_range_for_difficulty ───{RESET}")

diff_cases = [
    ("Easy returns 1-20",   "Easy",   (1, 20)),
    ("Normal returns 1-100","Normal", (1, 100)),
    ("Hard returns 1-50",   "Hard",   (1, 50)),
    ("Unknown → 1-100",     "???",    (1, 100)),
]
for name, diff, expected in diff_cases:
    result = get_range_for_difficulty(diff)
    run_test(name, result, expected)


# ── SUMMARY ───────────────────────────────────────────────────────────────────
total  = len(results)
passed = sum(1 for r in results if r["passed"])
failed = total - passed
pct    = round(100 * passed / total) if total else 0

print(f"\n{BOLD}─────────────────────────────────────────{RESET}")
print(f"{BOLD}  RESULTS: {passed}/{total} passed ({pct}%)  {'✅' if failed == 0 else '⚠️'}{RESET}")
if failed:
    print(f"{RED}  {failed} test(s) failed:{RESET}")
    for r in results:
        if not r["passed"]:
            print(f"    • {r['name']}")
print(f"{BOLD}─────────────────────────────────────────{RESET}\n")

sys.exit(0 if failed == 0 else 1)
