# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# Movie & TV Reddit Discussions
@app.route("/reddit-media")
def get_reddit_forecast():
    try:
        with open("reddit_forecast.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Reader Personas (already working)
@app.route("/personas_output.json")
def get_personas_file():
    try:
        with open("personas_output.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
