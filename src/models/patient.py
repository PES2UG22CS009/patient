from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
from src.models.base import TimestampMixin


class Patient(Base, TimestampMixin):
    __tablename__ = "aaryan_patients"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
