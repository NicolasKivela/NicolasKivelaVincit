
from pydantic import BaseModel, field_validator
from datetime import datetime, UTC
from typing import  Optional
# Data Models
class TestRes(BaseModel):
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