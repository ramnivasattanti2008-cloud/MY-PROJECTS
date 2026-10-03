#!/usr/bin/env python3
"""
Git Stats - Display GitHub statistics for any user
Features: Repository list, stars, languages, contribution graph (ASCII)
Uses GitHub's public REST API (no authentication required for basic usage)
"""

import argparse
import requests
import sys
from collections import Counter
from datetime import datetime, timedelta

# Try to import colorama
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = CYAN = MAGENTA = WHITE = RESET = BLUE = ''
    class Style:
        BRIGHT = RESET_ALL = DIM = ''

# GitHub API base URL
GITHUB_API = "https://api.github.com"

# Language colors for ASCII display
LANGUAGE_COLORS = {
    "Python": Fore.YELLOW,
    "JavaScript": Fore.YELLOW,
    "TypeScript": Fore.CYAN,
    "Java": Fore.RED,
    "Go": Fore.CYAN,
    "Rust": Fore.RED,
    "C++": Fore.BLUE,
    "C": Fore.BLUE,
    "Ruby": Fore.RED,
    "PHP": Fore.MAGENTA,
    "Swift": Fore.YELLOW,
    "Kotlin": Fore.MAGENTA,
    "Dart": Fore.CYAN,
    "Shell": Fore.GREEN,
    "HTML": Fore.RED,
    "CSS": Fore.BLUE,
}


def get_user(username: str) -> dict:
    """Fetch user profile from GitHub API."""
    response = requests.get(f"{GITHUB_API}/users/{username}", timeout=10)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def get_user_repos(username: str, per_page: int = 100) -> list:
    """Fetch all repositories for a user."""
    repos = []
    page = 1

    while True:
        params = {"per_page": per_page, "page": page, "sort": "updated"}
        response = requests.get(
            f"{GITHUB_API}/users/{username}/repos",
            params=params,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if not data:
            break

        repos.extend(data)

        if len(data) < per_page:
            break

        page += 1

    return repos


def get_contributions(username: str) -> list:
    """Fetch contribution counts for the past year."""
    # GitHub doesn't provide public API for contributions,
    # so we use the events API as a proxy
    response = requests.get(
        f"{GITHUB_API}/users/{username}/events",
        params={"per_page": 100},
        timeout=10
    )

    if response.status_code != 200:
        return []

    events = response.json()
    contributions = []

    # Group events by date
    event_counts = Counter()
    for event in events:
        if event.get("created_at"):
            date = event["created_at"][:10]
            event_counts[date] += 1

    # Generate last 365 days
    today = datetime.now()
    for i in range(365):
        date = (today - timedelta(days=365-i-1)).strftime("%Y-%m-%d")
        contributions.append({
            "date": date,
            "count": event_counts.get(date, 0)
        })

    return contributions


def format_number(num: int) -> str:
    """Format large numbers with K/M suffix."""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)


