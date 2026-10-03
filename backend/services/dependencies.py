from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import User,Customer
from backend.services.auth import decode_access_token

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user

def get_current_customer(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.user_id == current_user.id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer profile not found"
        )

    return customer