from sqlalchemy.sql.schema import MetaData

from app.infrastructure.database.base.mixin import NameMixin, PrimaryKeyUUIDMixin, TimestampsMixin



class SQLTableBase(PrimaryKeyUUIDMixin, TimestampsMixin, NameMixin):
    """Base class for db tables."""

    __abstract__ = True

    metadata: MetaData = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })
