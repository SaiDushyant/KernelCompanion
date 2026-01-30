import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_MODEL = "models/gemini-2.5-flash"


class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not found in environment")

        self.client = genai.Client(api_key=api_key)

    def generate_command(self, user_input: str, os_name: str = "Linux") -> str:
        prompt = f"""
You are a Linux command generation engine.

Rules:
- Respond ONLY in valid JSON
- No markdown
- No explanations outside JSON
- Prefer non-destructive commands

JSON format:
{{
  "intent": "",
  "primary_command": "",
  "alternatives": [],
  "risk_level": "low | medium | high",
  "explanation": ""
}}

User request: "{user_input}"
Operating System: {os_name}
Shell: bash
"""

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        return response.text
