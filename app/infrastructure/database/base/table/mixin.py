import uuid
from datetime import datetime

from pydantic import UUID4
from sqlalchemy.orm import declarative_mixin, declared_attr, Mapped, mapped_column

from app.core.utils import camel_to_snake, utc_now
from app.infrastructure.database.base.sqltype import TIMESTAMP, UUIDIndependent


@declarative_mixin
class NameMixin:
    """Mixin for table names."""

    __abstract__: bool = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Make name of table in snake case."""

        return f"{camel_to_snake(cls.__name__)}s"


@declarative_mixin
class TimestampsMixin:
    """Mixin to add created_at and updated_at timestamp field."""

    __abstract__: bool = True

    created_at: Mapped[datetime] = mapped_column(
        "created_at",
        TIMESTAMP(timezone=True),
        default=utc_now,
        nullable=False,
        sort_order=-99,
    )

    updated_at: Mapped[datetime] = mapped_column(
        "updated_at",
        TIMESTAMP(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
        sort_order=-97,
    )


@declarative_mixin
class PrimaryKeyUUIDMixin:
    """Mixin to create PK as UUIDs."""

    __abstract__: bool = True

    id: Mapped[UUID4] = mapped_column(
        UUIDIndependent,
        primary_key=True,
        default=uuid.uuid4,
        sort_order=-100,
    )