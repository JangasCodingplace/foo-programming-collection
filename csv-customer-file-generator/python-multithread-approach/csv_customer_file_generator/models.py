from dataclasses import dataclass


@dataclass
class CustomerOrder:
    customer_id: str
    article_id: str
    order_id: int
    timestamp: int
