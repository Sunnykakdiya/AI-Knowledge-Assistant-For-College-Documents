
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing from .env")

client = Groq(api_key=api_key)

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system",
            "content": "You are a helpful college knowledge assistant."
        },
        {
            "role": "user",
            "content": "Reply with: Groq connection successful."
        },
    ],
    temperature=0,
    max_completion_tokens=100,
)

print("Groq API connection successful.")
print("Model:", response.model)
print("Response:", response.choices[0].message.content)
