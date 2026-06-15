from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import chromadb
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI()

# CORS Fix
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return {
        "message": "VITAssist API Running 🚀"
    }

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
You are VITAssist AI.

Answer ONLY from the provided context.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {
            "question": question,
            "answer": response.text
        }

    except Exception as e:
        return {
            "error": str(e)
        }