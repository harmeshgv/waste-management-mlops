import logging
import os
from logging.handlers import RotatingFileHandler

from pythonjsonlogger.json import JsonFormatter

try:
    from splunk_handler import SplunkHandler

    SPLUNK_AVAILABLE = True
except ImportError:
    SPLUNK_AVAILABLE = False
    print("⚠️ splunk_handler not installed — Splunk logs disabled.")

SPLUNK_HEC_HOST = os.getenv("SPLUNK_HEC_HOST", "192.168.49.1")
SPLUNK_HEC_PORT = int(os.getenv("SPLUNK_HEC_PORT", "8088"))
SPLUNK_HEC_TOKEN = os.getenv("SPLUNK_HEC_TOKEN", "").strip()

LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("WasteManagementBackend")
logger.setLevel(logging.INFO)

if not logger.hasHandlers():

    json_formatter = JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(module)s %(funcName)s %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(json_formatter)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, "app.log"),
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(json_formatter)
    logger.addHandler(file_handler)

    if SPLUNK_AVAILABLE and SPLUNK_HEC_TOKEN:
        try:
            splunk_handler = SplunkHandler(
                host=SPLUNK_HEC_HOST,
                port=SPLUNK_HEC_PORT,
                token=SPLUNK_HEC_TOKEN,
                index="main",
                verify=False,
            )
            splunk_handler.setLevel(logging.INFO)
            splunk_handler.setFormatter(json_formatter)
            logger.addHandler(splunk_handler)
            logger.info("Splunk logging enabled (HEC connected).")
        except Exception as e:
            logger.warning(f"Failed to initialize Splunk handler: {e}")
    elif SPLUNK_AVAILABLE:
        logger.info("Splunk token not configured - Splunk logs disabled.")

logger.info("Logger initialized successfully.")
