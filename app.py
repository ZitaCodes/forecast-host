from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import subprocess
from datetime import datetime

app = Flask(__name__)
CORS(app, origins=["https://bookmkttool.vercel.app"])

# ===== ROUTE 1: TrendTracker Tropes Panels =====
@app.route('/tropes')
def get_tropes():
    json_file = 'trendtracker_output.json'
    if not os.path.exists(json_file):
        return jsonify({"timestamp": None, "tropes": [], "insight": {"trope": None, "blurb": "TrendTracker data not yet generated."}})

    with open(json_file, 'r') as f:
        data = json.load(f)

    top_trope = data['tropes'][0] if data['tropes'] else {}
    insight = {}
    if top_trope:
        insight = {
            "trope": top_trope["name"],
            "blurb": f'"{top_trope["name"].title()}" is trending in reader discussions this week.'
        }

    push_json_to_github(json_file)
    return jsonify({"timestamp": data["timestamp"], "tropes": data["tropes"], "insight": insight})

# ===== ROUTE 2: Reddit Forecast Panel =====
@app.route('/reddit-update')
def reddit_update():
    json_file = 'reddit_forecast_output.json'
    if not os.path.exists(json_file):
        return jsonify({"status": "No reddit forecast data available."})

    push_json_to_github(json_file)
    with open(json_file, 'r') as f:
        return jsonify(json.load(f))

# ===== ROUTE 3: Reader Personas Panel =====
@app.route('/reader-personas')
def reader_personas():
    file_path = os.path.join(os.path.dirname(__file__), 'personas_output.json')
    
    if not os.path.exists(file_path):
        return jsonify({
            "timestamp": None,
            "personas": [],
            "insight": {
                "persona": None,
                "blurb": "Reader personas data not yet generated. Please run the scraper."
            }
        })

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        data['personas'] = data['personas'][:4]  # limit to 4
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "Error occurred", "details": str(e)}), 500

# ===== ROUTE 3a: Reader Personas Panel work around before dedicated API is built=====
@app.route('/reader-personas-filtered')
def reader_personas_filtered():
    genre = request.args.get('genre', None)

    master_path = os.path.join(os.path.dirname(__file__), 'reader_personas_master.json')
    log_path = os.path.join(os.path.dirname(__file__), 'genre_log.txt')

    if not os.path.exists(master_path):
        return jsonify({"message": "Master persona file missing."}), 500

    with open(master_path, "r") as f:
        master_data = json.load(f)
        all_personas = master_data.get("personas", [])

    matched = []
    if genre:
        matched = [p for p in all_personas if genre.lower() in [t.lower() for t in p.get("tags", [])]]
        # Log input genre
        try:
            with open(log_path, "a") as log:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log.write(f"{timestamp},{genre}\n")
        except Exception as e:
            print("Logging error:", e)

    if not matched:
        fallback = random.sample(all_personas, min(4, len(all_personas)))
        return jsonify({
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": "We didn’t find any personas that perfectly match your book’s genre or tropes this time. But don’t worry — we’re expanding our reader persona pool weekly, so your next pull will likely reveal stronger matches.",
            "personas": fallback
        })

    result = random.sample(matched, min(4, len(matched)))
    return jsonify({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "personas": result
    })



# ===== ROUTE 4: Media Forecast Panel JSON Direct Access =====
@app.route('/media_forecast_output.json')
def serve_media_forecast_json():
    json_file = 'media_forecast_output.json'
    if not os.path.exists(json_file):
        return jsonify({"status": "No media forecast data available."})
    
    with open(json_file, 'r') as f:
        return jsonify(json.load(f))


# ===== SHARED COMMIT LOGIC =====
def push_json_to_github(filename):
    try:
        subprocess.run(["git", "config", "--global", "user.name", "RenderBot"])
        subprocess.run(["git", "config", "--global", "user.email", "render@bot.com"])

        # Initialize and add remote if necessary
        remote_url = "git@github.com:ZitaCodes/forecast-host.git"
        subprocess.run(["git", "remote", "get-url", "origin"], check=False)
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"])
            subprocess.run(["git", "remote", "add", "origin", remote_url])

        subprocess.run(["git", "add", filename])
        subprocess.run(["git", "commit", "-m", f"Auto-update {filename} via Render"])
        subprocess.run(["git", "push", "origin", "main"])

    except Exception as e:
        print("🚫 Git push failed:", e)

if __name__ == '__main__':
    import socket

    def find_open_port(start_port, max_tries=10):
        port = start_port
        for _ in range(max_tries):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('localhost', port)) != 0:
                    return port  # Port is free
                port += 1
        raise RuntimeError("No available ports found.")

    try:
        chosen_port = find_open_port(10000)
        print(f"✅ Using available port: {chosen_port}")
        app.run(host="0.0.0.0", port=chosen_port)
    except Exception as e:
        print("🚫 Failed to start app:", e)
