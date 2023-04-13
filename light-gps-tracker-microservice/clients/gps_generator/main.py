import os
import requests
import random
import time
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()


COORDS = {
    "BERLIN": {
        "lat_min": 52.338234,
        "lat_max": 52.677287,
        "long_min": 13.088346,
        "long_max": 13.760610,
    },
}

VEHICLE_IDS = [
    "40ad23c6-5072-460f-9d1d-acddff5472fa",
]

BASE_URL = os.getenv("MY_DELIVERY_SERVICE_FQDN", "http://127.0.0.1:8000")


if __name__ == "__main__":
    while True:
        lat = round(random.uniform(COORDS["BERLIN"]["lat_min"], COORDS["BERLIN"]["lat_max"]), 6)
        long = round(random.uniform(COORDS["BERLIN"]["long_min"], COORDS["BERLIN"]["long_max"]), 6)
        speed = random.randint(0, 120)
        timestamp = int(datetime.now().timestamp())
        vehicle_id = VEHICLE_IDS[0]
        url = f'{BASE_URL}/create-position/{vehicle_id}'
        resp = requests.post(url, json={
            "vehicle_id": vehicle_id,
            "timestamp": timestamp,
            "lat": lat,
            "long": long,
            "speed": speed,
        })
        print(f"Generated Row: {timestamp},{lat},{long},{speed} - StatusCode: {resp.status_code}")
        time.sleep(5)
