import os
import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Gemini Client
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

print("\n🚀 VITAssist RAG v2 Started")
print("Type 'exit' to quit\n")

while True:
    question = input("You: ")

    if question.lower() == "exit":
        break

    # Retrieve top chunks
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

        print("\nBot:")
        print(response.text)
        print()

    except Exception as e:
        print("Error:", e)