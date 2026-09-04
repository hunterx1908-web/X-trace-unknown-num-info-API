import os
import requests
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# 🔑 Teri API Key
VALID_KEY = "@x_TRACEOWNER"

# Original API details
ORIGINAL_API_URL = "https://lynx.mireiariosss.workers.dev/api/search"

# 🔥 API Expiry Date
API_EXPIRY = "2099-11-05"

def is_expired():
    try:
        expiry = datetime.strptime(API_EXPIRY, "%Y-%m-%d")
        return datetime.utcnow() > expiry
    except:
        return False

@app.route('/')
def home():
    return jsonify({
        "status": True,
        "message": "Unknown Number Info API is working! (X-TRACE Edition)",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER",
        "expires_on": API_EXPIRY,
        "status": "Active" if not is_expired() else "Expired",
        "endpoints": {
            "info": "/api/search?key=YOUR_KEY&number=PHONE_NUMBER"
        },
        "example": "/api/search?key=@x_TRACEOWNER&number=9006640786"
    })

@app.route('/api/search')
def lynx_search():
    if is_expired():
        return jsonify({
            "status": False,
            "error": f"API expired on {API_EXPIRY}! Please contact support.",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER",
            "expires_on": API_EXPIRY
        }), 401
    
    key = request.args.get('key')
    number = request.args.get('number')
    
    if not key:
        return jsonify({"status": False, "error": "Missing API Key!", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 400
        
    if key != VALID_KEY:
        return jsonify({"status": False, "error": "Invalid API Key!", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 401
    
    if not number:
        return jsonify({"status": False, "error": "Missing 'number' parameter!", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 400
    
    number = number.strip().replace(" ", "").replace("+", "")
    if number.startswith("91") and len(number) == 12:
        number = number[2:]
    
    if not number.isdigit() or len(number) != 10:
        return jsonify({"status": False, "error": "Invalid phone number! Must be 10 digits.", "developer": "@x_TRACEOWNER", "credit": "@x_TRACEOWNER"}), 400
    
    try:
        response = requests.get(f"{ORIGINAL_API_URL}/{number}", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, dict):
            # Remove join: @lynx_apis
            data.pop('join', None)
            data.pop('developer', None)
            data.pop('credit', None)
            
            # Check if data exists
            if not data.get('results') or data.get('total') == 0:
                return jsonify({
                    "status": False,
                    "message": "No data found",
                    "developer": "@x_TRACEOWNER",
                    "credit": "@x_TRACEOWNER"
                }), 404
            
            # Add our branding
            data['developer'] = '@x_TRACEOWNER'
            data['credit'] = '@x_TRACEOWNER'
            data['api_expires_on'] = API_EXPIRY
            
        return jsonify(data)
        
    except requests.exceptions.Timeout:
        return jsonify({
            "status": False,
            "message": "Request timeout. Please try again later.",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 504
        
    except requests.exceptions.ConnectionError:
        return jsonify({
            "status": False,
            "message": "No data found",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 404
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": False,
            "message": "No data found",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 404
        
    except Exception as e:
        return jsonify({
            "status": False,
            "message": "No data found",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 404

@app.route('/api/search/<path:path>')
def catch_all(path):
    return jsonify({
        "status": False,
        "message": "No data found",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER"
    }), 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": False,
        "message": "No data found",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": False,
        "message": "No data found",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER"
    }), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))