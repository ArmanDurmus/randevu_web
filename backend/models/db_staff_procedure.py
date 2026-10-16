from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, relationship
from backend.models.base import table_registry
from backend.models.db_staff import Staff

@table_registry.mapped_as_dataclass
class StaffProcedure():
    __tablename__ = "staff-procedures"

    staff_id = Mapped[int] = mapped_column(
        ForeignKey("staff.id"),
        nullable=False
    )
    procedure_id: Mapped[int] = mapped_column(
        ForeignKey("procedures.id"),
        nullable=False
    )