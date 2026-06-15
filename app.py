import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score, is_duplicate_guess

# FIX: Initialize session state variables early to track state changes
def initialize_session_state():
    """Initialize or reset session state variables."""
    if "last_difficulty" not in st.session_state:
        st.session_state.last_difficulty = None
    if "input_key" not in st.session_state:
        st.session_state.input_key = 0
    if "last_outcome" not in st.session_state:
        st.session_state.last_outcome = None
    if "last_message" not in st.session_state:
        st.session_state.last_message = None
    if "last_invalid_message" not in st.session_state:
        st.session_state.last_invalid_message = None
    if "last_duplicate_message" not in st.session_state:
        st.session_state.last_duplicate_message = None

#UI
st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

initialize_session_state()

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# FIX #13: Start attempts at 0, not 1 (off-by-one error)
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# FIX: Initialize win/loss message state
if "show_win_message" not in st.session_state:
    st.session_state.show_win_message = False
if "win_message" not in st.session_state:
    st.session_state.win_message = None
if "show_loss_message" not in st.session_state:
    st.session_state.show_loss_message = False
if "loss_message" not in st.session_state:
    st.session_state.loss_message = None
if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

st.subheader("Make a guess")

# FIX #6: Show dynamic difficulty range instead of hardcoded 1-100
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# FIX #17: Use dynamic key to clear input on new game or difficulty change
raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}_{st.session_state.input_key}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX #23: Detect difficulty changes mid-game and reset
if st.session_state.last_difficulty != difficulty:
    st.session_state.last_difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.input_key += 1  # FIX #17, #23: Clear input on difficulty change
    st.session_state.last_outcome = None  # FIX: Clear hint on difficulty change
    st.session_state.last_message = None
    st.session_state.last_invalid_message = None
    st.session_state.last_duplicate_message = None
    st.session_state.show_win_message = False  # FIX: Clear win message on difficulty change
    st.session_state.win_message = None
    st.session_state.show_loss_message = False  # FIX: Clear loss message on difficulty change
    st.session_state.loss_message = None
    st.info(f"Difficulty changed! New game started with range {low} to {high}.")
    st.rerun()  # NEW FIX: Force rerun to immediately show new game state

if new_game:
    # FIX #5: Use get_range_for_difficulty instead of hardcoded 1-100
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.input_key += 1  # FIX #17: Clear input on new game
    st.session_state.last_outcome = None  # FIX: Clear hint on new game
    st.session_state.last_message = None
    st.session_state.last_invalid_message = None
    st.session_state.last_duplicate_message = None
    st.session_state.show_win_message = False  # FIX: Clear win message on new game
    st.session_state.win_message = None
    st.session_state.show_loss_message = False  # FIX: Clear loss message on new game
    st.session_state.loss_message = None
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won" and submit:
        st.success("You already won. Start a new game to play again.")
    elif st.session_state.status == "won" and not st.session_state.show_win_message:
        st.success("You already won. Start a new game to play again.")
    elif st.session_state.status == "lost" and not st.session_state.show_loss_message:
        st.error("Game over. Start a new game to try again.")
    # Don't call st.stop() - let the message display logic below handle it

if submit and st.session_state.status == "playing":
    # FIX #7: Pass low/high range to parse_guess for validation
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        # FIX #8, #9: Don't add invalid guesses to history
        st.session_state.last_invalid_message = err
        st.session_state.last_duplicate_message = None
        st.session_state.last_outcome = None  # FIX: Clear hint on invalid guess
        st.session_state.last_message = None
    else:
        if is_duplicate_guess(guess_int, st.session_state.history):
            st.session_state.last_duplicate_message = f"You already guessed {guess_int}. Try a different number."
            st.session_state.last_invalid_message = None
            st.session_state.last_outcome = None
            st.session_state.last_message = None
        else:
            st.session_state.last_duplicate_message = None
            st.session_state.attempts += 1

            # FIX #9: Only add valid guesses to history (consistent data type)
            st.session_state.history.append(guess_int)
            st.session_state.last_invalid_message = None

            # FIX #2: Remove even/odd type conversion - use clean integer comparison
            outcome, message = check_guess(guess_int, st.session_state.secret)
        
            # FIX: Store hint in session state so it persists across reruns
            st.session_state.last_outcome = outcome
            st.session_state.last_message = message

            st.session_state.score = update_score(
                current_score=st.session_state.score,
                outcome=outcome,
                attempt_number=st.session_state.attempts,
            )

            if outcome == "Win":
                st.session_state.status = "won"
                st.session_state.show_win_message = True
                st.session_state.show_balloons = True
                st.session_state.win_message = (
                    f"You won! The secret was {st.session_state.secret}. "
                    f"Final score: {st.session_state.score}"
                )
            else:
                # FIX #13: Check if attempts >= limit (not > limit) for correct boundary
                if st.session_state.attempts >= attempt_limit:
                    st.session_state.status = "lost"
                    st.session_state.show_loss_message = True
                    st.session_state.loss_message = (
                        f"Out of attempts! "
                        f"The secret was {st.session_state.secret}. "
                        f"Score: {st.session_state.score}"
                    )
    
    # FIX #23: Clear input after successful submission
    st.session_state.input_key += 1
    st.rerun()

# FIX: Display invalid input warning outside submit block so it persists across reruns
if st.session_state.last_invalid_message:
    st.warning(st.session_state.last_invalid_message)

# FIX: Display duplicate guess warning outside submit block so it persists across reruns
if st.session_state.last_duplicate_message:
    st.warning(st.session_state.last_duplicate_message)

# FIX: Display hint outside submit block so it persists across reruns
if st.session_state.last_outcome and st.session_state.last_message and show_hint:
    st.warning(st.session_state.last_message)

# FIX: Display win/loss messages outside submit block so they persist across reruns
if st.session_state.show_win_message and st.session_state.win_message:
    st.success(st.session_state.win_message)

if st.session_state.show_loss_message and st.session_state.loss_message:
    st.error(st.session_state.loss_message)

if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
# all fixes done using agent mode and verifed manually along with test cases in test_game_logic.py