def display_profile(user: dict) -> None:
    """Display user profile information."""
    print(f"\n{Fore.CYAN}{'═'*60}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Style.BRIGHT}  {user.get('name', user['login'])}{Style.RESET_ALL}")
    if user.get('name'):
        print(f"{Fore.DIM}  @{user['login']}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═'*60}{Style.RESET_ALL}\n")

    if user.get('bio'):
        print(f"{Fore.WHITE}{user['bio']}{Style.RESET_ALL}\n")

    # Stats row
    stats = [
        ("Repos", user.get('public_repos', 0)),
        ("Gists", user.get('public_gists', 0)),
        ("Followers", user.get('followers', 0)),
        ("Following", user.get('following', 0)),
    ]

    print(f"{Fore.YELLOW}┌{'─'*18}┬{'─'*18}┬{'─'*18}┬{'─'*18}┐{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}│{Style.RESET_ALL}", end="")

    for i, (label, value) in enumerate(stats):
        stat_str = f" {label}: {Fore.GREEN}{format_number(value)}{Style.RESET_ALL} "
        print(f"{stat_str:^18}", end="")
        if i < len(stats) - 1:
            print(f"{Fore.YELLOW}│{Style.RESET_ALL}", end="")

    print(f"{Fore.YELLOW}│{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}└{'─'*18}┴{'─'*18}┴{'─'*18}┴{'─'*18}┘{Style.RESET_ALL}\n")

    if user.get('company'):
        print(f"{Fore.DIM}  Company: {Style.RESET_ALL}{user['company']}")
    if user.get('location'):
        print(f"{Fore.DIM}  Location: {Style.RESET_ALL}{user['location']}")
    if user.get('blog'):
        print(f"{Fore.DIM}  Website: {Style.RESET_ALL}{user['blog']}")
    if user.get('created_at'):
        joined = datetime.strptime(user['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        print(f"{Fore.DIM}  Joined: {Style.RESET_ALL}{joined.strftime('%B %Y')}")


def display_repos(repos: list) -> None:
    """Display repository list."""
    if not repos:
        print(f"{Fore.YELLOW}No public repositories found.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}Top Repositories{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'─'*60}{Style.RESET_ALL}\n")

    # Sort by stars
    repos.sort(key=lambda r: r.get('stargazers_count', 0), reverse=True)

    for i, repo in enumerate(repos[:20], 1):  # Show top 20
        name = repo.get('name', 'Unknown')
        description = repo.get('description') or "No description"
        stars = repo.get('stargazers_count', 0)
        forks = repo.get('forks_count', 0)
        language = repo.get('language') or "Unknown"

        lang_color = LANGUAGE_COLORS.get(language, Fore.WHITE)

        # Truncate description
        if len(description) > 50:
            description = description[:47] + "..."

        print(f"{Fore.GREEN}{i}. {name}{Style.RESET_ALL}")
        print(f"   {Fore.DIM}{description}{Style.RESET_ALL}")
        print(f"   {Fore.YELLOW}★ {format_number(stars)}  {Fore.CYAN}⑂ {forks}  {lang_color}● {language}{Style.RESET_ALL}")
        print()


def display_languages(repos: list) -> None:
    """Display language breakdown."""
    languages = [r.get('language') for r in repos if r.get('language')]

    if not languages:
        print(f"{Fore.YELLOW}No language data found.{Style.RESET_ALL}")
        return

    counter = Counter(languages)
    total = sum(counter.values())

    print(f"\n{Fore.CYAN}{Style.BRIGHT}Languages{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─'*40}{Style.RESET_ALL}\n")

    for lang, count in counter.most_common(10):
        percentage = (count / total) * 100
        lang_color = LANGUAGE_COLORS.get(lang, Fore.WHITE)
        bar_length = int(percentage / 2)
        bar = "█" * bar_length + "░" * (50 - bar_length)

        print(f"{lang_color}● {lang:15} {Fore.WHITE}{percentage:5.1f}% {bar[:30]}{Style.RESET_ALL}")


def display_contribution_graph(contributions: list) -> None:
    """Display ASCII contribution graph."""
    if not contributions:
        print(f"\n{Fore.YELLOW}Contribution data not available.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.GREEN}{Style.BRIGHT}Contribution Activity (Last Year){Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'─'*60}{Style.RESET_ALL}\n")

    # Create weekly grid
    weeks = []
    current_week = []

    for i, contrib in enumerate(contributions):
        current_week.append(contrib['count'])
        if len(current_week) == 7 or i == len(contributions) - 1:
            weeks.append(current_week)
            current_week = []

    # Calculate max for scaling
    max_count = max(max(w) for w in weeks) if weeks else 1

    # Print months header
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    print(f"{Fore.DIM}         ", end="")

    # Print month labels
    month_positions = []
    current_month = None
    for i, week in enumerate(weeks):
        week_date = datetime.strptime(contributions[i*7]['date'], "%Y-%m-%d")
        if week_date.month != current_month:
            month_positions.append(i)
            current_month = week_date.month

    # Simple month display
    print(f"{Fore.WHITE}{' '*3}".join(months[:len(set(c['date'][:7] for c in contributions[:52*7:7]))]))
    print()

    # Print grid
    day_labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    for day in range(7):
        row = f"{Fore.DIM}{day_labels[day]:4} {Style.RESET_ALL}"

        for week in weeks:
            count = week[day] if day < len(week) else 0

            if count == 0:
                row += f"{Fore.DIM}░{Style.RESET_ALL}"
            elif count <= 2:
                row += f"{Fore.GREEN}▓{Style.RESET_ALL}"
            elif count <= 5:
                row += f"{Fore.GREEN}█{Style.RESET_ALL}"
            elif count <= 10:
                row += f"{Fore.GREEN}▓{Style.RESET_ALL}"
            else:
                row += f"{Fore.GREEN}█{Style.RESET_ALL}"

        print(row)

    print()
    print(f"{Fore.DIM}  Less    ", end="")
    print(f"{Fore.GREEN}░░░▓▓███{Style.RESET_ALL}", end="")
    print(f"  {Fore.DIM}More{Style.RESET_ALL}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Git Stats - Display GitHub statistics for any user",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  git-stats octocat
  git-stats torvalds --repos
  git-stats gaearon --languages
  git-stats facebook --contributions
        """
    )

    parser.add_argument("username", help="GitHub username")
    parser.add_argument("--repos", action="store_true", help="Show repository list")
    parser.add_argument("--languages", action="store_true", help="Show language breakdown")
    parser.add_argument("--contributions", action="store_true", help="Show contribution graph")
    parser.add_argument("--no-profile", action="store_true", help="Skip profile section")

    args = parser.parse_args()

    try:
        print(f"{Fore.CYAN}Fetching data for @{args.username}...{Style.RESET_ALL}\n")

        # Get user profile
        user = get_user(args.username)
        if not user:
            print(f"{Fore.RED}User not found: {args.username}{Style.RESET_ALL}")
            sys.exit(1)

        # Display profile unless skipped
        if not args.no_profile:
            display_profile(user)

        # Get repos
        repos = get_user_repos(args.username)

        # Default to showing repos if no specific option
        show_repos = args.repos or not (args.languages or args.contributions)
        show_languages = args.languages or not (args.repos or args.contributions)
        show_contributions = args.contributions

        if show_repos:
            display_repos(repos)

        if show_languages:
            display_languages(repos)

        if show_contributions:
            contributions = get_contributions(args.username)
            display_contribution_graph(contributions)

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Network error: {e}{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
