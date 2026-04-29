"""
logic_utils.py — Core game logic for Game Glitch Investigator
Includes logging for all key decisions and input guardrails.
"""

import logging

# ── Logging setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("game.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Refactored from app.py into logic_utils.py using Copilot Agent mode
    ranges = {
        "Easy":   (1, 20),
        "Normal": (1, 100),
        "Hard":   (1, 50),
    }
    result = ranges.get(difficulty, (1, 100))
    if difficulty not in ranges:
        logger.warning("Unknown difficulty '%s' — defaulting to range 1-100.", difficulty)
    else:
        logger.info("Difficulty set to '%s' — range %d-%d.", difficulty, *result)
    return result


def parse_guess(raw: str, low: int = 1, high: int = 100):
    """
    Parse user input into an int guess.
    Returns: (ok: bool, guess_int: int | None, error_message: str | None)

    Guardrails:
      - Rejects empty input
      - Rejects non-numeric input
      - Rejects out-of-range values (no attempt cost)
    """
    # FIX: Refactored from app.py and added range validation using Copilot
    if raw is None or raw == "":
        logger.warning("Empty input received — rejected without costing an attempt.")
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        logger.warning("Non-numeric input '%s' — rejected without costing an attempt.", raw)
        return False, None, "That is not a number."

    # FIXME: Range check was completely missing in the original code
    # FIX: Added range validation so out-of-range guesses don't cost an attempt
    if value < low or value > high:
        logger.warning(
            "Out-of-range guess %d (allowed %d-%d) — rejected without costing an attempt.",
            value, low, high,
        )
        return False, None, f"Number out of range! Guess between {low} and {high}."

    logger.info("Valid guess parsed: %d (range %d-%d).", value, low, high)
    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).
    outcome: "Win", "Too High", or "Too Low"
    """
    if guess == secret:
        logger.info("Correct guess! Secret was %d.", secret)
        return "Win", "🎉 Correct!"

    # FIXME: Hints were backwards — "Go HIGHER" showed when guess was above secret
    # FIX: Swapped the hint messages so they point the player in the right direction
    if guess > secret:
        logger.info("Guess %d too high (secret %d).", guess, secret)
        return "Too High", "📉 Go LOWER!"
    else:
        logger.info("Guess %d too low (secret %d).", guess, secret)
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        new_score = current_score + points
        logger.info(
            "Win on attempt %d: +%d points — score %d.", attempt_number, points, new_score
        )
        return new_score

    # FIX: Simplified — wrong guesses always lose 5 points
    # Original code inconsistently added 5 on even "Too High" attempts
    if outcome in ("Too High", "Too Low"):
        new_score = current_score - 5
        logger.info("Wrong guess (%s): -5 points — score %d.", outcome, new_score)
        return new_score

    logger.warning("Unknown outcome '%s' — score unchanged.", outcome)
    return current_score
