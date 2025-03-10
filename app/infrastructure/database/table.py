from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base.table import TableBase


class User(TableBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
