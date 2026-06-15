import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection(
    name="vit_knowledge"
)

while True:
    query = input("Query: ")

    if query.lower() == "exit":
        break

    results = collection.query(
        query_texts=[query],
        n_results=2
    )

    print("\nRESULTS:\n")

    for doc in results["documents"][0]:
        print(doc)
        print("-" * 40)