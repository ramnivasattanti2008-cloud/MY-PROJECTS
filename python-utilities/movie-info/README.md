# Movie Info

A command-line tool to look up movie information including ratings, cast, plot, and more. Uses the OMDB API.

## Features

- **Movie details**: Title, year, runtime, genre, ratings
- **Ratings display**: IMDb, Rotten Tomatoes, Metacritic with color coding
- **Cast information**: Actors list with truncation for long casts
- **Plot**: Full plot synopsis with text wrapping
- **Awards & Box Office**: Oscar wins, nominations, revenue data
- **Search mode**: Find multiple movies matching a title
- **ASCII art header**: Cinematic themed border

## Installation

```bash
pip install -r requirements.txt
```

## Setup

### Get an OMDB API Key

1. Visit [omdbapi.com/apikey.aspx](https://www.omdbapi.com/apikey.aspx)
2. Enter your email and request a free API key
3. Set the environment variable:

**Linux/Mac:**
```bash
export OMDB_API_KEY="your_api_key_here"
```

**Windows (PowerShell):**
```powershell
$env:OMDB_API_KEY="your_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set OMDB_API_KEY=your_api_key_here
```

> Note: The tool includes a demo key with limited requests. For unlimited access, get your own free key.

## Usage

### Basic Movie Lookup
```bash
python movie-info.py "The Matrix"
```

### Full Information
```bash
python movie-info.py "The Matrix" --full
```

### Search for Movies
```bash
python movie-info.py "Star Wars" --search
```

### Search TV Series
```bash
python movie-info.py "Breaking Bad" --type series
```

### Search Episodes
```bash
python movie-info.py "The Simpsons" --type episode
```

## Options

| Flag | Short | Description |
|------|-------|-------------|
| `--full` | `-f` | Show full information |
| `--search` | `-s` | Search mode (multiple results) |
| `--type` | `-t` | Content type: movie, series, episode |
| `--year` | `-y` | Filter by release year |

## Output Sections

### Header
ASCII art movie reel frame with title and year

### Ratings
Color-coded by source:
- **IMDb**: Yellow
- **Rotten Tomatoes**: Green (>60%) or Red (<60%)
- **Metacritic**: Green

### Plot
Wrapped text for readability

### Cast
First 6 actors listed, with count of remaining

## Examples

```bash
# Classic movies
python movie-info.py "Pulp Fiction"
python movie-info.py "The Godfather"
python movie-info.py "Fight Club"

# Recent films
python movie-info.py "Dune: Part Two"
python movie-info.py "Oppenheimer"

# TV Shows
python movie-info.py "Game of Thrones" --type series
python movie-info.py "Succession" --search

# Search for similar titles
python movie-info.py "Batman" --search
```

## Rate Limits

- **Free tier**: 1,000 requests per day
- **Demo key**: Very limited requests
- **Paid tier**: Unlimited requests

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OMDB_API_KEY` | Your OMDB API key |
