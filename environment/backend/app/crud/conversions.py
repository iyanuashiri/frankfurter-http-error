from sqlalchemy.orm import Session

from app.models.conversions import Conversion


def create_conversion(db: Session, *,user_id: int, base_currency: str, target_currency: str, 
                      amount: float, exchange_rate: float, converted_amount: float):
    conversion = Conversion(user_id=user_id, base_currency=base_currency, 
                            target_currency=target_currency, amount=amount, 
                            exchange_rate=exchange_rate, converted_amount=converted_amount)

    db.add(conversion)
    db.commit()
    db.refresh(conversion)

    return conversion


def get_user_conversions(db: Session, user_id: int):
    return (
        db.query(Conversion).filter(Conversion.user_id == user_id).
        order_by(Conversion.created_at.desc()).all()
    )