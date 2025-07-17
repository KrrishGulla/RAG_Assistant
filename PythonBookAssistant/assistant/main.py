import os
import hashlib
from pdf_utils import load_pdf, chunk_text
from embed_store import add_to_vector_store
from query_answer import generate_answer
import embed_store  # now cleanly at top

# Define relative PDF path
PDF_PATH = os.path.join("docs", "python-basics-sample-chapters.pdf")

# Dynamically generate the path for the embedding cache file
def get_cache_file_name(pdf_path):
    hash_val = hashlib.md5(pdf_path.encode("utf-8")).hexdigest()
    return os.path.join("cache", f"embedding_cache_{hash_val}.json")


def setup():
    print("Loading and chunking PDF...")
    text = load_pdf(PDF_PATH)
    chunks = chunk_text(text)
    print(f"Created {len(chunks)} chunks.")

    # Set the cache file path dynamically
    embed_store.CACHE_FILE = get_cache_file_name(PDF_PATH)

    print("Embedding and storing all chunks...")
    add_to_vector_store(chunks)
    print("Setup complete.")


def chat():
    print("\nAsk me a question")
    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        answer = generate_answer(query)
        print(f"\nAssistant: {answer}")


if __name__ == "__main__":
    setup()
    chat()
