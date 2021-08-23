from fast_api_app import schemas
from fast_api_app.routers import items
from fastapi import FastAPI, Request, Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyUserDatabase
from fast_api_app.database import Base, engine, database
from fast_api_app.models import UserTable
from fast_api_app.config import Settings
from decouple import config
from functools import lru_cache

SECRET = config('SECRET_KEY')


Base.metadata.create_all(engine)

users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(schemas.UserDB, database, users)


def on_after_register(user: schemas.UserDB, request: Request):
    print(f"User {user.id} has registered.")


def on_after_forgot_password(user: schemas.UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


def after_verification_request(user: schemas.UserDB, token: str, request: Request):
    print(
        f"Verification requested for user {user.id}. Verification token: {token}")


jwt_authentication = JWTAuthentication(
    secret=SECRET, lifetime_seconds=3600, tokenUrl="auth/jwt/login"
)

app = FastAPI()
fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    schemas.User,
    schemas.UserCreate,
    schemas.UserUpdate,
    schemas.UserDB,
)

app.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)

app.include_router(
    fastapi_users.get_reset_password_router(
        SECRET, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(
        SECRET, after_verification_request=after_verification_request
    ),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(fastapi_users.get_users_router(requires_verification=True),
                   prefix="/users", tags=["users"])

app.include_router(items.router, prefix="/users")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@lru_cache()
def get_settings():
    return Settings(admin_email="fernandogfleite@gmail.com")


@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
