from pydantic import BaseModel, model_validator

class BookingRequest(BaseModel):
    phone_number: int
    first_name: str
    last_name: str
    procedure_id: int
    staff_id = int
    start_time: str
    end_time: str

    @model_validator
    def validate_time_range(self):
        if self.start_time > self.end_time:
            raise ValueError
        return self

class BookingView(BaseModel):
    phone_number: int
    first_name: str
    last_name: str
    procedure_id: int
    staff_name: str
    start_time: str
    end_time: str

