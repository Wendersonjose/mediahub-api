from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str


class PostResponse(BaseModel):
    title: str
    content: str


class UserRead(BaseModel):
    id: str
    username: str
    email: str


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
