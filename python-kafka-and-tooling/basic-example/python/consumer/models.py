from dataclasses import dataclass


@dataclass
class CustomerOrder:
    customer_id: str
    order_id: int
    article_ids: list[str]
    timestamp: int
    amount: int
