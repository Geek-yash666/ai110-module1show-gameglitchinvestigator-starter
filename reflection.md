# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

### Major Bugs Identified

**Bug 1: Inverted Hint Logic (Misleading Player Guidance)**

- **Expected Behavior**: When a guess is too high (e.g., guess=75, secret=50), the hint should say "Go LOWER" to guide the player toward the correct number.
- **Actual Behavior**: The hint message is inverted. It says "📈 Go HIGHER!" when the guess is too high, and "📉 Go LOWER!" when the guess is too low, exactly backwards. This causes players to move further away from the secret, making the game unwinnable or frustrating. The emoji and text directly contradict the math.

**Bug 2: Chaotic & Inconsistent Scoring System**

- **Expected Behavior**: Scoring should follow consistent logic—players earn points for correct guesses and lose points for wrong guesses in a predictable manner.
- **Actual Behavior**: The scoring uses arbitrary even/odd logic (e.g., "Too High" gives +5 points on even attempts but -5 on odd attempts). Additionally, the formula can result in negative final scores (e.g., -15 after many wrong guesses), and the winning formula `100 - 10 * (attempt_number + 1)` sometimes yields 0 or negative points. Players cannot understand the scoring rule.

**Bug 3: Secret Number Ignores Difficulty Selection (Wrong Range)**

