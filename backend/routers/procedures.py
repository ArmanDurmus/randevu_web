from fastapi import APIRouter, Query
from http import HTTPStatus
from backend.database import DBSession
from backend.schemas.booking_schema import BookingRequest, BookingView
from backend.services import procedure_service

router = APIRouter(prefix="/procedures", tags=["Procedures"])

@router.get("/", status_code=HTTPStatus.OK, response_model=None)
async def get_all_procedures(session: DBSession):
    return await procedure_service.get_all(session)
