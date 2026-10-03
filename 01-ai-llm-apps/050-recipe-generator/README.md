# 🍳 AI Recipe Generator

A smart cooking assistant powered by Google Gemini that creates delicious recipes based on ingredients you already have.

## Features

- **10 Cuisine Options**: Italian, Indian, Mexican, Chinese, Japanese, Thai, French, Mediterranean, American, Middle Eastern
- **Difficulty Levels**: Easy, Medium, Hard
- **Meal Types**: Breakfast, Lunch, Dinner, Snack, Dessert
- **Servings Calculator**: 1-8 servings
- **Dietary Filters**: Vegetarian, Vegan, Gluten-Free, Dairy-Free, Keto, Low-Carb
- **Structured Output**: Prep time, cook time, ingredients, step-by-step instructions, chef's tips

## Installation

```bash
pip install -r requirements.txt
```

## Setup

1. Get a Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Set the environment variable:
   ```bash
   export GEMINI_API_KEY="your-api-key"  # Linux/Mac
   set GEMINI_API_KEY="your-api-key"     # Windows
   ```

## Usage

```bash
streamlit run app.py
```

## How It Works

1. Select your cuisine preference (or "Any" for surprises)
2. Choose difficulty level
3. Pick meal type
4. Adjust servings
5. Add dietary restrictions (optional)
6. Enter your available ingredients
7. Click "Generate Recipe" for a complete recipe

## Example Ingredients

```
chicken, garlic, lemon, olive oil, rosemary, potatoes
```

```
eggs, flour, sugar, butter, vanilla, chocolate chips
```

```
tofu, soy sauce, ginger, sesame oil, broccoli, rice
```

## Tech Stack

- Streamlit - Web UI framework
- Google Gemini - AI recipe generation

## Tips for Best Results

- Be specific with ingredients (e.g., "chicken breast" not just "chicken")
- Include herbs and spices for more creative outputs
- The more ingredients, the more options the AI has to work with
