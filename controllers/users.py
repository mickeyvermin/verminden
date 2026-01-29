from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.pydantic.commons import MessageResponse
from models.pydantic.users import CreateUserRequest, UpdateUserFamilyRelationsRequest
from services.users import create_user_service, update_user_family_relations_service
from utils.db import get_db


router = APIRouter()


@router.post("/", response_model=MessageResponse)
async def create_user_endpoint(
    request: CreateUserRequest,
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

