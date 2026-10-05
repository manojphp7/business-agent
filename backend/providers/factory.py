import os

from backend.providers.mock_ecommerce import MockEcommerceProvider
from backend.providers.rest_ecommerce import RestEcommerceProvider


def get_ecommerce_provider():

    provider = os.getenv("ECOMMERCE_PROVIDER", "mock")

    if provider == "rest":
        return RestEcommerceProvider()

    return MockEcommerceProvider()