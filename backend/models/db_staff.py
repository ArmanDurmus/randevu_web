from backend.models.base import table_registry
from sqlalchemy.orm import Mapped, declarative_base, mapped_as_dataclass, mapped_column
from sqlalchemy import String

@table_registry.mapped_as_dataclass
class Staff():
    __tablename__ = "staff"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)