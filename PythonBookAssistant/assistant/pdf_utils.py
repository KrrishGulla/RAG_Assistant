import fitz  # PyMuPDF
import tiktoken

def load_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text, max_tokens=500, overlap=50):
    tokenizer = tiktoken.get_encoding("cl100k_base")
    words = text.split("\n")
    chunks = []
    current_chunk = []

    def num_tokens(text):
        return len(tokenizer.encode(text))

    for line in words:
        if not line.strip():
            continue
        current_chunk.append(line.strip())
        if num_tokens(" ".join(current_chunk)) > max_tokens:
            chunk = " ".join(current_chunk)
            chunks.append(chunk)
            current_chunk = current_chunk[-overlap:]  # overlap for context

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
