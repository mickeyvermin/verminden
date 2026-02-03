from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.pydantic.commons import MessageResponse
from models.pydantic.users import (
    CreateUserRequest,
    LoginRequest,
    Token,
    UpdateUserFamilyRelationsRequest,
)
from services.auth import authenticate_user, create_access_token, get_current_user
from services.users import create_user_service, update_user_family_relations_service
from utils.db import get_db
from starlette.status import HTTP_401_UNAUTHORIZED


router = APIRouter()


@router.post("/signup", response_model=MessageResponse)
async def create_user_endpoint(
    request: CreateUserRequest,
    db: AsyncSession = Depends(get_db),
):
    create_user_message = await create_user_service(request, db)
    return MessageResponse(message=create_user_message)


@router.post("/signin", response_model=MessageResponse)
async def user_sign_in_endpoint(
    request: CreateUserRequest,
    _: Annotated[dict, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    create_user_message = await create_user_service(request, db)
    return MessageResponse(message=create_user_message)


@router.put("/parents", response_model=MessageResponse)
async def update_user_parents_endpoint(
    request: UpdateUserFamilyRelationsRequest,
    db: AsyncSession = Depends(get_db),
):
    update_user_family_relations_message = await update_user_family_relations_service(
        request, db
    )
    return MessageResponse(message=update_user_family_relations_message)


@router.post("/login")
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(request.email, request.password, db)
    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    token = create_access_token(user.email, user.id, timedelta(minutes=20))

    return Token(access_token=token)
