#!/usr/bin/env python3
"""
Movie Info - CLI movie information lookup
Features: Ratings, cast, plot, posters via ASCII art
Uses OMDB API (free tier available at omdbapi.com)
"""

import argparse
import os
import sys
import textwrap
import urllib.request
import json

# Try to import colorama
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = CYAN = MAGENTA = WHITE = RESET = BLUE = ''
    class Style:
        BRIGHT = RESET_ALL = DIM = ''

# OMDB API Configuration
# Get a free API key at https://www.omdbapi.com/apikey.aspx
OMDB_API_KEY = os.environ.get("OMDB_API_KEY", "4a3b711b")  # Demo key (limited requests)
OMDB_API_URL = "https://www.omdbapi.com/"


def fetch_movie_data(title: str, movie_type: str = "movie") -> dict:
    """Fetch movie data from OMDB API."""
    params = {
        "apikey": OMDB_API_KEY,
        "t": title,
        "type": movie_type,
        "plot": "full"
    }

    query_string = "&".join(f"{k}={urllib.parse.quote(v)}" for k, v in params.items())
    url = f"{OMDB_API_URL}?{query_string}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))

            if data.get("Response") == "False":
                error_msg = data.get("Error", "Movie not found")
                return {"error": error_msg}

            return data
    except urllib.error.URLError as e:
        return {"error": f"Network error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}


def get_poster_ascii(url: str) -> str:
    """Generate ASCII art placeholder for poster."""
    # Since we can't fetch actual images, create a nice frame
    frame = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}                                                                      {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}    ███████╗██╗   ██╗███╗   ███╗███████╗██████╗  ██████╗       {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}    ██╔════╝██║   ██║████╗ ████║██╔════╝██╔══██╗██╔═══██╗      {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}    ███████╗██║   ██║██╔████╔██║█████╗  ██████╔╝██║   ██║      {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}    ╚════██║██║   ██║██║╚██╔╝██║██╔══╝  ██╔══██╗██║   ██║      {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}    ███████║╚██████╔╝██║ ╚═╝ ██║███████╗██║  ██║╚██████╔╝      {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}    ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝       {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}                                                                      {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}              🎬  M O V I E  I N F O  🎬                        {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}                                                                      {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    return frame


def display_movie_info(movie: dict) -> None:
    """Display formatted movie information."""
    print()
    print(get_poster_ascii(""))

    # Title and Year
    title = movie.get("Title", "Unknown")
    year = movie.get("Year", "N/A")
    print(f"{Fore.WHITE}{Style.BRIGHT}  {title} ({year}){Style.RESET_ALL}\n")

    # Meta info row
    meta_parts = []
    if movie.get("Rated"):
        meta_parts.append(f"{Fore.YELLOW}Rated: {movie['Rated']}{Style.RESET_ALL}")
    if movie.get("Runtime"):
        meta_parts.append(f"{Fore.CYAN}Runtime: {movie['Runtime']}{Style.RESET_ALL}")
    if movie.get("Genre"):
        meta_parts.append(f"{Fore.MAGENTA}{movie['Genre']}{Style.RESET_ALL}")

    if meta_parts:
        print(f"  {' | '.join(meta_parts)}\n")

    # Ratings
    ratings = movie.get("Ratings", [])
    if ratings:
        print(f"  {Fore.GREEN}Ratings:{Style.RESET_ALL}")
        for rating in ratings:
            source = rating.get("Source", "Unknown")
            value = rating.get("Value", "N/A")

            # Color code by source
            if "IMDb" in source:
                color = Fore.YELLOW
            elif "Rotten" in source:
                color = Fore.RED if float(value.rstrip('%').split('/')[0]) < 60 else Fore.GREEN
            elif "Metacritic" in source:
                color = Fore.GREEN
            else:
                color = Fore.WHITE

            print(f"    {color}● {source}: {value}{Style.RESET_ALL}")
        print()

    # Plot
    plot = movie.get("Plot", "")
    if plot:
        print(f"  {Fore.WHITE}Plot:{Style.RESET_ALL}")
        wrapped = textwrap.wrap(plot, width=65)
        for line in wrapped:
            print(f"    {Fore.DIM}{line}{Style.RESET_ALL}")
        print()

    # Director, Writer, Cast
    if movie.get("Director") and movie.get("Director") != "N/A":
        print(f"  {Fore.CYAN}Director:{Style.RESET_ALL} {movie['Director']}")
    if movie.get("Writer") and movie.get("Writer") != "N/A":
        print(f"  {Fore.CYAN}Writer:{Style.RESET_ALL} {movie['Writer']}")

    cast = movie.get("Actors", "")
    if cast and cast != "N/A":
        print(f"  {Fore.GREEN}Cast:{Style.RESET_ALL}")
        actors = [a.strip() for a in cast.split(",")]
        for i, actor in enumerate(actors[:6]):  # Show first 6 actors
            print(f"    {Fore.WHITE}• {actor}{Style.RESET_ALL}")
        if len(actors) > 6:
            print(f"    {Fore.DIM}...and {len(actors) - 6} more{Style.RESET_ALL}")

    print()

    # Awards
    awards = movie.get("Awards", "")
    if awards and awards != "N/A":
        print(f"  {Fore.YELLOW}Awards:{Style.RESET_ALL} {awards}\n")

    # Box Office
    box_office = movie.get("BoxOffice", "")
    if box_office and box_office != "N/A":
        print(f"  {Fore.MAGENTA}Box Office:{Style.RESET_ALL} {box_office}\n")

    # Production
    production = movie.get("Production", "")
    if production and production != "N/A":
        print(f"  {Fore.CYAN}Production:{Style.RESET_ALL} {production}\n")

    print(f"{Fore.CYAN}{'═'*70}{Style.RESET_ALL}\n")


def search_movies(title: str) -> list:
    """Search for movies by title (returns multiple results)."""
    params = {
        "apikey": OMDB_API_KEY,
        "s": title,
        "type": "movie"
    }

    query_string = "&".join(f"{k}={urllib.parse.quote(v)}" for k, v in params.items())
    url = f"{OMDB_API_URL}?{query_string}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))

            if data.get("Response") == "False":
                return []

            return data.get("Search", [])
    except Exception:
        return []


def display_search_results(results: list) -> None:
    """Display search results."""
    if not results:
        print(f"{Fore.RED}No movies found.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}{'═'*60}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Style.BRIGHT}  Search Results ({len(results)} found){Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═'*60}{Style.RESET_ALL}\n")

    for i, movie in enumerate(results[:10], 1):  # Show max 10
        title = movie.get("Title", "Unknown")
        year = movie.get("Year", "N/A")
        type_ = movie.get("Type", "movie")
        imdb_id = movie.get("imdbID", "")

        print(f"{Fore.GREEN}{i}. {title}{Style.RESET_ALL} ({year})")
        print(f"   {Fore.DIM}Type: {type_} | IMDb: {imdb_id}{Style.RESET_ALL}")
        print()


def main():
    """Main entry point."""
    # Add urllib.parse import for Python 3
    global urllib
    import urllib.parse

    parser = argparse.ArgumentParser(
        description="Movie Info - CLI movie information lookup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  movie-info "The Matrix"
  movie-info "Inception" --full
  movie-info "Star Wars" --search
  movie-info "Batman" --type series

Environment:
  OMDB_API_KEY - Your OMDB API key (get one at omdbapi.com)
        """
    )

    parser.add_argument("title", help="Movie title to search for")
    parser.add_argument("--full", "-f", action="store_true",
                       help="Show full information")
    parser.add_argument("--search", "-s", action="store_true",
                       help="Search mode (show multiple results)")
    parser.add_argument("--type", "-t", choices=["movie", "series", "episode"],
                       default="movie", help="Type of content")
    parser.add_argument("--year", "-y", help="Year of release")

    args = parser.parse_args()

    # Check for API key
    if not os.environ.get("OMDB_API_KEY"):
        print(f"{Fore.YELLOW}Using demo API key. For unlimited requests, get a free key at:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  https://www.omdbapi.com/apikey.aspx{Style.RESET_ALL}\n")
        print(f"{Fore.DIM}Set OMDB_API_KEY environment variable to use your key.{Style.RESET_ALL}\n")

    if args.search:
        # Search mode - show multiple results
        results = search_movies(args.title)
        if results:
            display_search_results(results)
            print(f"{Fore.DIM}Run with --full to get details on a specific movie.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}No movies found matching: {args.title}{Style.RESET_ALL}")
    else:
        # Single movie lookup
        movie = fetch_movie_data(args.title, args.type)

        if "error" in movie:
            print(f"{Fore.RED}Error: {movie['error']}{Style.RESET_ALL}")
            sys.exit(1)

        display_movie_info(movie)


if __name__ == "__main__":
    main()
