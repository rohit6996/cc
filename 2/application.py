from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

# EB expects the Flask app variable to be named 'application'
application = Flask(__name__)

# File to store items
DATA_FILE = 'items.json'

# Utility functions to load/save items
def load_items():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_items(items):
    with open(DATA_FILE, 'w') as f:
        json.dump(items, f, indent=2)

# Home route
@application.route('/')
def index():
    return render_template('index.html')

# API to get all items
@application.route('/api/items', methods=['GET'])
def get_items():
    items = load_items()
    return jsonify(items)

# API to add a new item
@application.route('/api/items', methods=['POST'])
def add_item():
    items = load_items()
    
    new_item = {
        'id': len(items) + 1,
        'name': request.json.get('name'),
        'description': request.json.get('description'),
        'type': request.json.get('type'),
        'location': request.json.get('location'),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'contact': request.json.get('contact'),
        'status': request.json.get('status', 'Pending')
    }
    
    items.append(new_item)
    save_items(items)
    
    return jsonify(new_item), 201

# API to update item status
@application.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    items = load_items()
    
    for item in items:
        if item['id'] == item_id:
            item['status'] = request.json.get('status', item['status'])
            save_items(items)
            return jsonify(item)
    
    return jsonify({'error': 'Item not found'}), 404

# API to search items
@application.route('/api/items/search')
def search_items():
    query = request.args.get('q', '').lower()
    items = load_items()
    
    if query:
        filtered_items = [item for item in items 
                          if query in item['name'].lower() 
                          or query in item['description'].lower()
                          or query in item['location'].lower()]
    else:
        filtered_items = items
    
    return jsonify(filtered_items)

# Run the app on port 8080 for EB
if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080, debug=False)
