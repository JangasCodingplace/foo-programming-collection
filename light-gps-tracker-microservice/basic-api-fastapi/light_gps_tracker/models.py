import uuid
from pydantic import BaseModel


class VehiclePosition(BaseModel):
    timestamp: int
    vehicle_id: uuid.UUID
    lat: float
    long: float
    speed: int
