#!/usr/bin/env python3
"""
GitHub Profile Stats
Generate visual ASCII art statistics for a GitHub profile.
"""

import requests
import argparse
import sys
import datetime
from typing import Dict, List, Optional
import time


class GitHubStats:
    """GitHub profile statistics generator."""

    API_BASE = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.session = requests.Session()
        if token:
            self.session.headers.update({
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            })
        else:
            self.session.headers.update({
                "Accept": "application/vnd.github.v3+json"
            })

    def get_user(self, username: str) -> Dict:
        """Get user profile information."""
        response = self.session.get(f"{self.API_BASE}/users/{username}")
        response.raise_for_status()
        return response.json()

    def get_repos(self, username: str, per_page: int = 100) -> List[Dict]:
        """Get user repositories."""
        repos = []
        page = 1

        while True:
            response = self.session.get(
                f"{self.API_BASE}/users/{username}/repos",
                params={"per_page": per_page, "page": page, "sort": "pushed"}
            )
            response.raise_for_status()
            data = response.json()

            if not data:
                break

            repos.extend(data)

            if len(data) < per_page:
                break

            page += 1
            time.sleep(0.5)  # Rate limiting

        return repos

    def get_events(self, username: str) -> List[Dict]:
        """Get user events (for activity stats)."""
        events = []
        page = 1

        while True:
            response = self.session.get(
                f"{self.API_BASE}/users/{username}/events",
                params={"per_page": 100, "page": page}
            )
            response.raise_for_status()
            data = response.json()

            if not data:
                break

            events.extend(data)

            if len(data) < 100:
                break

            page += 1
            time.sleep(0.5)

        return events

    def get_contributions(self, username: str) -> Dict:
        """Get contribution stats."""
        try:
            # Get events to analyze contributions
            events = self.get_events(username)

            contributions = {
                "commits": 0,
                "prs": 0,
                "issues": 0,
                "reviews": 0,
                "stars": 0,
                "forks": 0
            }

            for event in events:
                event_type = event.get("type", "")
                if event_type == "PushEvent":
                    contributions["commits"] += len(event.get("payload", {}).get("commits", []))
                elif event_type == "PullRequestEvent":
                    contributions["prs"] += 1
                elif event_type == "IssuesEvent":
                    contributions["issues"] += 1
                elif event_type == "PullRequestReviewEvent":
                    contributions["reviews"] += 1
                elif event_type == "WatchEvent":
                    contributions["stars"] += 1
                elif event_type == "ForkEvent":
                    contributions["forks"] += 1

            return contributions

        except Exception as e:
            return {
                "commits": 0,
                "prs": 0,
                "issues": 0,
                "reviews": 0,
                "stars": 0,
                "forks": 0
            }

    def get_language_stats(self, repos: List[Dict]) -> Dict[str, int]:
        """Get language statistics from repositories."""
        languages = {}

        for repo in repos:
            lang = repo.get("language")
            if lang:
                languages[lang] = languages.get(lang, 0) + 1

        return dict(sorted(languages.items(), key=lambda x: x[1], reverse=True))

    def get_most_active_days(self, events: List[Dict]) -> Dict[str, int]:
        """Get most active days of the week."""
        days = {
            "Monday": 0, "Tuesday": 0, "Wednesday": 0,
            "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0
        }

        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday",
                     "Friday", "Saturday", "Sunday"]

        for event in events:
            created_at = event.get("created_at", "")
            if created_at:
                try:
                    dt = datetime.datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    day = day_names[dt.weekday()]
                    days[day] += 1
                except:
                    pass

        return days


