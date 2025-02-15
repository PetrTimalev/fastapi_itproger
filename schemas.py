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


class PostCreate(PostBase):  # для добавления нового поста
    pass


class Post(PostBase):
    id: int
    author: User

    class Config:
        orm_mode = True
