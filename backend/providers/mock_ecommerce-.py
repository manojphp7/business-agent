from backend.providers.ecommerce import EcommerceProvider


class MockEcommerceProvider(EcommerceProvider):

    def get_order_status(self, order_id: int):
        orders = {
            1001: "Shipped",
            1002: "Delivered",
            1003: "Processing",
        }

        status = orders.get(order_id)

        if not status:
            return {
                "order_id": order_id,
                "message": "Order not found"
            }

        return {
            "order_id": order_id,
            "status": status
        }

    def get_product(self, product_id: int):
        products = {
            101: {
                "product_id": 101,
                "name": "Red Shirt",
                "price": 999
            },
            102: {
                "product_id": 102,
                "name": "Blue Jeans",
                "price": 1499
            }
        }

        return products.get(
            product_id,
            {
                "product_id": product_id,
                "message": "Product not found"
            }
        )