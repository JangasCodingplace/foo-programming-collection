from typing import List
import uuid
from fastapi import FastAPI, HTTPException

from models import VehiclePosition
from repositories import VehiclePositionRepository


app = FastAPI()


@app.get("/get-position/{vehicle_id}")
def get_position(vehicle_id: uuid.UUID) -> VehiclePosition:
    entity = VehiclePositionRepository.retrieve(vehicle_id)
    if not entity:
        raise HTTPException(
            status_code=404,
            detail=f"No entity for vehicle with ID `{vehicle_id}` found",
        )
    return entity


@app.get("/get-positions/{vehicle_id}")
def get_positions(vehicle_id: uuid.UUID, min_dt: int, max_dt: int) -> List[VehiclePosition]:
    return VehiclePositionRepository.list(vehicle_id, min_dt, max_dt)


@app.post("/create-position/{vehicle_id}")
def create_position(vehicle_id: uuid.UUID, vehicle_position: VehiclePosition) -> VehiclePosition:
    VehiclePositionRepository.create(vehicle_position)
    return vehicle_position
