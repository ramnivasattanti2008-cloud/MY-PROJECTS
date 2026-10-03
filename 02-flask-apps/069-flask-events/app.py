from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = 'events.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS events
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     title TEXT NOT NULL,
                     description TEXT,
                     event_date TEXT NOT NULL,
                     event_time TEXT,
                     location TEXT,
                     created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')

    conn.execute('''CREATE TABLE IF NOT EXISTS rsvps
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     event_id INTEGER NOT NULL,
                     name TEXT NOT NULL,
                     email TEXT,
                     status TEXT DEFAULT 'attending',
                     created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                     FOREIGN KEY (event_id) REFERENCES events(id))''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    view = request.args.get('view', 'list')
    month = request.args.get('month')
    year = request.args.get('year')

    now = datetime.now()
    if not month:
        month = now.strftime('%m')
    if not year:
        year = now.strftime('%Y')

    conn = get_db()

    if view == 'calendar':
        # Get events for the selected month
        events = conn.execute('''
            SELECT * FROM events
            WHERE strftime('%m', event_date) = ? AND strftime('%Y', event_date) = ?
            ORDER BY event_date, event_time
        ''', (month, year)).fetchall()
    else:
        # List view - upcoming events
        today = datetime.now().strftime('%Y-%m-%d')
        events = conn.execute('''
            SELECT * FROM events
            WHERE event_date >= ?
            ORDER BY event_date, event_time
        ''', (today,)).fetchall()

    # Get event counts
    event_counts = {}
    cursor = conn.execute('SELECT event_id, COUNT(*) FROM rsvps WHERE status="attending" GROUP BY event_id')
    for row in cursor:
        event_counts[row['event_id']] = row[1]

    conn.close()

    # Calendar data
    if view == 'calendar':
        month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        month_name = month_names[int(month)]

        # Calculate prev/next month
        prev_month = int(month) - 1 if int(month) > 1 else 12
        prev_year = int(year) if int(month) > 1 else int(year) - 1
        next_month = int(month) + 1 if int(month) < 12 else 1
        next_year = int(year) if int(month) < 12 else int(year) + 1

        # Days in month and starting weekday
        days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if int(year) % 4 == 0:
            days_in_month[2] = 29

        first_day = datetime(int(year), int(month), 1).weekday()
        calendar_data = {
            'month': month,
            'year': year,
            'month_name': month_name,
            'days_in_month': days_in_month[int(month)],
            'first_day': first_day,
            'prev_month': prev_month,
            'prev_year': prev_year,
            'next_month': next_month,
            'next_year': next_year
        }
    else:
        calendar_data = None

    return render_template('index.html', events=events, event_counts=event_counts,
                         view=view, calendar_data=calendar_data)

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    conn = get_db()
    event = conn.execute('SELECT * FROM events WHERE id=?', (event_id,)).fetchone()

    rsvps = conn.execute('''
        SELECT * FROM rsvps WHERE event_id=? ORDER BY status, created_at
    ''', (event_id,)).fetchall()

    attending = [r for r in rsvps if r['status'] == 'attending']
    maybe = [r for r in rsvps if r['status'] == 'maybe']
    not_attending = [r for r in rsvps if r['status'] == 'not_attending']

    conn.close()
    return render_template('event_detail.html', event=event, attending=attending,
                         maybe=maybe, not_attending=not_attending)

@app.route('/create', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        event_date = request.form['event_date']
        event_time = request.form['event_time']
        location = request.form['location']

        conn = get_db()
        conn.execute('INSERT INTO events (title, description, event_date, event_time, location) VALUES (?, ?, ?, ?, ?)',
                    (title, description, event_date, event_time, location))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create_event.html')

@app.route('/rsvp/<int:event_id>', methods=['POST'])
def rsvp(event_id):
    name = request.form['name']
    email = request.form.get('email', '')
    status = request.form['status']

    conn = get_db()
    conn.execute('INSERT INTO rsvps (event_id, name, email, status) VALUES (?, ?, ?, ?)',
                (event_id, name, email, status))
    conn.commit()
    conn.close()
    return redirect(url_for('event_detail', event_id=event_id))

@app.route('/delete/<int:event_id>')
def delete_event(event_id):
    conn = get_db()
    conn.execute('DELETE FROM rsvps WHERE event_id=?', (event_id,))
    conn.execute('DELETE FROM events WHERE id=?', (event_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
