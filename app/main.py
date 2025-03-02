from fastapi import FastAPI

from app.presentation.api.v1.auth.tw_oauth import router as auth_router

app = FastAPI()

app.include_router(auth_router)
