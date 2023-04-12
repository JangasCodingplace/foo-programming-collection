import os
import psycopg2.pool
from typing import Union, List
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
        self.cursor.execute(query, *args)

    def fetchone(self, query: str, *args):
        self.execute(query, *args)
        return self.cursor.fetchone()

    def fetchall(self, query: str, *args):
        self.execute(query, *args)
        return self.cursor.fetchall()


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

    @staticmethod
    def retrieve(vehicle_id: Union[str, uuid.UUID]) -> VehiclePosition:
        # https://docs.timescale.com/api/latest/hyperfunctions/last/#last
        query = """
            SELECT timestamp, vehicle_id, lat, long, speed
            FROM vehicle_position
            WHERE vehicle_id = %s
            ORDER BY timestamp DESC
            LIMIT 1;
        """
        with TimeScaleHandler(TIMESCALE_CONNECTION_POOL) as db_handler:
            row = db_handler.fetchone(query, (str(vehicle_id), ))
        return VehiclePosition(
            timestamp=int(row[0].timestamp()),
            vehicle_id=row[1],
            lat=row[2],
            long=row[3],
            speed=row[4],
        )

    @staticmethod
    def list(vehicle_id: Union[str, uuid.UUID], min_dt: int, max_dt: int) -> List[VehiclePosition]:
        min_dt, max_dt = (min_dt, max_dt) if min_dt <= max_dt else (max_dt, min_dt)

        # https://docs.timescale.com/api/latest/hyperfunctions/last/#last
        query = """
                SELECT timestamp, vehicle_id, lat, long, speed
                FROM vehicle_position
                WHERE vehicle_id = %s AND timestamp >= %s AND timestamp <= %s
                ORDER BY timestamp ASC
            """
        with TimeScaleHandler(TIMESCALE_CONNECTION_POOL) as db_handler:
            rows = db_handler.fetchall(query, (
                str(vehicle_id),
                datetime.fromtimestamp(min_dt),
                datetime.fromtimestamp(max_dt),
            ))
        return [
            VehiclePosition(
                timestamp=int(row[0].timestamp()),
                vehicle_id=row[1],
                lat=row[2],
                long=row[3],
                speed=row[4],
            ) for row in rows
        ]


@app.get("/get-position/{vehicle_id}")
def get_position(vehicle_id: uuid.UUID) -> VehiclePosition:
    return VehiclePositionRepository.retrieve(vehicle_id)


@app.get("/get-positions/{vehicle_id}")
def get_positions(vehicle_id: uuid.UUID, min_dt: int, max_dt: int) -> List[VehiclePosition]:
    return VehiclePositionRepository.list(vehicle_id, min_dt, max_dt)


@app.post("/create-position/{vehicle_id}")
def create_position(vehicle_id: uuid.UUID, vehicle_position: VehiclePosition) -> VehiclePosition:
    VehiclePositionRepository.create(vehicle_position)
    return vehicle_position
