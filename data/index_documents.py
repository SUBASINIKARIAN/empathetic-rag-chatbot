import json
import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from embedder import embed

PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME", "empathetic-chatbot")
DATA_FILE = os.path.join(os.path.dirname(__file__), "knowledge_base.json")


def ingest():
    pc = Pinecone(api_key=PINECONE_API_KEY)

    if INDEX_NAME not in [i.name for i in pc.list_indexes()]:
        pc.create_index(
            name=INDEX_NAME,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        print(f"Created index: {INDEX_NAME}")

    index = pc.Index(INDEX_NAME)

    with open(DATA_FILE) as f:
        documents = json.load(f)

    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=40)
    vectors = []

    for doc in documents:
        chunks = splitter.split_text(doc["content"])
        for i, chunk in enumerate(chunks):
            vector_id = f"{doc['id']}_chunk_{i}"
            embedding = embed(chunk)
            vectors.append((
                vector_id,
                embedding,
                {"title": doc["title"], "category": doc["category"], "text": chunk},
            ))

        if len(vectors) % 100 == 0:
            print(f"Prepared {len(vectors)} chunks...")

    index.upsert(vectors=vectors)
    print(f"Done. Upserted {len(vectors)} chunks into '{INDEX_NAME}'.")


if __name__ == "__main__":
    ingest()
