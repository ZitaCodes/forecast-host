if __name__ == "__main__":
    forecast = get_reddit_forecast()
    with open("reddit_forecast.json", "w") as f:
        json.dump(forecast, f, indent=2)
