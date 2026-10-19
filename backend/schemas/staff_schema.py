from pydantic import BaseModel, ConfigDict

class StaffView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    title: str

class ChangePasswordRequest(BaseModel):
    staff_id: int
    old_password: str
    new_password: str
