from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Sample dashboard data
stats = {
    'total_users': 12543,
    'revenue': 89432,
    'orders': 3421,
    'growth': 12.5
}

charts_data = {
    'revenue_monthly': [12000, 15000, 18000, 22000, 19000, 25000, 28000, 32000, 35000, 38000, 42000, 48000],
    'users_monthly': [1200, 1450, 1680, 1920, 2100, 2450, 2800, 3100, 3450, 3800, 4200, 4600],
    'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
}

table_data = [
    {'id': 1, 'name': 'Alice Johnson', 'email': 'alice@example.com', 'status': 'Active', 'plan': 'Pro', 'joined': '2026-01-15'},
    {'id': 2, 'name': 'Bob Smith', 'email': 'bob@example.com', 'status': 'Active', 'plan': 'Enterprise', 'joined': '2026-02-20'},
    {'id': 3, 'name': 'Carol Williams', 'email': 'carol@example.com', 'status': 'Inactive', 'plan': 'Starter', 'joined': '2026-03-10'},
    {'id': 4, 'name': 'David Brown', 'email': 'david@example.com', 'status': 'Active', 'plan': 'Pro', 'joined': '2026-04-05'},
    {'id': 5, 'name': 'Eva Martinez', 'email': 'eva@example.com', 'status': 'Active', 'plan': 'Pro', 'joined': '2026-05-18'},
]

@app.route('/')
def index():
    return render_template('index.html', stats=stats, table_data=table_data)

@app.route('/api/chart-data')
def chart_data():
    return jsonify(charts_data)

@app.route('/users')
def users():
    return render_template('users.html', users=table_data)

@app.route('/analytics')
def analytics():
    return render_template('analytics.html', stats=stats)

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True)
