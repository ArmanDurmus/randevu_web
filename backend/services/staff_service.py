from backend.database import DBSession
from backend.models.db_staff import Staff
from backend.services.security_service import hash_password, verify_password

async def change_password(staff_id: int, old_password: str, new_password: str, session: DBSession) -> None:
    """
    Change the password of a staff member.

    Args:
        staff_id (int): The ID of the staff member.
        new_password (str): The new password to set.
        session (DBSession): The database session.

    Raises:
        ValueError: If the staff member with the given ID is not found.
    """
    # Fetch the staff member from the database
    staff = await session.get(Staff, staff_id)
    if not staff:
        raise ValueError(f"Staff with ID {staff_id} not found.")
    if not verify_password(staff.hashed_password, old_password):
        #Replace with custom
        raise Exception

    staff.hashed_password = hash_password(new_password)

    # Commit the changes to the database
    await session.commit()
