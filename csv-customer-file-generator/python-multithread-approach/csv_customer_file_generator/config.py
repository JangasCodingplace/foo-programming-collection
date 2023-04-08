import logging
import multiprocessing
from pathlib import Path


BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"

LOG_FMT = logging.Formatter("%(name)s %(asctime)s %(levelname)-8s %(message)s")

MAX_THREAD_COUNT = multiprocessing.cpu_count()
