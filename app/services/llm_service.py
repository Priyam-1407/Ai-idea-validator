from google import genai
from app.config import settings
import json

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def analyze_startup_idea(title: str, description: str, industry: str | None) -> dict:
    prompt = f"""
You are a startup analyst. Analyze this startup idea and respond ONLY with valid JSON, no markdown, no extra text.

Startup Title: {title}
Description: {description}
Industry: {industry or "Not specified"}

Return JSON in exactly this structure:
{{
  "summary": "2-3 sentence summary of the idea",
  "competitors": ["Competitor 1", "Competitor 2", "Competitor 3"],
  "features": ["Feature 1", "Feature 2", "Feature 3", "Feature 4"],
  "revenue_model": "1-2 sentence revenue model suggestion",
  "risks": ["Risk 1", "Risk 2", "Risk 3"],
  "roadmap": ["MVP step 1", "MVP step 2", "MVP step 3"],
  "success_score": 7.5
}}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    raw_text = response.text.strip()

    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        raw_text = raw_text.replace("json", "", 1).strip()

    return json.loads(raw_text)