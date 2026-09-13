import os


# ============================================================
# PROJECT DIRECTORIES
# ============================================================

BACKEND_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_DIR = os.path.dirname(
    BACKEND_DIR
)

DATA_DIR = os.path.join(
    PROJECT_DIR,
    "data"
)


# ============================================================
# DATA FILES
# ============================================================

PERSONS_FILE = os.path.join(
    DATA_DIR,
    "persons.csv"
)

CALLS_FILE = os.path.join(
    DATA_DIR,
    "calls.csv"
)

TRANSACTIONS_FILE = os.path.join(
    DATA_DIR,
    "transactions.csv"
)

CASES_FILE = os.path.join(
    DATA_DIR,
    "cases.csv"
)


# ============================================================
# APPLICATION SETTINGS
# ============================================================

APP_NAME = "CrimeGraph AI"

API_HOST = "127.0.0.1"

API_PORT = 5000


# ============================================================
# RISK SETTINGS
# ============================================================

HIGH_TRANSACTION_MULTIPLIER = 2.0

REPEATED_CALL_THRESHOLD = 2

HIGH_RISK_SCORE = 70

MEDIUM_RISK_SCORE = 40