
from fastapi import APIRouter, HTTPException
from typing import List
from schemas.reservation import TestRes
from database.database import db_reservations
# --- API Endpoints ---
router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.get("/{room_id}/reservations", response_model=List[TestRes])
def get_room_reservations(room_id: str):
    """Lists all reservations for a specific room."""
    room_res = [r for r in db_reservations if r.room_id == room_id]
    return room_res