from backend.models.db_booking import Booking
from backend.models.db_staff import Staff
from backend.models.db_staff import Staff
from backend.schemas.booking_schema import BookingRequest, BookingView
from backend.database import DBSession
from sqlalchemy import select

class StaffNotFoundError(Exception):
    pass

class BookingConflictError(Exception):
    pass

async def create_booking(data: BookingRequest, session: DBSession) -> BookingView:
    """
    Create a new booking in the database.

    Args:
        data (BookingRequest): The booking request data.
        session (DBSession): The database session.

    Returns:
        None
    """
     # 1. Lock the staff row so concurrent booking requests
    # for this staff member are processed safely.
    staff = await session.scalar(
        select(Staff)
        .where(Staff.id == data.staff_id)
        .with_for_update()
    )

    if staff is None:
        raise StaffNotFoundError(
            f"Staff member {data.staff_id} does not exist"
        )

    # 2. Check for an existing booking that overlaps.
    conflict_query = (
        select(Booking.id)
        .where(
            Booking.staff_id == data.staff_id,
            Booking.start_time < data.end_time,
            Booking.end_time > data.start_time,
        )
        .limit(1)
    )

    conflicting_booking_id = await session.scalar(conflict_query)

    if conflicting_booking_id is not None:
        raise BookingConflictError(
            "This staff member is already booked during that time"
        )
    
    # Create a new booking instance
    new_booking = Booking(
        phone_number=data.phone_number,
        first_name=data.first_name,
        last_name=data.last_name,
        staff_id=data.staff.id,
        start_time=data.start_time,
        end_time=data.end_time
    )
    staff = await session.get(Staff, data.staff.id)
    if not staff:
        raise ValueError(f"Staff with ID {data.staff.id} not found.")
    staff_name = f"{staff.first_name} {staff.last_name}"

    session.add(new_booking)
    await session.commit()
    await session.refresh(new_booking)

    return BookingView(
        phone_number=new_booking.phone_number,
        first_name=new_booking.first_name,
        last_name=new_booking.last_name,
        staff_name=staff_name,
        start_time=new_booking.start_time,
        end_time=new_booking.end_time
    )

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
    # Fetch the existing booking
    existing_booking = await session.get(Booking, booking_id)
    if not existing_booking:
        raise ValueError(f"Booking with ID {booking_id} not found.")

    staff = await session.get(Staff, data.staff.id)
    if not staff:
        raise ValueError(f"Staff with ID {data.staff.id} not found.")
    staff_name = f"{staff.first_name} {staff.last_name}"

    existing_booking.start_time = data.start_time
    existing_booking.end_time = data.end_time
    existing_booking.staff_id = data.staff_id

    # Commit the changes to the database
    await session.commit()
    await session.refresh(existing_booking)

    return BookingView(
        phone_number=existing_booking.phone_number,
        first_name=existing_booking.first_name,
        last_name=existing_booking.last_name,
        staff_name=staff_name,
        start_time=existing_booking.start_time,
        end_time=existing_booking.end_time
    ) 
