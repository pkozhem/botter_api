from fastapi.routing import APIRouter
from starlette.responses import Response

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get(path="/")
async def auth():
    from app.config import get_settings
    a = get_settings()
    print("Correct!")
    return Response()
