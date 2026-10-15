from fastapi import APIRouter, Query
from http import HTTPStatus
from backend.database import DBSession
from backend.schemas.booking_schema import BookingRequest, BookingView
from backend.services import booking_service

router = APIRouter(prefix="/booking", tags=["Booking"])

@router.post("/", status_code=HTTPStatus.CREATED, response_model=None)
async def create_booking(data: BookingRequest, session: DBSession) -> BookingView:
    return await booking_service.create_booking(data, session)