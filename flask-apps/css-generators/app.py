"""
CSS Generators - Flask Application
5 CSS generator tools: Gradient, Box Shadow, Button, Card, Animation
"""
from flask import Flask, render_template, request, jsonify, send_file
import random
import string

app = Flask(__name__)
app.secret_key = 'css-generators-secret-key-2024'


def generate_random_id():
    """Generate a random ID for preview elements"""
    return 'gen_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))


# ============ GRADIENT GENERATOR ============
@app.route('/gradient')
def gradient():
    return render_template('gradient.html', active_tab='gradient')


# ============ BOX SHADOW GENERATOR ============
@app.route('/box-shadow')
def box_shadow():
    return render_template('box-shadow.html', active_tab='box-shadow')


# ============ BUTTON GENERATOR ============
@app.route('/button')
def button():
    return render_template('button.html', active_tab='button')


# ============ CARD GENERATOR ============
@app.route('/card')
def card():
    return render_template('card.html', active_tab='card')


# ============ ANIMATION GENERATOR ============
@app.route('/animation')
def animation():
    return render_template('animation.html', active_tab='animation')


# ============ HOME / ALL GENERATORS ============
@app.route('/')
def index():
    return render_template('index.html', active_tab='home')


# ============ API ENDPOINTS ============
@app.route('/api/generate-id')
def api_generate_id():
    """Generate a unique ID for preview elements"""
    return jsonify({'id': generate_random_id()})


if __name__ == '__main__':
    print("\n" + "="*50)
    print("  CSS Generators")
    print("="*50)
    print("  Running at: http://127.0.0.1:5000")
    print("  Available routes:")
    print("    /           - All generators")
    print("    /gradient   - Gradient generator")
    print("    /box-shadow - Box shadow generator")
    print("    /button     - Button style generator")
    print("    /card       - Card generator")
    print("    /animation  - Animation generator")
    print("="*50 + "\n")
    app.run(debug=True, host='127.0.0.1', port=5000)
