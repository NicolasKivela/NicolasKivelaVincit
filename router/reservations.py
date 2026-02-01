from fastapi import APIRouter, HTTPException, status, Path
from schemas.reservation import TestRes
from utils import check_overlap
import uuid
# --- API Endpoints ---
router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post(
    "/", 
    response_model=TestRes, 
    status_code=status.HTTP_201_CREATED,
    responses={400: {"description": "Booking Conflict"}}
)
def create_reservation(res: TestRes):
    """
    Creates a new reservation with overlap check.
    """
    try:
        if check_overlap(res):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Room is already booked for the selected time."
            )
        
        res.id = str(uuid.uuid4())
        db_reservations.append(res)
        return res
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the reservation."
        )

@router.delete(
    "/{res_id}", 
    status_code=status.HTTP_200_OK,
    responses={404: {"description": "Not Found"}}
)
def cancel_reservation(
    res_id: str = Path(..., min_length=36, description="The UUID of the reservation")
):
    """
    Cancels a reservation by ID with validation.
    """
    global db_reservations
      
    original_len = len(db_reservations)
    
    try:
        # Perform the deletion logic
        db_reservations = [r for r in db_reservations if r.id != res_id]
        
        if len(db_reservations) == original_len:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Reservation with ID {res_id} not found."
            )
        
        return {"message": "Reservation cancelled successfully."}

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while trying to delete the reservation."
        )
