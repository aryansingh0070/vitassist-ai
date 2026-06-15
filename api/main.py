from fastapi import FastAPI
import chromadb
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI()

# Gemini
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ChromaDB
chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_collection(
    name="vit_knowledge"
)

@app.get("/")
def home():
    return {"message": "VITAssist API Running 🚀"}

@app.get("/ask")
def ask(question: str):

    results = collection.query(
        query_texts=[question],
        n_results=2
    )

    context = "\n\n".join(
        results["documents"][0]
    )

    prompt = f"""
Answer ONLY using the context below.

CONTEXT:
{context}

QUESTION:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {
        "question": question,
        "answer": response.text
    }