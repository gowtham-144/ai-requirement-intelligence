from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

def analyze_requirement(text):

    system_prompt = """
You are a senior software architect.

Return ONLY valid JSON:

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

        return json.loads(response.choices[0].message.content)

    except Exception as e:
        return {"error": str(e)}
