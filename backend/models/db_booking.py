from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, relationship
from backend.models.base import table_registry
from backend.models.db_staff import Staff
from backend.models.db_procedure import Procedure

@table_registry.mapped_as_dataclass
class Booking():
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    procedure_id: Mapped[str] = mapped_column(
        ForeignKey("procedures.id"),
        nullable=False)
    procedure = Mapped[Procedure] = relationship(init=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    staff_id: Mapped[int] = mapped_column(
        ForeignKey("staff.id"),
        nullable=False
    )
    staff: Mapped[Staff] = relationship(init=False)
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), onupdate=func.now()
    )