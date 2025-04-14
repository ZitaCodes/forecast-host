import json
from datetime import datetime

def get_personas():
    return {
        "timestamp": datetime.now().strftime("%m-%d-%Y"),
        "personas": [
            {
                "label": "The Netflix Binger",
                "traits": "Marathon-watcher, introvert, loves bingeable series",
                "trope_signals": ["slow burn", "found family"],
                "hashtags": ["#bingeworthy", "#weekendread"],
                "promo_tip": "Use phrases like 'just one more chapter' and compare your book to popular Netflix hits."
            },
            {
                "label": "The Spice Addict",
                "traits": "Loves heat, alpha males, and dark romance",
                "trope_signals": ["possessive hero", "touch her and die"],
                "hashtags": ["#spicyread", "#alphamale", "#darkromance"],
                "promo_tip": "Lead with your heat level and tease one irresistible quote."
            }
        ]
    }

if __name__ == "__main__":
    data = get_personas()
    with open("personas_output.json", "w") as f:
        json.dump(data, f, indent=2)