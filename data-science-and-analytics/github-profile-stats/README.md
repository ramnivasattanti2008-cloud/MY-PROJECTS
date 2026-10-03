# GitHub Profile Stats

A Python script that generates visual ASCII art statistics for any GitHub profile. Display commits, repositories, languages, activity, and more in a beautiful terminal format.

## Features

- Profile information display
- Repository statistics with stars and forks
- Language distribution with ASCII bar charts
- Weekly activity visualization
- Contribution tracking
- GitHub streak calculation
- ASCII art banner

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python github-stats.py username
```

### With GitHub Token (for higher rate limits)

```bash
python github-stats.py username --token YOUR_GITHUB_TOKEN
```

### Options

| Option | Description |
|--------|-------------|
| `username` | GitHub username (required) |
| `-t, --token` | GitHub API token for higher rate limits |
| `-r, --repos` | Number of repos to display (default: 10) |
| `--no-events` | Skip event/activity data |
| `-q, --quiet` | Suppress ASCII art banner |

## Examples

```bash
# View your own stats
python github-stats.py octocat

# With more repos shown
python github-stats.py torvalds --repos 20

# Suppress banner for scripting
python github-stats.py microsoft --quiet

# Skip activity data (faster)
python github-stats.py facebook --no-events
```

## Output Sample

```
╔═══════════════════════════════════════════════════════════════════╗
║     ██╗     ██╗   ██╗ ██████╗ ██╗  ██╗████████╗ ██████╗ ██████╗   ║
║     ██║     ██║   ██║██╔════╝ ██╗  ██║╚══██╔══╝██╔═══██╗██╔══██╗  ║
║     ██║     ██║   ██║██║  ███╗███████║   ██║   ██║   ██║██████╔╝  ║
║     ██║     ██║   ██║██║   ██║██╔══██║   ██║   ██║   ██║██╔══██╗  ║
║     ███████╗╚██████╔╝╚██████╔╝██║  ██║   ██║   ╚██████╔╝██║  ██║  ║
║     ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝  ║
╚═══════════════════════════════════════════════════════════════════╝
  @octocat

  ═══════════════════════════════════════════════════════════════════════
  │ PROFILE
  ─────────────────────────────────────────────────────────────────────
  │ Name:        The Octocat
  │ Bio:         GitHub mascot
  │ Company:     @GitHub
  │ Location:    San Francisco, CA
  │ Followers:   25,000
  │ Following:   0
  │ Public Repos: 8
  ═══════════════════════════════════════════════════════════════════════

  ═══════════════════════════════════════════════════════════════════════
  │ LANGUAGES
  ─────────────────────────────────────────────────────────────────────
  │ [===] Shell        ████████████████████████████ 45.5%
  │ <JS>  JavaScript   ████████████████ 30.0%
  │ [##]  Java         ██████ 12.5%
  │ [--]  Other        █████ 11.5%
  ═══════════════════════════════════════════════════════════════════════
```

## Rate Limits

Without a GitHub token:
- 60 requests per hour

With a GitHub token:
- 5,000 requests per hour

Create a token at: https://github.com/settings/tokens (no special scopes needed)

## Requirements

- Python 3.6+
- requests library
