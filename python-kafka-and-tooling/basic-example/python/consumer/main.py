import json
from utils import get_logger
from config import KAFKA
from confluent_kafka import Consumer
from multiplexer import send_line_items
from models import CustomerOrder

logger = get_logger(__name__)


def main():
    logger.debug("Script Started")
    consumer = Consumer(**{
        "bootstrap.servers": KAFKA["host"],
        'group.id': KAFKA["group"],
        'session.timeout.ms': 6000,
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe(["order-data-json"])

    while True:
        msg = consumer.poll(timeout=1)
        if msg is None:
            logger.info("Nothing To Do")
        elif msg.error():
            logger.error(f"{msg.error()}")
        else:
            logger.debug(f"received message: {msg.value()}")
            order = CustomerOrder(**json.loads(msg.value()))
            send_line_items(order)


if __name__ == "__main__":
    main()
