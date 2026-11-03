import os
from pypdf import PdfReader
from io import BytesIO

def extract_text_from_pdf(file_input) -> str:
    """
    PDF file (chahe file path ho ya uploaded file bytes) se saara text extract karta hai.
    """
    text = ""
    try:
        # Agar file path diya gaya ho ya binary stream ho
        reader = PdfReader(file_input)
        
        # Har page par loop chala kar text collect karein
        for page_index, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                
    except Exception as e:
        raise Exception(f"PDF read karne mein error aa gaya: {str(e)}")
        
    # Extra spaces ya formatting clean kar lein
    return text.strip()