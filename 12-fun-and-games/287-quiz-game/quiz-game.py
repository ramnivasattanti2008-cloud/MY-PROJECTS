"""
Quiz Game - Multi-choice quiz with categories
Choose from Science, History, Geography, and more!
Track your score and compete against yourself!
"""

import random
import os
import json
from datetime import datetime

# Quiz questions organized by category
QUIZ_DATA = {
    "Science": [
        {
            "question": "What is the chemical symbol for gold?",
            "options": ["Ag", "Au", "Fe", "Cu"],
            "answer": 1,
            "explanation": "Au comes from 'Aurum', the Latin word for gold."
        },
        {
            "question": "What planet is known as the Red Planet?",
            "options": ["Venus", "Mars", "Jupiter", "Saturn"],
            "answer": 1,
            "explanation": "Mars appears red due to iron oxide (rust) on its surface."
        },
        {
            "question": "What is the hardest natural substance on Earth?",
            "options": ["Gold", "Iron", "Diamond", "Platinum"],
            "answer": 2,
            "explanation": "Diamond ranks 10 on the Mohs hardness scale."
        },
        {
            "question": "How many bones are in the adult human body?",
            "options": ["186", "206", "226", "246"],
            "answer": 1,
            "explanation": "Babies are born with about 270 bones, but many fuse together."
        },
        {
            "question": "What is the speed of light in vacuum?",
            "options": ["299,792 km/s", "199,792 km/s", "399,792 km/s", "149,792 km/s"],
            "answer": 0,
            "explanation": "Light travels at approximately 299,792 kilometers per second."
        },
        {
            "question": "What gas do plants absorb from the atmosphere?",
            "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
            "answer": 2,
            "explanation": "Plants use CO2 in photosynthesis to produce oxygen."
        },
        {
            "question": "What is the largest organ in the human body?",
            "options": ["Liver", "Brain", "Skin", "Heart"],
            "answer": 2,
            "explanation": "The skin covers about 20 square feet in adults!"
        },
        {
            "question": "What is the atomic number of Carbon?",
            "options": ["4", "6", "8", "12"],
            "answer": 1,
            "explanation": "Carbon has 6 protons in its nucleus."
        },
    ],
    "History": [
        {
            "question": "In which year did World War II end?",
            "options": ["1943", "1944", "1945", "1946"],
            "answer": 2,
            "explanation": "WWII ended on September 2, 1945, with Japan's surrender."
        },
        {
            "question": "Who was the first President of the United States?",
            "options": ["Thomas Jefferson", "John Adams", "George Washington", "Benjamin Franklin"],
            "answer": 2,
            "explanation": "George Washington served from 1789 to 1797."
        },
        {
            "question": "The Great Wall of China was primarily built to defend against whom?",
            "options": ["Japanese", "Mongols", "Romans", "Persians"],
            "answer": 1,
            "explanation": "The wall was built to protect against Mongol invasions."
        },
        {
            "question": "In which year did India gain independence?",
            "options": ["1945", "1946", "1947", "1948"],
            "answer": 2,
            "explanation": "India gained independence on August 15, 1947."
        },
        {
            "question": "Who wrote the famous autobiography 'The Story of My Experiments with Truth'?",
            "options": ["Jawaharlal Nehru", "Mahatma Gandhi", "Subhas Chandra Bose", "Rabindranath Tagore"],
            "answer": 1,
            "explanation": "Mahatma Gandhi wrote his autobiography in 1927."
        },
        {
            "question": "The Renaissance period began in which country?",
            "options": ["France", "Germany", "England", "Italy"],
            "answer": 3,
            "explanation": "The Renaissance began in Italy in the 14th century."
        },
        {
            "question": "Who discovered America in 1492?",
            "options": ["Vasco da Gama", "Christopher Columbus", "Ferdinand Magellan", "Amerigo Vespucci"],
            "answer": 1,
            "explanation": "Columbus landed in the Bahamas on October 12, 1492."
        },
        {
            "question": "The French Revolution began in which year?",
            "options": ["1776", "1789", "1799", "1804"],
            "answer": 1,
            "explanation": "The French Revolution started with the storming of the Bastille on July 14, 1789."
        },
    ],
    "Geography": [
        {
            "question": "What is the capital of Australia?",
            "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"],
            "answer": 2,
            "explanation": "Canberra was purpose-built as the capital between Sydney and Melbourne."
        },
        {
            "question": "Which is the largest ocean on Earth?",
            "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
            "answer": 3,
            "explanation": "The Pacific Ocean covers about 63 million square miles."
        },
        {
            "question": "What is the longest river in the world?",
            "options": ["Amazon", "Nile", "Mississippi", "Yangtze"],
            "answer": 1,
            "explanation": "The Nile River is approximately 6,650 km long."
        },
        {
            "question": "Which country has the most natural lakes?",
            "options": ["United States", "Russia", "Canada", "Finland"],
            "answer": 2,
            "explanation": "Canada has over 2 million lakes, more than any other country."
        },
        {
            "question": "Mount Everest is located in which mountain range?",
            "options": ["Andes", "Alps", "Rockies", "Himalayas"],
            "answer": 3,
            "explanation": "Mount Everest is in the Mahalangur Himal range of the Himalayas."
        },
        {
            "question": "What is the smallest country in the world?",
            "options": ["Monaco", "San Marino", "Vatican City", "Liechtenstein"],
            "answer": 2,
            "explanation": "Vatican City is only 0.44 square kilometers in area."
        },
        {
            "question": "The Amazon Rainforest is primarily located in which country?",
            "options": ["Colombia", "Peru", "Brazil", "Venezuela"],
            "answer": 2,
            "explanation": "About 60% of the Amazon is in Brazil."
        },
        {
            "question": "Which desert is the largest in the world?",
            "options": ["Sahara", "Arabian", "Gobi", "Antarctic"],
            "answer": 3,
            "explanation": "Antarctica is technically the largest desert at 14.2 million sq km."
        },
    ],
    "Technology": [
        {
            "question": "Who is the founder of Microsoft?",
            "options": ["Steve Jobs", "Bill Gates", "Mark Zuckerberg", "Elon Musk"],
            "answer": 1,
            "explanation": "Bill Gates co-founded Microsoft with Paul Allen in 1975."
        },
        {
            "question": "What does 'HTTP' stand for?",
            "options": ["HyperText Transfer Protocol", "High Tech Transfer Protocol", "HyperText Transmission Process", "High Transfer Text Protocol"],
            "answer": 0,
            "explanation": "HTTP is the foundation of data communication on the web."
        },
        {
            "question": "In what year was Google founded?",
            "options": ["1996", "1998", "2000", "2002"],
            "answer": 1,
            "explanation": "Google was founded on September 4, 1998, by Larry Page and Sergey Brin."
        },
        {
            "question": "What programming language is known as the 'language of the web'?",
            "options": ["Python", "Java", "JavaScript", "C++"],
            "answer": 2,
            "explanation": "JavaScript is the only programming language that runs natively in browsers."
        },
        {
            "question": "What does 'AI' stand for?",
            "options": ["Automated Intelligence", "Artificial Intelligence", "Advanced Integration", "Automated Integration"],
            "answer": 1,
            "explanation": "Artificial Intelligence refers to machine-simulated intelligence."
        },
        {
            "question": "Who invented the World Wide Web?",
            "options": ["Bill Gates", "Steve Jobs", "Tim Berners-Lee", "Vint Cerf"],
            "answer": 2,
            "explanation": "Tim Berners-Lee invented the WWW in 1989 at CERN."
        },
        {
            "question": "What is the name of Apple's voice assistant?",
            "options": ["Alexa", "Cortana", "Siri", "Google Assistant"],
            "answer": 2,
            "explanation": "Siri was introduced on iPhone 4S in October 2011."
        },
        {
            "question": "What does 'RAM' stand for?",
            "options": ["Random Access Memory", "Read Access Memory", "Rapid Access Module", "Ready Access Memory"],
            "answer": 0,
            "explanation": "RAM is volatile memory that stores data temporarily."
        },
    ],
    "Sports": [
        {
            "question": "How many players are on a standard soccer team on the field?",
            "options": ["9", "10", "11", "12"],
            "answer": 2,
            "explanation": "Each team has 11 players including the goalkeeper."
        },
        {
            "question": "In which sport would you perform a 'slam dunk'?",
            "options": ["Volleyball", "Basketball", "Tennis", "Badminton"],
            "answer": 1,
            "explanation": "A slam dunk is when a player jumps and thrusts the ball through the hoop."
        },
        {
            "question": "Which country has won the most FIFA World Cups?",
            "options": ["Germany", "Argentina", "Brazil", "Italy"],
            "answer": 2,
            "explanation": "Brazil has won 5 World Cups (1958, 1962, 1970, 1994, 2002)."
        },
        {
            "question": "What is the national sport of Japan?",
            "options": ["Judo", "Karate", "Sumo Wrestling", "Kendo"],
            "answer": 2,
            "explanation": "Sumo wrestling has been Japan's national sport for centuries."
        },
        {
            "question": "How many rings are on the Olympic flag?",
            "options": ["4", "5", "6", "7"],
            "answer": 1,
            "explanation": "The 5 rings represent the 5 inhabited continents."
        },
        {
            "question": "Which sport uses the terms 'strike' and 'spare'?",
            "options": ["Golf", "Tennis", "Bowling", "Baseball"],
            "answer": 2,
            "explanation": "In bowling, a strike is knocking down all pins on first ball."
        },
        {
            "question": "What is the maximum score in a single frame of bowling?",
            "options": ["20", "25", "30", "35"],
            "answer": 2,
            "explanation": "A strike in the 10th frame gives 2 bonus balls worth 30 max."
        },
        {
            "question": "In cricket, what is a 'century'?",
            "options": ["100 runs", "50 runs", "10 wickets", "5 catches"],
            "answer": 0,
            "explanation": "A century is scoring 100 or more runs in one innings."
        },
    ],
}


