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
    # Set Git user
    subprocess.run(["git", "config", "--global", "user.name", "RenderBot"])
    subprocess.run(["git", "config", "--global", "user.email", "render@bot.com"])

    # Init Git repo if not already
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"])
        subprocess.run([
            "git", "remote", "add", "origin",
            "git@github.com:ZitaCodes/forecast-host.git"  # 👈 update per repo
        ])
    else:
        subprocess.run(["git", "remote", "set-url", "origin",
            "git@github.com:ZitaCodes/forecast-host.git"  # 👈 update per repo
        ])

    # Add, commit, push
    subprocess.run(["git", "add", "yourfile.json"])  # 👈 update for personas, reddit, etc.
    subprocess.run(["git", "commit", "-m", "Auto-update via Render"])
    subprocess.run(["git", "push", "origin", "main"])

except Exception as e:
    print("❌ Git push failed:", e)
