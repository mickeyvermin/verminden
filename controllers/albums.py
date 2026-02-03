from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.pydantic.albums import AlbumListResponse, AlbumSingleResponse, CreateAlbumRequest
from models.pydantic.commons import MessageResponse
from services.albums import create_album_service, get_album_by_id_service, search_albums_by_name_service
from services.auth import get_current_user
from utils.db import get_db


router = APIRouter()


@router.get("/{album_id}", response_model=AlbumSingleResponse)
async def get_album_by_id_endpoint(
    album_id: int,
    _: Annotated[dict, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    result = await get_album_by_id_service(album_id, db)
    return result


@router.get("/search/{album_name}", response_model=AlbumListResponse)
async def search_album_by_name_endpoint(
    album_name: str | None,
    db: AsyncSession = Depends(get_db),
):
    results = await search_albums_by_name_service(album_name, db)
    return results


@router.post("/", response_model=MessageResponse)
async def create_album_endpoint(
    request: CreateAlbumRequest,
    db: AsyncSession = Depends(get_db),
):
    await create_album_service(request, db)
    return MessageResponse(message=f"Album '{request.album_name}' created successfully.")
