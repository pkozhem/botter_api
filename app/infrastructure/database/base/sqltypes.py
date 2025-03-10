import uuid
from typing import Any

from pydantic import UUID4
from sqlalchemy import CHAR, Dialect, TypeDecorator
from sqlalchemy.types import UUID
from sqlalchemy.sql.type_api import TypeEngine


class UUIDIndependent(TypeDecorator[UUID4]):
    """ DB independent UUID type. Uses PostgreSQL's UUID type, otherwise uses CHAR(36), storing as regular strings."""

    class UUIDChar(CHAR):
        """UUID type for CHAR."""

        python_type: UUID4 = UUID4

    impl = UUIDChar
    cache_ok = True

    def load_dialect_impl(self, dialect: Dialect) -> TypeEngine[Any]:
        """Load dialect implementation."""

        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value: UUID4 | str | None, dialect: Dialect) -> str | None:
        """Process bind param."""

        if value is None:
            return value
        if dialect.name == "postgresql":
            return str(value)
        if not isinstance(value, uuid.UUID):
            return str(uuid.UUID(value))
        return str(value)

    def process_result_value(self, value: UUID4 | None, dialect: Dialect) -> UUID4 | None:
        """Process result value."""

        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            value = uuid.UUID(value)
        return value
