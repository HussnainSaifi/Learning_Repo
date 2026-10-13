import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Available Models Fetch Karo
models = groq_client.models.list()
print("--- APKI API KEY KE LIYE AVAILABLE GROQ MODELS ---")
for m in models.data:
    print(f"- {m.id}")