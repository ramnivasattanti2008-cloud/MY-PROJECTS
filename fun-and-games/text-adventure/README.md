# Text Adventure Game - Castle Quest

A classic text adventure game where you explore a mysterious castle, collect items, solve puzzles, and find the legendary Royal Crown!

## Features

- **7 Unique Rooms**: Grand Hall, Armory, Library, Courtyard, Dungeon, Treasury, and Castle Gate
- **Secret Chamber**: Hidden room discovered through puzzle solving
- **Multiple Items**: Candle, key, sword, book, torch, crown, and amulet
- **Puzzles**: Locked doors, hidden passages, and item-based progression
- **ASCII Art**: Beautiful terminal UI with colored text and maps
- **Win Condition**: Find the Royal Crown and escape through the castle gate!

## How to Play

```bash
python text-adventure.py
```

## Commands

| Command | Description |
|---------|-------------|
| `look` or `l` | Examine your surroundings |
| `go <dir>` | Move in a direction |
| `n/s/e/w` | Quick movement (north/south/east/west) |
| `examine <item>` | Look at an item closely |
| `take <item>` | Pick up an item |
| `drop <item>` | Drop an item |
| `use <item>` | Use an item |
| `inventory` or `i` | Check your items |
| `map` or `m` | View the castle map |
| `help` | Show help |
| `quit` | Exit the game |

## Game Map

```
                         ┌─────────────────────┐
                         │     CASTLE MAP       │
                         │                     │
    ┌──────────┐    ┌────┴────┐    ┌──────────┐
    │  ARMORY  │────│  HALL   │────│ LIBRARY  │
    └──────────┘    └────┬────┘    └──────────┘
                         │
              ┌──────────┼──────────┐
              │          │          │
        ┌─────┴────┐ ┌───┴───┐ ┌────┴─────┐
        │  DUNGEON │ │COURTYARD│ │TREASURY │
        └──────────┘ └───┬───┘ └──────────┘
                         │
                   ┌─────┴─────┐
                   │   GATE    │
                   └───────────┘
```

## Walkthrough

1. **Start** in the Grand Hall
2. Go **north** to the Armory, take the **key** and **sword**
3. Return **south** to the Hall
4. Go **south** to the Courtyard, then **east** to the Treasury
5. Use the **key** to unlock the Treasury
6. Take the **crown**
7. Go **west** back to Courtyard, then **south** to the Gate
8. **Victory!** You escaped with the Royal Crown!

### Bonus: Secret Chamber

1. After getting the key, go **east** to the Library
2. Use the **key** to enter
3. Take the **book** and read it
4. Go **north** to the Hall, then back **east** to Library
5. Use the **book** to reveal the secret chamber
6. Go **north** to find the **amulet**!

## Items

| Item | Location | Purpose |
|------|----------|---------|
| Candle | Hall | Examine for atmospheric description |
| Key | Armory | Unlocks Library and Treasury |
| Sword | Armory | Part of the adventure |
| Book | Library | Reveals secret chamber |
| Torch | Dungeon | Illuminates the darkness |
| Crown | Treasury | Win condition item |
| Amulet | Secret Chamber | Bonus magical item |

## Tips

- Examine everything - descriptions contain hints
- Some doors require specific items to unlock
- The book reveals a secret passage
- You need the crown to win at the gate

## Requirements

- Python 3.6+
- No external dependencies

## Files

```
text-adventure.py   - Main game file
README.md          - This file
```
