from datetime import datetime
from sqlalchemy import ForeignKey
from init_db import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    file_name: Mapped[str] = mapped_column(unique=True)
    size: Mapped[int]
    path: Mapped[str]
    date_added: Mapped[datetime]
    year_taken: Mapped[int]

    albums = relationship(
        "Album",
        secondary="image_album_association",
        back_populates="images",
        passive_deletes=True,
    )


class Album(Base):
    __tablename__ = "albums"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    album_name: Mapped[str] = mapped_column(unique=True)

    images = relationship(
        "Image",
        secondary="image_album_association",
        back_populates="albums",
        passive_deletes=True,
    )


class ImageToAlbumAssociation(Base):
    __tablename__ = "image_album_association"

    image_id: Mapped[int] = mapped_column(
        ForeignKey("images.id", ondelete="CASCADE"), primary_key=True
    )
    album_id: Mapped[int] = mapped_column(
        ForeignKey("albums.id", ondelete="CASCADE"), primary_key=True
    )
