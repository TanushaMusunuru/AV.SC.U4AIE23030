import requests
import os
from dotenv import load_dotenv
from logging_middleware.logger import logger

logger.info("Loading environment variables")

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

vehicle_url = "http://20.207.122.201/evaluation-service/vehicles"

logger.info("Fetching vehicle tasks from API")

vehicle_response = requests.get(vehicle_url, headers=headers)

logger.info(f"Vehicle API status code: {vehicle_response.status_code}")

print("Vehicle API Status:", vehicle_response.status_code)

vehicle_data = vehicle_response.json()

if "vehicles" not in vehicle_data:

    logger.error("Failed to fetch vehicles data")

    print(vehicle_data)

    exit()

vehicles = vehicle_data["vehicles"]

depot_url = "http://20.207.122.201/evaluation-service/depots"

logger.info("Fetching depots data from API")

depot_response = requests.get(depot_url, headers=headers)

logger.info(f"Depot API status code: {depot_response.status_code}")

print("Depot API Status:", depot_response.status_code)

depot_data = depot_response.json()

if "depots" not in depot_data:

    logger.error("Failed to fetch depots data")

    print(depot_data)

    exit()

depots = depot_data["depots"]

MAX_HOURS = depots[0]["MechanicHours"]

logger.info(f"Mechanic hours available: {MAX_HOURS}")

print(f"\nMechanic Hours Available: {MAX_HOURS}")

vehicles.sort(key=lambda x: x["Impact"], reverse=True)

logger.info("Sorting tasks based on impact")

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

print("\nSelected Tasks:\n")

for task in selected_tasks:
    print(task)

print(f"\nTotal Hours Used: {total_hours}")
print(f"Total Impact Achieved: {total_impact}")

logger.info("Vehicle scheduling completed successfully")