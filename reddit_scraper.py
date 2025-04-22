import subprocess  # ✅ Added
import json
from datetime import datetime

def get_reddit_forecast():
    return {
        "last_updated": datetime.now().strftime("%m-%d-%Y"),
        "reddit_forecast": [
            {
                "title": "Dark Matter (Apple TV)",
                "trend_type": "Sci-Fi Thriller",
                "description": "Redditors are dissecting every scene of this multiverse story — perfect for fans of time loops and emotional what-ifs."
            },
            {
                "title": "Ripley",
                "trend_type": "Psychological Suspense",
                "description": "Everyone’s obsessing over the eerie atmosphere and morally gray anti-heroes — great for dark romance or dual-identity promo tie-ins."
            },
            {
                "title": "3 Body Problem",
                "trend_type": "Genre Crossover",
                "description": "Hard sci-fi meets deep human themes — Redditors are craving alien contact, survival ethics, and world-ending stakes."
            }
        ]
    }


if __name__ == "__main__":
    forecast = get_reddit_forecast()
    with open("reddit_forecast.json", "w") as f:
        json.dump(forecast, f, indent=2)

# Local Git commit (optional - no push)
try:
    subprocess.run(["git", "add", "trendtracker_output.json"], check=True)
    subprocess.run(["git", "commit", "-m", "Auto-update trendtracker_output.json"], check=True)
    print("✅ JSON file committed locally.")
except subprocess.CalledProcessError as e:
    print("⚠️ Git commit failed:", e)
