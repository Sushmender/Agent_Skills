"""
Quick test to verify the Gemini API key works using the Interactions API.
Run: .venv\\Scripts\\python.exe tests/test_gemini.py
"""
import os
import sys

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv

# Load .env from project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

# The Interactions API expects generation_config as a plain dict.
# thinking_level must be nested inside thinking_config.
generation_config = {
    "temperature": 1,
    "max_output_tokens": 1024,
    "top_p": 0.95,
    "thinking_config": {
        "thinking_level": "medium",
    },
}

print("Connecting to Gemini API...")
print("Sending test prompt...\n")

interaction = client.interactions.create(
    model="models/gemini-2.5-flash",
    input="Say hello and tell me one interesting fact about multi-agent AI systems in 2-3 sentences.",
    generation_config=generation_config,
)

print("Response received!\n")
print("-" * 60)
print(interaction.output_text)
print("-" * 60)
