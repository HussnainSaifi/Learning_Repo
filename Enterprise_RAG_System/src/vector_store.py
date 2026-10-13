import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any

class VectorStoreManager:
    def __init__(self, collection_name: str = "pdf_knowledge_base"):
        # Local Persistent Storage ke liye client (Memory loss se bachata hai)
        self.chroma_client = chromadb.Client()
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        
        # Collection Initialization
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )

    def add_chunks(self, chunks: List[str], source_filename: str = "company_policy.pdf"):
        """PDF chunks ko metadata aur unique IDs ke sath Vector DB mein inject karta hai."""
        ids = [f"{source_filename}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source": source_filename, "chunk_id": i} for i in range(len(chunks))]

        self.collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
        print(f"✅ Successfully indexed {len(chunks)} chunks into ChromaDB!")

    def query_similar_chunks(self, user_query: str, n_results: int = 2) -> List[Dict[str, Any]]:
        """User query ke aground sabse relevant chunks vector search se nikalta hai."""
        results = self.collection.query(
            query_texts=[user_query],
            n_results=n_results
        )
        
        retrieved_docs = []
        if results and results['documents']:
            for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
                retrieved_docs.append({
                    "content": doc,
                    "metadata": meta
                })
        return retrieved_docs

# Bottom section in src/vector_store.py
if __name__ == "__main__":
    from pathlib import Path
    from src.pdf_loader import PDFProcessor
    

    # 1. PDF Load & Chunking
    pdf_path = Path(__file__).resolve().parent.parent / "data" / "company_policy.pdf"
    processor = PDFProcessor(chunk_size=500, chunk_overlap=50)
    
    raw_text = processor.extract_text(pdf_path)
    chunks = processor.create_chunks(raw_text)

    # 2. Vector DB Indexing
    v_db = VectorStoreManager()
    v_db.add_chunks(chunks)

    # 3. Test Vector Search
    test_query = "What is the policy regarding leave or working hours?"
    matches = v_db.query_similar_chunks(test_query, n_results=1)
    
    print(f"\n❓ Test Query: {test_query}")
    print(f"🔍 Top Matched Chunk:\n{matches[0]['content']}")