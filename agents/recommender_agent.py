import os
from google import genai
from google.genai import types
from utils.prompts import RECOMMENDER_SYSTEM
from dotenv import load_dotenv
import json

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

def synthesize_plan(user_profile: dict, weather_summary: str, events: list, places: list, availability: dict):
    """
    availability: {"start": "09:00", "end": "21:00"} or full ISO datetimes
    events: list of {title, start, end, url, venue}
    places: list of place names (strings)
    """
    payload = {
        "user_profile": user_profile,
        "weather_summary": weather_summary,
        "events": events,
        "places": places,
        "availability": availability
    }
    prompt = f"""Create a personalized day plan using the following JSON payload. Output the plan as clear markdown with headings for Morning, Afternoon, and Evening. Include quick reasons and two alternate options at the end.

Payload:
{json.dumps(payload, indent=2)}
"""
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(system_instruction=RECOMMENDER_SYSTEM)
    )
    try:
        txt = resp.candidates[0].content.parts[0].text
    except Exception:
        txt = getattr(resp, "text", str(resp))
    return txt
