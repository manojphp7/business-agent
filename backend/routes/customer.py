from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.tools.database import create_customer, get_customer
from backend.schemas import CustomerCreate


router = APIRouter(prefix="/customers", tags=["Customers"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_customer_route(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(
        db,
        customer.name,
        customer.email
    )


@router.get("/{customer_id}")
def customer_details(
    customer_id: int,
    db: Session = Depends(get_db)
):
    return get_customer(db, customer_id)