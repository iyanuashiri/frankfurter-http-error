from sqlalchemy.orm import Session

from app.models.users import User
from app.core.security import hash_password


def get_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_by_api_key(db: Session, api_key: str) -> User | None:
    return db.query(User).filter(User.api_key == api_key).first()


def get_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def list_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.id).all()


def create_user(db: Session, username: str, password: str) -> User:
    user = User(username=username, password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user(db: Session, user: User, **kwargs, ) -> User:
    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


def decrement_credits(db: Session, user: User,) -> User:
    if user.credits > 0:
        user.credits -= 1

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()