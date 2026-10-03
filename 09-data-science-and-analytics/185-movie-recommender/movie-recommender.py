"""
Movie Recommender CLI
Recommend movies based on genre preference using an embedded dataset
Features ASCII art display and interactive interface
"""

import json
import random
from dataclasses import dataclass
from typing import Optional
from enum import Enum


@dataclass
class Movie:
    """Movie data structure."""
    title: str
    year: int
    genre: list
    rating: float
    director: str
    runtime: int  # minutes
    description: str


class Color:
    """ASCII color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


GENRES = [
    "Action", "Adventure", "Animation", "Comedy", "Crime",
    "Documentary", "Drama", "Fantasy", "Horror", "Mystery",
    "Romance", "Sci-Fi", "Thriller", "War", "Western"
]

ASCII_ART = r"""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║     ███╗   ███╗██╗███████╗███████╗██╗ ██████╗ ███╗   ██╗ ║
    ║     ████╗ ████║██║██╔════╝██╔════╝██║██╔═══██╗████╗  ██║ ║
    ║     ██╔████╔██║██║███████╗███████╗██║██║   ██║██╔██╗ ██║ ║
    ║     ██║╚██╔╝██║██║╚════██║╚════██║██║██║   ██║██║╚██╗██║ ║
    ║     ██║ ╚═╝ ██║██║███████║███████║██║╚██████╔╝██║ ╚████║ ║
    ║     ╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ║
    ║                                                          ║
    ║              M O V I E   R E C O M M E N D E R           ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
"""


def load_movies(filepath: str = "data/movies.json") -> list[Movie]:
    """Load movies from JSON file."""
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return [Movie(**m) for m in data]
    except FileNotFoundError:
        print(f"{Color.RED}Error: {filepath} not found!{Color.RESET}")
        return []


def print_header():
    """Print ASCII art header."""
    print(f"\n{Color.CYAN}{ASCII_ART}{Color.RESET}")
    print(f"{Color.DIM}    Your personal movie recommendation assistant{Color.RESET}\n")


def print_movie(movie: Movie, index: int):
    """Display a movie with ASCII art styling."""
    genre_str = " | ".join(movie.genre)
    stars = "★" * int(movie.rating // 2) + "☆" * (5 - int(movie.rating // 2))

    print(f"\n{Color.BOLD}{Color.CYAN}{'─' * 60}{Color.RESET}")
    print(f"{Color.YELLOW}{index}. {movie.title}{Color.RESET} ({movie.year})")
    print(f"{Color.DIM}{'─' * 60}{Color.RESET}")
    print(f"{Color.GREEN}Genres:{Color.RESET} {genre_str}")
    print(f"{Color.GREEN}Director:{Color.RESET} {movie.director}")
    print(f"{Color.GREEN}Runtime:{Color.RESET} {movie.runtime} min")
    print(f"{Color.GREEN}Rating:{Color.RESET} {stars} ({movie.rating}/10)")
    print(f"\n{Color.WHITE}{movie.description}{Color.RESET}")
    print(f"{Color.DIM}{'─' * 60}{Color.RESET}\n")


def print_banner(text: str):
    """Print a styled banner."""
    width = 60
    print(f"\n{Color.MAGENTA}{'═' * width}{Color.RESET}")
    padding = (width - len(text) - 2) // 2
    print(f"{Color.MAGENTA}║{' ' * padding}{Color.BOLD}{text}{' ' * (width - padding - len(text) - 2)}{Color.RESET}{Color.MAGENTA}║{Color.RESET}")
    print(f"{Color.MAGENTA}{'═' * width}{Color.RESET}\n")


def get_genre_preference() -> list[str]:
    """Get user's genre preferences."""
    print_banner("SELECT YOUR FAVORITE GENRES")

    print(f"{Color.CYAN}Available genres:{Color.RESET}")
    for i, genre in enumerate(GENRES, 1):
        print(f"  {Color.YELLOW}{i:2}.{Color.RESET} {genre}")

    print(f"\n{Color.DIM}Enter genre numbers separated by commas (e.g., 1,3,5){Color.RESET}")
    print(f"{Color.DIM}Or press Enter for all genres:{Color.RESET}\n")

    try:
        user_input = input(f"{Color.GREEN}Your choice: {Color.RESET}").strip()
        if not user_input:
            return GENRES

        indices = [int(x.strip()) - 1 for x in user_input.split(",")]
        selected = [GENRES[i] for i in indices if 0 <= i < len(GENRES)]
        return selected if selected else GENRES
    except (ValueError, IndexError):
        print(f"{Color.YELLOW}Invalid input. Showing all genres.{Color.RESET}")
        return GENRES


def get_rating_preference() -> float:
    """Get minimum rating preference."""
    print(f"\n{Color.CYAN}Minimum rating filter:{Color.RESET}")
    print(f"  {Color.YELLOW}1.{Color.RESET} Any rating")
    print(f"  {Color.YELLOW}2.{Color.RESET} 6.0+ (Decent)")
    print(f"  {Color.YELLOW}3.{Color.RESET} 7.0+ (Good)")
    print(f"  {Color.YELLOW}4.{Color.RESET} 8.0+ (Great)")
    print(f"  {Color.YELLOW}5.{Color.RESET} 9.0+ (Masterpiece)")

    try:
        choice = input(f"\n{Color.GREEN}Your choice (1-5): {Color.RESET}").strip()
        rating_map = {"1": 0, "2": 6.0, "3": 7.0, "4": 8.0, "5": 9.0}
        return rating_map.get(choice, 0)
    except ValueError:
        return 0


