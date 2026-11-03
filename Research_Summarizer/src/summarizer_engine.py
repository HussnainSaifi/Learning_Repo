import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Groq client initialize karein
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chunk_text(text: str, max_chunk_size: int = 3000) -> list[str]:
    """
    Lambay text ko chunks mein divide karta hai taake LLM ki context limit cross na ho.
    """
    words = text.split()
    chunks = []
    current_chunk = []
    
    current_length = 0
    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1
        if current_length >= max_chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
            
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks

def summarize_chunk(chunk_text: str) -> str:
    """
    Aik single chunk ko summarize karne ke liye Groq API ko call karta hai.
    """
    system_prompt = "You are an expert research paper summarizer. Provide a concise, professional summary of the given text snippet highlighting key findings."
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": chunk_text}
        ],
        temperature=0.3
    )
    
    return response.choices[0].message.content

def generate_final_summary(full_text: str) -> str:
    """
    Pure document par chunking apply karta hai aur final summary compile karta hai.
    """
    chunks = chunk_text(full_text)
    
    # Agar document chhota hai aur 1 hi chunk hai
    if len(chunks) == 1:
        return summarize_chunk(chunks[0])
    
    # Agar lamba document hai toh har chunk ka summary nikal kar combine karenge
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1} of {len(chunks)}...")
        summary = summarize_chunk(chunk)
        chunk_summaries.append(summary)
        
    combined_summaries = "\n\n".join(chunk_summaries)
    
    # Final Reduce pass
    final_prompt = "Combine the following chunk summaries into a cohesive, well-structured final report with an Executive Summary and Key Takeaways."
    
    final_response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": final_prompt},
            {"role": "user", "content": combined_summaries}
        ],
        temperature=0.3
    )
    
    return final_response.choices[0].message.content