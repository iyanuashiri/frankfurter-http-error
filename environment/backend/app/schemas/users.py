from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    api_key: str
    is_active: bool
    created_at: datetime
    credits: int

    model_config = ConfigDict(from_attributes=True)