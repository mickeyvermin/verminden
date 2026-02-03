from fastapi import APIRouter
from controllers import (
    images,
    albums,
    users
)

router = APIRouter()

router.include_router(images.router, prefix="/images", tags=["Images"])
router.include_router(albums.router, prefix="/albums", tags=["Albums"])
router.include_router(users.router, prefix="/users", tags=["Users"])
