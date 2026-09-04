import os
from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")


@app.route("/api/search", methods=["GET"])
def search():
    key = request.args.get("key")
    query = request.args.get("query")

    # API key verification
    if not key or key != API_KEY:
        return jsonify({
            "success": False,
            "message": "Invalid API key"
        }), 401

    # Query validation
    if not query:
        return jsonify({
            "success": False,
            "message": "Query is required"
        }), 400

    # Safe demo response
    return jsonify({
        "success": True,
        "message": "Demo API response",
        "query": query,
        "data": {
            "id": "DEMO-001",
            "status": "active",
            "source": "demo"
        }
    })


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "Demo API is online"
    })


if __name__ == "__main__":
    app.run()