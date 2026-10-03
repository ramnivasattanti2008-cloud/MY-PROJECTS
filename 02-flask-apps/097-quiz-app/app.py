from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'
DATABASE = 'quiz_app.db'

CATEGORIES = [
    ('general', 'General Knowledge'),
    ('science', 'Science'),
    ('history', 'History'),
    ('geography', 'Geography'),
    ('sports', 'Sports'),
    ('entertainment', 'Entertainment'),
    ('technology', 'Technology'),
]

DIFFICULTIES = [
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
]

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_answer VARCHAR(1) NOT NULL,
                category VARCHAR(50) NOT NULL,
                difficulty VARCHAR(20) DEFAULT 'medium',
                explanation TEXT,
                times_asked INTEGER DEFAULT 0,
                times_correct INTEGER DEFAULT 0
            )
        ''')

        db.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name VARCHAR(100) NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                category VARCHAR(50),
                difficulty VARCHAR(20),
                time_taken INTEGER,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        db.execute('''
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name VARCHAR(100) UNIQUE NOT NULL,
                total_score INTEGER DEFAULT 0,
                games_played INTEGER DEFAULT 0,
                average_score REAL DEFAULT 0,
                best_score INTEGER DEFAULT 0,
                last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        existing = db.execute('SELECT COUNT(*) as count FROM questions').fetchone()['count']
        if existing == 0:
            seed_questions(db)

        db.commit()

