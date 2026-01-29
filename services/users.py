from sqlalchemy import select

from sqlalchemy import or_
from classes.genealogy_node import GenealogyNode
from models.pydantic.users import CreateUserRequest, UpdateUserFamilyRelationsRequest
from sqlalchemy.ext.asyncio import AsyncSession

from models.sql.lineage import Genealogy, User


async def create_user_service(request: CreateUserRequest, db: AsyncSession):
    query = select(User).where(User.email == request.email)
    result = await db.execute(query)
    found_user = result.scalar_one_or_none()

    if found_user:
        return "Email already in use."

    new_user = User(
        email=request.email,
        display_name=request.display_name,
        password=request.password,
    )

    db.add(new_user)
    await db.flush()

    new_genealogy = Genealogy(user_id=new_user.id)

    db.add(new_genealogy)
    await db.commit()

    return "User created successfully."


async def update_user_family_relations_service(
    request: UpdateUserFamilyRelationsRequest, db: AsyncSession
):
    query = select(Genealogy).where(Genealogy.user_id == request.user_id)
    result = await db.execute(query)
    genealogy_entry = result.scalar_one_or_none()

    if not genealogy_entry:
        return "Ummm what?"

    for field, value in request.model_dump().items():
        if field != "user_id":  # Exclude "user_id" from fields to be set
            setattr(genealogy_entry, field, value)

    db.add(genealogy_entry)
    await db.commit()

    return "User family relations have been updated successfully."


async def genealogy_tree_builder(
    user_id: int, db: AsyncSession, max_depth: int, visited: set[int] = None
):
    if max_depth <= 0:
        return None
    if visited is None:
        visited = set()
    if user_id in visited:
        return None

    visited.add(user_id)
    max_depth -= 1

    genealogy_query = select(Genealogy).where(Genealogy.user_id == user_id)
    genealogy_result = await db.execute(genealogy_query)
    genealogy = genealogy_result.scalar_one_or_none()

    if not genealogy:
        return None

    parent_nodes = []
    for parent_id in [genealogy.father_id, genealogy.mother_id]:
        if parent_id:
            parent_node = await genealogy_tree_builder(
                parent_id, db, max_depth, visited
            )
            if parent_node:
                parent_nodes.append(parent_node)

    spouse_node = None
    if genealogy.spouse_id:
        spouse_node = await genealogy_tree_builder(
            genealogy.spouse_id, db, max_depth, visited
        )

    children_query = select(Genealogy).where(
        or_(Genealogy.father_id == user_id, Genealogy.mother_id == user_id)
    )
    children_result = await db.execute(children_query)
    children = children_result.scalars().all()
    children_nodes = []
    for child in children:
        child_node = await genealogy_tree_builder(child.user_id, db, max_depth, visited)
        if child_node:
            children_nodes.append(child_node)

    return GenealogyNode(
        user_id=user_id,
        parent_nodes=parent_nodes,
        spouse_node=spouse_node,
        children_nodes=children_nodes,
    )
