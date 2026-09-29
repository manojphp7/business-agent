import ollama
import json
from backend.database import SessionLocal
from backend.tools.business import check_order_status
from backend.services.retrieval import search_similar_chunks
from backend.services.generation import generate_answer

def run_agent(query: str):
    prompt = f"""
You are a business support AI agent.

Analyze the user's question and decide which action is required.

Available actions:

1. ORDER_STATUS
   Use when the user asks about the status of an order.

2. KNOWLEDGE_BASE
   Use for company policies, return policy, refund policy,
   shipping policy, cancellation policy, FAQs, etc.

If the action is ORDER_STATUS, extract the order ID from the question.

Return ONLY valid JSON.

Examples:

User: What is the status of order 1?
Output:
{{"action": "ORDER_STATUS", "order_id": 1}}

User: Tell me the status of order 25
Output:
{{"action": "ORDER_STATUS", "order_id": 25}}

User: What is your return policy?
Output:
{{"action": "KNOWLEDGE_BASE", "order_id": null}}

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
    order_id = agent_result["order_id"]

    # Database branch
    if action == "ORDER_STATUS":
        if order_id is None:
            return {
                "answer": "Please provide a valid order ID."
            }

        db = SessionLocal()

        try:
            result = check_order_status(db, order_id)

            return {
                "answer": f"Your order {order_id} status is {result.get('status', result.get('message'))}.",
                "action": action,
                "data": result
            }
        finally:
            db.close()

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