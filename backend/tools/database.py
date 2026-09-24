from sqlalchemy.orm import Session
from backend.models import Customer, Order

def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def create_customer(db: Session, name: str, email: str):
    customer = Customer(
        name=name,
        email=email
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer



def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def get_customer_orders(db: Session, customer_id: int):
    return db.query(Order).filter(Order.customer_id == customer_id).all()