def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Display the game header"""
    print("=" * 60)
    print("              🧠 QUIZ MASTER 🧠")
    print("=" * 60)


def print_categories():
    """Display available quiz categories"""
    print("\n  📚 Available Categories:")
    print("  " + "-" * 40)
    categories = list(QUIZ_DATA.keys())
    for i, category in enumerate(categories, 1):
        question_count = len(QUIZ_DATA[category])
        print(f"  {i}. {category} ({question_count} questions)")
    print(f"  0. All Categories (Mixed)")
    print()


def select_category():
    """Let player choose a category"""
    print_categories()
    categories = list(QUIZ_DATA.keys())

    while True:
        try:
            choice = input("  Select category (0-5): ").strip()
            if choice == "":
                continue
            choice_num = int(choice)

            if choice_num == 0:
                # All categories
                all_questions = []
                for category_questions in QUIZ_DATA.values():
                    all_questions.extend(category_questions)
                random.shuffle(all_questions)
                return "All Categories", all_questions
            elif 1 <= choice_num <= len(categories):
                selected = categories[choice_num - 1]
                questions = QUIZ_DATA[selected].copy()
                random.shuffle(questions)
                return selected, questions
            else:
                print("  Invalid choice. Please try again.")
        except ValueError:
            print("  Please enter a number.")


def select_difficulty():
    """Let player select number of questions"""
    print("\n  🎯 Select Difficulty:")
    print("  " + "-" * 40)
    print("  1. Easy (3 questions)")
    print("  2. Medium (5 questions)")
    print("  3. Hard (8 questions)")

    while True:
        try:
            choice = input("\n  Enter choice (1-3): ").strip()
            if choice == "":
                continue
            choice_num = int(choice)

            if choice_num == 1:
                return 3
            elif choice_num == 2:
                return 5
            elif choice_num == 3:
                return 8
            else:
                print("  Invalid choice.")
        except ValueError:
            print("  Please enter a number.")


def display_question(question_num, total, question_data):
    """Display a single quiz question"""
    clear_screen()
    print_header()
    print(f"\n  Question {question_num}/{total}")
    print("  " + "=" * 40)

    print(f"\n  {question_data['question']}\n")

    for i, option in enumerate(question_data['options']):
        print(f"    {i + 1}. {option}")

    print()


def get_answer():
    """Get and validate player's answer"""
    while True:
        try:
            answer = input("  Your answer (1-4): ").strip()
            if answer == "":
                continue
            choice = int(answer)
            if 1 <= choice <= 4:
                return choice - 1  # Convert to 0-indexed
            else:
                print("  Please enter 1, 2, 3, or 4.")
        except ValueError:
            print("  Please enter a number (1-4).")


