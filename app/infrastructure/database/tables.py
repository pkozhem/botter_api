from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.infrastructure.database.base.mixins import (
    NameConventionMixin,
    TableNameMixin,
    TimestampsMixin,
    UUIDPrimaryKeyMixin,
)


class TableBase(
    NameConventionMixin,
    TableNameMixin,
    TimestampsMixin,
    UUIDPrimaryKeyMixin,
    DeclarativeBase,
):
    """Base class for db tables."""

    __abstract__ = True


class User(TableBase):

    name: Mapped[str] = mapped_column(nullable=False)
