import os
import psycopg2
import uuid
from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel


app = FastAPI()


class VehiclePosition(BaseModel):
    timestamp: int
    vehicle_id: uuid.UUID
    lat: float
    long: float
    speed: int


class VehiclePositionRepository:
    @staticmethod
    def create(vehicle_position: VehiclePosition):
        conn = psycopg2.connect(
            user=os.getenv("TIMESCALEDB_USER", "rootuser"),
            password=os.getenv("TIMESCALEDB_PASSWORD", "rootpassword"),
            database=os.getenv("TIMESCALEDB_DATABASE", "my_delivery"),
            host=os.getenv("TIMESCALEDB_HOST", "localhost"),
            port=os.getenv("TIMESCALEDB_PORT", "5432"),
        )
        cursor = conn.cursor()
        query = """
            INSERT INTO vehicle_position (timestamp, vehicle_id, lat, long, speed)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            datetime.fromtimestamp(vehicle_position.timestamp),
            str(vehicle_position.vehicle_id),
            vehicle_position.lat,
            vehicle_position.long,
            vehicle_position.speed,
        ))
        conn.commit()

        cursor.close()
        conn.close()


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
    VehiclePositionRepository.create(vehicle_position)
    return vehicle_position
