import logging
from app.config.config import get_settings

settings = get_settings()

LOG_LEVEL = logging.DEBUG if settings.DEBUG else logging.INFO


def get_logger(name: str = "app"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(LOG_LEVEL)
    return logger 