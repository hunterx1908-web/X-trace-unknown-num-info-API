import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔑 Sirf Teri API Key
VALID_KEY = "@x_TRACEOWNER"

# Original API
ORIGINAL_API_URL = "https://lynx.mireiariosss.workers.dev/api/search"

@app.route('/')
def home():
    return jsonify({
        "status": True,
        "message": "Lynx Number Info API is working!",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER"
    })

@app.route('/api/search')
def lynx_search():
    key = request.args.get('key')
    number = request.args.get('number')
    
    # 🔐 Key verify
    if key != VALID_KEY:
        return jsonify({"status": False, "error": "Invalid API Key!"}), 401
    
    if not number:
        return jsonify({"status": False, "error": "Missing 'number' parameter!"}), 400
    
    # Clean number
    number = number.strip().replace(" ", "").replace("+", "")
    if number.startswith("91") and len(number) == 12:
        number = number[2:]
    
    if not number.isdigit() or len(number) != 10:
        return jsonify({"status": False, "error": "Invalid phone number!"}), 400
    
    # 🔥 Sirf forward — kuch extra nahi
    try:
        response = requests.get(f"{ORIGINAL_API_URL}/{number}", timeout=10)
        data = response.json()
        
        # Sirf join: @lynx_apis hatao
        data.pop('join', None)
        
        return jsonify(data)
        
    except:
        return jsonify({"status": False, "message": "No data found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))