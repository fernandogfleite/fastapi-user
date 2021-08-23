from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException
)
from decouple import config
from typing import List


from fast_api_app import (
    crud,
    schemas
)

from fast_api_app.models import Item, UserTable
from fast_api_app.database import database
from fastapi_users.db.sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users.authentication import JWTAuthentication
from fastapi_users import FastAPIUsers


SECRET_KEY = config("SECRET_KEY")

users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(schemas.UserDB, database, users)

jwt_authentication = JWTAuthentication(
    secret=SECRET_KEY, lifetime_seconds=3600)

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    schemas.User,
    schemas.UserCreate,
    schemas.UserUpdate,
    schemas.UserDB,
)

current_active_verified_user = fastapi_users.current_user(
    active=True, verified=True)

router = APIRouter(prefix="/items", tags=['items'])


@router.post("/", response_model=schemas.Item, status_code=status.HTTP_201_CREATED)
async def create_item_for_user(item: schemas.ItemCreate, current_user: schemas.User = Depends(current_active_verified_user)):
    user_id = current_user.id
    if item.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"price": "Valor inválido."})
    return await crud.create_user_item(item=item, user_id=user_id)


@router.get("/", response_model=List[schemas.Item])
async def read_items(current_user: schemas.User = Depends(current_active_verified_user)):
    user_id = current_user.id
    db_user = await crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Usuário não encontrado.")

    items = await crud.get_items(user_id=user_id)
    return items
