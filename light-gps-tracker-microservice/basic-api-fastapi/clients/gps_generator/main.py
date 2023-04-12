import random
import time
from datetime import datetime


COORDS = {
    "BERLIN": {
        "lat_min": 52.338234,
        "lat_max": 52.677287,
        "long_min": 13.088346,
        "long_max": 13.760610,
    },
}


def generate_values():
    lat = round(random.uniform(COORDS["BERLIN"]["lat_min"], COORDS["BERLIN"]["lat_max"]), 6)
    long = round(random.uniform(COORDS["BERLIN"]["long_min"], COORDS["BERLIN"]["long_max"]), 6)
    return lat, long


if __name__ == "__main__":
    while True:
        lat, long = generate_values()
        speed = random.randint(0, 120)
        timestamp = int(datetime.now().timestamp())
        print(f"Generated Row: {timestamp},{lat},{long},{speed}")
        time.sleep(5)
