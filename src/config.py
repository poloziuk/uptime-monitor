import os
from dotenv import load_dotenv

load_dotenv()

URLS = os.getenv("URLS", "https://google.com,https://github.com").split(",")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK", "")
DB_URL = os.getenv("DB_URL", "sqlite:///monitor.db")

