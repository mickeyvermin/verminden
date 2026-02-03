from pydantic import BaseModel


class CreateAlbumRequest(BaseModel):
    album_name: str


class AlbumSingleResponse(BaseModel):
    album_name: str


class AlbumListResponse(BaseModel):
    album_list: list[AlbumSingleResponse]
