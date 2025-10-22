import os
import json
from datetime import datetime, timedelta

LOCAL_CAL_FILE = os.path.join(os.path.dirname(__file__), "../data/local_calendar.json")

def load_local_calendar():
    try:
        with open(LOCAL_CAL_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        now = datetime.now()
        return [
            {"title": "Morning Standup", "start": (now.replace(hour=9, minute=0)).isoformat(), "end": (now.replace(hour=9, minute=15)).isoformat(), "location": "Zoom"},
            {"title": "Deep Work (Project)", "start": (now.replace(hour=10, minute=0)).isoformat(), "end": (now.replace(hour=12, minute=0)).isoformat(), "location": "Home Office"},
            {"title": "Lunch with Sam", "start": (now.replace(hour=13, minute=0)).isoformat(), "end": (now.replace(hour=14, minute=0)).isoformat(), "location": "Local Cafe"},
        ]

def events_within_window(events, window_start, window_end):
    from dateutil import parser
    res = []
    for e in events:
        s = parser.parse(e["start"])
        en = parser.parse(e["end"])
        if (s < window_end) and (en > window_start):
            res.append(e)
    return res
