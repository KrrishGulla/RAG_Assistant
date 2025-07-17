import os
import json
import hashlib
import time
from tqdm import tqdm
from openai import AzureOpenAI
import chromadb
from dotenv import load_dotenv

# Load environment variables from the root .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

EMBED_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="python_book")

# This will be overridden by main.py dynamically
CACHE_FILE = None


def embed_text(texts):
    response = client.embeddings.create(
        input=texts,
        model=EMBED_MODEL
    )
    return [r.embedding for r in response.data]


def compute_hash(chunks):
    joined = "".join(chunks)
    return hashlib.md5(joined.encode("utf-8")).hexdigest()


def load_cache():
    global CACHE_FILE
    if CACHE_FILE and os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_cache(hash_val):
    global CACHE_FILE
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)  # ✅ Ensure directory exists
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({"hash": hash_val}, f)


def add_to_vector_store(chunks, batch_size=100, delay=60):
    current_hash = compute_hash(chunks)
    cache = load_cache()
    if cache and cache.get("hash") == current_hash:
        print("Embeddings already cached. Skipping re-embedding.")
        return

    total = len(chunks)
    for i in tqdm(range(0, total, batch_size), desc="Embedding batches"):
        batch_chunks = chunks[i:i + batch_size]
        embeddings = embed_text(batch_chunks)
        for j, (chunk, embedding) in enumerate(zip(batch_chunks, embeddings)):
            collection.add(
                documents=[chunk],
                embeddings=[embedding],
                ids=[f"chunk_{i + j}"]
            )
        if i + batch_size < total:
            time.sleep(delay)

    save_cache(current_hash)
    print("Embeddings cached for future use.")


def search_similar_chunks(query, top_k=5):
    query_embedding = embed_text([query])[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results["documents"][0]
