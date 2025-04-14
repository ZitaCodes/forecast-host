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


import stripe  # add this near your other imports

# 🔐 Add your actual webhook secret key from Stripe Dashboard
stripe.api_key = "sk_test_xxxx"  # optional if using only webhooks
endpoint_secret = "we_1RDcwWKcBIwVNUGjYqrDfM5T"  # 👈 paste your webhook secret here

@app.route("/stripe-webhook", methods=["POST"])
def stripe_webhook():
    from flask import request
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        return "Invalid signature", 400

    # Only handle subscription events
    if event["type"] in [
        "checkout.session.completed",
        "customer.subscription.created",
        "customer.subscription.updated",
        "customer.subscription.deleted",
    ]:
        session = event["data"]["object"]
        email = session.get("customer_email") or session.get("customer_details", {}).get("email")
        price_id = session["items"]["data"][0]["price"]["id"] if "items" in session else None

        tier = {
            "price_1R8BRgKcBIwVNUGj4uZDYz2b": "Tier 1",  # replace with your real Stripe Price IDs
            "price_1RCWrsKcBIwVNUGjVanTTXxl": "Tier 2",
            "price_1RCWvwKcBIwVNUGjYDJdTR7R": "Tier 3",
        }.get(price_id, "Unknown")

        if email:
            with open("subscribers.json", "r") as f:
                subs = json.load(f)
            subs[email] = {"tier": tier, "timestamp": datetime.now().strftime("%m-%d-%Y %I:%M %p")}
            with open("subscribers.json", "w") as f:
                json.dump(subs, f, indent=2)

    return "", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
