from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'api-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
CORS(app)
jwt = JWTManager(app)

items = [
    {'id': 1, 'name': 'Item One', 'description': 'First sample item', 'price': 19.99, 'created_at': '2026-01-01T10:00:00'},
    {'id': 2, 'name': 'Item Two', 'description': 'Second sample item', 'price': 29.99, 'created_at': '2026-01-02T10:00:00'},
]
next_id = 3

def api_response(data=None, message='Success', status=200):
    return jsonify({'success': True, 'message': message, 'data': data}), status

def error_response(message='Error', status=400):
    return jsonify({'success': False, 'message': message, 'data': None}), status

@app.route('/')
def index():
    return api_response({'message': 'Flask REST API', 'version': '1.0'})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return error_response('Username and password required')
    token = create_access_token(identity=data['username'])
    return api_response({'token': token, 'expires_in': 86400})

@app.route('/api/items', methods=['GET'])
@jwt_required()
def get_items():
    return api_response(items)

@app.route('/api/items/<int:item_id>', methods=['GET'])
@jwt_required()
def get_item(item_id):
    item = next((i for i in items if i['id'] == item_id), None)
    if item:
        return api_response(item)
    return error_response('Item not found', 404)

@app.route('/api/items', methods=['POST'])
@jwt_required()
def create_item():
    global next_id
    data = request.get_json()
    if not data or 'name' not in data:
        return error_response('Name is required')
    item = {
        'id': next_id,
        'name': data['name'],
        'description': data.get('description', ''),
        'price': data.get('price', 0.0),
        'created_at': datetime.utcnow().isoformat()
    }
    items.append(item)
    next_id += 1
    return api_response(item, 'Item created', 201)

@app.route('/api/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    item = next((i for i in items if i['id'] == item_id), None)
    if not item:
        return error_response('Item not found', 404)
    data = request.get_json()
    if not data:
        return error_response('Request body required')
    item.update({k: v for k, v in data.items() if k in ['name', 'description', 'price']})
    return api_response(item, 'Item updated')

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    global items
    item = next((i for i in items if i['id'] == item_id), None)
    if not item:
        return error_response('Item not found', 404)
    items = [i for i in items if i['id'] != item_id]
    return api_response(None, 'Item deleted')

@app.errorhandler(404)
def not_found(e):
    return error_response('Endpoint not found', 404)

@app.errorhandler(500)
def server_error(e):
    return error_response('Internal server error', 500)

if __name__ == '__main__':
    app.run(debug=True)
