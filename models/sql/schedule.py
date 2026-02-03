from datetime import datetime
from init_db import Base
from sqlalchemy.orm import mapped_column, Mapped


class Schedule(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    schedule_title: Mapped[str]
    schedule_description: Mapped[str | None] = mapped_column(nullable=True)
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]

class GroupSchedule(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)



