import subprocess  # ✅ Added
import os
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
print("🔁 Starting auto-commit and push to GitHub...")

try:
    subprocess.run(["git", "config", "--global", "user.name", "RenderBot"])
    subprocess.run(["git", "config", "--global", "user.email", "render@bot.com"])
    
    # Force SSH for the remote URL (important!)
    subprocess.run(["git", "remote", "set-url", "origin", "git@github.com:ZitaCodes/forecast-host.git"])

    # Stage + commit JSON update
    subprocess.run(["git", "add", "trendtracker_output.json"])
    subprocess.run(["git", "commit", "-m", "✅ Auto-update trendtracker output via Render"])
    print("✅ Committed trendtracker_output.json locally")

    # Push to GitHub — this is the step we need to verify!
    push_result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)

    if push_result.returncode == 0:
        print("🚀 Git push succeeded.")
    else:
        print("❌ Git push failed.")
        print("STDOUT:", push_result.stdout)
        print("STDERR:", push_result.stderr)

except Exception as e:
    print("💥 Exception during Git operations:", e)
