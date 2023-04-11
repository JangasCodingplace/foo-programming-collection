from fastapi import FastAPI
import uuid
from datetime import datetime
from pydantic import BaseModel


app = FastAPI()


class VehiclePosition(BaseModel):
    timestamp: int
    vehicle_id: uuid.UUID
    lat: float
    long: float
    speed: int


@app.get("/get-position/{vehicle_id}")
def get_position(vehicle_id: uuid.UUID) -> VehiclePosition:
    current_position = VehiclePosition(**{
        "id": vehicle_id,
        "timestamp": int(datetime.now().timestamp()),
        "lat": 52.516908,
        "long": 13.519248,
        "speed": 45,
    })
    return current_position


@app.post("/create-position/{vehicle_id}")
def create_position(vehicle_id: uuid.UUID, vehicle_position: VehiclePosition) -> VehiclePosition:
    pass
