"""
Flask Quiz App with Open Trivia DB API, score tracking, and dark theme.
"""
import requests
import secrets
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from contextlib import contextmanager

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['DATABASE'] = 'quiz.db'
app.config['OPENTDB_URL'] = 'https://opentdb.com/api.php'


def get_db():
    """Get database connection."""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_db_conn():
    """Context manager for database connections."""
    conn = get_db()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_db():
    """Initialize the database with required tables."""
    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                player_name TEXT,
                category TEXT,
                difficulty TEXT,
                correct_answers INTEGER,
                total_questions INTEGER,
                score_percentage REAL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_session ON scores(session_id)')


def fetch_questions(amount=10, category=None, difficulty=None):
    """Fetch questions from Open Trivia DB API."""
    params = {'amount': amount}

    if category:
        params['category'] = category
    if difficulty:
        params['difficulty'] = difficulty.lower()

    try:
        response = requests.get(app.config['OPENTDB_URL'], params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data['response_code'] != 0:
            return None, 'Failed to fetch questions. Please try different settings.'

        questions = data['results']
        for q in questions:
            q['shuffled_answers'] = q['incorrect_answers'] + [q['correct_answer']]
            import random
            random.shuffle(q['shuffled_answers'])
            q['decoded_question'] = decode_html(q['question'])
            q['decoded_correct'] = decode_html(q['correct_answer'])
            q['decoded_answers'] = [decode_html(a) for a in q['shuffled_answers']]

        return questions, None
    except requests.RequestException as e:
        return None, f'Network error: {str(e)}'


def decode_html(text):
    """Decode HTML entities in text."""
    import html
    return html.unescape(text)


CATEGORIES = [
    ('', 'Any Category'),
    (9, 'General Knowledge'),
    (10, 'Entertainment: Books'),
    (11, 'Entertainment: Film'),
    (12, 'Entertainment: Music'),
    (14, 'Entertainment: Television'),
    (15, 'Entertainment: Video Games'),
    (17, 'Science & Nature'),
    (18, 'Science: Computers'),
    (19, 'Science: Mathematics'),
    (21, 'Sports'),
    (22, 'Geography'),
    (23, 'History'),
    (27, 'Animals'),
]


@app.route('/')
def index():
    """Home page with quiz settings."""
    if 'quiz_session' not in session:
        session['quiz_session'] = secrets.token_hex(16)

    return render_template('index.html', categories=CATEGORIES)


@app.route('/setup', methods=['POST'])
def setup_quiz():
    """Set up quiz parameters and fetch questions."""
    amount = min(max(int(request.form.get('amount', 10)), 1), 50)
    category = request.form.get('category', '')
    difficulty = request.form.get('difficulty', '')
    player_name = request.form.get('player_name', 'Anonymous').strip()[:50]

    questions, error = fetch_questions(amount, category or None, difficulty or None)

    if error:
        return render_template('index.html', categories=CATEGORIES, error=error)

    session['questions'] = questions
    session['current_question'] = 0
    session['answers'] = []
    session['player_name'] = player_name
    session['quiz_category'] = category
    session['quiz_difficulty'] = difficulty
    session['quiz_amount'] = amount

    return redirect(url_for('quiz'))


@app.route('/quiz')
def quiz():
    """Display current quiz question."""
    questions = session.get('questions', [])
    current = session.get('current_question', 0)

    if not questions or current >= len(questions):
        return redirect(url_for('results'))

    question = questions[current]
    total = len(questions)

    return render_template('quiz.html',
                         question=question,
                         current=current + 1,
                         total=total)


@app.route('/answer', methods=['POST'])
def submit_answer():
    """Submit answer and move to next question."""
    selected = request.form.get('answer', '')
    questions = session.get('questions', [])
    current = session.get('current_question', 0)

    if current >= len(questions):
        return redirect(url_for('results'))

    question = questions[current]
    correct = question['decoded_correct']
    is_correct = selected == correct

    answers = session.get('answers', [])
    answers.append({
        'question': question['decoded_question'],
        'selected': selected,
        'correct': correct,
        'is_correct': is_correct
    })
    session['answers'] = answers

    session['current_question'] = current + 1
    session.modified = True

    if current + 1 >= len(questions):
        return redirect(url_for('results'))

    return redirect(url_for('quiz'))


@app.route('/results')
def results():
    """Display quiz results."""
    questions = session.get('questions', [])
    answers = session.get('answers', [])
    player_name = session.get('player_name', 'Anonymous')
    category = session.get('quiz_category', '')
    difficulty = session.get('quiz_difficulty', '')

    if not answers:
        return redirect(url_for('index'))

    correct = sum(1 for a in answers if a['is_correct'])
    total = len(answers)
    percentage = round(correct / total * 100, 1) if total > 0 else 0

    category_name = next((name for cid, name in CATEGORIES if str(cid) == str(category)), 'Any Category')

    try:
        with get_db_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO scores (session_id, player_name, category, difficulty, correct_answers, total_questions, score_percentage)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (session.get('quiz_session'), player_name, category_name, difficulty, correct, total, percentage))
    except Exception:
        pass

    session.pop('questions', None)
    session.pop('current_question', None)
    session.pop('answers', None)

    return render_template('results.html',
                         answers=answers,
                         correct=correct,
                         total=total,
                         percentage=percentage,
                         player_name=player_name,
                         category_name=category_name,
                         difficulty=difficulty)


@app.route('/leaderboard')
def leaderboard():
    """Display top scores."""
    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT player_name, category, difficulty, correct_answers, total_questions,
                   score_percentage, completed_at
            FROM scores
            ORDER BY score_percentage DESC, correct_answers DESC
            LIMIT 50
        ''')
        scores = cursor.fetchall()

        cursor.execute('SELECT COUNT(*) as total, AVG(score_percentage) as avg FROM scores')
        stats = cursor.fetchone()

    return render_template('leaderboard.html',
                         scores=[dict(s) for s in scores],
                         total=stats['total'],
                         average=round(stats['avg'] or 0, 1))


@app.route('/api/categories')
def api_categories():
    """API endpoint to get available categories."""
    return jsonify({'categories': [{'id': cid, 'name': name} for cid, name in CATEGORIES]})


@app.route('/api/stats')
def api_stats():
    """API endpoint to get player statistics."""
    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) as total, AVG(score_percentage) as avg,
                   MAX(correct_answers) as best_score,
                   COUNT(DISTINCT player_name) as players
            FROM scores
        ''')
        stats = dict(cursor.fetchone())

    return jsonify(stats)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5005)
