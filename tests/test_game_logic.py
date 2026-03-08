import sys
from unittest.mock import MagicMock

# Mock streamlit before any app import so top-level st calls don't fail
if "streamlit" not in sys.modules:
    st_mock = MagicMock()
    st_mock.sidebar.selectbox.return_value = "Normal"
    st_mock.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
    sys.modules["streamlit"] = st_mock

from app import parse_guess, check_guess, update_score


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# ---------------------------------------------------------------------------
# New Game button + Submit button tests
# ---------------------------------------------------------------------------


def fresh_state(secret=50):
    return {
        "attempts": 0,
        "secret": secret,
        "score": 0,
        "status": "playing",
        "history": [],
        "input_counter": 0,
    }


def do_new_game(state: dict, new_secret=50) -> dict:
    """Mirrors the new_game button block in app.py."""
    state["attempts"] = 0
    state["secret"] = new_secret
    state["status"] = "playing"
    state["history"] = []
    state["score"] = 0
    state["input_counter"] = state.get("input_counter", 0) + 1
    return state


def do_submit(state: dict, raw_guess: str, attempt_limit: int = 8):
    """Mirrors the submit button block in app.py. Returns (state, outcome, error)."""
    state["attempts"] += 1
    ok, guess_int, err = parse_guess(raw_guess)
    if not ok:
        state["history"].append(raw_guess)
        return state, None, err
    state["history"].append(guess_int)
    secret = str(state["secret"]) if state["attempts"] % 2 == 0 else state["secret"]
    outcome, _ = check_guess(guess_int, secret)
    state["score"] = update_score(state["score"], outcome, state["attempts"])
    if outcome == "Win":
        state["status"] = "won"
    elif state["attempts"] >= attempt_limit:
        state["status"] = "lost"
    return state, outcome, None


# --- New Game button ---

def test_new_game_resets_attempts():
    state = fresh_state()
    state["attempts"] = 5
    state = do_new_game(state)
    assert state["attempts"] == 0


def test_new_game_resets_score():
    state = fresh_state()
    state["score"] = 75
    state = do_new_game(state)
    assert state["score"] == 0


def test_new_game_resets_status_to_playing():
    state = fresh_state()
    state["status"] = "won"
    state = do_new_game(state)
    assert state["status"] == "playing"


def test_new_game_clears_history():
    state = fresh_state()
    state["history"] = [10, 20, 30]
    state = do_new_game(state)
    assert state["history"] == []


def test_new_game_increments_input_counter():
    state = fresh_state()
    state["input_counter"] = 3
    state = do_new_game(state)
    assert state["input_counter"] == 4


def test_new_game_after_won_allows_playing():
    state = fresh_state()
    state["status"] = "won"
    state["attempts"] = 3
    state = do_new_game(state, new_secret=50)
    assert state["status"] == "playing"
    state, outcome, err = do_submit(state, "50")
    assert err is None
    assert outcome == "Win"
    assert state["status"] == "won"


def test_new_game_after_lost_allows_playing():
    state = fresh_state()
    state["status"] = "lost"
    state["attempts"] = 8
    state = do_new_game(state, new_secret=50)
    assert state["status"] == "playing"
    state, outcome, err = do_submit(state, "30")
    assert err is None
    assert outcome == "Too Low"


# --- Submit button ---

def test_submit_increments_attempts():
    state = fresh_state()
    state, _, _ = do_submit(state, "30")
    assert state["attempts"] == 1


def test_submit_correct_guess_wins():
    state = fresh_state(secret=50)
    state, outcome, err = do_submit(state, "50")
    assert err is None
    assert outcome == "Win"
    assert state["status"] == "won"


def test_submit_too_low_outcome():
    state = fresh_state(secret=50)
    state, outcome, _ = do_submit(state, "30")
    assert outcome == "Too Low"


def test_submit_too_high_outcome():
    state = fresh_state(secret=50)
    state, outcome, _ = do_submit(state, "70")
    assert outcome == "Too High"


def test_submit_empty_input_returns_error():
    state = fresh_state()
    state, outcome, err = do_submit(state, "")
    assert err == "Enter a guess."
    assert outcome is None


def test_submit_negative_number_returns_error():
    state = fresh_state()
    state, outcome, err = do_submit(state, "-5")
    assert err == "Please enter a positive number."
    assert outcome is None


def test_submit_non_number_returns_error():
    state = fresh_state()
    state, outcome, err = do_submit(state, "abc")
    assert err == "That is not a number."
    assert outcome is None


def test_submit_valid_guess_added_to_history():
    state = fresh_state(secret=50)
    state, _, _ = do_submit(state, "30")
    assert 30 in state["history"]


def test_submit_invalid_input_added_to_history():
    state = fresh_state()
    do_submit(state, "xyz")
    assert "xyz" in state["history"]


def test_submit_exhausted_attempts_sets_lost():
    state = fresh_state(secret=50)
    state["attempts"] = 7
    state, _, _ = do_submit(state, "30", attempt_limit=8)
    assert state["status"] == "lost"


def test_submit_not_lost_before_limit():
    state = fresh_state(secret=50)
    state["attempts"] = 3
    state, _, _ = do_submit(state, "30", attempt_limit=8)
    assert state["status"] == "playing"
