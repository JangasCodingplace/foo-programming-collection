import multiprocessing
from datetime import datetime, timedelta
from models import CustomerOrder
from random import randint
from abc import ABC, abstractmethod
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rows = []
        self._lock = multiprocessing.Lock()

    def generate_rows(self, max_row_count: int, thread_count: int) -> list[CustomerOrder]:
        max_row_count_per_thread = max_row_count // thread_count
        processes = []
        for i in range(thread_count):
            start_order_id = 1000 + i * max_row_count
            p = multiprocessing.Process(
                target=self._generate_orders,
                args=(start_order_id, max_row_count_per_thread),
            )
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        return self.rows

    def _generate_orders(self, start_order_id: int, max_row_count: int):
        logger.debug("Start Chunk")
        tmp_rows = 0
        while tmp_rows < max_row_count:
            order = self._generate_order(start_order_id)
            with self._lock:
                self.rows.extend(order)
            start_order_id += 1
            tmp_rows += len(order)
        logger.debug("Exit Chunk")
