# Quiz Game

A multi-choice quiz game with multiple categories and difficulty levels. Test your knowledge!

## How to Play

1. **Run the game:**
   ```bash
   python quiz-game.py
   ```

2. **Select a Category:**
   - Science
   - History
   - Geography
   - Technology
   - Sports
   - All Categories (Mixed)

3. **Choose Difficulty:**
   - Easy: 3 questions
   - Medium: 5 questions
   - Hard: 8 questions

4. **Answer Questions:**
   - Read each question carefully
   - Enter 1, 2, 3, or 4 to select your answer
   - See explanations for correct answers

## Features

- **5 Categories** with 8 questions each
- **3 Difficulty Levels** - 3, 5, or 8 questions
- **Score Tracking** - Tracks your performance
- **Explanations** - Learn why each answer is correct
- **Scoreboard** - View your past quiz scores
- **Mixed Mode** - Random questions from all categories

## Categories

| Category | Questions | Topics |
|----------|-----------|--------|
| Science | 8 | Chemistry, Space, Biology, Physics |
| History | 8 | World History, Indian History, Wars |
| Geography | 8 | Capitals, Landforms, Countries |
| Technology | 8 | Computing, Internet, Programming |
| Sports | 8 | Soccer, Olympics, Cricket |

## Game Preview

```
============================================================
              🧠 QUIZ MASTER 🧠
============================================================

  Question 2/5
  ========================================
  What planet is known as the Red Planet?

    1. Venus
    2. Mars
    3. Jupiter
    4. Saturn

  Your answer (1-4): 2

  ========================================
  ✅ CORRECT!

  Correct answer: Mars
  Mars appears red due to iron oxide (rust) on its surface.
```

## Requirements

- Python 3.x (standard library only)
- No external dependencies

## Adding New Questions

To add more questions, edit the `QUIZ_DATA` dictionary in the file:

```python
QUIZ_DATA = {
    "Your Category": [
        {
            "question": "Your question here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": 0,  # Index of correct answer (0-3)
            "explanation": "Why this is correct."
        },
        # Add more questions...
    ],
}
```
