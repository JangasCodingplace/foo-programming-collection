from dataclasses import dataclass


@dataclass
class CustomerOrder:
    customer_id: int
    article_id: int
    order_id: int
    timestamp: int
