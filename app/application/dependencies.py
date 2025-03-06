from typing import Annotated, Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.infrastructure.database.base.session import get_async_session

AsyncSessionType: Type[AsyncSession] = Annotated[AsyncSession, Depends(get_async_session)]
SettingsType: Type[Settings] = Annotated[Settings, Depends(get_settings)]
