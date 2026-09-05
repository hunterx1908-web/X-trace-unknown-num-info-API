import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Original API
ORIGINAL_API_URL = "https://lynx.mireiariosss.workers.dev/api/search"

@app.route('/')
def home():
    return jsonify({
        "status": True,
        "message": "Lynx Number Info API is working!"
    })

@app.route('/api/search')
def lynx_search():
    number = request.args.get('number')
    
    if not number:
        return jsonify({"status": False, "error": "Missing 'number' parameter!"}), 400
    
    # 🔥 Sirf 10 digits
    number = number.strip().replace(" ", "").replace("+", "")
    
    # Agar 91 se start ho toh hata do
    if number.startswith("91") and len(number) == 12:
        number = number[2:]
    
    # Sirf 10 digits allow
    if not number.isdigit() or len(number) != 10:
        return jsonify({"status": False, "error": "Invalid phone number! Must be 10 digits."}), 400
    
    # 🔥 Forward to original API (with 91)
    try:
        response = requests.get(f"{ORIGINAL_API_URL}/91{number}", timeout=10)
        data = response.json()
        
        # Sirf join: @lynx_apis hatao
        data.pop('join', None)
        
        return jsonify(data)
        
    except:
        return jsonify({"status": False, "message": "No data found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))