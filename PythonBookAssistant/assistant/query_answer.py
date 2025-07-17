import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

from openai import AzureOpenAI
from embed_store import search_similar_chunks

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

CHAT_MODEL = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")

def generate_answer(user_query):
    relevant_chunks = search_similar_chunks(user_query, top_k=5)
    context = "\n\n".join(relevant_chunks)

    system_prompt = (
        "You are a helpful assistant that answers questions based only on the provided document. "
        "If the information isn't in the context, give a conversational response saying you dont know."
        "You also have memory of previous interactions, so you can refer to them if needed."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_query}"}
    ]

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0.5,
        max_tokens=500
    )

    return response.choices[0].message.content
