from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from backend.database import DBSession
from backend.schemas.staff_schema import ChangePasswordRequest, StaffView
from backend.services import staff_service
from backend.services import staff_procedure_service
from backend.services.staff_procedure_service import NoEligibleStaff
from backend.services.staff_service import CannotBeOldPassword, InvalidPasswordError

router = APIRouter(prefix="/staff", tags=["Staff"])

@router.get("/list-by-procedure", status_code=HTTPStatus.OK, response_model=list[StaffView])
async def get_related_staff(procedure_id: int, session: DBSession):
    try:
        return await staff_procedure_service.get_eligible_staff(procedure_id, session)
    except NoEligibleStaff as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

@router.put("/change-password", status_code=HTTPStatus.OK, response_model=None)
async def change_password(data: ChangePasswordRequest, session: DBSession) -> None:
    try:
        await staff_service.change_password(
            data.staff_id, data.old_password, data.new_password, session=session
        )
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
    except InvalidPasswordError as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=str(e))
    except CannotBeOldPassword as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
