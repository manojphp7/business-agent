from fastapi import FastAPI
from backend.routes.customer import router as customer_router
app = FastAPI()

app.include_router(customer_router)

@app.get("/")
def home():
    return {"message": "Business Agent API is running"}