from pypdf import PdfReader
import chromadb
import os

# ChromaDB
client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="vit_knowledge"
)

pdf_folder = "pdfs"

chunk_id = collection.count() + 1000

print("📂 Looking inside:", pdf_folder)

for filename in os.listdir(pdf_folder):

    print("Processing:", filename)

    if not filename.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(
        pdf_folder,
        filename
    )

    try:

        reader = PdfReader(pdf_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        if not text.strip():
            print(
                f"⚠️ No text found in {filename}"
            )
            continue

        chunks = [
            text[i:i + 500]
            for i in range(
                0,
                len(text),
                500
            )
        ]

        for chunk in chunks:

            collection.add(
                documents=[chunk],
                ids=[
                    f"pdf_chunk_{chunk_id}"
                ]
            )

            chunk_id += 1

        print(
            f"✅ Added {filename} ({len(chunks)} chunks)"
        )

    except Exception as e:

        print(
            f"❌ Error in {filename}: {e}"
        )

print("\n🚀 PDF ingestion complete")
print(
    "📊 Total documents:",
    collection.count()
)
