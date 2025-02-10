from pydantic import BaseModel


class UserBase(BaseModel):  # базовый класс User
    name: str
    age: int


class UserCreate(UserBase):
    pass


class User(UserBase):  # наследуем от класса UserBase
    id: int

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    body: str
    author_id: int


class PostCreate(BaseModel): # для добавления нового поста
    title: str
    body: str
    author_id: int
