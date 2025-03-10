from datetime import datetime
from uuid import uuid4

from pydantic import UUID4
from sqlalchemy import TIMESTAMP, MetaData
from sqlalchemy.orm import Mapped, declarative_mixin, declared_attr, mapped_column

from app.core.utils import camel_to_snake, utc_now
from app.infrastructure.database.base.sqltypes import UUIDIndependent


@declarative_mixin
class TableNameMixin:
    """Mixin to automatically have pretty table name."""

    __abstract__: bool = True

    @declared_attr.directive
    def __tablename__(self):
        """Return name of table as class name in snake case."""

        return f"{camel_to_snake(self.__name__)}s"


@declarative_mixin
class TimestampsMixin:
    """Mixin to have created_at and updated_at fields."""

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
class UUIDPrimaryKeyMixin:
    """Mixin to have UUID as PK."""

    __abstract__: bool = True

    id: Mapped[UUID4] = mapped_column(
        UUIDIndependent,
        primary_key=True,
        index=True,
        default=uuid4,
        sort_order=-100,
    )


@declarative_mixin
class NameConventionMixin:
    """Mixin to have nice name convention."""

    __abstract__: bool = True

    metadata: MetaData = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })
