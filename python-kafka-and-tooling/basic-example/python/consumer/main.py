from utils import get_logger
from config import KAFKA
from confluent_kafka import Consumer

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


if __name__ == "__main__":
    main()
