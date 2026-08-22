from pydantic import BaseModel, ConfigDict, Field


class PublicUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    first_name: str
    last_name: str | None = None


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'  # noqa: S105


class CreateUserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=32, pattern=r'^[a-zA-Z0-9_.-]+$')
    first_name: str = Field(min_length=1, max_length=64)
    last_name: str | None = None
    password: str = Field(min_length=12, max_length=128)
