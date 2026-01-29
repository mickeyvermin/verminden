from fastapi import UploadFile
from pydantic import BaseModel

from utils.decorators import as_form


@as_form
class ImageUploadRequest(BaseModel):
    file: UploadFile
    file_name: str
    album_id: int | None = None
    year_taken: int


class AddImagesToAlbumRequest(BaseModel):
    image_id_list: list[int]
    album_id: int
