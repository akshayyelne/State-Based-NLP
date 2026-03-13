import os

# ======================================
# BASE DIRECTORY
# ======================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ======================================
# ENVIRONMENT
# ======================================
ENVIRONMENT = os.getenv("APP_ENV", "development")

# ======================================
# DATA DIRECTORY
# ======================================
DATA_DIR = os.path.join(BASE_DIR, "data")

# ======================================
# DATABASE CONFIGURATION
# ======================================
DB_PATH = os.getenv(
    "DB_PATH",
    os.path.join(DATA_DIR, "insurance.db")
)

# ======================================
# CHAT LOG
# ======================================
CHAT_LOG_PATH = os.path.join(BASE_DIR, "chat_log.csv")

# ======================================
# NLP CONFIGURATION
# ======================================
INTENTS_PATH = os.getenv(
    "INTENTS_PATH",
    os.path.join(DATA_DIR, "intents.json")
)

# ======================================
# ADMIN CONFIGURATION
# ======================================
ADMIN_PASSWORD = os.getenv(
    "ADMIN_PASSWORD",
    "SuperFinance123"
)

# ======================================
# LOGGING CONFIGURATION
# ======================================
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "insurance_system.log")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ======================================
# APPLICATION SETTINGS
# ======================================
APP_NAME = "SuperFinance Insurance Assistant"
APP_VERSION = "1.0.0"
COMPANY_NAME = "SuperFinance"
