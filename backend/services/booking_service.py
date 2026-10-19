import logging
from datetime import datetime, timedelta
from backend.models.db_booking import Booking
from backend.models.db_staff import Staff
from backend.schemas.booking_schema import BookingRequest, BookingView
from backend.database import DBSession
from sqlalchemy import select
from backend.services import sms_service as sms_sender

logger = logging.getLogger(__name__)

BOOKING_DURATION = timedelta(minutes=30)

class StaffNotFoundError(Exception):
    pass

class BookingNotFoundError(Exception):
    pass

class BookingConflictError(Exception):
    pass

async def _get_staff_for_update(staff_id: int, session: DBSession) -> Staff:
    staff = await session.scalar(
        select(Staff)
        .where(Staff.id == staff_id)
        .with_for_update()
    )

    if staff is None:
        raise StaffNotFoundError(
            f"Staff member {staff_id} does not exist"
        )
    return staff

async def _check_conflict(
    staff_id: int,
    start_time: datetime,
    end_time: datetime,
    session: DBSession,
    ignore_booking_id: int | None = None,
) -> None:
    conflict_query = (
        select(Booking.id)
        .where(
            Booking.staff_id == staff_id,
            Booking.start_time < end_time,
            Booking.end_time > start_time,
        )
        .limit(1)
    )
    # When updating, the booking must not conflict with itself.
    if ignore_booking_id is not None:
        conflict_query = conflict_query.where(Booking.id != ignore_booking_id)

    if await session.scalar(conflict_query) is not None:
        raise BookingConflictError(
            "This staff member is already booked during that time"
        )

async def _notify(phone_number: str, message: str) -> None:
    # The booking is already saved, so an SMS failure should not fail the request.
    try:
        await sms_sender.send_sms_call(phone_number, message)
    except Exception:
        logger.exception("Failed to send SMS to %s", phone_number)

def _to_view(booking: Booking, staff: Staff) -> BookingView:
    return BookingView(
        phone_number=booking.phone_number,
        first_name=booking.first_name,
        last_name=booking.last_name,
        procedure_id=booking.procedure_id,
        staff_name=f"{staff.first_name} {staff.last_name}",
        start_time=booking.start_time,
        end_time=booking.end_time
    )

async def create_booking(data: BookingRequest, session: DBSession) -> BookingView:
    """
    Create a new booking in the database.

    Args:
        data (BookingRequest): The booking request data.
        session (DBSession): The database session.

    Returns:
        BookingView: The created booking view.
    """
    staff = await _get_staff_for_update(data.staff_id, session)

    end_time = data.start_time + BOOKING_DURATION
    await _check_conflict(data.staff_id, data.start_time, end_time, session)

    new_booking = Booking(
        procedure_id=data.procedure_id,
        phone_number=data.phone_number,
        first_name=data.first_name,
        last_name=data.last_name,
        staff_id=data.staff_id,
        start_time=data.start_time,
        end_time=end_time
    )

    session.add(new_booking)
    await session.commit()
    await session.refresh(new_booking)

    #change the sms message later on
    await _notify(new_booking.phone_number, "Randevunuz basariyla olusturulmustur")

    return _to_view(new_booking, staff)

async def update_booking(booking_id: int, data: BookingRequest, session: DBSession) -> BookingView:
    """
    Update an existing booking in the database.

    Args:
        booking_id (int): The ID of the booking to update.
        data (BookingRequest): The updated booking request data.
        session (DBSession): The database session.

    Returns:
        BookingView: The updated booking view.
    """
    existing_booking = await session.get(Booking, booking_id)
    if not existing_booking:
        raise BookingNotFoundError(f"Booking with ID {booking_id} not found.")

    staff = await _get_staff_for_update(data.staff_id, session)

    end_time = data.start_time + BOOKING_DURATION
    await _check_conflict(
        data.staff_id, data.start_time, end_time, session,
        ignore_booking_id=booking_id
    )

    existing_booking.phone_number = data.phone_number
    existing_booking.first_name = data.first_name
    existing_booking.last_name = data.last_name
    existing_booking.procedure_id = data.procedure_id
    existing_booking.staff_id = data.staff_id
    existing_booking.start_time = data.start_time
    existing_booking.end_time = end_time

    await session.commit()
    await session.refresh(existing_booking)

    #Change the message later on
    await _notify(existing_booking.phone_number, "Randevunuzdaki degisiklikler basariyla kaydedildi")

    return _to_view(existing_booking, staff)
