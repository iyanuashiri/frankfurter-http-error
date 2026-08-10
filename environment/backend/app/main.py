from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from app.api.main import api_router
from app.core.database import create_db_and_tables


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title="Currency Converter API",
    description="A simple currency converter API",
    version="2.0.0",
    openapi_url="/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)


@app.on_event("startup")
def startup():
    create_db_and_tables()


origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    api_router,
    prefix="/api/v1",
)