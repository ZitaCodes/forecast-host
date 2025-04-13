# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/reddit-forecast")
def reddit_forecast():
    data = {
        "last_updated": datetime.now().strftime("%m-%d-%Y"),
        "reddit_forecast": [
            {
                "title": "Dark Matter (Apple TV)",
                "trend_type": "Sci-Fi Thriller",
                "description": "Redditors are dissecting every scene of this multiverse story - perfect for fans of time loops and emotional what-ifs."
            },
            {
                "title": "Ripley",
                "trend_type": "Psychological Suspense",
                "description": "Everyone's obsessing over the eerie atmosphere and morally gray anti-heroes - great for dark romance or dual-identity promo tie-ins."
            },
            {
                "title": "3 Body Problem",
                "trend_type": "Genre Crossover",
                "description": "Hard sci-fi meets deep human themes - Redditors are craving alien contact, survival ethics, and world-ending stakes."
            }
        ]
    }
    return jsonify(data)

if __name__ == "__main__":
   import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

