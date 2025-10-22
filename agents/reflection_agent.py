import os
import uuid
import json
from google import genai
from google.genai import types
from utils.prompts import REFLECTION_SYSTEM
from dotenv import load_dotenv
from memory.memory_manager import MemoryManager

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

mem = MemoryManager()

def reflect_and_update(profile: dict, feedback_text: str, rating: int = None):
    """
    profile: current user profile dict
    feedback_text: freeform feedback from user
    rating: optional 1-5 int
    Returns: (delta_json, updated_profile_preview)
    """
    prompt = f"""Current profile:\n{json.dumps(profile)}\n\nUser feedback:\nRating: {rating}\nText: {feedback_text}\n\nProduce ONLY a JSON object that describes small changes to the profile (e.g. add to likes/dislikes, update energy_pattern). Do not output extra text."""
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(system_instruction=REFLECTION_SYSTEM)
    )
    try:
        delta_text = resp.candidates[0].content.parts[0].text
    except Exception:
        delta_text = getattr(resp, "text", "{}")
    # attempt to parse delta
    try:
        delta = json.loads(delta_text)
    except Exception:
        # fallback: put feedback into memory and return no structured delta
        delta = {"notes": f"unparsed_feedback: {feedback_text[:200]}"}
    # store feedback into vector memory
    safe_metadata = {
    "rating": str(rating) if rating is not None else "N/A",
    "delta_preview": json.dumps(delta) if isinstance(delta, dict) else str(delta or "")
}

    mem.add_memory(feedback_text, metadata=safe_metadata)
    mem.persist()
    # produce an updated preview (merge shallow)
    updated = profile.copy()
    for k, v in (delta.items() if isinstance(delta, dict) else []):
        updated[k] = v
    return delta, updated
