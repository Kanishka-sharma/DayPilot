import os
from google import genai
from google.genai import types
import json
from utils.api_wrappers import fetch_weather
from utils.prompts import WEATHER_SYSTEM
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

def summarize_weather_with_gemini(city: str):
    raw = fetch_weather(city)
    if not isinstance(raw, dict):
        return "Could not fetch weather data."
    if raw.get("cod") == "404":
        return f"City {city} not found."
    # pass JSON as text to Gemini
    content = f"City: {city}\n\nWeather JSON:\n{json.dumps(raw)}"
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=content,
        config=types.GenerateContentConfig(system_instruction=WEATHER_SYSTEM)
    )
    text = None
    # support both response shapes
    try:
        text = resp.candidates[0].content.parts[0].text
    except Exception:
        text = getattr(resp, "text", str(resp))
    return text
