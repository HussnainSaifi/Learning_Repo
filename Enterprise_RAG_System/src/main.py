from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.agent_engine import AgentEngine

# 1. FastAPI App Initialization
app = FastAPI(
    title="Enterprise Agentic AI API",
    description="Production-Grade API leveraging Agentic AI with Tool Calling & RAG Capabilities",
    version="2.0.0"
)

# Global Agent Engine State
agent_engine = None

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str

@app.on_event("startup")
def startup_event():
    global agent_engine
    print("🚀 Initializing Enterprise Agentic AI Engine on Startup...")
    agent_engine = AgentEngine()
    print("✅ Agentic AI Engine Ready for Tool Calling Requests!")

@app.get("/")
def health_check():
    return {"status": "online", "message": "Enterprise Agentic AI Service is running smoothly!"}

@app.post("/api/v1/query", response_model=QueryResponse)
def query_agent(request: QueryRequest):
    if not agent_engine:
        raise HTTPException(status_code=500, detail="Agent Engine initialize nahi hua.")
    
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question empty nahi ho sakta.")

    answer = agent_engine.run(request.question)
    return QueryResponse(question=request.question, answer=answer)