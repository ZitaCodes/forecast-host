# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
import json  # 👈 THIS LINE IS THE FIX


app = Flask(__name__)
CORS(app)

@app.route("/reddit-media")
def get_reddit_forecast():
    with open("reddit_forecast.json", "r") as f:
        data = json.load(f)
    return jsonify(data)


@app.route("/personas_output.json")
def get_personas_file():
    with open("personas_output.json", "r") as f:
        data = json.load(f)
    return jsonify(data)



if __name__ == "__main__":
   import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

