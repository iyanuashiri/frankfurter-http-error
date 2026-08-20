from fastapi import APIRouter, HTTPException, status
from limits import parse
from limits.aio.strategies import FixedWindowRateLimiter
from limits.storage import storage_from_string

from frankfurter.rest_adapter import RestAdapter

from app.api.deps import CurrencyService, CurrentUser, DBSession
from app.crud.users import decrement_credits
from app.crud.conversions import create_conversion, get_user_conversions
from app.schemas.conversions import ConversionHistoryResponse
from app.services.currency_service import Currency 


router = APIRouter(prefix="/currencies", tags=["Currencies"])

memory = storage_from_string("async+memory://")
rate_limiter = FixedWindowRateLimiter(memory)
ten_per_minute = parse("10/minute")

currency_service = Currency()


@router.get("/")
async def get_currencies(current_user: CurrentUser, db: DBSession, service: CurrencyService):
    if current_user.credits < 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough credits")

    window = await rate_limiter.get_window_stats(ten_per_minute, "subscriptions", current_user.id)

    # TODO:
    # The current implementation allows 9 successful requests and rejects the 10th
    # with a 10/minute limit. Investigate the limits library usage to ensure the
    # intended behavior is 10 successful requests and the 11th is rejected.
    if window.remaining < 1:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded",
        )

    response = await service.get_currencies()

    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currencies not found",
        )

    await rate_limiter.hit(ten_per_minute, "subscriptions", current_user.id)

    current_user = decrement_credits(db, current_user)

    return {"currencies": response, "credits": current_user.credits}


@router.get("/conversions/")
async def get_currency_rates(base_currency: str, target_currency: str, amount: float,
                             current_user: CurrentUser, db: DBSession):
    if current_user.credits <= 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough credits",
        )

    window = await rate_limiter.get_window_stats(ten_per_minute, "subscriptions",
        current_user.id,
    )

    if window.remaining < 1:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded",
        )

    response = await currency_service.convert(
        base_currency=base_currency, target_currency=target_currency)

    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency rates not found",
        )
    
    await rate_limiter.hit(ten_per_minute, "subscriptions", current_user.id,
    )

    current_user = decrement_credits(db, current_user)

    rate = response["rates"][target_currency]
    converted_amount = amount * rate
    create_conversion(
        db=db, user_id=current_user.id, base_currency=base_currency, 
        target_currency=target_currency, amount=amount, exchange_rate=rate, 
        converted_amount=converted_amount)

    return {"base_currency": base_currency, "target_currency": target_currency,
            "amount": amount, "rate": rate, "converted_amount": converted_amount,
            "credits": current_user.credits,
    }


@router.get("/historical-rates/{date}")
async def get_historical_currency_rates(date: str, base_currency: str = "USD",
                                        target_currency: str = "EUR", current_user: CurrentUser = None,
                                        db: DBSession = None):
    if current_user.credits < 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough credits",
        )

    window = await rate_limiter.get_window_stats(ten_per_minute, "subscriptions", current_user.id,
    )

    if window.remaining < 1:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, 
            detail="Rate limit exceeded",
        )

    response = await currency_service.historical(
        date=date, base_currency=base_currency, target_currency=target_currency)

    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Historical currency rates not found",
        )

    await rate_limiter.hit(ten_per_minute, "subscriptions", current_user.id)

    current_user = decrement_credits(db, current_user)

    return {
        "base_currency": base_currency, "date": date, "rates": response,
        "credits": current_user.credits,
    }


@router.get("/history", response_model=list[ConversionHistoryResponse])
def get_history(current_user: CurrentUser, db: DBSession):
    return get_user_conversions(db, current_user.id)