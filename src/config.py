import os
from dotenv import load_dotenv

load_dotenv()

URLS = [
    u.strip()
    for u in os.getenv("URLS", "https://google.com,https://github.com").split(",")
    if u.strip()
]
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK", "")
DB_URL = os.getenv("DB_URL", "sqlite:///monitor.db")

# Consecutive checks required before a state change is alerted on — guards
# against flapping on a single blip.
FAILURE_THRESHOLD = int(os.getenv("FAILURE_THRESHOLD", 3))
SUCCESS_THRESHOLD = int(os.getenv("SUCCESS_THRESHOLD", 1))
ALERT_TIMEOUT = float(os.getenv("ALERT_TIMEOUT", 10))