def display_result(question_data, selected_answer, is_correct):
    """Display the result after answering"""
    correct = question_data["answer"]

    print("\n  " + "=" * 40)

    if is_correct:
        print("  ✅ CORRECT!")
    else:
        print("  ❌ WRONG!")

    print(f"\n  Correct answer: {question_data['options'][correct]}")
    print(f"  {question_data.get('explanation', '')}")

    input("\n  Press ENTER to continue...")


def display_final_score(score, total, category):
    """Display the final quiz results"""
    clear_screen()
    print_header()

    percentage = (score / total) * 100

    print(f"\n  📊 QUIZ COMPLETE - {category}")
    print("  " + "=" * 40)
    print(f"\n  Your Score: {score}/{total} ({percentage:.0f}%)")

    if percentage == 100:
        rating = "🌟 PERFECT! You're a genius!"
    elif percentage >= 80:
        rating = "🎉 Excellent! Outstanding knowledge!"
    elif percentage >= 60:
        rating = "👍 Good job! Keep learning!"
    elif percentage >= 40:
        rating = "🤔 Not bad, but room for improvement."
    else:
        rating = "📚 Keep studying! You'll get better!"

    print(f"\n  {rating}")
    print()


def show_scoreboard(all_scores):
    """Display the scoreboard with past scores"""
    if not all_scores:
        return

    clear_screen()
    print_header()
    print("\n  🏆 SCOREBOARD - Past 10 Quizzes")
    print("  " + "=" * 40)

    for i, entry in enumerate(all_scores[-10:], 1):
        score, total, category, date = entry
        percentage = (score / total) * 100
        print(f"  {i}. {category}: {score}/{total} ({percentage:.0f}%) - {date}")

    input("\n  Press ENTER to continue...")


