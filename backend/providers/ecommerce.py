from abc import ABC, abstractmethod


class EcommerceProvider(ABC):

    @abstractmethod
    def get_order_status(self, order_id: int):
        pass

    @abstractmethod
    def get_product(self, product_id: int):
        pass