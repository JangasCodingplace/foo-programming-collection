import io
import requests
import avro.schema
import avro.io
from utils import get_logger
from config import KAFKA, SCHEMA_REGISTRY_URL
from confluent_kafka import Consumer

logger = get_logger(__name__)


class SchemaRegistry:
    def __init__(self, url: str):
        self.url = url

    def get_registered_schema_names(self):
        response = requests.get(
            url=f'{self.url}/subjects'
        )
        response.raise_for_status()
        return response.json()

    def get_latest_schema_version(self, schema_name: str):
        response = requests.get(
            url=f'{self.url}/subjects/{schema_name}/versions'
        )
        response.raise_for_status()
        return response.json()[-1]

    def get_avro_schema(self, schema_name) -> avro.schema.Schema:
        version = self.get_latest_schema_version(schema_name)
        response = requests.get(
            url=f'{self.url}/subjects/{schema_name}/versions/{version}'
        )
        response.raise_for_status()
        schema = response.json()
        return avro.schema.parse(schema['schema'])

    def message_to_dict(self, message: bytes, schema_name: str):
        bytes_reader = io.BytesIO(message)
        decoder = avro.io.BinaryDecoder(bytes_reader)
        reader = avro.io.DatumReader(self.get_avro_schema(schema_name))
        decoded_msg = reader.read(decoder)
        return decoded_msg


def main():
    logger.debug("Script Started")
    consumer = Consumer(**{
        "bootstrap.servers": KAFKA["host"],
        'group.id': KAFKA["group"],
        'session.timeout.ms': 6000,
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe(["order-data-pbuf"])
    schema_registry = SchemaRegistry(SCHEMA_REGISTRY_URL)

    while True:
        msg = consumer.poll(timeout=1)
        if msg is None:
            logger.info("Nothing To Do")
        elif msg.error():
            logger.error(f"{msg.error()}")
        else:
            logger.debug(f"received message: {msg.value()}")
            parsed_message = schema_registry.message_to_dict(msg.value(), msg.topic())
            logger.debug(f"parsed message {parsed_message}")


if __name__ == "__main__":
    main()
