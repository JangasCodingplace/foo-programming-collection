import config
import json
from utils import get_logger
from generators import OrderGenerator
from config import GENERATOR
from confluent_kafka import Producer

logger = get_logger(__name__)


def main():
    logger.debug("Script Started")
    generator = OrderGenerator(**GENERATOR)
    producer = Producer(**{
        "bootstrap.servers": config.KAFKA_HOST,
    })

    for row in generator.generate_rows():
        logger.debug(f"Send row {row} to kafka")
        producer.produce("order-data-json", json.dumps(row.__dict__))


if __name__ == "__main__":
    main()
