from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import re
import requests

from backend.database import SessionLocal
from backend.models import Company
from backend.services.retrieval import search_similar_chunks
from backend.services.generation import generate_answer


router = APIRouter(prefix="/widget", tags=["Widget"])


class WidgetRequest(BaseModel):
    agent_key: str
    query: str
    order_id: Optional[int] = None
    phone: Optional[str] = None


@router.post("/chat")
def widget_chat(request: WidgetRequest):

    db = SessionLocal()

    try:
        company = db.query(Company).filter(
            Company.agent_key == request.agent_key
        ).first()

        if not company:
            raise HTTPException(
                status_code=404,
                detail="Invalid agent key"
            )

    finally:
        db.close()

    query = request.query.strip()

    # =========================
    # Detect Order ID
    # =========================

    order_id = request.order_id

    if not order_id:

        order_match = re.search(
            r"\b\d{3,10}\b",
            query
        )

        if order_match:
            order_id = int(
                order_match.group()
            )

    # =========================
    # Detect Phone Number
    # =========================

    phone = request.phone

    if not phone:

        phone_match = re.search(
            r"\b\d{10}\b",
            query
        )

        if phone_match:
            phone = phone_match.group()

    # =========================
    # Order Status Detection
    # =========================

    order_keywords = [
        "order status",
        "status of order",
        "where is my order",
        "track my order",
        "order tracking",
        "order status",
    ]

    is_order_query = any(
        keyword in query.lower()
        for keyword in order_keywords
    )

    # =========================
    # Order Verification
    # =========================

    if is_order_query or (
        order_id is not None and phone is not None
    ):

        # Order ID missing
        if order_id is None:

            return StreamingResponse(
                iter([
                    "Please provide your order ID."
                ]),
                media_type="text/plain"
            )

        # Phone missing
        if phone is None:

            return StreamingResponse(
                iter([
                    "Please provide your registered phone number "
                    "to verify the order."
                ]),
                media_type="text/plain"
            )

        # =========================
        # Call Mock Ecommerce API
        # =========================

        try:
            print("ORDER ID:", order_id)
            print("PHONE:", phone)
            response = requests.get(
                f"http://127.0.0.1:9000/orders/{order_id}",
                params={
                    "phone": phone
                },
                headers={
                    "Authorization": "Bearer demo-key"
                },
                timeout=10
            )

            # Wrong phone
            if response.status_code == 403:

                return StreamingResponse(
                    iter([
                        "The phone number does not match "
                        "the registered phone number for this order."
                    ]),
                    media_type="text/plain"
                )

            # Order not found
            if response.status_code == 404:

                return StreamingResponse(
                    iter([
                        "I could not find that order."
                    ]),
                    media_type="text/plain"
                )

            # Other API error
            if not response.ok:

                return StreamingResponse(
                    iter([
                        "Unable to verify the order right now."
                    ]),
                    media_type="text/plain"
                )

            order_data = response.json()

            status = order_data.get("status")

            if not status:

                return StreamingResponse(
                    iter([
                        "Order status is currently unavailable."
                    ]),
                    media_type="text/plain"
                )

            return StreamingResponse(
                iter([
                    f"Your order {order_id} is currently {status}."
                ]),
                media_type="text/plain"
            )

        except requests.RequestException:

            return StreamingResponse(
                iter([
                    "Unable to connect to the order system right now."
                ]),
                media_type="text/plain"
            )

    # =========================
    # Normal RAG Query
    # =========================

    results = search_similar_chunks(
        query,
        company_id=company.id,
        limit=2
    )

    context = "\n\n".join(
        result.chunk_text
        for result, distance in results
    )

    # =========================
    # Streaming Generator
    # =========================

    def generate():

        for chunk in generate_answer(
            query,
            context
        ):
            yield chunk

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )