import datetime
from src.vector_store import VectorStoreManager

# Global Vector Store Instance for Tools
v_store = VectorStoreManager()

def query_company_policy(query: str) -> str:
    """
    Company ki HR aur Operations Policy ke hawale se questions ka answer search karta hai.
    """
    matched_chunks = v_store.query_similar_chunks(query, n_results=3)
    if not matched_chunks:
        return "No relevant information found in company policy."
    
    return "\n\n".join([chunk["content"] for chunk in matched_chunks])

def get_current_time() -> str:
    """
    Current date and server time return karta hai.
    """
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# Groq API ko Pass hone wala Tool Specifications JSON Schema
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "query_company_policy",
            "description": "Searches and retrieves relevant policy details from company policy documents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The policy topic or search question in English."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Returns the current date and time of the server system.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]