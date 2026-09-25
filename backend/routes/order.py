from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Order
from backend.schemas import OrderCreate, OrderResponse


router = APIRouter(prefix="/orders", tags=["Orders"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):

    new_order = Order(
        customer_id=order.customer_id,
        product=order.product,
        amount=order.amount,
        status=order.status
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order

@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.id == order_id).first()

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    existing_order = db.query(Order).filter(Order.id == order_id).first()

    if existing_order is None:
        return {"message": "Order not found"}

    existing_order.customer_id = order.customer_id
    existing_order.product = order.product
    existing_order.amount = order.amount
    existing_order.status = order.status

    db.commit()
    db.refresh(existing_order)

    return existing_order