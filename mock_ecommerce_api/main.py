from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="Mock Ecommerce API")


ORDERS = {
    1001: {
        "order_id": 1001,
        "phone": "9876543210",
        "status": "Shipped",
        "product": "Red Shirt",
        "amount": 999
    },
    1002: {
        "order_id": 1002,
        "phone": "9876543210",
        "status": "Delivered",
        "product": "Blue Jeans",
        "amount": 1499
    }
}


PRODUCTS = {
    101: {
        "product_id": 101,
        "name": "Red Shirt",
        "price": 999,
        "stock": 25
    },
    102: {
        "product_id": 102,
        "name": "Blue Jeans",
        "price": 1499,
        "stock": 10
    }
}


def verify_api_key(authorization: str | None):

    if authorization != "Bearer demo-key":
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )


@app.get("/")
def home():
    return {
        "message": "Mock Ecommerce API is running"
    }


@app.get("/orders/{order_id}")
def get_order(
    order_id: int,
    phone: str,
    authorization: str | None = Header(default=None)
):
    verify_api_key(authorization)

    order = ORDERS.get(order_id)

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    # Verify registered phone number
    if order["phone"] != phone:
        raise HTTPException(
            status_code=403,
            detail="Invalid phone number for this order"
        )

    return {
        "order_id": order_id,
        "status": order["status"]
    }


@app.get("/products/{product_id}")
def get_product(
    product_id: int,
    authorization: str | None = Header(default=None)
):
    verify_api_key(authorization)

    product = PRODUCTS.get(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product