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

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
