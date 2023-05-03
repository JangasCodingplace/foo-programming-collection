import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"

LOG_FMT = logging.Formatter("%(name)s %(asctime)s %(levelname)-8s %(message)s")

KAFKA_HOST = os.getenv("KAFKA_HOST", "localhost:9092")

GENERATOR = {
    "article_count": int(os.getenv("GENERATOR_ARTICLE_COUNT", 100)),
    "customer_count": int(os.getenv("GENERATOR_CUSTOMER_COUNT", 1000)),
}
