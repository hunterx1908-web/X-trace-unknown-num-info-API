import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# Config
API_KEY = os.environ.get('API_KEY', '')
TARGET_API = 'https://lynx.mireiariosss.workers.dev/api/search'

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': '🚀 Active',
        'message': 'Lynx API Clone by @lynx_apis',
        'endpoint': '/api/search?number=PHONE_NUMBER',
        'example': '/api/search?number=9006640786',
        'methods': ['GET', 'POST'],
        'credit': 'Join: @lynx_apis'
    })

@app.route('/api/search', methods=['GET', 'POST', 'OPTIONS'])
def search():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    # Get number
    if request.method == 'GET':
        number = request.args.get('number')
    else:
        number = request.json.get('number') if request.is_json else None
    
    # Validate
    if not number:
        return jsonify({
            'success': False,
            'error': '❌ Phone number required!',
            'usage': 'GET /api/search?number=9006640786'
        }), 400
    
    # Clean number
    number = re.sub(r'[^0-9]', '', str(number))
    
    if len(number) != 10:
        return jsonify({
            'success': False,
            'error': '❌ Invalid number! Must be 10 digits'
        }), 400
    
    # Call actual API
    try:
        response = requests.get(
            f'{TARGET_API}/{number}',
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            },
            timeout=30
        )
        
        data = response.json()
        
        # Add our own metadata
        data['cloned_by'] = 'Vercel 🔥'
        data['source'] = 'Lynx API'
        data['api_key_used'] = '✅ Yes'
        
        # Extract unique numbers
        if data.get('success') and data.get('results'):
            unique_mobiles = list(set([
                r.get('mobile') for r in data['results'] 
                if r.get('mobile')
            ]))
            data['unique_mobiles'] = unique_mobiles
            data['total_unique'] = len(unique_mobiles)
        
        return jsonify(data), response.status_code
        
    except requests.exceptions.Timeout:
        return jsonify({
            'success': False,
            'error': '⏰ Request timeout'
        }), 504
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'💀 Error: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': '❌ 404 - Not Found',
        'available_endpoints': ['/api/search?number=X']
    }), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({
        'success': False,
        'error': '💀 Internal Server Error'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)