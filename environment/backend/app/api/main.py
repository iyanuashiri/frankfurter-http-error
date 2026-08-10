from fastapi import APIRouter

from app.api.routes import currencies, users

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(currencies.router)
