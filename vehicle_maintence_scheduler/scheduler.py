import requests
import os
from dotenv import load_dotenv
from logging_middleware.logger import logger

# =========================
# LOAD TOKEN
# =========================

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# =========================
# FETCH VEHICLE TASKS
# =========================

vehicle_url = "http://20.207.122.201/evaluation-service/vehicles"

vehicle_response = requests.get(vehicle_url, headers=headers)

print("Vehicle API Status:", vehicle_response.status_code)

vehicle_data = vehicle_response.json()

if "vehicles" not in vehicle_data:
    print(vehicle_data)
    exit()

vehicles = vehicle_data["vehicles"]

# =========================
# FETCH DEPOT DATA
# =========================

depot_url = "http://20.207.122.201/evaluation-service/depots"

depot_response = requests.get(depot_url, headers=headers)

print("Depot API Status:", depot_response.status_code)

depot_data = depot_response.json()

if "depots" not in depot_data:
    print(depot_data)
    exit()

depots = depot_data["depots"]

# =========================
# GET MECHANIC HOURS
# =========================

MAX_HOURS = depots[0]["MechanicHours"]

print(f"\nMechanic Hours Available: {MAX_HOURS}")

# =========================
# SORT TASKS BY IMPACT
# =========================

vehicles.sort(key=lambda x: x["Impact"], reverse=True)

# =========================
# SCHEDULER LOGIC
# =========================

selected_tasks = []

total_hours = 0
total_impact = 0

logger.info("Scheduling started")

for task in vehicles:

    duration = task["Duration"]
    impact = task["Impact"]

    if total_hours + duration <= MAX_HOURS:

        selected_tasks.append(task)

        total_hours += duration

        total_impact += impact

        logger.info(f"Selected Task {task['TaskID']}")

# =========================
# FINAL OUTPUT
# =========================

print("\nSelected Tasks:\n")

for task in selected_tasks:
    print(task)

print(f"\nTotal Hours Used: {total_hours}")
print(f"Total Impact Achieved: {total_impact}")