# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

URL = "https://www.imdb.com/calendar/?region=US&type=MOVIE"
HEADERS = {"User-Agent": "Mozilla/5.0"}

forecast_data = []

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.content, "html.parser")

# 🔁 New structure: each release block is inside an <article> with this testid
sections = soup.select("article[data-testid='calendar-section']")
print(f"📦 Found {len(sections)} release sections.")

for section in sections:
    date_header = section.select_one("h3.ipc-title__text")
    if not date_header:
        continue

    raw_date = date_header.text.strip()
    try:
        parsed_date = datetime.strptime(raw_date, "%b %d, %Y")
        us_date = parsed_date.strftime("%b %d, %Y")
    except Exception:
        us_date = raw_date

    movies = section.select("li[data-testid='coming-soon-entry'] img")
    print(f"📆 {raw_date}: {len(movies)} movies found")

    for movie in movies:
        title = movie.get("alt", "Untitled").strip()
        forecast_data.append({
            "source": "IMDb",
            "title": title,
            "release_date": us_date,
            "aligning_tropes": []  # We’ll fill this in again later!
        })

# Save to file
with open("forecast_output.json", "w") as f:
    json.dump({"forecasts": forecast_data}, f, indent=2)

print(f"✅ Scraped {len(forecast_data)} movies from IMDb!")
