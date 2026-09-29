import ollama


def generate_answer(query: str, context: str):

    prompt = f"""
You are an AI business support assistant.

Answer the user's question using only the information provided in the context.

If the answer is not available in the context, say:
"I don't have enough information in the company knowledge base."

Context:
{context}

Question:
{query}

Answer:
"""

    response = ollama.chat(
        model="gemma3:1b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]