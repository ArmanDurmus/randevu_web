from backend.models.db_booking import Booking
from backend.models.db_procedure import Procedure
from backend.database import DBSession
from sqlalchemy import select

async def get_all(session: DBSession):
    processes = await session.scalars(
        select(Procedure)
    )

    return processes.all()