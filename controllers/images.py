from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.pydantic.commons import MessageResponse
from models.pydantic.images import AddImagesToAlbumRequest, ImageUploadRequest
from services.photos import add_image_to_album_service, image_upload_service
from utils.db import get_db

router = APIRouter()

@router.post("/", response_model=MessageResponse)
async def image_upload_endpoint(
    request: ImageUploadRequest = Depends(ImageUploadRequest.as_form),
    db: AsyncSession = Depends(get_db),
):
    await image_upload_service(request, db)
    return MessageResponse(message="Image uploaded successfully.")

@router.put("/add-to-album", response_model=MessageResponse)
async def add_images_to_album_endpoint(
    request: AddImagesToAlbumRequest,
    db: AsyncSession = Depends(get_db),
):
    await add_image_to_album_service(request, db)
    return MessageResponse(message="Images added to album successfully")
