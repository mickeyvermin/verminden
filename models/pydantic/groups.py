from utils.db import Base


class CreateGroupRequest(Base):
    display_name: str
    members_ids: list[int]