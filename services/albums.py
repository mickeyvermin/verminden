from select import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.pydantic.albums import (
    AlbumListResponse,
    AlbumSingleResponse,
    CreateAlbumRequest,
)
from models.sql.photos import Album


async def get_album_by_id_service(
    album_id: int, db: AsyncSession
) -> AlbumSingleResponse:
    query = select(Album).where(Album.id == album_id)
    result = await db.execute(query)
    album = result.scalar_one_or_none()

    return AlbumSingleResponse(album.album_name)


async def search_albums_by_name_service(
    album_name: int, db: AsyncSession
) -> AlbumListResponse:
    query = select(Album).where(Album.album_name.icontains(album_name))
    result = await db.execute(query)
    albums = result.scalars().all()

    return AlbumListResponse(albums)


async def create_album_service(request: CreateAlbumRequest, db: AsyncSession):
    new_album = Album(album_name=request.album_name)

    db.add(new_album)
    await db.commit()
