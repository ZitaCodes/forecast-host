import json
import subprocess
from datetime import datetime

# Step 1: Your scraped (mocked) data
persona_data = {
  "timestamp": datetime.now().strftime("%m-%d-%Y %I:%M %p"),
  "personas": [
    {
      "id": "persona-01",
      "label": "📚 Cozy Fantasy + Tea Aesthetic",
      "traits": [
        "enjoys slow-burn romance",
        "loves cozy fantasy books",
        "subscribes to book box services",
        "posts herbal tea reviews"
      ],
      "hashtags": [
        "#CozyReads",
        "#TeaAndBooks",
        "#SlowBurnFantasy"
      ],
      "trope_signals": [
        "slow burn",
        "found family",
        "magical cottagecore"
      ],
      "promo_tip": "Use calm, earthy visuals and soft tagline language. Frame your book as a comfort + escape."
    },
    {
      "id": "persona-02",
      "label": "💋 Spicy Romance + Skincare Babe",
      "traits": [
        "reads alpha male romance on Kindle Unlimited",
        "regularly reviews beauty boxes",
        "follows #BookTok influencers",
        "posts self-care content"
      ],
      "hashtags": [
        "#AlphaMale",
        "#RomanceReader",
        "#SkincareAddict"
      ],
      "trope_signals": [
        "possessive hero",
        "fated mates",
        "enemies to lovers"
      ],
      "promo_tip": "Use glam visuals and bold copy. Lead with desire + danger. Mention luxury or indulgent themes."
    },
    {
      "id": "persona-03",
      "label": "🏋🏾‍♀️ Fit & Fierce Dark Romance Fan",
      "traits": [
        "reads during treadmill workouts",
        "shares gym selfies & steamy books",
        "follows MMA fighters & mafia romance authors",
        "comments on dark FMC arcs"
      ],
      "hashtags": [
        "#DarkRomance",
        "#MafiaBooks",
        "#FitGirlsRead"
      ],
      "trope_signals": [
        "morally grey hero",
        "forced proximity",
        "redemption arc"
      ],
      "promo_tip": "Target energetic, dramatic hooks. Use dark/light contrast in your visuals. Lead with 'intensity meets intimacy'."
    }
  ]
}

# Step 2: Save data to file
with open("personas_output.json", "w") as f:
    f.write(json.dumps(persona_data, indent=2))

# Step 3: Auto-commit to GitHub
try:
    subprocess.run(["git", "config", "--global", "user.name", "RenderBot"])
    subprocess.run(["git", "config", "--global", "user.email", "render@bot.com"])
    subprocess.run(["git", "add", "personas_output.json"])
    subprocess.run(["git", "commit", "-m", "Update trending personas via Render worker"])
    subprocess.run(["git", "push", "origin", "main"])
except Exception as e:
    print("Git push failed:", e)
