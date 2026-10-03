# Magic 8-Ball

A mystical fortune-telling experience in your terminal! Ask any yes/no question and receive wisdom from the oracle.

## Features

- **Mystical ASCII Art** - Beautiful 8-ball visualization
- **Shake Animation** - Animated effect when the ball is "shaking"
- **24 Different Responses** - Mix of positive, negative, neutral, and mystical answers
- **Colored Terminal Output** - Using colorama for vibrant visuals
- **Easy to Use** - Simple CLI interface

## Installation

```bash
# Install colorama for colored output
pip install colorama

# Or run without colorama (will use fallback colors)
python magic-8ball.py
```

## Usage

```bash
python magic-8ball.py
```

Then simply type your yes/no question and press Enter!

### Commands
- `quit` or `exit` - End the program
- Any yes/no question - Get your fortune revealed!

## Sample Responses

**Positive:**
- "It is certain"
- "Yes, definitely"
- "Signs point to yes"

**Negative:**
- "My reply is no"
- "Don't count on it"
- "Very doubtful"

**Mystical:**
- "The spirits whisper... yes"
- "The void gazes back... and grins"

## Example Session

```
    > Should I take that job?
    
    ✨ Concentrate on your question... ✨
    
    [ SHAKING! ]
    
    💫 The spirits are channeling... 💫
    
    ┌──────────────────────────────────────────────────┐
    │  The spirits whisper... yes                       │
    └──────────────────────────────────────────────────┘
    
    ✨ The stars align in your favor! ✨
```

## Requirements

- Python 3.6+
- colorama (optional, for colored output)

## License

MIT License - Feel free to modify and share!
