from pydantic import BaseModel


class PublicUserSchema(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str | None


class CreateUserSchema(BaseModel):
    username: str
    first_name: str
    last_name: str | None
    password: str


class UpdateUserSchema(BaseModel):
    username: str | None
    first_name: str | None
    last_name: str | None
    password: str | None
