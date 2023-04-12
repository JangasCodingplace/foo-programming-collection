from models import VehiclePosition
from timescaledb import TimeScaleHandler
from typing import Union, List, Optional
import uuid
from datetime import datetime


class VehiclePositionRepository:
    @staticmethod
    def create(vehicle_position: VehiclePosition):
        query = """
            INSERT INTO vehicle_position (timestamp, vehicle_id, lat, long, speed)
            VALUES (%s, %s, %s, %s, %s)
        """
        with TimeScaleHandler() as db_handler:
            db_handler.execute(query, (
                datetime.fromtimestamp(vehicle_position.timestamp),
                str(vehicle_position.vehicle_id),
                vehicle_position.lat,
                vehicle_position.long,
                vehicle_position.speed,
            ))

    @staticmethod
    def retrieve(vehicle_id: Union[str, uuid.UUID]) -> Optional[VehiclePosition]:
        # https://docs.timescale.com/api/latest/hyperfunctions/last/#last
        query = """
            SELECT timestamp, vehicle_id, lat, long, speed
            FROM vehicle_position
            WHERE vehicle_id = %s
            ORDER BY timestamp DESC
            LIMIT 1;
        """
        with TimeScaleHandler() as db_handler:
            row = db_handler.fetchone(query, (str(vehicle_id), ))
        if not row:
            return None
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
        with TimeScaleHandler() as db_handler:
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
