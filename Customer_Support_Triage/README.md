
# Automated Customer Support Ticket Triage System

An AI-powered backend service built with FastAPI and Groq LLMs that automatically categorizes support tickets, sets priority levels, generates concise summaries, and drafts professional responses using structured JSON outputs.

## 🚀 Key Features

- **Structured JSON Output:** Enforces strict Pydantic schemas to guarantee machine-readable responses.
- **Prompt Injection Defense:** Uses XML delimiters (`<customer_message>`) and instruction isolation.
- **Zero-Shot / Deterministic Execution:** Uses `Temperature = 0.0` for consistent classification.

## 🛠️ Tech Stack

- Python 3.10+
- FastAPI & Uvicorn
- Groq API (Llama-3)
- Pydantic v2

## ⚙️ Setup & Installation

1. Clone the repository and navigate to the folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
