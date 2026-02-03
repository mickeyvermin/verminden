from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.groups import create_group_service
from models.pydantic.groups import CreateGroupRequest
from models.pydantic.commons import MessageResponse
from utils.db import get_db

router = APIRouter()

@router.post("/", response_model=MessageResponse)
async def create_group_endpoint(
    request: CreateGroupRequest,
    db: AsyncSession = Depends(get_db),
):
    await create_group_service(request, db)
    return MessageResponse(message="Group created successfully.")