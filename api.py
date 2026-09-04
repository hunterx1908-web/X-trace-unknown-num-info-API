from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Your test key
API_KEY = "@x_TRACEOWNER"

# Harmless public demo API
DEMO_API = "https://lynx.mireiariosss.workers.dev/api/search"


@app.route("/")
def home():
    return jsonify({
        "success": True,
        "message": "X-Trace Testing API is online"
    })


@app.route("/api/search", methods=["GET"])
def search():
    key = request.args.get("key")
    query = request.args.get("query")

    # API key check
    if key != API_KEY:
        return jsonify({
            "success": False,
            "message": "Invalid API key"
        }), 401

    if not query:
        return jsonify({
            "success": False,
            "message": "Query is required"
        }), 400

    try:
        response = requests.get(
            DEMO_API,
            timeout=10
        )

        response.raise_for_status()

        demo_data = response.json()

        return jsonify({
            "success": True,
            "query": query,
            "data": demo_data
        })

    except requests.RequestException as e:
        return jsonify({
            "success": False,
            "message": "Upstream API error"
        }), 502


if __name__ == "__main__":
    app.run()