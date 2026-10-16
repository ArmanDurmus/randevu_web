from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column
from backend.models.base import table_registry
from backend.models.db_staff import Staff

@table_registry.mapped_as_dataclass
class Procedure():
    __tablename__ = "procedures"

    id: Mapped[int] =  mapped_column(primary_key=True, autoincrement=True)
    operation: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)