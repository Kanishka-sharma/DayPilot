import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def fetch_weather(city: str):
    """Return JSON from OpenWeather"""
    if not OPENWEATHER_API_KEY:
        return {"error": "OPENWEATHER_API_KEY not configured"}
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}"
    )
    resp = requests.get(url, timeout=10)
    return resp.json()

def fetch_news(topic: str, page_size: int = 5):
    """Return top news articles for a topic using NewsAPI """
    if not NEWSAPI_KEY:
        return {"error": "NEWSAPI_KEY not configured"}
    url = f"https://newsapi.org/v2/everything?q={topic}&pageSize={page_size}&sortBy=publishedAt&apiKey={NEWSAPI_KEY}"
    resp = requests.get(url, timeout=10)
    return resp.json().get("articles", [])

def fetch_events_serp(city: str, num=10):
    """Use SerpAPI to fetch local Google Events """
    if not SERPAPI_KEY:
        return {"error": "SERPAPI_KEY not configured"}
    url = f"https://serpapi.com/search.json?engine=google_events&q=Events in {city}&api_key={SERPAPI_KEY}"
    resp = requests.get(url, timeout=10)
    return resp.json()
