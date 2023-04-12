import os
import psycopg2
import psycopg2.pool
from typing import Type
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


TIMESCALE_CONNECTION_POOL = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    user=os.getenv("TIMESCALEDB_USER", "rootuser"),
    password=os.getenv("TIMESCALEDB_PASSWORD", "rootpassword"),
    database=os.getenv("TIMESCALEDB_DATABASE", "my_delivery"),
    host=os.getenv("TIMESCALEDB_HOST", "localhost"),
    port=os.getenv("TIMESCALEDB_PORT", "5432"),
)


class TimeScaleHandler:
    def __init__(self, pool: psycopg2.pool):
        self.pool = pool

    def __enter__(self):
        self.conn = self.pool.getconn()
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, *args, **kwargs):
        self.cursor.close()
        self.pool.putconn(self.conn)
        return

    def execute(self, query: str, *args):
        return self.cursor.execute(query, *args)


class VehiclePositionRepository:
    @staticmethod
    def create(vehicle_position: VehiclePosition):
        query = """
            INSERT INTO vehicle_position (timestamp, vehicle_id, lat, long, speed)
            VALUES (%s, %s, %s, %s, %s)
        """
        with TimeScaleHandler(TIMESCALE_CONNECTION_POOL) as db_handler:
            db_handler.execute(query, (
                datetime.fromtimestamp(vehicle_position.timestamp),
                str(vehicle_position.vehicle_id),
                vehicle_position.lat,
                vehicle_position.long,
                vehicle_position.speed,
            ))


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
