from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None

class OrderCreate(BaseModel):
    customer_id: int
    product: str
    amount: float
    status: str


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    product: str
    amount: float
    status: str

    class Config:
        from_attributes = True