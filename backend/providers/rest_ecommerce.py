import os
import requests

from dotenv import load_dotenv
from backend.providers.ecommerce import EcommerceProvider

load_dotenv()


class RestEcommerceProvider(EcommerceProvider):

    def __init__(self):
        self.base_url = os.getenv("ECOMMERCE_API_BASE_URL")
        self.api_key = os.getenv("ECOMMERCE_API_KEY")

    def get_order_status(self, order_id: int):

        response = requests.get(
            f"{self.base_url}/orders/{order_id}",
            headers={
                "Authorization": f"Bearer {self.api_key}"
            },
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    def get_product(self, product_id: int):

        response = requests.get(
            f"{self.base_url}/products/{product_id}",
            headers={
                "Authorization": f"Bearer {self.api_key}"
            },
            timeout=10
        )

        response.raise_for_status()

        return response.json()