def get_range_for_difficulty(difficulty: str):
    # FIX: Refactored logic into logic_utils.py using agent mode
    """Return (low, high) inclusive range for a given difficulty.
    
    FIX: Corrected Hard difficulty to have a larger range (1-500) instead of 1-50,
    making it actually harder than Normal difficulty.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 500  # FIX: Changed from 1-50 to 1-500 (actually hard now)
    return 1, 100


def parse_guess(raw: str, low: int = None, high: int = None):
    # FIX: Refactored logic into logic_utils.py using agent mode
    """Parse user input into an int guess with optional range validation.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    
    FIX: Added range validation, whitespace stripping, decimal rejection,
    and special float value handling.
    """
    if raw is None:
        return False, None, "Enter a guess."

    # FIX #19: Strip leading/trailing whitespace
    raw = raw.strip()
    
    if raw == "":
        return False, None, "Enter a guess."

    # FIX #18: Reject special float values (inf, -inf, nan)
    if raw.lower() in ["inf", "-inf", "infinity", "-infinity", "nan"]:
        return False, None, "That is not a valid number."

    # FIX #15: Reject decimal inputs instead of truncating
    if "." in raw:
        return False, None, "Please enter a whole number, not a decimal."

    try:
        value = int(raw)
    except ValueError:
        return False, None, "That is not a number."
    except OverflowError:
        # FIX #16: Handle extremely large numbers
        return False, None, "Number is too large. Please enter a reasonable value."

    # FIX #7, #17: Validate range if provided
    if low is not None and high is not None:
        if value < low or value > high:
            return False, None, f"Please guess a number between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    # FIX: Refactored logic into logic_utils.py using agent mode
    """Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    
    FIX: Corrected inverted hint logic and removed fragile type conversion.
    """
    # FIX #2: Ensure both are integers for clean comparison
    guess = int(guess)
    secret = int(secret)
    
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIX #1: Corrected inverted hints
    if guess > secret:
        return "Too High", "📉 Go LOWER!"  # FIX: Was showing "Go HIGHER!" when should go lower
    else:
        return "Too Low", "📈 Go HIGHER!"  # FIX: Was showing "Go LOWER!" when should go higher


def is_duplicate_guess(guess, history):
    """Return True when the guess already exists in the history."""
    if history is None:
        return False
    return guess in history


def update_score(current_score: int, outcome: str, attempt_number: int):
    # FIX: Refactored logic into logic_utils.py using agent mode
    """Update score based on outcome and attempt number.
    
    FIX: Replaced chaotic even/odd logic with consistent, logical scoring.
    - Win: 100 - (5 * (attempts - 1)) capped at minimum 10
    - Wrong guess: -2 points (consistent penalty)
    """
    # FIX #11, #12: Removed arbitrary even/odd logic, using consistent formula
    if outcome == "Win":
        # Award points based on efficiency: fewer attempts = more points
        # Max 100 (won on attempt 1), min 10 (won on attempt 11+)
        points = max(10, 100 - 5 * (attempt_number - 1))
        return current_score + points

    # FIX #11, #12, #22: Both "Too High" and "Too Low" lose consistent points
    # Penalty is -2 per wrong guess (logical and consistent)
    if outcome in ["Too High", "Too Low"]:
        new_score = current_score - 2
        # FIX #22: Ensure score never goes below 0
        return max(0, new_score)

    return current_score
