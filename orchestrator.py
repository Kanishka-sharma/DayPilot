from agents.weather_agent import summarize_weather_with_gemini
from agents.news_agent import get_and_summarize_news
from agents.recommender_agent import synthesize_plan
from agents.calendar_agent import load_local_calendar, events_within_window
from agents.reflection_agent import reflect_and_update
from memory.memory_manager import MemoryManager
from datetime import datetime, timedelta
import uuid

mem = MemoryManager()

def create_daily_plan(user_profile: dict, city: str, availability: dict):
    # 1) Weather
    weather_summary = summarize_weather_with_gemini(city)

    # 2) Calendar events 
    events = load_local_calendar()

    # 3) Local places -> simple static list 
    places = ["City Museum", "Central Park", "Old Town Market", "Riverside Walk", "Main Mall"]

    # 4) Recommender to synthesize plan
    plan_text = synthesize_plan(user_profile, weather_summary, events, places, availability)

    # 5) Save the generated plan to memory as a "planning" event 
    mem.add_memory(plan_text, metadata={"type": "plan", "city": city, "created_at": datetime.utcnow().isoformat()})


    return {
        "plan_text": plan_text,
        "weather_summary": weather_summary,
        "events": events,
        "places": places
    }

def handle_feedback(user_profile: dict, feedback_text: str, rating: int = None):
    delta, updated = reflect_and_update(user_profile, feedback_text, rating)
    return {"delta": delta, "updated_profile": updated}
