from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    email: str
    display_name: str
    password: str


class UpdateUserFamilyRelationsRequest(BaseModel):
    user_id: int
    spouse_id: int | None
    father_id: int | None
    mother_id: int | None
    children_ids: list[int] | None
