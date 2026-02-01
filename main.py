from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from datetime import datetime, UTC
from typing import List, Optional
import uuid

app = FastAPI(title="Meeting Room Booking API")

# Data Models
class Reservation(BaseModel):
    id: Optional[str] = None
    room_id: str
    start_time: datetime
    end_time: datetime

    @field_validator('end_time')
    @classmethod
    def end_must_be_after_start(cls, v, info):
        if 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError('End time must be after the start time')
        return v

    @field_validator('start_time')
    @classmethod
    def start_must_be_in_future(cls, v):
        # Using UTC for consistency
        if v < datetime.now(UTC):
            raise ValueError('Reservation cannot be in the past')
        return v

# In-memory "database"
db_reservations: List[Reservation] = []

# --- Helper Functions ---

def check_overlap(new_res: Reservation) -> bool:
    """Checks if the new reservation overlaps with existing ones."""
    for res in db_reservations:
        if res.room_id == new_res.room_id:
            # Logic: (StartA < EndB) AND (StartB < EndA)
            if new_res.start_time < res.end_time and res.start_time < new_res.end_time:
                return True
    return False

# --- API Endpoints ---

@app.post("/reservations", response_model=Reservation)
def create_reservation(res: Reservation):
    """Creates a new reservation."""
    if check_overlap(res):
        raise HTTPException(status_code=400, detail="Room is already booked for the selected time.")
    
    res.id = str(uuid.uuid4())
    db_reservations.append(res)
    return res

@app.delete("/reservations/{res_id}")
def cancel_reservation(res_id: str):
    """Cancels a reservation by ID."""
    global db_reservations
    original_len = len(db_reservations)
    db_reservations = [r for r in db_reservations if r.id != res_id]
    
    if len(db_reservations) == original_len:
        raise HTTPException(status_code=404, detail="Reservation not found.")
    
    return {"message": "Reservation cancelled successfully."}

@app.get("/rooms/{room_id}/reservations", response_model=List[Reservation])
def get_room_reservations(room_id: str):
    """Lists all reservations for a specific room."""
    room_res = [r for r in db_reservations if r.room_id == room_id]
    return room_res

if __name__ == "__main__":
    import uvicorn
    # Note: When running in Docker, we use the CMD in Dockerfile instead of this block
    uvicorn.run(app, host="0.0.0.0", port=8000)