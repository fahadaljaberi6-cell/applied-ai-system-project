# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

When I first launched the game, there was "Game Glitch Investigator" on the top, under it was "Make a guess". Then in a blue box were the instructions: "Guess a number between 1 and 100. Attempts left: 7". There was a developer debug info dropdown, a text input for guesses, and three buttons: "Submit Guess", "New Game", and "Show Hint". Below the buttons, hints would appear when submitting a guess with the show hint checkbox enabled.

- List at least two concrete bugs you noticed at the start:

  Bug One — Backwards hints: If the secret was 40 and I guessed 39, the hint said "Go LOWER" instead of "Go HIGHER." If I guessed 41, it said "Go HIGHER" instead of "Go LOWER." The hint messages were completely swapped.

  Bug Two — No range validation: Entering a number outside 1–100 (like -5 or 200) didn't show an error. Instead it gave a hint and used up an attempt. It should have displayed "Number out of range" and not cost an attempt.

  Bug Three — Invalid input costs an attempt: Entering text like "abc" correctly showed "That is not a number," but it still used up one of your attempts, which shouldn't happen for bad input.

  Bug Four — New Game button broken: After losing, clicking "New Game" did nothing — the "Game over" message stayed forever. Only a full page refresh actually reset the game. The code never reset the `status` session state variable back to "playing."

  Bug Five — Off-by-one attempt counting: The first valid guess didn't use up an attempt. Only after the second guess did the counter start going down. This was because `attempts` started at 1 instead of 0, and it incremented before checking the guess.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project?

  I used GitHub Copilot in VS Code and Claude (claude.ai) to help identify bugs and plan fixes.

- Give one example of an AI suggestion that was correct:

  I asked Copilot to fix the backwards hints in `check_guess`. It correctly identified that the messages were swapped — when `guess > secret`, the original code said "Go HIGHER!" but it should say "Go LOWER!" Copilot swapped the two messages and I verified the fix by running the game, using the debug panel to see the secret number, and confirming that guessing above the secret now correctly says "Go LOWER."

- Give one example of an AI suggestion that was incorrect or misleading:

  When I first asked Copilot to fix the attempt counting bug, it suggested simply changing the initial value of `attempts` from 1 to 0 but didn't mention that the `attempts += 1` line also needed to move below the validation check. I caught this by testing — entering "abc" still cost an attempt. I then asked Copilot specifically about invalid input costing attempts, and it correctly suggested moving the increment to only happen after a valid guess was confirmed.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

  I used two methods: running `pytest` to check automated tests, and manually playing the game while using the Developer Debug Info panel to see the secret number and attempt count. If both the tests passed and the game behaved correctly during manual play, I considered the bug fixed.

- Describe at least one test you ran and what it showed you:

  I ran `test_guess_too_high` which calls `check_guess(60, 50)` and asserts the outcome is "Too High." Before the fix, this test failed because the original code returned "Too High" with the wrong message. After swapping the hint messages, the test passed, confirming the logic was now correct. I also ran `test_parse_out_of_range_negative` which passes "-5" and confirms it returns an error instead of accepting the guess.

- Did AI help you design or understand any tests?

  Yes, I asked Copilot to generate pytest cases targeting the specific bugs I fixed. It created tests for the hint direction, range validation, and invalid input handling. I reviewed each test to make sure it was actually checking the right thing before running them.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend?

  Streamlit reruns the entire Python script from top to bottom every time the user interacts with the page — clicking a button, typing in a box, anything. This means regular variables reset every time. To keep data between interactions (like the secret number or score), you use `st.session_state`, which is like a persistent dictionary that survives reruns. If you forget to store something in session state, it vanishes the moment the user clicks anything.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse?

  I want to keep using the pattern of writing specific tests for each bug before and after fixing it. Running `pytest` gave me confidence that my fixes actually worked and didn't break other things. It's much faster than manually testing every scenario each time.

- What is one thing you would do differently next time?

  I would fix one bug at a time and commit after each fix instead of trying to fix everything at once. That way if something breaks, I can easily go back to the last working version with git instead of trying to remember what I changed.

- How did this project change the way you think about AI-generated code?

  It taught me that AI-generated code can look correct at first glance but have subtle logic errors that only show up when you actually test it. I now know to always run and test AI-written code carefully rather than trusting it blindly.