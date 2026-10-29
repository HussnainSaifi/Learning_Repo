from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.triage_engine import analyze_ticket, TriageResult

app = FastAPI(title="Customer Support Triage API", version="1.0")

class TicketRequest(BaseModel):
    message: str

@app.post("/triage", response_model=TriageResult)
def triage_customer_ticket(request: TicketRequest):
    try:
        result = analyze_ticket(request.message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "Triage API is running successfully!"}