from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from src.database import Base


class UserOrm(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str | None] = mapped_column(String(100))
    last_name: Mapped[str | None] = mapped_column(String(100))
    age: Mapped[int | None]
    gender: Mapped[str | None] = mapped_column(String(100))
