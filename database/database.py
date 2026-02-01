from typing import List, Optional
from schemas.reservation import TestRes

class ReservationRepository:
    def __init__(self):
        
        self._data: List[TestRes] = []

    def get_all(self, room_id: str) -> List[TestRes]:
        """Returns all reservations for a specific room."""
        return [r for r in self._data if r.room_id == room_id]

    def add(self, reservation: TestRes) -> None:
        """Adds a new reservation to the collection."""
        self._data.append(reservation)

    def remove(self, res_id: str) -> bool:
        """Removes a reservation and returns True if successful."""
        original_count = len(self._data)
        
        self._data = [r for r in self._data if r.id != res_id]
        return len(self._data) < original_count
    
    def get_all_raw(self) -> List[TestRes]:
        """Helper to see everything in the 'database'"""
        return self._data

db = ReservationRepository()