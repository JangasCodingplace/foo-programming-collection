from datetime import datetime, timedelta
from models import CustomerOrder
from random import randint
from abc import ABC, abstractmethod
from threading import Thread
from utils import get_logger


logger = get_logger(__name__)


class Generator(ABC):
    def __init__(
        self,
        article_count: int,
        customer_count: int,
        min_date: datetime,
        max_date: datetime
    ):
        self.articles = [i for i in range(10**5, 10**5 + article_count)]
        self.customers = [i for i in range(10 ** 3, 10 ** 3 + customer_count)]
        self.date_list = [min_date + timedelta(days=d) for d in range((max_date - min_date).days)]

    def _generate_order(self, order_id: int) -> list[CustomerOrder]:
        date = self.date_list[randint(0, len(self.date_list)-1)]
        timestamp = datetime(
            year=date.year,
            month=date.month,
            day=date.day,
            hour=randint(0, 23),
            minute=randint(0, 59),
            second=randint(0, 59),
        )
        customer = self.customers[randint(0, len(self.customers)-1)]
        item_count = randint(1, 20)
        articles = [self.articles[randint(0, len(self.articles)-1)] for _ in range(item_count)]
        return [
            CustomerOrder(
                customer_id=customer,
                article_id=article,
                order_id=order_id,
                timestamp=int(timestamp.timestamp()),
            ) for article in articles
        ]

    @abstractmethod
    def generate_rows(self, *args, **kwargs):
        pass


class SingleThreadGenerator(Generator):
    def generate_rows(self, max_row_count: int) -> list[CustomerOrder]:
        order_id = 1000
        rows = []
        while len(rows) < max_row_count:
            order = self._generate_order(order_id)
            rows += order
            order_id += 1
        return rows


class MultithreadGenerator(Generator):
    def generate_rows(self, max_row_count: int, thread_count: int) -> list[CustomerOrder]:
        max_row_count_per_thread = max_row_count // thread_count
        threads = []
        rows = []
        for i in range(thread_count):
            start_order_id = 1000 + i * max_row_count
            t = Thread(
                target=lambda: rows.extend(
                    self._generate_orders(start_order_id, max_row_count_per_thread)
                )
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return rows

    def _generate_orders(self, start_order_id: int, max_row_count: int) -> list[CustomerOrder]:
        logger.debug("Start Chunk")
        rows = []
        while len(rows) < max_row_count:
            order = self._generate_order(start_order_id)
            rows += order
            start_order_id += 1
        logger.debug("Exit Chunk")
        return rows
