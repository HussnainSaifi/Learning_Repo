import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Relative package import fix
from src.vector_store import VectorStoreManager

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class RAGEngine:
    def __init__(self, vector_store: VectorStoreManager):
        self.vector_store = vector_store
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_name = "openai/gpt-oss-20b"

    def ask(self, user_query: str) -> str:
        matched_chunks = self.vector_store.query_similar_chunks(user_query, n_results=3)
        
        if not matched_chunks:
            return "Knowledge base mein koi relevant information nahi mili."

        context_text = "\n\n".join([chunk["content"] for chunk in matched_chunks])

        system_prompt = (
            "You are an enterprise HR & Operations AI assistant. "
            "You are given a Context extracted from company policy documents (in English). "
            "Answer the User's Question accurately using ONLY the provided Context. "
            "If the question is in Roman Urdu or Urdu, respond in clear Roman Urdu or Urdu."
        )
        
        user_prompt = f"--- CONTEXT START ---\n{context_text}\n--- CONTEXT END ---\n\nUser Question: {user_query}"

        response = self.groq_client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=250
        )

        return response.choices[0].message.content