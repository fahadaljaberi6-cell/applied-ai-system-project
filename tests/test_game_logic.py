from logic_utils import check_guess, parse_guess, update_score


# --- check_guess tests ---

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- parse_guess tests ---

def test_parse_valid_guess():
    ok, value, err = parse_guess("50", 1, 100)
    assert ok is True
    assert value == 50
    assert err is None


def test_parse_empty_string():
    ok, value, err = parse_guess("", 1, 100)
    assert ok is False
    assert err == "Enter a guess."


def test_parse_non_number():
    ok, value, err = parse_guess("abc", 1, 100)
    assert ok is False
    assert err == "That is not a number."


def test_parse_out_of_range_high():
    ok, value, err = parse_guess("150", 1, 100)
    assert ok is False
    assert "out of range" in err.lower()


def test_parse_out_of_range_negative():
    ok, value, err = parse_guess("-5", 1, 100)
    assert ok is False
    assert "out of range" in err.lower()


def test_parse_decimal():
    ok, value, err = parse_guess("3.7", 1, 100)
    assert ok is True
    assert value == 3


# --- update_score tests ---

def test_score_on_win():
    score = update_score(0, "Win", 1)
    assert score > 0


def test_score_decreases_on_wrong():
    score = update_score(50, "Too High", 1)
    assert score == 45