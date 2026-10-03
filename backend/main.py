from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.customer import router as customer_router
from backend.routes.order import router as order_router
from backend.routes.document import router as document_router
from backend.routes.auth import router as auth_router
from backend.database import engine
from backend import models
app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(customer_router)
app.include_router(order_router)
app.include_router(document_router)
app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "Business Agent API is running"}