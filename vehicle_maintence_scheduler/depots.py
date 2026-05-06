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


url = "http://20.207.122.201/evaluation-service/depots"


logger.info("Fetching depots data from API")

response = requests.get(url, headers=headers)

logger.info(f"Depots API status code: {response.status_code}")

print(response.status_code)
print(response.text)


if response.status_code != 200:

    logger.error("Failed to fetch depots API")

    print("ERROR FETCHING DEPOTS API")

    exit()

logger.info("Depots data fetched successfully")