def seed_questions(db):
    questions = [
        # General Knowledge
        ("What is the capital of France?", "London", "Berlin", "Paris", "Madrid", "C", "general", "easy", "Paris has been the capital of France since 987 AD."),
        ("How many continents are there on Earth?", "5", "6", "7", "8", "C", "general", "easy", "The seven continents are Africa, Antarctica, Asia, Australia, Europe, North America, and South America."),
        ("What is the largest ocean on Earth?", "Atlantic", "Indian", "Arctic", "Pacific", "D", "general", "easy", "The Pacific Ocean covers more area than all land combined."),
        ("Who painted the Mona Lisa?", "Van Gogh", "Da Vinci", "Picasso", "Michelangelo", "B", "general", "medium", "Leonardo da Vinci painted the Mona Lisa between 1503 and 1519."),

        # Science
        ("What is the chemical symbol for water?", "O2", "H2O", "CO2", "NaCl", "B", "science", "easy", "Water is composed of two hydrogen atoms and one oxygen atom."),
        ("What planet is known as the Red Planet?", "Venus", "Mars", "Jupiter", "Saturn", "B", "science", "easy", "Mars appears red due to iron oxide on its surface."),
        ("What is the speed of light in vacuum?", "300,000 km/s", "150,000 km/s", "500,000 km/s", "1,000,000 km/s", "A", "science", "medium", "Light travels at approximately 299,792 km/s in vacuum."),
        ("What is the powerhouse of the cell?", "Nucleus", "Ribosome", "Mitochondria", "Golgi Body", "C", "science", "medium", "Mitochondria produce ATP through cellular respiration."),
        ("What is the atomic number of Carbon?", "4", "6", "8", "12", "B", "science", "medium", "Carbon has 6 protons in its nucleus."),

        # History
        ("In what year did World War II end?", "1943", "1944", "1945", "1946", "C", "history", "easy", "WWII ended in 1945 with the surrender of Japan."),
        ("Who was the first President of the United States?", "Thomas Jefferson", "John Adams", "George Washington", "Abraham Lincoln", "C", "history", "easy", "George Washington served from 1789 to 1797."),
        ("The Great Wall of China was primarily built to protect against which group?", "Mongols", "Japanese", "Koreans", "Russians", "A", "history", "medium", "The wall was built to defend against Mongol invasions."),
        ("In what year did the Berlin Wall fall?", "1987", "1988", "1989", "1990", "C", "history", "medium", "The Berlin Wall fell on November 9, 1989."),

        # Geography
        ("What is the longest river in the world?", "Amazon", "Nile", "Mississippi", "Yangtze", "B", "geography", "easy", "The Nile River is approximately 6,650 km long."),
        ("Which country has the largest population?", "USA", "India", "China", "Indonesia", "C", "geography", "easy", "China has over 1.4 billion people."),
        ("Mount Everest is located in which mountain range?", "Alps", "Andes", "Himalayas", "Rockies", "C", "geography", "easy", "Mount Everest is 8,849 meters high."),
        ("What is the smallest country in the world?", "Monaco", "San Marino", "Vatican City", "Liechtenstein", "C", "geography", "medium", "Vatican City is only 0.44 km²."),

        # Sports
        ("How many players are on a soccer team?", "9", "10", "11", "12", "C", "sports", "easy", "A soccer team has 11 players including the goalkeeper."),
        ("In which sport would you perform a slam dunk?", "Volleyball", "Tennis", "Basketball", "Badminton", "C", "sports", "easy", "A slam dunk is a type of basketball shot."),
        ("How many Grand Slam tournaments are there in tennis?", "3", "4", "5", "6", "B", "sports", "medium", "Australian Open, French Open, Wimbledon, US Open."),
        ("What country hosted the 2016 Summer Olympics?", "China", "Brazil", "UK", "Russia", "B", "sports", "medium", "The 2016 Olympics were held in Rio de Janeiro."),

        # Entertainment
        ("Who directed the movie Inception?", "Steven Spielberg", "Christopher Nolan", "James Cameron", "Martin Scorsese", "B", "entertainment", "medium", "Christopher Nolan wrote and directed Inception in 2010."),
        ("What is the name of the fictional city where Batman operates?", "Metropolis", "Gotham", "Star City", "Central City", "B", "entertainment", "easy", "Gotham City is Batman's home base."),
        ("Which band performed 'Bohemian Rhapsody'?", "The Beatles", "Led Zeppelin", "Queen", "Pink Floyd", "C", "entertainment", "easy", "Queen released Bohemian Rhapsody in 1975."),
        ("What year was the first Harry Potter movie released?", "1999", "2000", "2001", "2002", "C", "entertainment", "medium", "Harry Potter and the Sorcerer's Stone was released in 2001."),

        # Technology
        ("Who founded Microsoft?", "Steve Jobs", "Bill Gates", "Mark Zuckerberg", "Jeff Bezos", "B", "technology", "easy", "Bill Gates co-founded Microsoft in 1975 with Paul Allen."),
        ("What does CPU stand for?", "Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Core Processing Unit", "A", "technology", "easy", "The CPU is the main processor of a computer."),
        ("In what year was the iPhone first released?", "2005", "2006", "2007", "2008", "C", "technology", "medium", "The first iPhone was released on June 29, 2007."),
        ("What programming language was created by Guido van Rossum?", "Ruby", "Python", "Perl", "JavaScript", "B", "technology", "medium", "Python was created in 1991."),
        ("What does HTML stand for?", "Hyper Text Markup Language", "High Tech Modern Language", "Home Tool Markup Language", "Hyperlink Text Management Language", "A", "technology", "easy", "HTML is the standard markup language for web pages."),
    ]

    for q in questions:
        db.execute('''
            INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_answer, category, difficulty, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', q)

@app.route('/')
def index():
    with get_db() as db:
        stats = {
            'total_questions': db.execute('SELECT COUNT(*) as count FROM questions').fetchone()['count'],
            'total_games': db.execute('SELECT COUNT(*) as count FROM scores').fetchone()['count'],
            'top_score': db.execute('SELECT MAX(score) as max FROM scores').fetchone()['max'] or 0,
        }

    return render_template('index.html', categories=CATEGORIES, difficulties=DIFFICULTIES, stats=stats)

@app.route('/quiz', methods=['POST'])
def start_quiz():
    category = request.form.get('category', 'all')
    difficulty = request.form.get('difficulty', 'all')
    player_name = request.form.get('player_name', 'Anonymous').strip()

    if not player_name:
        player_name = 'Anonymous'

    with get_db() as db:
        query = 'SELECT * FROM questions WHERE 1=1'
        params = []

        if category != 'all':
            query += ' AND category = ?'
            params.append(category)

        if difficulty != 'all':
            query += ' AND difficulty = ?'
            params.append(difficulty)

        query += ' ORDER BY RANDOM() LIMIT 10'
        questions = db.execute(query, params).fetchall()

    if not questions:
        flash('No questions found for selected criteria', 'error')
        return redirect(url_for('index'))

    session['questions'] = [dict(q) for q in questions]
    session['current_question'] = 0
    session['score'] = 0
    session['player_name'] = player_name
    session['category'] = category
    session['difficulty'] = difficulty
    session['start_time'] = datetime.now().isoformat()

    return redirect(url_for('quiz_question'))

@app.route('/quiz/question')
def quiz_question():
    if 'questions' not in session or not session['questions']:
        return redirect(url_for('index'))

    current = session['current_question']
    total = len(session['questions'])
    question = session['questions'][current]

    return render_template('question.html',
                         question=question,
                         current=current + 1,
                         total=total)

@app.route('/quiz/answer', methods=['POST'])
def submit_answer():
    if 'questions' not in session:
        return redirect(url_for('index'))

    answer = request.form.get('answer')
    current = session['current_question']
    question = session['questions'][current]

    if answer == question['correct_answer']:
        session['score'] += 1
        correct = True
    else:
        correct = False

    session['current_question'] += 1

    if session['current_question'] >= len(session['questions']):
        return redirect(url_for('results'))
    else:
        return render_template('answer.html',
                             correct=correct,
                             correct_answer=question['correct_answer'],
                             explanation=question['explanation'])

@app.route('/quiz/results')
def results():
    if 'questions' not in session:
        return redirect(url_for('index'))

    score = session['score']
    total = len(session['questions'])
    player_name = session['player_name']
    category = session.get('category', 'all')
    difficulty = session.get('difficulty', 'all')

    percentage = (score / total) * 100

    if percentage >= 80:
        grade = 'Excellent!'
        grade_color = '#22c55e'
    elif percentage >= 60:
        grade = 'Good Job!'
        grade_color = '#22d3ee'
    elif percentage >= 40:
        grade = 'Keep Learning!'
        grade_color = '#f59e0b'
    else:
        grade = 'Try Again!'
        grade_color = '#ef4444'

    with get_db() as db:
        db.execute('''
            INSERT INTO scores (player_name, score, total_questions, category, difficulty)
            VALUES (?, ?, ?, ?, ?)
        ''', (player_name, score, total, category, difficulty))

        db.execute('''
            INSERT INTO leaderboard (player_name, total_score, games_played, best_score)
            VALUES (?, ?, 1, ?)
            ON CONFLICT(player_name) DO UPDATE SET
                total_score = total_score + ?,
                games_played = games_played + 1,
                best_score = MAX(best_score, ?),
                last_played = CURRENT_TIMESTAMP
        ''', (player_name, score, score, score, score))

        db.commit()

    session.pop('questions', None)
    session.pop('current_question', None)
    session.pop('score', None)
    session.pop('player_name', None)
    session.pop('category', None)
    session.pop('difficulty', None)
    session.pop('start_time', None)

    return render_template('results.html',
                         score=score,
                         total=total,
                         player_name=player_name,
                         grade=grade,
                         grade_color=grade_color,
                         percentage=percentage)

@app.route('/leaderboard')
def leaderboard():
    with get_db() as db:
        top_players = db.execute('''
            SELECT * FROM leaderboard
            ORDER BY total_score DESC
            LIMIT 20
        ''').fetchall()

        recent_games = db.execute('''
            SELECT * FROM scores
            ORDER BY completed_at DESC
            LIMIT 10
        ''').fetchall()

    return render_template('leaderboard.html',
                         top_players=top_players,
                         recent_games=recent_games)

@app.route('/api/questions')
def api_questions():
    category = request.args.get('category', 'all')
    difficulty = request.args.get('difficulty', 'all')

    with get_db() as db:
        query = 'SELECT * FROM questions WHERE 1=1'
        params = []

        if category != 'all':
            query += ' AND category = ?'
            params.append(category)

        if difficulty != 'all':
            query += ' AND difficulty = ?'
            params.append(difficulty)

        questions = db.execute(query + ' ORDER BY RANDOM() LIMIT 10', params).fetchall()

    return jsonify([{
        'id': q['id'],
        'question': q['question'],
        'options': {
            'A': q['option_a'],
            'B': q['option_b'],
            'C': q['option_c'],
            'D': q['option_d']
        },
        'category': q['category'],
        'difficulty': q['difficulty']
    } for q in questions])

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5003)
