from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.users import get_by_api_key
from app.models.users import User
from app.services.currency_service import Currency


def get_current_user(
        api_key: str = Header(..., alias="X-API-Key", description="Your API Key for authentication.",), 
        db: Session = Depends(get_db)) -> User:
    """
    Authenticate a user using their API key.
    """

    user = get_by_api_key(db, api_key)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key or User not found",
        )

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive",
        )

    return user


def get_currency_service():
    return Currency()


DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrencyService = Annotated[Currency, Depends(get_currency_service)]