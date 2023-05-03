import uuid
from time import sleep
from typing import Iterable
from datetime import datetime
from models import CustomerOrder
from random import randint
from utils import get_logger


logger = get_logger(__name__)


class OrderGenerator:
    def __init__(
        self,
        article_count: int,
        customer_count: int,
    ):
        self.articles = [{"id": str(uuid.uuid4()), "amount": randint(1000, 50000)} for _ in range(article_count)]
        self.customers = [str(uuid.uuid4()) for _ in range(10 ** 3, 10 ** 3 + customer_count)]

    def _generate_order(self, order_id: int) -> CustomerOrder:
        timestamp = datetime.now()
        customer = self.customers[randint(0, len(self.customers)-1)]
        item_count = randint(1, 20)
        articles = [self.articles[randint(0, len(self.articles)-1)] for _ in range(item_count)]
        article_list = [a["id"] for a in articles]
        amount = sum(a["amount"] for a in articles)
        return CustomerOrder(
            customer_id=customer,
            article_ids=article_list,
            order_id=order_id,
            timestamp=int(timestamp.timestamp()),
            amount=amount
        )

    def generate_rows(self) -> Iterable[CustomerOrder]:
        order_id = 1000
        while True:
            yield self._generate_order(order_id)
            order_id += 1
            sleep(1)
