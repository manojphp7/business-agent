import os

from backend.providers.rest_ecommerce import RestEcommerceProvider


def get_ecommerce_provider():

    provider = os.getenv("ECOMMERCE_PROVIDER", "rest")

    if provider == "rest":
        return RestEcommerceProvider()

    return RestEcommerceProvider()