def play_again():
    """Ask if player wants to play again"""
    while True:
        response = input("\n  Play again? (y/n): ").strip().lower()
        if response in ('y', 'yes'):
            return True
        elif response in ('n', 'no'):
            return False
        else:
            print("  Please enter 'y' or 'n'.")


def main():
    """Main game loop"""
    print("\n  Welcome to Quiz Master!")
    print("  Test your knowledge across different categories!")
    input("\n  Press ENTER to start...")

    all_scores = []

    while True:
        clear_screen()
        print_header()

        # Select category
        category, questions = select_category()

        # Select difficulty
        num_questions = select_difficulty()

        # Take only the required number of questions
        quiz_questions = questions[:num_questions]

        # Play the quiz
        score = 0
        for i, question in enumerate(quiz_questions, 1):
            display_question(i, num_questions, question)
            answer = get_answer()
            is_correct = answer == question["answer"]

            if is_correct:
                score += 1

            display_result(question, answer, is_correct)

        # Show final score
        display_final_score(score, num_questions, category)

        # Save score
        date = datetime.now().strftime("%Y-%m-%d")
        all_scores.append((score, num_questions, category, date))

        # Show scoreboard option
        if len(all_scores) >= 3:
            show = input("\n  View scoreboard? (y/n): ").strip().lower()
            if show == 'y':
                show_scoreboard(all_scores)

        if not play_again():
            break

    # Final goodbye
    clear_screen()
    print_header()
    print("\n  Thanks for playing Quiz Master!")
    if all_scores:
        print(f"\n  You played {len(all_scores)} quiz(es)")
        avg_score = sum(s[0]/s[1] for s in all_scores) / len(all_scores) * 100
        print(f"  Average score: {avg_score:.1f}%")
    print("\n  See you next time! 👋")
    print("=" * 60)


if __name__ == "__main__":
    main()
