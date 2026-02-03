from models.pydantic.groups import CreateGroupRequest
from models.sql.gather import Group, UserGroupAssociation
from sqlalchemy.ext.asyncio import AsyncSession


async def create_group_service(request: CreateGroupRequest, db: AsyncSession):
    new_group = Group(display_name=request.display_name)
    db.add(new_group)
    await db.flush()

    for member_id in request.members_ids:
        new_member_group_association = UserGroupAssociation(
            user_id=member_id, group_id=new_group.id
        )
        db.add(new_member_group_association)

    await db.commit()


