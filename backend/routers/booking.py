from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from backend.database import DBSession
from backend.schemas.booking_schema import BookingRequest, BookingView
from backend.services import booking_service
from backend.services.booking_service import (
    BookingConflictError,
    BookingNotFoundError,
    StaffNotFoundError,
)

router = APIRouter(prefix="/booking", tags=["Booking"])

@router.post("/", status_code=HTTPStatus.CREATED, response_model=BookingView)
async def create_booking(data: BookingRequest, session: DBSession) -> BookingView:
    try:
        return await booking_service.create_booking(data, session)
    except StaffNotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
    except BookingConflictError as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))

@router.put("/{booking_id}", status_code=HTTPStatus.OK, response_model=BookingView)
async def update_booking(booking_id: int, data: BookingRequest, session: DBSession) -> BookingView:
    try:
        return await booking_service.update_booking(booking_id, data, session)
    except (BookingNotFoundError, StaffNotFoundError) as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
    except BookingConflictError as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))
