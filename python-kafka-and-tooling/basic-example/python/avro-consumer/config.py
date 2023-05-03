import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"

LOG_FMT = logging.Formatter("%(name)s %(asctime)s %(levelname)-8s %(message)s")

KAFKA = {
    "host": os.getenv("KAFKA_HOST", "localhost:9092"),
    "group": os.getenv("KAFKA_GROUP_ID", "python-avro-consumer"),
}

SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL", "http://localhost:8081")
