from fastapi import APIRouter
from backend.services.agent import execute_agent

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.get("/")
def agent(query: str):
    return execute_agent(query)