from fastapi import APIRouter, Query
from http import HTTPStatus
from backend.database import DBSession
from backend.models.db_staff import Staff
from backend.services import staff_service

router = APIRouter(prefix="/staff", tags=["Booking"])

@router.put("/change-password", status_code=HTTPStatus.OK, response_model=None)
async def change_password(staff: Staff, new_password: str, session: DBSession) -> None:
    staff_service.change_password(staff.id, staff.hashed_password, new_password=new_password, session=session)