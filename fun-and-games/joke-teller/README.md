# Joke Teller

Get ready to laugh with random jokes and fun facts! Features standard jokes, programming humor, and surprising facts.

## Features

- **Standard Jokes** - Classic setup/punchline format
- **Programming Jokes** - Tech humor from JokeAPI
- **Fun Facts** - Surprising facts to impress your friends
- **Typewriter Effect** - Jokes appear letter by letter
- **API Integration** - Fetches real jokes from official-joke-api
- **Fallback System** - Works offline with built-in jokes

## Installation

```bash
# Install colorama for colored output
pip install colorama

# Run the program
python joke-teller.py
```

## Usage

```bash
python joke-teller.py
```

### Menu Options

1. **Random Joke** - Classic jokes with setup and punchline
2. **Programming Joke** - Jokes for the tech-savvy
3. **Random Fun Fact** - Surprising facts to learn
4. **Mix it up!** - Random selection of jokes or facts
5. **Quit** - Exit the program

## Sample Output

```
    ┌────────────────────────────────────────────────────┐
    │  😂 JOKE TIME! 😂                                   │
    └────────────────────────────────────────────────────┘

    📢 Why don't scientists trust atoms?
    
    ⏳ Prepare for impact...
    💫

    😆 Because they make up everything!

    🤣😂🤣
```

## API Sources

- **Official Joke API**: `https://official-joke-api.appspot.com/jokes/random`
- **JokeAPI Programming**: `https://v2.jokeapi.dev/joke/Programming`

## Built-in Fallbacks

If API calls fail, the program falls back to 5+ built-in jokes and 20+ fun facts.

## Requirements

- Python 3.6+
- colorama (optional, for colored output)
- internet connection (optional, for live jokes)

## License

MIT License - Share a laugh with your friends!
