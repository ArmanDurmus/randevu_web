from fastapi import APIRouter, Query
from http import HTTPStatus
from backend.database import DBSession
from backend.models.db_staff import Staff
from backend.services import staff_service
from backend.services import staff_procedure_service

router = APIRouter(prefix="/staff", tags=["Staff"])

@router.get("/list-by-procedure", status_code=HTTPStatus.OK, response_model=None)
async def get_related_staff(procedure_id: int, session: DBSession):
    return await staff_procedure_service.get_eligible_staff(procedure_id, session)
    
@router.put("/change-password", status_code=HTTPStatus.OK, response_model=None)
async def change_password(staff: Staff, new_password: str, session: DBSession) -> None:
    staff_service.change_password(staff.id, staff.hashed_password, new_password=new_password, session=session)