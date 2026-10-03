# 🗡️ AI Dungeon

An interactive text adventure game powered by Google Gemini where your choices shape the story. Every decision matters in this AI-driven narrative experience.

## Features

- **7 Genres**: Fantasy Quest, Space Opera, Mystery, Horror, Comedy, Romance, Post-Apocalyptic
- **6 Character Classes**: Warrior, Mage, Rogue, Ranger, Paladin, Bard
- **4 Difficulty Levels**: Easy, Normal, Hard, Permadeath
- **Persistent Stats**: Health, Gold, Level tracking
- **Branching Narrative**: Every choice creates a unique path
- **Dynamic Storytelling**: AI adapts to your actions

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

## How to Play

1. **Create Your Hero**: Choose a name, class, and optionally add a backstory hint
2. **Begin Adventure**: Start your journey into the AI-generated world
3. **Make Choices**: Read the narrative and select your action
4. **Shape the Story**: Your decisions affect stats and future events
5. **Continue or Act**: Choose from suggestions or describe your own action

## Character Classes

| Class | Strengths | Playstyle |
|-------|-----------|-----------|
| Warrior | Combat, Strength | Direct approach |
| Mage | Magic, Knowledge | Strategic casting |
| Rogue | Stealth, Precision | Sneaky and cunning |
| Ranger | Archery, Survival | Balanced outdoors |
| Paladin | Holy Power, Defense | Righteous combat |
| Bard | Charisma, Tricks | Silver tongue |

## Genres

- **Fantasy Quest**: Classic sword-and-sorcery adventure
- **Space Opera**: Sci-fi exploration and conflict
- **Mystery**: Detective and puzzle-solving
- **Horror**: Survival against dark forces
- **Comedy Adventure**: Humorous misadventures
- **Romance**: Love stories with drama
- **Post-Apocalyptic**: Survival in a broken world

## Tips for Best Experience

- Be descriptive in your actions for more interesting responses
- Consider your character's class when making decisions
- Higher difficulties mean lower starting health
- Explore different paths - every playthrough is unique!

## Tech Stack

- Streamlit - Web UI framework
- Google Gemini - AI narrative generation

## Example Gameplay

```
You are Aldric the Brave, a seasoned warrior standing at the gates
of the abandoned castle. Lightning flashes overhead as you contemplate
your next move...

CHOICES:
1. Storm the main entrance
2. Search for a secret passage
3. Set up camp and wait for dawn
```

Your choice determines the story's direction!
