import requests
from src.config import SLACK_WEBHOOK

def send_slack_alert(message: str):
    if not SLACK_WEBHOOK:
        return
    requests.post(SLACK_WEBHOOK, json={"text": message})

