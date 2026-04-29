# 🎮 Game Glitch Investigator: Applied AI System

> A number-guessing game extended with a structured reliability testing system, input guardrails, and full observability logging — demonstrating how AI-generated code can be made production-worthy through systematic evaluation.

---

## 🎬 Demo Walkthrough

<!-- TODO: Replace this with your Loom link before submitting -->
🎥 **[Loom Walkthrough — ADD YOUR LINK HERE](https://loom.com)**

---

## 📦 Base Project

This project extends **Game Glitch Investigator** (Module 1).

The original project was an intentionally buggy AI-generated Streamlit number guessing game. The goal was to find and fix five specific bugs introduced by GitHub Copilot — including backwards hints, missing range validation, broken session state resets, invalid input costing attempts, and an off-by-one error in attempt counting. All bugs were identified, fixed, and verified with pytest.

---

## 🧠 What's New in This Version (Module 5 Extensions)

| Feature | What Was Added |
|---|---|
| **Reliability / Test Harness** | `tests/test_suite.py` — 30 predefined test cases with structured pass/fail output and a percentage summary |
| **Logging** | All game decisions (valid guesses, rejections, score changes, wins) are logged to `game.log` via Python's `logging` module |
| **Input Guardrails** | `parse_guess` rejects empty, non-numeric, and out-of-range inputs without costing the player an attempt |
| **Edge Case Coverage** | Boundary values, unknown difficulty strings, late-game score floors, and float truncation are all explicitly tested |

---

## 🏗️ Architecture Overview

```
User Input (Streamlit UI)
        │
        ▼
   app.py (UI layer)
   - Manages session state
   - Renders game UI
   - Handles difficulty settings
        │
        ▼
   logic_utils.py (Logic layer)
   - get_range_for_difficulty()   → range lookup + logging
   - parse_guess()                → input guardrails + logging
   - check_guess()                → win/loss logic + logging
   - update_score()               → scoring + logging
        │
        ├──────► game.log         (audit trail of all game events)
        │
        ▼
   tests/
   ├── test_game_logic.py         (pytest unit tests — 10 cases)
   └── test_suite.py              (reliability harness — 30 cases, formatted report)
```

See [`assets/architecture.svg`](assets/architecture.svg) for the visual diagram.

---

## ⚙️ Setup Instructions

**Requirements:** Python 3.8+, pip

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/applied-ai-system-project.git
cd applied-ai-system-project

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the game
python -m streamlit run app.py

# 5. Run the pytest unit tests
pytest tests/test_game_logic.py -v

# 6. Run the reliability test harness
python tests/test_suite.py
```

---

## 🖥️ Sample Interactions

### Example 1 — Valid guess, correct hint direction
```
Input:  Guess 60 (secret is 42)
Output: "📉 Go LOWER!"
Log:    [INFO] Guess 60 too high (secret 42).
```

### Example 2 — Out-of-range input rejected (no attempt cost)
```
Input:  "150" (Normal mode, range 1-100)
Output: "Number out of range! Guess between 1 and 100."
Log:    [WARNING] Out-of-range guess 150 (allowed 1-100) — rejected without costing an attempt.
Attempts remaining: unchanged
```

### Example 3 — Test harness summary output
```
─── check_guess ───
  [PASS] Exact match returns Win
  [PASS] Guess above secret → Too High
  [PASS] Guess below secret → Too Low
  ...

─────────────────────────────────────────
  RESULTS: 30/30 passed (100%)  ✅
─────────────────────────────────────────
```

---

## 🎨 Design Decisions

**Why a test harness over more pytest tests?**
The existing `test_game_logic.py` covers happy paths well. The test harness adds a *runner* layer — it runs predefined scenarios, formats results for human readability, and exits with a non-zero code on failure. This makes it suitable for CI/CD pipelines, not just local development.

**Why Python's `logging` module instead of print statements?**
Logging to `game.log` creates a persistent audit trail across sessions. It also separates concerns — the UI layer (`app.py`) stays clean while the logic layer records everything it does.

**Trade-off: Debug panel left visible**
The Developer Debug Info expander (showing the secret number) was intentionally kept for this project since it was core to the Module 1 learning experience. In a real deployment it would be removed or gated behind an environment variable.

---

## 🧪 Testing Summary

- **30/30 test harness cases pass** across `check_guess`, `parse_guess`, `update_score`, and `get_range_for_difficulty`
- **10/10 pytest unit tests pass**
- The `update_score` late-game floor (minimum 10 points for a win) was untested in Module 1 — the harness caught and confirmed this behavior
- Testing `get_range_for_difficulty` with an unknown string confirmed silent fallback — a `logger.warning` was added to make this visible

**What didn't work at first:** Copilot's initial fix for the attempt-counting bug missed that `attempts += 1` needed to move below the validation check, not just start at 0. Targeted follow-up prompting fixed it.

---

## 🤔 Reflection & Ethics

See [`model_card.md`](./model_card.md) for the full reflection including:
- System limitations and scoring biases
- Misuse considerations (debug panel exposes secret)
- Detailed AI collaboration log
- Testing surprises

---

## 📁 Project Structure

```
applied-ai-system-project/
├── app.py                    # Streamlit UI
├── logic_utils.py            # Core game logic + logging
├── requirements.txt
├── model_card.md             # Ethics, limitations, AI collaboration
├── README.md
├── tests/
│   ├── test_game_logic.py    # Pytest unit tests (Module 1)
│   └── test_suite.py         # Reliability test harness (Module 5)
├── assets/
│   └── architecture.svg      # System architecture diagram
└── game.log                  # Generated at runtime (gitignored)
```

---

*Built as part of an Applied AI Systems course. The AI that generated the original buggy code still claims it was production-ready.*
