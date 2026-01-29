from sqlalchemy import ForeignKey
from init_db import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True)
    display_name: Mapped[str]
    password: Mapped[str]

    genealogy = relationship("Genealogy", back_populates="user", passive_deletes=True)
    groups = relationship(
        "Group",
        secondary="user_group_association",
        back_populates="users",
        passive_deletes=True,
    )


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    display_name: Mapped[str]

    users = relationship(
        "User",
        secondary="user_group_association",
        back_populates="groups",
        passive_deletes=True,
    )


class Genealogy(Base):
    __tablename__ = "genealogy"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    spouse_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    father_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    mother_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    user = relationship("User", foreign_keys=[user_id])
    spouse = relationship("User", foreign_keys=[spouse_id])
    father = relationship("User", foreign_keys=[father_id])
    mother = relationship("User", foreign_keys=[mother_id])


class UserGroupAssociation(Base):
    __tablename__ = "user_group_association"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True
    )

    users = relationship("User", foreign_keys=[user_id])
    group = relationship("Group", foreign_keys=[group_id])
