import streamlit as st
from openai import OpenAI
import json
import os

API_KEY = st.secrets.get("OPENROUTER_API_KEY") or os.environ.get("OPENROUTER_API_KEY")

if not API_KEY:
    raise Exception("OPENROUTER_API_KEY not configured.")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://ai-requirement-intelligence.streamlit.app",
        "X-Title": "AI Requirement Intelligence"
    }
)

def analyze_requirement(text):

    system_prompt = """
You are a senior software architect.

Return ONLY valid JSON in this exact structure:

{
  "executive_summary": "",
  "functional_requirements": [],
  "non_functional_requirements": [],
  "missing_requirements": [],
  "ambiguities": [],
  "technical_risks": [],
  "improvements": [],
  "ai_clarity_score": 0
}

Score must be between 0 and 100.
Do not include explanations outside JSON.
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.2
        )

        raw_output = response.choices[0].message.content.strip()

        try:
            return json.loads(raw_output)
        except json.JSONDecodeError:
            return {
                "error": "Model returned invalid JSON.",
                "raw_response": raw_output
            }

    except Exception as e:
        return {"error": str(e)}