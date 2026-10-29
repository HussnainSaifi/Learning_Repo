import os
import json
from groq import Groq
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Pydantic Schema for Structured JSON Output
class TriageResult(BaseModel):
    category: str = Field(description="Category of the ticket: Technical, Billing, or General")
    priority: str = Field(description="Priority level: High, Medium, or Low")
    summary: str = Field(description="A 1-sentence summary of the customer issue")
    draft_response: str = Field(description="A professional draft response to send back to the customer")

def analyze_ticket(customer_message: str) -> TriageResult:
    system_prompt = """
    You are an AI customer support triage assistant. Analyze the incoming customer message and classify it.
    You MUST return a valid JSON object with EXACTLY these four keys:
    1. "category" (string: e.g., "Billing", "Technical", "General")
    2. "priority" (string: e.g., "High", "Medium", "Low")
    3. "summary" (string: a short 1-sentence summary of the issue)
    4. "draft_response" (string: a polite professional draft response to the customer)

    Do not add any extra text or markdown blocks outside the JSON. Return raw JSON only.
    """

    user_payload = f"""
    <customer_message>
    {customer_message}
    </customer_message>
    """

# Calling LLM with Temperature = 0.0 for deterministic classification
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_payload}
        ],
        temperature=0.0,
        response_format={"type": "json_object"}
    )

    raw_content = response.choices[0].message.content
    parsed_data = json.loads(raw_content)
    
    return TriageResult(**parsed_data)