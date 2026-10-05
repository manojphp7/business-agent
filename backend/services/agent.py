import ollama
import json

from backend.providers.factory import get_ecommerce_provider
from backend.services.retrieval import search_similar_chunks
from backend.services.generation import generate_answer


ecommerce = get_ecommerce_provider()


def run_agent(query: str):

    prompt = f"""
You are a business support AI agent.

Analyze the user's question and decide which action is required.

Available actions:

1. ORDER_STATUS
   Use when the user asks about the status of an order.

2. PRODUCT_INFO
   Use when the user asks about a product.

3. KNOWLEDGE_BASE
   Use for company policies, return policy, refund policy,
   shipping policy, cancellation policy, FAQs, etc.

Extract order_id or product_id when required.

Return ONLY valid JSON.

Examples:

User: What is the status of order 1001?
Output:
{{"action": "ORDER_STATUS", "order_id": 1001, "product_id": null}}

User: Tell me about product 101
Output:
{{"action": "PRODUCT_INFO", "order_id": null, "product_id": 101}}

User: What is your refund policy?
Output:
{{"action": "KNOWLEDGE_BASE", "order_id": null, "product_id": null}}

User question:
{query}
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

    content = response["message"]["content"].strip()

    return json.loads(content)


def execute_agent(query: str):

    agent_result = run_agent(query)

    action = agent_result["action"]
    order_id = agent_result.get("order_id")
    product_id = agent_result.get("product_id")

    # Ecommerce API branch
    if action == "ORDER_STATUS":

        if order_id is None:
            return {
                "answer": "Please provide a valid order ID."
            }

        result = ecommerce.get_order_status(order_id)

        return {
            "answer": (
                f"Order {order_id} status is "
                f"{result.get('status', result.get('message'))}."
            ),
            "action": action,
            "data": result
        }

    # Product branch
    if action == "PRODUCT_INFO":

        if product_id is None:
            return {
                "answer": "Please provide a valid product ID."
            }

        result = ecommerce.get_product(product_id)

        return {
            "answer": str(result),
            "action": action,
            "data": result
        }

    # RAG branch
    if action == "KNOWLEDGE_BASE":

        results = search_similar_chunks(query)

        context = "\n\n".join(
            result.chunk_text
            for result, distance in results
        )

        answer = generate_answer(query, context)

        return {
            "answer": answer,
            "action": action,
            "sources": [
                {
                    "filename": result.filename,
                    "chunk_index": result.chunk_index,
                    "distance": distance
                }
                for result, distance in results
            ]
        }

    return {
        "answer": "I could not determine how to handle your question.",
        "action": action
    }