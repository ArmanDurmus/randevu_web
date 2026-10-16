from sqlalchemy import select
from backend.models.db_staff_procedure import StaffProcedure
from backend.models.db_staff import Staff
from backend.database import DBSession


async def check_eligible_staff(procedure_id: int, session: DBSession) -> list[Staff]:

    available_staff = await session.scalars(
        select(Staff)
        .join(
            StaffProcedure,
            StaffProcedure.staff_id == id
        )
        .where(StaffProcedure.procedure_id == procedure_id)
    )

    return available_staff.all()
    
    