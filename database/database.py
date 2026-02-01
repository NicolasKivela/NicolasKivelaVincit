from typing import List 
from schemas.reservation import Reservation


# Temporary In-memory "database"
# TODO: Add database connection and queries here
db_reservations: List[Reservation] = []