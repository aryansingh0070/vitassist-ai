from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import chromadb
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI()

# CORS
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

# Create collection if missing
collection = chroma_client.get_or_create_collection(
    name="vit_knowledge"
)

@app.get("/")
def home():
    return {
        "message": "VITAssist API Running 🚀",
        "documents": collection.count()
    }

@app.get("/ask")
def ask(question: str):

    # Empty DB protection
    if collection.count() == 0:
        return {
            "question": question,
            "answer": "Knowledge base is empty. Please ingest documents first."
        }

    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    context = "\n\n".join(
        results["documents"][0]
    )

    context = context[:4000]

    prompt = f"""
You are VITAssist AI.

Answer ONLY from the provided context.

If the answer is not present in the context, reply:

I don't know based on the available documents.

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

        print("Gemini Error:", e)

        return {
            "question": question,
            "answer": context[:1000],
            "warning": "Gemini unavailable. Returning retrieved content."
        }