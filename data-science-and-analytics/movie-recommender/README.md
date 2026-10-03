# Movie Recommender CLI

A Python CLI application that recommends movies based on your genre preferences. Features ASCII art display, interactive menus, and a curated embedded dataset.

## Features

- **Genre-based Recommendations**: Select multiple genres and get personalized movie suggestions
- **Rating Filters**: Filter by minimum rating (6.0, 7.0, 8.0, 9.0+)
- **Top Rated List**: View the highest-rated movies in the library
- **Browse by Genre**: Explore movies organized by genre
- **Random Pick**: Get a surprise movie recommendation
- **Library Statistics**: View stats about the movie database
- **ASCII Art UI**: Beautiful terminal interface with colors

## Installation

No external dependencies required! Just ensure you have Python 3.6+ installed.

```bash
# Navigate to the project directory
cd movie-recommender

# Run the application
python movie-recommender.py
```

## Usage

```
╔══════════════════════════════════════════════════════════╗
║     ███╗   ███╗██╗███████╗███████╗██╗ ██████╗ ███╗   ██╗║
║     ████╗ ████║██║██╔════╝██╔════╝██║██╔═══██╗████╗  ██║║
║     ██╔████╔██║██║███████╗███████╗██║██║   ██║██╔██╗ ██║║
║     ██║╚██╔╝██║██║╚════██║╚════██║██║██║   ██║██║╚██╗██║║
║     ██║ ╚═╝ ██║██║███████║███████║██║╚██████╔╝██║ ╚████║║
║     ╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝║
║              M O V I E   R E C O M M E N D E R           ║
╚══════════════════════════════════════════════════════════╝
```

### Menu Options

| Option | Description |
|--------|-------------|
| 1 | Get Recommendations - Select genres and get personalized picks |
| 2 | Show Top Rated - View highest-rated movies |
| 3 | Browse by Genre - Explore movies by category |
| 4 | Random Pick - Get a surprise recommendation |
| 5 | Library Stats - View database statistics |
| 0 | Exit the application |

### Example Session

```
MAIN MENU
════════════════════════════════════════════════════════════

  1. Get Recommendations
  2. Show Top Rated
  3. Browse by Genre
  4. Random Pick
  5. Library Stats
  0. Exit

Enter choice: 1

════════════════════════════════════════════════════════════
║                    SELECT YOUR FAVORITE GENRES            ║
════════════════════════════════════════════════════════════

Available genres:
   1. Action       6. Documentary   11. Romance
   2. Adventure     7. Drama         12. Sci-Fi
   3. Animation     8. Fantasy       13. Thriller
   4. Comedy        9. Horror        14. War
   5. Crime        10. Mystery       15. Western

Enter genre numbers separated by commas (e.g., 1,3,5)
Or press Enter for all genres:

Your choice: 1,2,5

YOUR RECOMMENDATIONS
════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────
1. The Dark Knight (2008)
────────────────────────────────────────────────────────────
Genres: Action | Crime | Drama | Thriller
Director: Christopher Nolan
Runtime: 152 min
Rating: ★★★★★ (9.0/10)

When the menace known as the Joker wreaks havoc and chaos on the people of Gotham...
────────────────────────────────────────────────────────────
```

## Project Structure

```
movie-recommender/
├── movie-recommender.py     # Main application
├── data/
│   └── movies.json         # Embedded movie dataset (30 movies)
├── requirements.txt         # No external dependencies!
└── README.md
```

## Requirements

- Python 3.6 or higher
- No external packages needed

## Dataset

The application includes 30 curated movies spanning various genres and decades:
- Classic films (1972-1994)
- Modern masterpieces (1999-2019)
- Multiple genres: Action, Drama, Sci-Fi, Comedy, and more
- Ratings sourced from popular movie databases

## Customization

To add your own movies, edit `data/movies.json`:

```json
{
  "title": "Your Movie Title",
  "year": 2020,
  "genre": ["Action", "Adventure"],
  "rating": 8.0,
  "director": "Director Name",
  "runtime": 120,
  "description": "Brief movie description..."
}
```
