from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.document import router as document_router
from backend.routes.agent import router as agent_router
from backend.routes.company import router as company_router
from backend.routes.widget import router as widget_router
from backend.database import engine

from backend import models
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router)
app.include_router(document_router)
app.include_router(company_router)
app.include_router(widget_router)

@app.get("/")
def home():
    return {"message": "Business Agent API is running"}