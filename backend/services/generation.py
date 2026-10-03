import ollama


def generate_answer(query: str, context: str):

    prompt = f"""
You are an AI business support assistant for AuraCart.

Your task is to answer the user's question using the provided company knowledge base.

IMPORTANT RULES:
1. Use the information from the Context to answer the Question.
2. If the answer is clearly present in the Context, ALWAYS provide the answer.
3. Do not say "I don't have enough information" when the answer can be found in the Context.
4. Do not use outside knowledge.
5. Keep the answer short and direct.
6. If the Context does not contain the answer, say exactly:
"I don't have enough information in the company knowledge base."

Context:
{context}

Question:
{query}

Answer:
"""

    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]