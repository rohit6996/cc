from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

# EB expects this variable
application = Flask(__name__)

DATA_FILE = 'items.json'

def load_items():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_items(items):
    with open(DATA_FILE, 'w') as f:
        json.dump(items, f, indent=2)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(load_items())

@application.route('/api/items', methods=['POST'])
def add_item():
    items = load_items()
    new_item = {
        'id': len(items)+1,
        'name': request.json.get('name'),
        'description': request.json.get('description'),
        'type': request.json.get('type'),
        'location': request.json.get('location'),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'contact': request.json.get('contact'),
        'status': request.json.get('status','Pending')
    }
    items.append(new_item)
    save_items(items)
    return jsonify(new_item), 201

if __name__ == '__main__':
    # Must bind to 0.0.0.0 and port 8080 for EB
    application.run(host='0.0.0.0', port=8080, debug=False)
