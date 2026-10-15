from datetime import datetime
import uuid
from sqlalchemy import UUID, func
from sqlalchemy.orm import Mapped, declarative_base, mapped_as_dataclass, mapped_column
from backend.models.base import table_registry

@table_registry.mapped_as_dataclass
class Booking():
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    booking_reference: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        default=uuid.uuid4, 
        unique=True, 
        index=True,
        nullable=False
    )
    phone_number: Mapped[int] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    staff_id: Mapped[int] = mapped_column(nullable=False)
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), onupdate=func.now()
    )