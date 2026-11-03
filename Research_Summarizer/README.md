
📄 AI Research Paper & Article Summarizer

A production-ready, full-stack AI web application designed to automatically process, extract text from, and summarize long-form research papers, articles, and documents in PDF format using High-Speed LLMs via the Groq API.

🌟 Key Features

High-Performance Backend: Built with FastAPI for asynchronous, high-speed HTTP request handling.

Interactive Frontend: Built with Streamlit to offer a clean, responsive UI for document uploads and summary visualization.

Smart PDF Extraction: Robust PDF text parsing powered by pypdf.

API Abuse & Security Checks:

File format validation (statically enforcing .pdf).

File size limits to prevent server crashes.

IP-based rate limiting via slowapi to protect against spam and high API costs.

Groq SDK Integration: Connects to ultra-fast LLM models (e.g., Llama 3 / Mixtral) for instant, high-quality executive summaries.

🏗️ Architecture & Tech Stack

Language: Python 3.12+

Backend Framework: FastAPI, Uvicorn

Frontend Framework: Streamlit

AI Provider: Groq SDK / Groq Cloud API

PDF Engine: PyPDF

Security & Rate Limiting: SlowAPI, HTTPX, Python-Multipart

📁 Project Structure

Research_Summarizer/
├── src/
│   ├── __init__.py
│   ├── main.py          # FastAPI backend engine with rate limiting & security
│   └── summarizer.py    # LLM integration & prompt logic
├── app.py               # Streamlit frontend web interface
├── .env                 # Environment variables (API Keys) - Excluded from Git
├── .gitignore           # Git ignore configurations
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation

🚀 Local Setup & Installation Guide

Prerequisites

Python 3.10+ installed

Groq API Key (Get one for free at console.groq.com)

1. Clone the Repository

git clone https://github.com/YOUR_USERNAME/Research_Summarizer.git
cd Research_Summarizer

2. Set Up Virtual Environment

# Windows

python -m venv venv
venv\Scripts\activate

# macOS/Linux

python3 -m venv venv
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Configure Environment Variables

Create a .env file in the root directory:

GROQ_API_KEY=your_actual_groq_api_key_here

🏃 Running the Application

This app runs in two components (Backend API & Frontend UI).

Step 1: Start the FastAPI Backend

Open Terminal #1, activate venv, and run:

uvicorn src.main:app --reload

The backend will start on http://127.0.0.1:8000

Step 2: Start the Streamlit Frontend

Open Terminal #2, activate venv, and run:

streamlit run app.py

The frontend web app will automatically open in your default browser at http://localhost:8501.

🛡️ Security Features Implemented

Environment Key Isolation: API keys are never hardcoded or pushed to version control (.env protected via .gitignore).

Rate Limiting: Restricted to 5 requests per minute per IP to prevent quota depletion and DDoS attacks.

Payload Guardrails: Restricts file uploads exclusively to validated PDF formats under a specific file size threshold.

📄 License

This project is open-source and available under the MIT License.
