from abc import ABC, abstractmethod
from typing import Any, Iterable, Optional

from pydantic import BaseModel, UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import ForUpdateParameter
from typing_extensions import TypeVar

from app.infrastructure.database.base.errors import RepositoryConsistentError, ObjectNotFoundError

Model = TypeVar("Model", bound=BaseModel)
Table = TypeVar("Table", bound=BaseModel)
UpdateModel = TypeVar("UpdateModel", bound=BaseModel)
CreateModel = TypeVar("CreateModel", bound=BaseModel)
ID = TypeVar("ID", bound=str | UUID4)


class IBaseRepository(ABC):
    """Interface for any repositories."""

    @abstractmethod
    async def refresh(
        self,
        instance: Model,
        attribute_names: Optional[Iterable[str]] = None,
        with_for_update: ForUpdateParameter = None,
    ) -> None:
        ...

    @abstractmethod
    async def get(self, id_: ID) -> Model | None:
        ...

    @abstractmethod
    async def all(self) -> list[Model] | None:
        ...

    @abstractmethod
    async def create(self, model: CreateModel) -> Model:
        ...

    @abstractmethod
    async def update(self, id_: ID, model: UpdateModel) -> Model:
        ...

    async def delete(self, id_: ID) -> None:
        ...

class BaseRepository(ABC, IBaseRepository):
    """Base class for SQLAlchemy repository."""

    table: Table
    auto_commit: bool
    auto_flush: bool

    def _check_consistent(self):
        if self.auto_commit is False and self.auto_flush is False:
            raise RepositoryConsistentError(
                msg="You should specify auto_commit or auto_flush parameter.",
            )
        if not self.table:
            raise RepositoryConsistentError(
                msg="You should specify table parameter.",
            )


class Repository(BaseRepository):
    """Parent class for all SQLAlchemy repositories."""

    table: Table
    auto_commit: bool = False
    auto_flush: bool = True

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session
        self._check_consistent()

    @staticmethod
    def _get_create_data(model: CreateModel) -> dict[str, Any]:
        """Return dict data a for creating new instance."""

        return model.model_dump()

    @staticmethod
    def _get_update_data(model: UpdateModel) -> dict[str, Any]:
        """Return dict data a for updating new instance."""

        return model.model_dump(exclude_unset=True)

    async def consign(self):
        """Commits or flushes in current transaction."""

        if self.auto_commit:
            await self.session.commit()
        else:
            await self.session.flush()

    async def refresh(
        self,
        instance: Model,
        attribute_names: Optional[Iterable[str]] = None,
        with_for_update: ForUpdateParameter = None,
    ) -> None:
        """Refresh instance in current session."""

        if self.auto_commit:
            await self.session.refresh(
                instance=instance,
                attribute_names=attribute_names,
                with_for_update=with_for_update,
            )

    async def get(self, id_: ID) -> Model | None:
        """Get instance by ID."""

        return (await self.session.execute(
            statement=select(self.table).where(self.table.id == id_),
        )).scalar()

    async def all(self):
        """Return all instances of table."""

        return (await self.session.execute(
            statement=select(self.table),
        )).scalars().all()

    async def create(self, model: UpdateModel) -> UpdateModel:
        """Create new instance."""

        data: dict[str, Any] = self._get_create_data(model=model)
        instance: Model = self.table(**data)
        self.session.add(instance)
        await self.consign()
        await self.refresh(instance)
        return instance

    async def bulk_create(self, models: list[Model]) -> list[Model]:
        """Create new instances in bulk."""

        instances: list[Model] | None = [self.table(**self._get_create_data(model=model)) for model in models]
        self.session.add_all(instances=instances)

        await self.consign()

        for instance in instances:
            await self.refresh(instance=instance)

        return instances

    async def update(self, id_: ID, model: UpdateModel) -> Model:
        """Update instance by ID."""

        instance: Model = await self.get(id_=id_)
        if not instance:
            raise ObjectNotFoundError(id_=id_) from None

        data: dict[str, Any] = self._get_update_data(model=model)
        for k, v in data:
            setattr(instance,k , v)

        await self.consign()
        await self.refresh(instance)

        return instance

    async def delete(self, id_: ID) -> None:
        """Delete instance by ID."""

        instance: Model = await self.get(id_=id_)
        if not instance:
            raise ObjectNotFoundError(id_=id_) from None

        await self.session.delete(instance=instance)
        await self.consign()
