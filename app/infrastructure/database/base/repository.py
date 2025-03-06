from collections.abc import Callable, Iterable
from typing import (
    Any,
    ClassVar,
    Final,
    Literal,
    TypeAlias,
    TypedDict,
    TypeVar,
)

from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.selectable import ForUpdateParameter

from app.infrastructure.database.base.error import ObjectNotFoundError

ConcreteTable = TypeVar("ConcreteTable", bound=DeclarativeBase)
AutoConvertTypes: TypeAlias = dict[str, Callable[[Any], Any]]

ID = TypeVar("ID")
Model = TypeVar("Model", bound=BaseModel)
CreateModel = TypeVar("CreateModel", bound=BaseModel)
UpdateModel = TypeVar("UpdateModel", bound=BaseModel)

CREATE_RULE: Final = "create"
UPDATE_RULE: Final = "update"
CONVERTION_RULES = Literal["create", "update"]


class AutoConvertionRules(TypedDict):
    create: AutoConvertTypes
    update: AutoConvertTypes


class BaseRepository:
    table: ConcreteTable
    auto_commit: bool = False
    __auto_convert_types__: ClassVar[AutoConvertionRules] = {
        CREATE_RULE: {},
        UPDATE_RULE: {},
    }

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def __auto_convert(self, type_: str, data: dict[str, Any]) -> dict[str, Any]:
        """Convert by rule."""

        rules: AutoConvertTypes = self.__auto_convert_types__.get(type_, {})
        for key in rules:
            if key not in data:
                continue
            data[key] = rules[key](data[key])
        return data

    def _get_create_data(self, data: CreateModel) -> dict[str, Any]:
        """Get create data."""

        return self.__auto_convert(type_=CREATE_RULE, data=data.model_dump())

    def _get_update_data(self, data: UpdateModel) -> dict[str, Any]:
        """Get update data."""

        return self.__auto_convert(
            type_=UPDATE_RULE,
            data=data.model_dump(exclude_unset=True),
        )

    async def ok(self) -> None:
        """Commit or flush transaction."""

        if self.auto_commit:
            await self.commit()
        else:
            await self.flush()

    async def commit(self) -> None:
        """Commit transaction."""

        await self.session.commit()

    async def flush(self) -> None:
        """Flush transaction."""

        await self.session.flush()

    async def refresh(
        self,
        obj: ConcreteTable,
        attribute_names: Iterable[str] | None = None,
        with_for_update: ForUpdateParameter = None,
    ) -> None:
        """Refresh object."""

        if self.auto_commit:
            await self.session.refresh(
                obj,
                attribute_names=attribute_names,
                with_for_update=with_for_update,
            )

    async def get(self, id_: ID) -> ConcreteTable | None:
        """Get object by ID."""

        return (await self.session.execute(select(self.table).where(self.table.id == id_))).scalar()

    async def get_all(self) -> list[ConcreteTable]:
        """Get all records of this model."""

        return (await self.session.execute(select(self.table))).scalars().all()

    async def create(self, data: CreateModel) -> ConcreteTable:
        """Create object."""

        obj = self.table(**self._get_create_data(data))
        self.session.add(obj)
        await self.ok()
        await self.refresh(obj)
        return obj

    async def create_bulk(self, datas: list[CreateModel]) -> list[ConcreteTable]:
        """Bulk create several objects."""

        objs = [self.table(**self._get_create_data(data)) for data in datas]
        self.session.add_all(objs)

        await self.ok()

        for obj in objs:
            await self.refresh(obj)

        return objs

    async def update(self, id_: ID, data: UpdateModel) -> ConcreteTable:
        """Update object by ID."""

        obj = await self.get(id_)
        if obj is None:
            raise ObjectNotFoundError(id_) from None

        update_data = self._get_update_data(data)
        for key, value in update_data.items():
            setattr(obj, key, value)

        await self.ok()
        await self.refresh(obj)

        return obj

    async def update_returning(self, id_: ID, data: UpdateModel) -> ConcreteTable:
        """Return updated object."""

        obj = (
            await self.session.execute(
                update(self.table).where(self.table.id == id_).values(**data.model_dump()).returning(self.table),
            )
        ).scalar_one_or_none()
        if obj is None:
            raise ObjectNotFoundError(id_) from None

        await self.ok()
        await self.refresh(obj)
        return obj

    async def delete(self, id_: ID) -> None:
        """Delete object by ID."""

        obj = await self.get(id_)
        if obj is None:
            raise ObjectNotFoundError(id_) from None
        await self.session.delete(obj)
        await self.ok()
