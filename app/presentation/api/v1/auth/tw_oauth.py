from fastapi.routing import APIRouter
from starlette.responses import Response

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get(path="/")
async def auth():
    print("Correct!")
    return Response()
