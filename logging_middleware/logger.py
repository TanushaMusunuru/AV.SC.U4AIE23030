import requests
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

LOG_API = "http://20.207.122.201/evaluation-service/logs"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

class Logger:

    def info(self, message):

        payload = {
            "stack": "backend",
            "level": "info",
            "package": "service",
            "message": message
        }

        requests.post(LOG_API, json=payload, headers=headers)

    def error(self, message):

        payload = {
            "stack": "backend",
            "level": "error",
            "package": "handler",
            "message": message
        }

        requests.post(LOG_API, json=payload, headers=headers)

logger = Logger()