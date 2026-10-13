
# Enterprise RAG System (Retrieval-Augmented Generation)

A backend pipeline designed to ground Large Language Models (LLMs) with private enterprise documentation, eliminating hallucinations using deterministic system design.

---

## 🚀 Key Architecture & Features

- **Vector Search Engine:** Built using ChromaDB with Cosine Similarity for fast semantic retrieval.
- **Chunking Pipeline:** Splits large enterprise documents into context-aware chunks with overlap strategy.
- **Zero Hallucination Control:** Enforces `Temperature = 0.0` and strict system role guardrails.
- **FastAPI Backend:** Asynchronous REST API ready for enterprise integration.

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI / Uvicorn
- **Vector Database:** ChromaDB
- **Embeddings:** Sentence-Transformers / Hugging Face
- **LLM Provider:** Groq API (Llama-3)

---
