from sqlalchemy.orm import Session
from backend.models import Order



def get_business_info():
    return {
        "company_name": "ABC Technologies",
        "industry": "Software Development",
        "services": [
            "Software Development",
            "Cloud Computing",
            "AI Solutions"
        ],
        "employees": 250
    }


def check_order_status(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        return {
            "message": "Order not found"
        }

    return {
        "order_id": order.id,
        "status": order.status
    }