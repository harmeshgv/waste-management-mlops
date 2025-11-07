import logging
import os
from logging.handlers import RotatingFileHandler

try:
    from splunk_handler import SplunkHandler

    SPLUNK_AVAILABLE = True
except ImportError:
    SPLUNK_AVAILABLE = False
    print("⚠️ splunk_handler not installed — Splunk logs disabled.")

# === Splunk Configuration ===
SPLUNK_HEC_HOST = os.getenv("SPLUNK_HEC_HOST", "192.168.49.1")
SPLUNK_HEC_PORT = int(os.getenv("SPLUNK_HEC_PORT", "8088"))
SPLUNK_HEC_TOKEN = os.getenv("SPLUNK_HEC_TOKEN", "d8a28e5d-dd93-4395-99e4-eac7c8598a7c")

# === Log file directory ===
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# === Logger setup ===
logger = logging.getLogger("WasteManagementBackend")
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # File Handler
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, "app.log"),
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
    )
    file_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(module)s | %(funcName)s | %(message)s"
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add console + file handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Optional Splunk Handler
    if SPLUNK_AVAILABLE:
        try:
            splunk_handler = SplunkHandler(
                host=SPLUNK_HEC_HOST,
                port=SPLUNK_HEC_PORT,
                token=SPLUNK_HEC_TOKEN,
                index="main",
                verify=False,
            )
            splunk_handler.setLevel(logging.INFO)
            splunk_handler.setFormatter(formatter)
            logger.addHandler(splunk_handler)
            logger.info("✅ Splunk logging enabled (HEC connected).")
        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize Splunk handler: {e}")

logger.info("Logger initialized successfully.")
