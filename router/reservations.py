from fastapi import APIRouter, HTTPException
from schemas.reservation import TestRes
from utils import check_overlap
import uuid
# --- API Endpoints ---
router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post("/", response_model=TestRes)
def create_reservation(res: TestRes):
    """Creates a new reservation."""
    if check_overlap(res):
        raise HTTPException(status_code=400, detail="Room is already booked for the selected time.")
    
    res.id = str(uuid.uuid4())
    db_reservations.append(res)
    return res

@router.delete("/{res_id}")
def cancel_reservation(res_id: str):
    """Cancels a reservation by ID."""
    global db_reservations
    original_len = len(db_reservations)
    db_reservations = [r for r in db_reservations if r.id != res_id]
    
    if len(db_reservations) == original_len:
        raise HTTPException(status_code=404, detail="Reservation not found.")
    
    return {"message": "Reservation cancelled successfully."}
