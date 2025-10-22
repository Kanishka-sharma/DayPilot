import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import streamlit as st
from dotenv import load_dotenv
import os
from orchestrator import create_daily_plan, handle_feedback
from memory.memory_manager import MemoryManager
from agents.news_agent import get_and_summarize_news
from agents.weather_agent import summarize_weather_with_gemini
import json
from datetime import datetime, timedelta

load_dotenv()

st.set_page_config(page_title="DayPilot", layout="wide")
st.title(" DayPilot")

# Simple persistent user profile on disk
PROFILE_PATH = "user_profile.json"
if not os.path.exists(PROFILE_PATH):
    sample_profile = {
        "name": "Kanishka Sharma",
        "preferences": {
            "likes": ["jogging", "coffee", "museums"],
            "dislikes": ["crowded areas"],
            "energy_pattern": "high in mornings",
            "goals": ["improve focus", "stay fit"]
        },
        "history": []
    }
    with open(PROFILE_PATH, "w") as f:
        json.dump(sample_profile, f, indent=2)

with open(PROFILE_PATH, "r") as f:
    user_profile = json.load(f)

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Home", "Weather", "News", "Smart Planner", "Memory & Feedback"])
st.sidebar.markdown("---")
st.sidebar.write(f"User: **{user_profile.get('name','User')}**")
st.sidebar.markdown("---")

if page == "Home":
    st.subheader("A Thought for Your Day")
    st.info('"Small consistent steps build the best routines."')
    st.write("Use the sidebar to navigate. DayPilot remembers your feedback and improves over time.")

elif page == "Weather":
    st.header("Weather")
    city = st.text_input("City", value="London")
    if st.button("Get weather"):
        with st.spinner("Fetching..."):
            summary = summarize_weather_with_gemini(city)
        st.markdown("**Weather summary**")
        st.write(summary)

elif page == "News":
    st.header("News by Interest")
    topic = st.text_input("Topic", value="Technology")
    if st.button("Fetch news"):
        with st.spinner("Fetching news..."):
            articles = get_and_summarize_news(topic)
        if isinstance(articles, dict) and articles.get("error"):
            st.error(articles.get("error"))
        else:
            for a in articles:
                st.markdown(f"### {a['title']}")
                if a.get("image"):
                    st.image(a["image"], width=250)
                st.write(a["summary"])
                st.markdown(f"[Read original]({a['url']})")
                st.markdown("---")

elif page == "Smart Planner":
    st.header("Smart Planner")
    city = st.text_input("City for planning", value="London")
    start_time = st.time_input("Available from", value=datetime.now().replace(hour=9, minute=0).time())
    end_time = st.time_input("Available until", value=datetime.now().replace(hour=21, minute=0).time())
    if st.button("Generate Plan"):
        availability = {"start": start_time.isoformat(), "end": end_time.isoformat()}
        with st.spinner("Generating personalized plan..."):
            result = create_daily_plan(user_profile, city, availability)
        st.subheader("Weather")
        st.write(result["weather_summary"])
        st.subheader("Plan")
        st.write(result["plan_text"])
        st.subheader("Calendar events considered")
        for e in result["events"]:
            st.write(f"- {e.get('title')} ({e.get('start')})")

        # quick feedback widget
        st.markdown("---")
        st.subheader("How was this plan?")
        rating = st.slider("Rate (1-5)", 1, 5, 4)
        feedback_text = st.text_area("Feedback (what to change / what you liked):")
        if st.button("Submit feedback"):
            with st.spinner("Reflecting and updating profile..."):
                out = handle_feedback(user_profile, feedback_text, rating)
                # update local profile file with merged preview (simple shallow merge)
                user_profile.update(out.get("updated_profile", {}))
                with open(PROFILE_PATH, "w") as f:
                    json.dump(user_profile, f, indent=2)
            st.success("Thanks! Feedback recorded and profile updated (preview).")

elif page == "Memory & Feedback":
    st.header("Memory insights")
    mm = MemoryManager()
    query = st.text_input("Query memory (e.g., 'likes', 'yoga', 'traffic')", value="yoga")
    if st.button("Search memory"):
        res = mm.retrieve_similar(query, k=5)
        if not res:
            st.write("No memories found.")
        for r in res:
            st.write("—", r["document"])
            st.write("metadata:", r["metadata"])
            st.markdown("---")
