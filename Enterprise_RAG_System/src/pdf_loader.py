import os
from pathlib import Path
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class PDFProcessor:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

    def extract_text(self, pdf_path: str) -> str:
        """Extracts all text from a given PDF file path."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found at path: {pdf_path}")
            
        reader = PdfReader(pdf_path)
        extracted_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        return extracted_text

    def create_chunks(self, raw_text: str):
        """Splits raw text into manageable chunks with overlap."""
        return self.text_splitter.split_text(raw_text)

# Local Quick Test
if __name__ == "__main__":
    sample_pdf = Path(__file__).resolve().parent.parent / "data" / "company_policy.pdf"
    processor = PDFProcessor()
    
    if os.path.exists(sample_pdf):
        text = processor.extract_text(sample_pdf)
        chunks = processor.create_chunks(text)
        print(f"✅ Extracted {len(text)} characters.")
        print(f"✂️ Total Chunks Created: {len(chunks)}")
    else:
        print(f"⚠️ Test PDF not found. Place a sample PDF in 'data/company_policy.pdf'")