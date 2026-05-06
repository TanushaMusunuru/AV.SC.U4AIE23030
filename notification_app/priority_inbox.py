import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# LOAD ENV
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# HEADERS
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# API URL
url = "http://20.207.122.201/evaluation-service/notifications"

# FETCH DATA
response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)

# CHECK API STATUS
if response.status_code != 200:
    print("ERROR FETCHING NOTIFICATIONS API")
    exit()

# CONVERT TO JSON
data = response.json()

notifications = data["notifications"]

# PRIORITY WEIGHTS
priority_map = {
    "Placement": 3,
    "Result": 2,
    "Event": 1
}

priority_notifications = []

# CALCULATE PRIORITY
for notification in notifications:

    notification_type = notification["Type"]

    weight = priority_map.get(notification_type, 0)

    timestamp = notification["Timestamp"]

    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

    time_score = dt.timestamp()

    final_score = (weight * 10000000000) + time_score

    notification["priorityScore"] = final_score

    priority_notifications.append(notification)

# SORT BY PRIORITY
priority_notifications.sort(
    key=lambda x: x["priorityScore"],
    reverse=True
)

# TOP 10
top_notifications = priority_notifications[:10]

# OUTPUT
print("\nTOP 10 PRIORITY NOTIFICATIONS\n")

for notification in top_notifications:

    print("----------------------------------")

    print("ID:", notification["ID"])

    print("Type:", notification["Type"])

    print("Message:", notification["Message"])

    print("Timestamp:", notification["Timestamp"])