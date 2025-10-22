# agents/news_agent.py
import os
from google import genai
from google.genai import types
from utils.api_wrappers import fetch_news
from utils.prompts import NEWS_SUMMARY_SYSTEM
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

def get_and_summarize_news(topic: str, limit: int = 5):
    articles = fetch_news(topic, page_size=limit)
    if isinstance(articles, dict) and articles.get("error"):
        return {"error": articles.get("error")}
    summaries = []
    for a in articles[:limit]:
        title = a.get("title")
        description = a.get("description") or ""
        url = a.get("url")
        text_input = f"Title: {title}\nDescription: {description}\nURL: {url}\n\nSummarize:"
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=text_input,
            config=types.GenerateContentConfig(system_instruction=NEWS_SUMMARY_SYSTEM)
        )
        try:
            s = resp.candidates[0].content.parts[0].text
        except Exception:
            s = getattr(resp, "text", "")
        summaries.append({"title": title, "url": url, "summary": s, "image": a.get("urlToImage")})
    return summaries
