# Generative PDF Embedding Assistant

A document-grounded RAG chatbot that answers questions strictly from uploaded PDFs — no generic internet answers. Responses are delivered through a real-time 3D talking avatar with synchronized lip movement.

Built during an internship at iSpace.

## How it works

1. PDFs are chunked and embedded using Azure OpenAI's embedding model
2. Embeddings are stored in ChromaDB for semantic similarity search
3. User query is embedded and top-matching chunks are retrieved
4. Retrieved context + query are sent to Azure OpenAI's Chat Completion API
5. The response is spoken aloud via Azure Speech SDK through a WebGL-based 3D avatar

## Stack

Python · Flask · Azure OpenAI · ChromaDB · Azure Speech SDK · HTML/CSS/JavaScript

