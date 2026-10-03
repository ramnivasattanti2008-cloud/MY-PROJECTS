"""
Quiz API Flask Application
Get random trivia questions, submit answers, and track scores
"""
import os
import sqlite3
import json
import urllib.request
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DATABASE = os.path.join(os.path.dirname(__file__), 'quiz.db')

# Open Trivia DB API base URL
TRIVIA_API_URL = 'https://opentdb.com/api.php'


def get_db():
    """Get database connection with row factory"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database schema"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_key VARCHAR(64) UNIQUE NOT NULL,
            player_name TEXT,
            total_questions INTEGER DEFAULT 0,
            correct_answers INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            user_answer TEXT NOT NULL,
            is_correct INTEGER DEFAULT 0,
            category TEXT,
            difficulty TEXT,
            answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES quiz_sessions(id)
        )
    ''')
    conn.commit()
    conn.close()


def fetch_questions(amount=10, category=None, difficulty=None):
    """Fetch questions from Open Trivia DB API"""
    url = f'{TRIVIA_API_URL}?amount={amount}&type=multiple'

    if category:
        url += f'&category={category}'
    if difficulty:
        url += f'&difficulty={difficulty}'

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            if data['response_code'] == 0:
                return data['results']
            return []
    except Exception as e:
        print(f'Error fetching questions: {e}')
        return []


def decode_html(text):
    """Decode HTML entities in text"""
    import html
    return html.unescape(text)


def shuffle_answers(question):
    """Shuffle the correct answer with incorrect ones"""
    answers = [
        {'text': decode_html(question['correct_answer']), 'correct': True}
    ]
    for wrong in question['incorrect_answers']:
        answers.append({'text': decode_html(wrong), 'correct': False})

    import random
    random.shuffle(answers)
    return answers


@app.route('/')
def index():
    """Home page with quiz start form"""
    # Get high scores
    conn = get_db()
    cursor = conn.cursor()
    high_scores = cursor.execute('''
        SELECT player_name, total_questions, correct_answers, completed_at
        FROM quiz_sessions
        WHERE completed_at IS NOT NULL
        ORDER BY (CAST(correct_answers AS FLOAT) / total_questions) DESC, completed_at DESC
        LIMIT 10
    ''').fetchall()
    conn.close()

    return render_template('index.html', high_scores=high_scores)


@app.route('/start', methods=['POST'])
def start_quiz():
    """Start a new quiz session"""
    player_name = request.form.get('player_name', '').strip() or 'Anonymous'
    num_questions = int(request.form.get('num_questions', 10))
    difficulty = request.form.get('difficulty', '')

    # Limit questions
    num_questions = min(max(num_questions, 1), 50)

    # Fetch questions from API
    questions = fetch_questions(
        amount=num_questions,
        difficulty=difficulty if difficulty in ['easy', 'medium', 'hard'] else None
    )

    if not questions:
        flash('Could not fetch questions. Please try again.', 'error')
        return redirect(url_for('index'))

    # Create session in database
    import secrets
    session_key = secrets.token_hex(32)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO quiz_sessions (session_key, player_name, total_questions)
        VALUES (?, ?, ?)
    ''', (session_key, player_name, len(questions)))
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Prepare questions for display (decode HTML, shuffle answers)
    prepared_questions = []
    for q in questions:
        prepared_q = {
            'question': decode_html(q['question']),
            'category': decode_html(q['category']),
            'difficulty': q['difficulty'],
            'correct_answer': decode_html(q['correct_answer']),
            'answers': shuffle_answers(q)
        }
        prepared_questions.append(prepared_q)

    # Store in session
    session['session_key'] = session_key
    session['session_id'] = session_id
    session['questions'] = prepared_questions
    session['current_question'] = 0
    session['player_name'] = player_name
    session['score'] = 0

    return redirect(url_for('quiz'))


@app.route('/quiz')
def quiz():
    """Quiz page - display current question"""
    if 'session_key' not in session or 'questions' not in session:
        flash('No active quiz. Please start a new one.', 'error')
        return redirect(url_for('index'))

    current = session['current_question']
    questions = session['questions']

    if current >= len(questions):
        return redirect(url_for('result'))

    question = questions[current]
    total = len(questions)

    return render_template('index.html',
                         quiz_mode=True,
                         question=question,
                         question_number=current + 1,
                         total_questions=total,
                         player_name=session['player_name'])


@app.route('/answer', methods=['POST'])
def submit_answer():
    """Submit answer and move to next question"""
    if 'session_key' not in session or 'questions' not in session:
        flash('No active quiz.', 'error')
        return redirect(url_for('index'))

    answer = request.form.get('answer', '')
    questions = session['questions']
    current = session['current_question']

    if current >= len(questions):
        return redirect(url_for('result'))

    question = questions[current]
    is_correct = answer == question['correct_answer']

    # Save result to database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO quiz_results (session_id, question, correct_answer, user_answer, is_correct, category, difficulty)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        session['session_id'],
        question['question'],
        question['correct_answer'],
        answer,
        1 if is_correct else 0,
        question['category'],
        question['difficulty']
    ))
    conn.commit()
    conn.close()

    # Update session score
    if is_correct:
        session['score'] = session.get('score', 0) + 1

    session['current_question'] = current + 1

    # Check if quiz is complete
    if session['current_question'] >= len(questions):
        return redirect(url_for('result'))

    return redirect(url_for('quiz'))


@app.route('/result')
def result():
    """Show quiz results"""
    if 'session_key' not in session or 'questions' not in session:
        flash('No active quiz.', 'error')
        return redirect(url_for('index'))

    score = session.get('score', 0)
    total = len(session['questions'])
    percentage = round((score / total) * 100, 1) if total > 0 else 0

    # Mark session as completed
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE quiz_sessions
        SET correct_answers = ?, completed_at = ?
        WHERE id = ?
    ''', (score, datetime.now().isoformat(), session['session_id']))
    conn.commit()
    conn.close()

    # Get result details
    conn = get_db()
    results = conn.execute('''
        SELECT * FROM quiz_results WHERE session_id = ?
        ORDER BY answered_at ASC
    ''', (session['session_id'],)).fetchall()
    conn.close()

    # Clear session data
    session.pop('session_key', None)
    session.pop('session_id', None)
    session.pop('questions', None)
    session.pop('current_question', None)
    session.pop('score', None)

    return render_template('result.html',
                         player_name=session.get('player_name', 'Player'),
                         score=score,
                         total=total,
                         percentage=percentage,
                         results=results)


@app.route('/quit')
def quit_quiz():
    """Quit current quiz without saving"""
    session.pop('session_key', None)
    session.pop('session_id', None)
    session.pop('questions', None)
    session.pop('current_question', None)
    session.pop('score', None)
    flash('Quiz ended.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5004)
