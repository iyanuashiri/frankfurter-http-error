from fastapi import APIRouter, HTTPException, status

from app.crud.users import create_user, get_by_username, list_users
from app.api.deps import DBSession
from app.schemas.users import UserCreate, UserResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(user: UserCreate, db: DBSession):
    existing_user = get_by_username(db, user.username)

    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Username already exists")

    created_user = create_user(db=db, username=user.username, password=user.password)

    return created_user


@router.get("/", response_model=list[UserResponse])
async def get_users(db: DBSession, ):
    return list_users(db)