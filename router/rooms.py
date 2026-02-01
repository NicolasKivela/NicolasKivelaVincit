
from fastapi import APIRouter, HTTPException, Path, status
from typing import List
from schemas.reservation import TestRes
from database.database import db_reservations
# --- API Endpoints ---
router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.get(
    "/{room_id}/reservations", 
    response_model=List[TestRes],
    responses={
        404: {"description": "Room not found"},
        422: {"description": "Validation Error"}
    }
)
def get_room_reservations(
    room_id: str = Path(..., min_length=1, max_length=10, description="The ID of the room to search for")
):
    """
    Lists all reservations for a specific room.
    """
    try:
        room_res = [r for r in db_reservations if r.room_id == room_id]
        return room_res
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred while fetching reservations."
        )