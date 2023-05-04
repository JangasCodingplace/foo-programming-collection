from confluent_kafka import Producer
from config import KAFKA
from models import CustomerOrder, LineItem


producer = Producer(**{
    "bootstrap.servers": KAFKA["host"],
})


def send_line_items(order: CustomerOrder):
    for article_id in order.article_ids:
        line_item = LineItem(order.customer_id, order.order_id, article_id, order.timestamp)
        producer.produce("line-item-data-pbuf", line_item.to_avro())
