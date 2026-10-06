from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Company

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get("/validate/{agent_key}")
def validate_agent_key(
    agent_key: str
):

    db = SessionLocal()
    company = db.query(Company).filter(
        Company.agent_key == agent_key
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Invalid agent key"
        )

    return {
        "valid": True,
        "company_id": company.id,
        "company_name": company.name
    }