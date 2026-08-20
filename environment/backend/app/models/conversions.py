from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Conversion(Base):
    __tablename__ = "conversions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    base_currency: Mapped[str] = mapped_column(String(3))
    target_currency: Mapped[str] = mapped_column(String(3))
    amount: Mapped[float] = mapped_column(Float)
    exchange_rate: Mapped[float] = mapped_column(Float)
    converted_amount: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="conversions",)