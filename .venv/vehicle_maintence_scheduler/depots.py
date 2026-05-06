import requests
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

url = "http://20.207.122.201/evaluation-service/depots"

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)