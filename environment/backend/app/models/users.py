import datetime
import secrets

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.security import generate_api_key
from app.core.database import Base

INITIAL_CREDITS = 10


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String)
    api_key: Mapped[str] = mapped_column(String(255), unique=True, default=generate_api_key)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    credits: Mapped[int] = mapped_column(Integer, default=INITIAL_CREDITS)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    conversions = relationship("Conversion", back_populates="user", cascade="all, delete-orphan",)
