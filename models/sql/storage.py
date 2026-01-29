from sqlalchemy import ForeignKey
from init_db import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    item_name: Mapped[str]
    container_id: Mapped[int] = mapped_column(ForeignKey("containers.id"))

    container = relationship(
        "Container", foreign_keys=[container_id], back_populates="items"
    )


class Container(Base):
    __tablename__ = "containers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    container_name: Mapped[str] = mapped_column(unique=True)

    items = relationship("Item", back_populates="container")