def print_banner(username: str) -> None:
    """Print ASCII art banner."""
    banner = f"""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║     ██╗     ██╗   ██╗ ██████╗ ██╗  ██╗████████╗ ██████╗ ██████╗   ║
    ║     ██║     ██║   ██║██╔════╝ ██╗  ██║╚══██╔══╝██╔═══██╗██╔══██╗  ║
    ║     ██║     ██║   ██║██║  ███╗███████║   ██║   ██║   ██║██████╔╝  ║
    ║     ██║     ██║   ██║██║   ██║██╔══██║   ██║   ██║   ██║██╔══██╗  ║
    ║     ███████╗╚██████╔╝╚██████╔╝██║  ██║   ██║   ╚██████╔╝██║  ██║  ║
    ║     ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝  ║
    ║                                                                   ║
    ║                    Profile Statistics                              ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print(f"  @{username}")
    print()


def print_profile(user: Dict) -> None:
    """Print profile information."""
    name = user.get("name") or user.get("login")
    bio = user.get("bio") or ""
    company = user.get("company") or ""
    location = user.get("location") or ""
    blog = user.get("blog") or ""
    twitter = user.get("twitter_username") or ""
    followers = user.get("followers", 0)
    following = user.get("following", 0)
    public_repos = user.get("public_repos", 0)

    created_at = user.get("created_at", "")
    if created_at:
        try:
            dt = datetime.datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            created_at = dt.strftime("%B %d, %Y")
        except:
            pass

    print("  " + "═" * 68)
    print("  │ PROFILE")
    print("  " + "─" * 68)

    if name:
        print(f"  │ Name:        {name}")

    if bio:
        # Wrap bio if too long
        bio_lines = [bio[i:i+50] for i in range(0, len(bio), 50)]
        for i, line in enumerate(bio_lines):
            prefix = "  │ Bio:         " if i == 0 else "  │              "
            print(f"{prefix}{line}")

    if company:
        print(f"  │ Company:     {company}")
    if location:
        print(f"  │ Location:    {location}")
    if blog:
        print(f"  │ Website:     {blog}")
    if twitter:
        print(f"  │ Twitter:     @{twitter}")

    print(f"  │")
    print(f"  │ Followers:   {followers:,}")
    print(f"  │ Following:   {following:,}")
    print(f"  │ Public Repos: {public_repos}")
    print(f"  │ Member Since: {created_at}")
    print("  " + "═" * 68)
    print()


def print_stats(stats: Dict) -> None:
    """Print contribution statistics."""
    print("  " + "═" * 68)
    print("  │ ACTIVITY")
    print("  " + "─" * 68)
    print(f"  │ Commits:     {stats.get('commits', 0):,}")
    print(f"  │ Pull Requests: {stats.get('prs', 0):,}")
    print(f"  │ Issues:      {stats.get('issues', 0):,}")
    print(f"  │ Reviews:     {stats.get('reviews', 0):,}")
    print(f"  │ Stars Given:  {stats.get('stars', 0):,}")
    print(f"  │ Forks:       {stats.get('forks', 0):,}")
    print("  " + "═" * 68)
    print()


def print_repos(repos: List[Dict], limit: int = 10) -> None:
    """Print top repositories."""
    print("  " + "═" * 68)
    print("  │ TOP REPOSITORIES")
    print("  " + "─" * 68)

    # Sort by stars
    sorted_repos = sorted(repos, key=lambda x: x.get("stargazers_count", 0), reverse=True)

    for i, repo in enumerate(sorted_repos[:limit], 1):
        name = repo.get("name", "")
        description = repo.get("description") or "No description"
        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)
        language = repo.get("language") or ""

        # Truncate description
        if len(description) > 50:
            description = description[:47] + "..."

        print(f"  │ {i}. {name}")
        print(f"  │    {description}")
        print(f"  │    Stars: {stars:,} | Forks: {forks:,}" + (f" | {language}" if language else ""))
        print()

    print("  " + "═" * 68)
    print()


def print_languages(languages: Dict[str, int], repos: List[Dict]) -> None:
    """Print language statistics with ASCII bar chart."""
    print("  " + "═" * 68)
    print("  │ LANGUAGES")
    print("  " + "─" * 68)

    if not languages:
        print("  │ No language data available")
    else:
        total = sum(languages.values())
        max_lang_name = max(len(name) for name in languages.keys())

        # Color mapping for common languages (using ASCII art, no colors)
        color_icons = {
            "Python": "[===]",
            "JavaScript": "<JS>",
            "TypeScript": "<TS>",
            "Java": "[##]",
            "C++": "[C+]",
            "C": "[C]",
            "C#": "<C#>",
            "Ruby": "<R>",
            "Go": "[Go]",
            "Rust": "[Rs]",
            "Swift": "[Sw]",
            "Kotlin": "[Kt]",
            "PHP": "[PHP]",
            "HTML": "<HT>",
            "CSS": "<CS>",
        }

        for lang, count in list(languages.items())[:10]:
            percentage = (count / total) * 100
            bar_length = int(percentage / 2)
            bar = "█" * bar_length
            icon = color_icons.get(lang, "[--]")
            print(f"  │ {icon} {lang:<{max_lang_name}} {bar} {percentage:.1f}%")

    print("  " + "═" * 68)
    print()


def print_activity_chart(days: Dict[str, int]) -> None:
    """Print ASCII activity chart."""
    print("  " + "═" * 68)
    print("  │ WEEKLY ACTIVITY")
    print("  " + "─" * 68)

    max_activity = max(days.values()) if days.values() else 1

    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    day_full = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Print header
    print("  │", end="")
    for day in day_names:
        print(f" {day:^6}", end="")
    print()
    print("  │" + "─" * 49)

    # Print bars
    print("  │", end="")
    for day in day_full:
        count = days.get(day, 0)
        if max_activity > 0:
            height = int((count / max_activity) * 4)
        else:
            height = 0

        # Create mini bar
        bar = ""
        for h in range(4, 0, -1):
            if height >= h:
                bar += "█"
            else:
                bar += " "
        print(f" {bar:^6}", end="")
    print()

    # Print counts
    print("  │", end="")
    for day in day_full:
        count = days.get(day, 0)
        print(f" {count:^6}", end="")
    print()

    print("  " + "═" * 68)
    print()


def print_streak(events: List[Dict]) -> None:
    """Calculate and print contribution streak."""
    if not events:
        print("  │ Contribution Streak: N/A")
        return

    # Get unique dates
    dates = set()
    for event in events:
        created_at = event.get("created_at", "")
        if created_at:
            try:
                dt = datetime.datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                dates.add(dt.date())
            except:
                pass

    if not dates:
        print("  │ Contribution Streak: N/A")
        return

    sorted_dates = sorted(dates, reverse=True)

    # Calculate current streak
    today = datetime.date.today()
    streak = 0

    check_date = today
    while check_date in dates:
        streak += 1
        check_date -= datetime.timedelta(days=1)

    # If no activity today, check yesterday
    if streak == 0:
        check_date = today - datetime.timedelta(days=1)
        while check_date in dates:
            streak += 1
            check_date -= datetime.timedelta(days=1)

    print(f"  │ Current Streak: {streak} day{'s' if streak != 1 else ''}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate GitHub profile statistics in ASCII art",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s username
  %(prog)s username --token YOUR_GITHUB_TOKEN
  %(prog)s octocat --repos 20
        """
    )

    parser.add_argument("username", help="GitHub username")
    parser.add_argument("-t", "--token", help="GitHub API token for higher rate limits")
    parser.add_argument("-r", "--repos", type=int, default=10,
                        help="Number of repos to display (default: 10)")
    parser.add_argument("--no-events", action="store_true",
                        help="Skip event/activity data")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Suppress ASCII art banner")

    args = parser.parse_args()

    try:
        # Initialize GitHub stats
        gh = GitHubStats(token=args.token)

        if not args.quiet:
            print_banner(args.username)

        print(f"  Fetching profile data for @{args.username}...")
        print()

        # Get user data
        user = gh.get_user(args.username)
        print_profile(user)

        # Get repositories
        print(f"  Fetching repositories...")
        repos = gh.get_repos(args.username)
        print_repos(repos, limit=args.repos)

        # Get language stats
        languages = gh.get_language_stats(repos)
        print_languages(languages, repos)

        # Get activity stats
        if not args.no_events:
            print(f"  Fetching activity data (this may take a moment)...")
            events = gh.get_events(args.username)
            contributions = gh.get_contributions(events)
            active_days = gh.get_most_active_days(events)

            print_stats(contributions)
            print_activity_chart(active_days)
            print_streak(events)
            print()

        print("  Done! Data fetched from GitHub API")
        print()

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"\nError: User '{args.username}' not found\n", file=sys.stderr)
        elif e.response.status_code == 403:
            print("\nError: Rate limit exceeded. Use --token for higher limits\n", file=sys.stderr)
        else:
            print(f"\nError: {e}\n", file=sys.stderr)
        sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(f"\nError: Network error - {e}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
