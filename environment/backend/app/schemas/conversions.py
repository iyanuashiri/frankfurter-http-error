from datetime import datetime

from pydantic import BaseModel


class ConversionHistoryResponse(BaseModel):
    id: int
    base_currency: str
    target_currency: str
    amount: float
    exchange_rate: float
    converted_amount: float
    created_at: datetime

    model_config = {
        "from_attributes": True
    }