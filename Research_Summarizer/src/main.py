from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from src.pdf_extractor import extract_text_from_pdf
from src.summarizer_engine import generate_final_summary
import io

app = FastAPI(
    title="Personal Research Paper & Article Summarizer Engine",
    description="Upload a research paper PDF and get an AI-powered executive summary and key takeaways.",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Welcome to the Research Summarizer API! Go to /docs to test file upload."}

@app.post("/summarize/")
async def summarize_research_paper(file: UploadFile = File(...)):
    """
    Research paper PDF upload karein aur AI-generated summary hasil karein.
    """
    # 1. Check karein ke file PDF hi hai ya nahi
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Sirf PDF files allow hain. Please valid PDF upload karein.")
    
    try:
        # 2. Uploaded file ka content bytes mein read karein
        contents = await file.read()
        file_stream = io.BytesIO(contents)
        
        # 3. PDF se text extract karein
        extracted_text = extract_text_from_pdf(file_stream)
        
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="PDF se text extract nahi ho saka. Yeh scanned image-based PDF lagti hai.")
        
        # 4. Groq API aur Summarizer engine ke zariye summary generate karein
        summary_result = generate_final_summary(extracted_text)
        
        # 5. Result return karein
        return JSONResponse(content={
            "filename": file.filename,
            "status": "success",
            "summary": summary_result
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing mein error aa gaya: {str(e)}")