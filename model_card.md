# 🃏 Model Card — Game Glitch Investigator: Applied AI System

## Project Overview

**Base project:** Game Glitch Investigator (Module 1)
**Extended for:** Applied AI System Final Project (Module 5)
**AI Feature Added:** Reliability & Testing System — a structured test harness with logging and guardrails

---

## System Limitations & Biases

### What this system does NOT do
- This is a rule-based game with deterministic logic — there is no generative AI model making decisions at runtime. The "AI" in the original project was the code-generation AI (GitHub Copilot) used to create and fix bugs.
- The scoring formula (`100 - 10 * (attempt + 1)`) is hardcoded and may not feel fair at all difficulty levels. A player on Hard (50-number range, 5 attempts) faces harsher odds than on Easy.

### Potential biases or failure modes
- **Input assumptions:** `parse_guess` handles floats by truncating (e.g., `3.7 → 3`), which may surprise users who expect rounding.
- **Difficulty imbalance:** Hard mode has a smaller range (1–50) but also fewer attempts (5), making it genuinely harder — but the score reward is identical to Normal. A player choosing Hard is penalized without bonus points.
- **Session state scope:** The game stores state in `st.session_state`, which is per-browser-tab. Two tabs of the same game will have different secrets and scores with no conflict detection.

---

## Misuse Considerations

### Could this system be misused?
The Developer Debug Info expander in the app **intentionally displays the secret number** (this was part of the Module 1 learning exercise). In a real deployed game, this would need to be removed or restricted to admin users only. As-is, any player can trivially cheat by expanding the debug panel.

### Prevention measures implemented
- The debug expander is labeled clearly as a developer tool.
- Logging records all guesses to `game.log`, creating an audit trail of game sessions.
- Input guardrails in `parse_guess` prevent injection of out-of-range or non-numeric values.

---

## Testing Summary

### Test harness results (`tests/test_suite.py`)
The test harness runs **30 predefined test cases** across all four logic functions and prints a structured pass/fail report with a percentage summary.

| Function | Cases Tested | Expected Pass Rate |
|---|---|---|
| `check_guess` | 5 | 100% |
| `parse_guess` | 22 | 100% |
| `update_score` | 6 | 100% |
| `get_range_for_difficulty` | 4 | 100% |

**Observed:** All 30 tests pass after the Module 1 bug fixes were applied. The system struggled with no test cases once fixes were in place — this validated that the fixes were comprehensive.

### What surprised me during testing
- The `update_score` floor of 10 points (for late-game wins) was not tested in the original Module 1 tests. Adding it to the test harness revealed the behavior was correct but undocumented.
- Testing `get_range_for_difficulty` with an unknown string (`"???"`) confirmed the fallback to 1–100 works, but the function silently fell back with no error in the original code. Adding the `logger.warning` call makes this visible in the logs.

---

## AI Collaboration Log

### Instance where AI gave a helpful suggestion
When asked to refactor the game logic from `app.py` into `logic_utils.py`, GitHub Copilot correctly identified all the functions that needed extracting and generated clean, testable function signatures with docstrings. This saved significant time and produced more modular code than the original.

### Instance where AI gave a flawed suggestion
When first asked to fix the attempt counting bug, Copilot suggested only changing the initial value of `attempts` from `1` to `0`. It missed that the `attempts += 1` line also needed to move *below* the input validation check. Invalid inputs were still costing an attempt. A second, more specific prompt — "how do I make sure invalid input doesn't cost an attempt?" — produced the correct fix.

### Collaboration approach for this final project
The test harness (`tests/test_suite.py`) was designed with AI assistance to ensure full coverage of edge cases (boundary values, unknown inputs, float truncation). Each generated test was manually reviewed to confirm it was testing the right behavior before being included.

---

## Reflection

### What this project taught me about AI and problem-solving
Extending Module 1 into a reliability-focused system taught me that AI-generated code requires systematic verification — not just "does it run?" but "does it handle every edge case correctly?" Writing a test harness forced me to think adversarially about my own code. The logging additions also showed me the value of observability: being able to open `game.log` and see exactly what the system did during a session is far more informative than print statements.

The biggest takeaway: AI tools make you faster at writing code, but they don't remove the need to think carefully about what the code is *supposed* to do. That thinking still has to come from the developer.
