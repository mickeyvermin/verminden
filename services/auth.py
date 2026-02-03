from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from config import get_settings
from models.pydantic.users import AuthenticatedUser
from models.sql.gather import User
from passlib.context import CryptContext


def get_oauth2_bearer():
    return OAuth2PasswordBearer(tokenUrl="auth/token")


def get_bcrypt_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


config = get_settings()
bcrypt_context = get_bcrypt_context()


# This checks if login credentials are correct
async def authenticate_user(email: str, password: str, db: AsyncSession):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user or not bcrypt_context.verify(password, user.hashed_password):
        return False

    return user


# This generates an access token for successful login. Will be called if authenticate_user is successful.
def create_access_token(email: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": email, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


# Dependency injection into API endpoints to ensure user is authenticated before being allowed to call endpoint
async def get_current_user(token: Annotated[str, Depends(get_oauth2_bearer())]):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        email: str = payload.get("sub")
        user_id: str = payload.get("id")
        if email is None or user_id is None:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate user."
            )
        # TODO: Add scope-based authentication layer before returning AuthenticatedUser

        return AuthenticatedUser(user_id=user_id)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )
