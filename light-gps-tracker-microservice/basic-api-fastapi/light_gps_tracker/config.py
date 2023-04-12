import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

TIMESCALE_DB = {
    "minconn": int(os.getenv("TIMESCALEDB_CONNECTION_MIN_CONNECTIONS", 1)),
    "maxconn": int(os.getenv("TIMESCALEDB_CONNECTION_MAX_CONNECTIONS", 1)),
    "user": os.getenv("TIMESCALEDB_USER", "rootuser"),
    "password": os.getenv("TIMESCALEDB_PASSWORD", "rootpassword"),
    "database": os.getenv("TIMESCALEDB_DATABASE", "my_delivery"),
    "host": os.getenv("TIMESCALEDB_HOST", "localhost"),
    "port": os.getenv("TIMESCALEDB_PORT", "5432"),
}
