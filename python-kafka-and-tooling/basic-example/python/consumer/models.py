import json
import io
import avro.schema
import avro.io
from utils import get_logger

from dataclasses import dataclass


logger = get_logger(__name__)


@dataclass
class CustomerOrder:
    customer_id: str
    order_id: int
    article_ids: list[str]
    timestamp: int
    amount: int


@dataclass
class LineItem:
    customer_id: str
    order_id: int
    article_id: str
    timestamp: int

    def to_avro(self) -> bytes:
        schema = avro.schema.parse(json.dumps({
            "namespace": "CustomerOrders",
            "type": "record",
            "name": "LineItem",
            "fields": [
                {"name": "customer_id", "type": "string"},
                {"name": "order_id", "type": "int"},
                {"name": "article_id", "type": "string"},
                {"name": "timestamp", "type": "int"},
            ]
        }))
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        avro.io.DatumWriter(schema).write(self.__dict__, encoder)
        value = bytes_writer.getvalue()
        logger.info(f"Parse LineItem: {self.__dict__} to Avro: {value}")
        return bytes_writer.getvalue()