- **Expected Behavior**: Selecting "Easy" should generate a secret between 1-20, "Normal" between 1-100, and "Hard" between 1-500 (or 1-50 as coded, but that's illogical).
- **Actual Behavior**: The secret is always generated as `random.randint(1, 100)` regardless of selected difficulty. Easy difficulty generates secrets up to 100 (not 20), and Hard difficulty generates secrets only up to 50 (not 500+). The difficulty selector has no effect on game difficulty. Even when you click "New Game," it regenerates with hardcoded `random.randint(1, 100)`.

---

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input / Scenario                                                            | Expected Behavior                                                                                          | Actual Behavior                                                                                              | Console Output / Error |
| --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ---------------------- |
| Guess 75 when secret is 50                                                  | Hint shows "Go LOWER" or "📉"                                                                              | Hint shows "📈 Go HIGHER!" (backwards)                                                                       | none                   |
| Guess 30 when secret is 50                                                  | Hint shows "Go HIGHER" or "📈"                                                                             | Hint shows "📉 Go LOWER!" (backwards)                                                                        | none                   |
| Select "Easy" difficulty, start game                                        | Secret is between 1-20                                                                                     | Secret is between 1-100 (ignores Easy setting)                                                               | none                   |
| Select "Hard" difficulty (1-50 range), click "New Game"                     | Secret respects current difficulty range                                                                   | Secret regenerated as `random.randint(1, 100)` (hardcoded, ignores current difficulty)                     | none                   |
| Make 5 wrong guesses in a row                                               | Score should decrease consistently                                                                         | Score alternates +5/-5 based on even/odd attempt number, producing unpredictable totals                      | none                   |
| Guess "-50" (negative number)                                               | Rejected with validation error or message                                                                  | Accepted and silently treated as "Too Low" with no feedback that it's out of range                           | none                   |
| Guess "999999" (extremely large number)                                     | Rejected with range validation error                                                                       | Accepted and silently treated as "Too High" with no feedback about limits                                    | none                   |
| Enter "abc" (invalid text) then click Submit                                | Error message, invalid guess NOT added to history                                                          | Error displays, but raw string "abc" is appended to history (pollutes history with non-numeric values)       | none                   |
| Guess "3.9" (decimal number)                                                | Rejected as invalid or rounded properly                                                                    | Silently truncates to 3 via `int(float("3.9"))`, causing 3.1 and 3.9 to both become 3                      | none                   |
| Enter guess, do NOT change input, click Submit again                        | Guess submitted once, input clears                                                                         | Same guess re-submitted as a new attempt (input box persists, no auto-clear)                                 | none                   |
| Change difficulty mid-game (e.g., Easy to Hard) without clicking "New Game" | Game acknowledges mismatch or resets automatically                                                         | Secret was generated for old difficulty range; new range doesn't match. Secret might be invalid in new range | none                   |
| Type "  42  " (with leading/trailing whitespace)                            | Parsed as 42                                                                                               | Behavior varies across systems; should strip whitespace:`raw.strip()`                                      | none                   |
| Info message at top of game                                                 | Displays "Guess a number between 1 and 20" (for Easy) or "1 and 100" (for Normal) or "1 and 50" (for Hard) | Always displays hardcoded "Guess a number between 1 and 100" regardless of selected difficulty               | none                   |

---

## 2. How did you use AI as a teammate?

**AI Tool Used:** Claude

**Correct AI Suggestion #1: Session State for Persistent UI Messages**

- **What the AI Suggested**: Instead of displaying hints/messages directly inside the `if submit:` block and having them disappear on rerun, store the outcome and message in session state, then render them *outside* the submit block. The AI suggested: "Store hint in session state so it persists across reruns."
- **Why It Was Correct**: Streamlit reruns the entire script on every interaction. Displaying something inside the submit block only shows it once, then the next rerun has `submit=False`. By storing state and rendering outside the submit block, the message stays visible after rerun.
- **How I Verified**: I tested by making a guess—the hint appeared and persisted on the rerun without disappearing. I compared it to the old code where hints vanished immediately.

**Correct AI Suggestion #2: Duplicate Guess Detection Function**

- **What the AI Suggested**: Create a helper function `is_duplicate_guess(guess, history)` in `logic_utils.py` to check if a guess already exists in the history list.
- **Why It Was Correct**: This follows the DRY principle and made the duplicate logic reusable and testable. The function returned a simple boolean, which was clean to test.
- **How I Verified**: I ran the pytest test `test_regression_duplicate_guess_detection` which passed, confirming the function correctly identified duplicates and non-duplicates. I also tested in the game: entering guess 42 twice showed "You already guessed 42" on the second attempt.

**Incorrect/Misleading AI Suggestion #1: Balloons in the Submit Block**

- **What the AI Suggested**: Put `st.balloons()` directly inside the `if outcome == "Win":` block to celebrate immediately.
- **Why It Was Misleading**: Streamlit executes `st.balloons()` during script execution, then immediately reruns. The balloons animation fires on the initial script run (during rerun), not on the *final* rendered page. The user would see the win message but no balloons.
- **How I Verified**: I tested by winning a game—the balloons didn't appear, even though the win message did. I realized the timing issue and moved balloons to session state, rendering them outside the submit block: `if st.session_state.show_balloons: st.balloons()`. This fixed it—balloons now appeared consistently.

**Incorrect/Misleading AI Suggestion #2: Status Gate for Win Messages**

- **What the AI Suggested**: Show the "You already won" message using only the condition `if st.session_state.status == "won" and not st.session_state.show_win_message:`.
- **Why It Was Misleading**: This condition was true during the *first* win render (when `show_win_message` was just set to True, then the page rendered). The gate should have prevented the stale message on first win, but it displayed it anyway, blocking the victory message.
- **How I Verified**: I won a game and saw "You already won. Start a new game..." instead of the victory message with final score. I tested the fix by adding a `submit` check: `if st.session_state.status == "won" and submit:` to distinguish first-win render from later submit clicks. After the fix, the first win showed the victory message, and clicking submit again showed the "already won" message.

---

## 3. Debugging and testing your fixes

**How I Verified Fixes**

1. **Pytest Unit Tests (70 passing tests)**: Created comprehensive test suite covering all 25+ identified bugs:

   - Range validation tests for each difficulty
   - Input parsing tests (decimals, whitespace, special values, negative numbers)
   - Scoring consistency tests (no even/odd penalties)
   - Regression tests (e.g., hints must not be inverted, score never negative)
   - Duplicate guess detection tests
2. **Manual Game Testing**: Played through realistic scenarios:

   - Easy/Normal/Hard difficulties with correct game flow
   - Edge cases: duplicate guesses, invalid inputs, post-game submit clicks
   - UI persistence: hints staying visible, balloons on win, warnings for duplicates
3. **Code Inspection**: Cross-referenced fixes against the 25 bugs documented

**Key Test Results**

**Test 1: Pytest Suite Validation**

```bash
pytest tests/test_game_logic.py -q
======  70 passed in 0.04s  ======
```

This verified all 25+ bug fixes worked correctly. Each test targeted a specific bug:

- `test_too_high_returns_go_lower_message` passed → hints are no longer inverted (FIX #1)
- `test_too_high_consistent_penalty` passed → scoring is no longer chaotic even/odd (FIX #11)
- `test_score_never_goes_below_zero` passed → score floor is 0, never negative (FIX #22)
- `test_hard_difficulty_range` passed → Hard is 1-500, not 1-50 (FIX #3)
- `test_regression_duplicate_guess_detection` passed → duplicates are detected (NEW FIX)

**Test 2: Manual Game - Duplicate Guess Detection**

- **Scenario**: Enter guess 42, then submit 42 again
- **Expected**: "You already guessed 42. Try a different number." warning; no attempt consumed
- **Result**: ✅ Warning appeared; attempts counter stayed the same
- **Bug Found & Fixed During Testing**: Invalid inputs (empty string, "abc") were consuming attempts and showing "Attempts left: -10". Fixed by moving `st.session_state.attempts += 1` to *after* validation, only counting valid/non-duplicate guesses.

**Test 3: Manual Game - Win State Messaging**

- **Scenario**: Win the game, then click submit again
- **Expected First Time**: Victory message with final score + balloons 🎉
- **Expected After**: "You already won. Start a new game to play again."
- **Result**: ✅ Both worked after fixing the status gate with `submit` check

**Test 4: Manual Game - Hint Persistence Across Reruns**

- **Scenario**: Make guess "75" when secret is "50"
- **Expected**: Hint "📉 Go LOWER!" persists on page
- **Result**: ✅ Hint stayed visible (verified session state rendering outside submit block)

**How AI Helped with Testing**

- The AI designed the comprehensive pytest structure, covering 70+ specific edge cases organized into test classes
- The AI explained *why* tests should use specific patterns (e.g., testing boundary values like 1 and 100 for a 1-100 range)

**Bugs Discovered During Manual Testing (Not in Initial Notes)**

| Bug                                   | How Found                                          | Fix Applied                                                 |
| ------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------- |
| Invalid inputs consumed attempts      | Submitted empty string 10x, attempts went negative | Moved attempt counter to valid-guess path only              |
| Hints didn't show after rerun         | Submitted guess, hint disappeared on next render   | Stored in session state, rendered outside submit block      |
| Balloons didn't appear on win         | Won game, saw message but no animation             | Moved to session state, rendered conditionally              |
| Post-game submit did nothing silently | Clicked submit after winning, no feedback          | Added `submit` check to show "already won" message        |
| Duplicate guesses consumed attempts   | Submitted same number twice, both counted          | Added duplicate check and skip before incrementing attempts |

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
