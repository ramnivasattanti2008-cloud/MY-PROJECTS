# Git Stats

A command-line tool to display GitHub statistics for any user. Shows repositories, stars, languages, and an ASCII contribution graph.

## Features

- **User profile**: Name, bio, location, join date, follower counts
- **Repository list**: Top repos sorted by stars with descriptions
- **Language breakdown**: Visual bar chart of most used languages
- **Contribution graph**: ASCII art representation of yearly activity
- **No authentication required**: Uses GitHub's public API

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python git-stats.py octocat
```

### Show Only Repositories
```bash
python git-stats.py torvalds --repos
```

### Show Only Languages
```bash
python git-stats.py gaearon --languages
```

### Show Contribution Graph
```bash
python git-stats.py facebook --contributions
```

### Skip Profile Section
```bash
python git-stats.py microsoft --no-profile --repos
```

## Options

| Flag | Description |
|------|-------------|
| `--repos` | Show repository list |
| `--languages` | Show language breakdown |
| `--contributions` | Show contribution graph |
| `--no-profile` | Skip profile section |

## Output Sections

### Profile
Displays user information including:
- Name and username
- Bio
- Public repositories, gists, followers, following

### Repositories
Shows top 20 repositories sorted by star count with:
- Repository name
- Description
- Stars, forks, language

### Languages
Visual breakdown of programming languages used:
- Percentage per language
- ASCII bar chart

### Contributions
ASCII grid showing activity levels:
- 365 days of contribution data
- 5-level intensity scale (░▓█)

## API Rate Limits

This tool uses GitHub's public API:
- **60 requests per hour** for unauthenticated requests
- Some features may require additional API calls

## Examples

```bash
# View your own stats
python git-stats.py your-username

# Check out popular developers
python git-stats.py torvalds
python git-stats.py gaearon
python git-stats.py kentcdodds

# Compare organizations
python git-stats.py microsoft --repos
python git-stats.py google --languages
```
