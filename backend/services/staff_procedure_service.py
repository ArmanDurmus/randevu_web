from sqlalchemy import select
from backend.models.db_staff_procedure import StaffProcedure
from backend.models.db_staff import Staff
from backend.database import DBSession

class NoEligibleStaff(Exception):
    pass

async def get_eligible_staff(procedure_id: int, session: DBSession) -> list[Staff]:

    available_staff = await session.scalars(
        select(Staff)
        .join(
            StaffProcedure,
            StaffProcedure.staff_id == Staff.id
        )
        .where(StaffProcedure.procedure_id == procedure_id)
    )
    
    staff_list = available_staff.all()
    if not staff_list:
        raise NoEligibleStaff('Bu islem icin uygun personelimiz yok')

    return staff_list
    