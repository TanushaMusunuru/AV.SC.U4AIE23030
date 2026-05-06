import requests
import os
from dotenv import load_dotenv
from datetime import datetime

from logging_middleware.logger import logger


logger.info("Loading environment variables")

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}


url = "http://20.207.122.201/evaluation-service/notifications"


logger.info("Fetching notifications from API")

response = requests.get(url, headers=headers)

logger.info(f"Notifications API status code: {response.status_code}")

print(response.status_code)
print(response.text)


if response.status_code != 200:

    logger.error("Failed to fetch notifications API")

    print("ERROR FETCHING NOTIFICATIONS API")

    exit()


logger.info("Converting response to JSON")

data = response.json()

notifications = data["notifications"]

priority_map = {
    "Placement": 3,
    "Result": 2,
    "Event": 1
}

priority_notifications = []

logger.info("Starting priority calculation")


for notification in notifications:

    logger.info(f"Processing notification ID: {notification['ID']}")

    notification_type = notification["Type"]

    weight = priority_map.get(notification_type, 0)

    timestamp = notification["Timestamp"]

    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

    time_score = dt.timestamp()

    final_score = (weight * 10000000000) + time_score

    notification["priorityScore"] = final_score

    priority_notifications.append(notification)


logger.info("Sorting notifications based on priority")

priority_notifications.sort(
    key=lambda x: x["priorityScore"],
    reverse=True
)


top_notifications = priority_notifications[:10]

logger.info("Displaying top 10 notifications")

# OUTPUT
print("\nTOP 10 PRIORITY NOTIFICATIONS\n")

for notification in top_notifications:

    print("----------------------------------")

    print("ID:", notification["ID"])

    print("Type:", notification["Type"])

    print("Message:", notification["Message"])

    print("Timestamp:", notification["Timestamp"])

logger.info("Priority inbox process completed successfully")