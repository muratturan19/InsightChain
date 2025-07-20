import logging
from logging.handlers import RotatingFileHandler
import os

logging.basicConfig(encoding="utf-8")

LOG_FILE = os.getenv("PIPELINE_LOGFILE", "pipeline.log")

logger = logging.getLogger("pipeline")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
