import requests
import random
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'quiz-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))
    difficulty = db.Column(db.String(20))
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False)
    played_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'player_name': self.player_name,
            'category': self.category,
            'difficulty': self.difficulty,
            'score': self.score,
            'total_questions': self.total_questions,
            'correct_answers': self.correct_answers,
            'played_at': self.played_at.isoformat()
        }


API_URL = 'https://opentdb.com/api.php'


def fetch_questions(amount=10, category=None, difficulty=None):
    params = {
        'amount': amount,
        'type': 'multiple'
    }
    if category:
        params['category'] = category
    if difficulty:
        params['difficulty'] = difficulty

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get('response_code') != 0:
            return None

        questions = data.get('results', [])
        for q in questions:
            answers = q['incorrect_answers'] + [q['correct_answer']]
            random.shuffle(answers)
            q['shuffled_answers'] = answers

        return questions
    except requests.RequestException:
        return None


CATEGORIES = [
    {'id': 9, 'name': 'General Knowledge'},
    {'id': 17, 'name': 'Science & Nature'},
    {'id': 18, 'name': 'Computer Science'},
    {'id': 21, 'name': 'Sports'},
    {'id': 22, 'name': 'Geography'},
    {'id': 23, 'name': 'History'},
    {'id': 25, 'name': 'Art'},
    {'id': 27, 'name': 'Animals'},
]


@app.route('/')
def index():
    return render_template('index.html', categories=CATEGORIES)


@app.route('/play', methods=['POST'])
def play():
    player_name = request.form.get('player_name', 'Player').strip()
    category = request.form.get('category', '')
    difficulty = request.form.get('difficulty', '')

    category_int = int(category) if category else None
    difficulty = difficulty if difficulty in ['easy', 'medium', 'hard'] else None

    questions = fetch_questions(
        amount=10,
        category=category_int,
        difficulty=difficulty
    )

    if not questions:
        return render_template('error.html', message='Failed to fetch questions. Please try again.')

    session['questions'] = questions
    session['player_name'] = player_name
    session['current_question'] = 0
    session['score'] = 0
    session['correct_answers'] = 0
    session['answers'] = []

    return redirect(url_for('question'))


@app.route('/question')
def question():
    questions = session.get('questions', [])
    current = session.get('current_question', 0)

    if current >= len(questions):
        return redirect(url_for('results'))

    q = questions[current]
    return render_template('question.html', question=q, number=current + 1, total=len(questions))


@app.route('/answer', methods=['POST'])
def answer():
    questions = session.get('questions', [])
    current = session.get('current_question', 0)
    selected = request.form.get('answer', '')
    time_taken = int(request.form.get('time_taken', 10))

    if current >= len(questions):
        return redirect(url_for('results'))

    q = questions[current]
    correct = q['correct_answer']
    is_correct = selected == correct

    if is_correct:
        session['score'] += max(100 - (time_taken * 5), 10)
        session['correct_answers'] += 1

    session['answers'].append({
        'question': q['question'],
        'selected': selected,
        'correct': correct,
        'is_correct': is_correct
    })

    session['current_question'] = current + 1

    return render_template('answer.html', question=q, selected=selected, is_correct=is_correct)


@app.route('/next')
def next_question():
    return redirect(url_for('question'))


@app.route('/results')
def results():
    if 'questions' not in session:
        return redirect(url_for('index'))

    score = Score(
        player_name=session.get('player_name', 'Player'),
        category=session.get('questions', [{}])[0].get('category', 'Mixed'),
        difficulty=request.form.get('difficulty') if request.method == 'POST' else None,
        score=session.get('score', 0),
        total_questions=len(session.get('questions', [])),
        correct_answers=session.get('correct_answers', 0)
    )
    db.session.add(score)
    db.session.commit()

    percentage = int((session.get('correct_answers', 0) / len(session.get('questions', [1]))) * 100)

    return render_template(
        'results.html',
        score=score,
        percentage=percentage,
        answers=session.get('answers', [])
    )


@app.route('/leaderboard')
def leaderboard():
    scores = Score.query.order_by(Score.score.desc()).limit(20).all()
    return render_template('leaderboard.html', scores=scores)


@app.route('/api/scores')
def api_scores():
    scores = Score.query.order_by(Score.score.desc()).limit(50).all()
    return jsonify([s.to_dict() for s in scores])


@app.route('/api/categories')
def api_categories():
    return jsonify(CATEGORIES)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5005)
