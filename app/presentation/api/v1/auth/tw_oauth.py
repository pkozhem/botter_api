from fastapi.routing import APIRouter
from starlette.responses import Response

from app.application.dependencies import AsyncSessionType

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get(path="/")
async def auth(
    session: AsyncSessionType,
):
    from app.config import get_settings
    a = get_settings()
    print(f"Correct!, {a=}")
    return Response()
