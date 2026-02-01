from schemas.reservation import TestRes
from database.database import db
# --- Helper Functions ---
def check_overlap(new_res: TestRes) -> bool:
    """Checks if the new reservation overlaps with existing ones."""
    all_reservations = db.get_all_raw()
    for res in all_reservations:
        if res.room_id == new_res.room_id:
            # Logic: (StartA < EndB) AND (StartB < EndA)
            if new_res.start_time < res.end_time and res.start_time < new_res.end_time:
                return True
    return False