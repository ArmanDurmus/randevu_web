from datetime import datetime
from pydantic import BaseModel

class BookingRequest(BaseModel):
    phone_number: str
    first_name: str
    last_name: str
    procedure_id: int
    staff_id: int
    start_time: datetime

class BookingView(BaseModel):
    phone_number: str
    first_name: str
    last_name: str
    procedure_id: int
    staff_name: str
    start_time: datetime
    end_time: datetime
