import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="vit_knowledge"
)

with open("data/vit_info.txt", "r") as f:
    data = f.read()

chunks = data.split("\n\n")

for i, chunk in enumerate(chunks):
    collection.add(
        documents=[chunk],
        ids=[f"chunk_{i}"]
    )

print(f"✅ Stored {len(chunks)} chunks")