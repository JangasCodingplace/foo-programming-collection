import logging
from config import LOG_DIR, LOG_FMT


def get_logger(name: str) -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(LOG_FMT)
    console_handler.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(LOG_DIR / "generator.log")
    file_handler.setFormatter(LOG_FMT)
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