def recommend_movies(
    movies: list[Movie],
    genres: list[str],
    min_rating: float = 0,
    count: int = 5
) -> list[Movie]:
    """Get movie recommendations based on preferences."""
    # Filter by genre and rating
    filtered = [
        m for m in movies
        if any(g in m.genre for g in genres) and m.rating >= min_rating
    ]

    if not filtered:
        return []

    # Sort by rating (with some randomness for variety)
    random.shuffle(filtered)
    filtered.sort(key=lambda x: x.rating, reverse=True)

    return filtered[:count]


def show_genre_breakdown(movies: list[Movie]):
    """Show movie count by genre."""
    genre_counts = {}
    for movie in movies:
        for genre in movie.genre:
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

    print_banner("MOVIES BY GENRE")
    for genre in sorted(genre_counts.keys(), key=lambda x: genre_counts[x], reverse=True):
        bar = "█" * (genre_counts[genre] * 2)
        print(f"  {genre:15} {bar} ({genre_counts[genre]})")


def show_top_rated(movies: list[Movie], count: int = 10):
    """Show top-rated movies."""
    sorted_movies = sorted(movies, key=lambda x: x.rating, reverse=True)[:count]

    print_banner(f"TOP {count} RATED MOVIES")
    for i, movie in enumerate(sorted_movies, 1):
        stars = "★" * int(movie.rating // 2)
        print(f"{Color.YELLOW}{i:2}.{Color.RESET} {movie.title:40} {stars} {movie.rating}")


def show_random_pick(movies: list[Movie]):
    """Show a random movie recommendation."""
    movie = random.choice(movies)
    print_banner("RANDOM PICK FOR YOU!")
    print_movie(movie, 1)


def main():
    """Main application loop."""
    movies = load_movies()

    if not movies:
        print(f"{Color.RED}No movies available. Please check data/movies.json{Color.RESET}")
        return

    print_header()

    while True:
        print_banner("MAIN MENU")
        print(f"  {Color.YELLOW}1.{Color.RESET} Get Recommendations")
        print(f"  {Color.YELLOW}2.{Color.RESET} Show Top Rated")
        print(f"  {Color.YELLOW}3.{Color.RESET} Browse by Genre")
        print(f"  {Color.YELLOW}4.{Color.RESET} Random Pick")
        print(f"  {Color.YELLOW}5.{Color.RESET} Library Stats")
        print(f"  {Color.YELLOW}0.{Color.RESET} Exit")
        print()

        choice = input(f"{Color.GREEN}Enter choice: {Color.RESET}").strip()

        if choice == "1":
            genres = get_genre_preference()
            min_rating = get_rating_preference()

            recommendations = recommend_movies(movies, genres, min_rating, count=5)

            if recommendations:
                print_banner("YOUR RECOMMENDATIONS")
                for i, movie in enumerate(recommendations, 1):
                    print_movie(movie, i)
            else:
                print(f"{Color.YELLOW}No movies match your criteria. Try different preferences.{Color.RESET}")

        elif choice == "2":
            show_top_rated(movies)

        elif choice == "3":
            print_banner("BROWSE BY GENRE")
            for i, genre in enumerate(GENRES, 1):
                print(f"  {Color.YELLOW}{i:2}.{Color.RESET} {genre}")

            try:
                genre_idx = int(input(f"\n{Color.GREEN}Select genre (1-{len(GENRES)}): {Color.RESET}")) - 1
                if 0 <= genre_idx < len(GENRES):
                    selected_genre = GENRES[genre_idx]
                    genre_movies = [m for m in movies if selected_genre in m.genre]
                    genre_movies.sort(key=lambda x: x.rating, reverse=True)

                    print_banner(f"{selected_genre.upper()} MOVIES")
                    for i, movie in enumerate(genre_movies, 1):
                        print_movie(movie, i)
            except ValueError:
                print(f"{Color.YELLOW}Invalid selection.{Color.RESET}")

        elif choice == "4":
            show_random_pick(movies)

        elif choice == "5":
            print_banner("LIBRARY STATISTICS")
            print(f"  {Color.CYAN}Total Movies:{Color.RESET} {len(movies)}")
            print(f"  {Color.CYAN}Average Rating:{Color.RESET} {sum(m.rating for m in movies) / len(movies):.2f}")
            print(f"  {Color.CYAN}Genres Available:{Color.RESET} {len(GENRES)}")
            print(f"  {Color.CYAN}Year Range:{Color.RESET} {min(m.year for m in movies)} - {max(m.year for m in movies)}")
            show_genre_breakdown(movies)

        elif choice == "0":
            print(f"\n{Color.CYAN}Thanks for using Movie Recommender!{Color.RESET}")
            print(f"{Color.DIM}Happy watching! 🍿{Color.RESET}\n")
            break

        else:
            print(f"{Color.YELLOW}Invalid choice. Please try again.{Color.RESET}")

        input(f"\n{Color.DIM}Press Enter to continue...{Color.RESET}")


if __name__ == "__main__":
    main()
