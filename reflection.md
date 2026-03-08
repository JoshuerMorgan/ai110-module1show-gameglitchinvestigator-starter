# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

I first read the instructions to understand what the game was about and tried playing it. I noticed the following:

- The logic was wrong; it kept saying "go lower" even when negative numbers were entered.
- It allowed the input of negative numbers.
- It automatically said "go lower" and did not register the first input submission.
- The "New Game" button did not clear previous inputs to start fresh.



---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?  
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---
I used Claude as my teammate. The input was not registering as submitted on the first attempt, and the AI suggested that I check whether the session state `attempt` was set to `0` instead of `1`.


## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---
I manually checked whether the bugs were fixed, then ran tests using `pytest` to check for any oversights. The AI also alerted me to refactor a function called `check_guess`.


## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

Next time, I will review the code more carefully on my own first so I can gain a deeper understanding of it, rather than just an overview, and better guide the AI in assisting me.