from select import select
from sqlalchemy.ext.asyncio import AsyncSession
import os
from models.pydantic.images import AddImagesToAlbumRequest, ImageUploadRequest
from models.sql.photos import Image
from config import Paths


async def image_upload_service(request: ImageUploadRequest, db: AsyncSession):
    file_size = request.file.file.seek(0, 2) / 1024  # in KB
    _, extension = os.path.splitext(request.file.filename)
    file_path = os.path.join(Paths.IMAGE_DIR, f"{request.file_name}{extension}")

    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join(
            Paths.IMAGE_DIR, f"{request.file_name}_{counter}{extension}"
        )
        counter += 1

    request.file.file.seek(0)

    with open(file_path, "wb") as f:
        f.write(await request.file.read())

    image_upload = Image(
        album_id=request.album_id,
        file_name=request.file_name,
        size=file_size,
        path=file_path,
    )

    db.add(image_upload)
    await db.commit()


async def add_image_to_album_service(request: AddImagesToAlbumRequest, db: AsyncSession):
    query = select(Image).filter(Image.id.in_(request.image_id_list))
    result = await db.execute(query)
    images_to_be_added = result.scalars().all()

    for image in images_to_be_added:
        image.album_id = request.album_id
        db.add(image)

    await db.commit()