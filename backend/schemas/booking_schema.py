from pydantic import BaseModel

class BookingRequest(BaseModel):
    phone_number: int
    first_name: str
    last_name: str
    staff_id: int
    start_time: str
    end_time: str

class BookingView(BaseModel):
    id: int
    phone_number: int
    first_name: str
    last_name: str
    staff_id: int
    start_time: str
    end_time: str

