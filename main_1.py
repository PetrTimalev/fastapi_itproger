from fastapi import FastAPI, HTTPException, Path, Query
from typing import Optional, List, Dict, Annotated
from pydantic import BaseModel, Field

# Создание экземпляра FastAPI
app = FastAPI()


# Модель данных для пользователя
class User(BaseModel):
    id: int  # Уникальный идентификатор пользователя
    name: str  # Имя пользователя
    age: int  # Возраст пользователя


# Модель данных для поста
class Post(BaseModel):
    id: int  # Уникальный идентификатор поста
    title: str  # Заголовок поста
    body: str  # Текст поста
    author: User  # Автор поста (связь с моделью User)


# Модель данных для создания нового поста
class PostCreate(BaseModel):
    title: str  # Заголовок поста
    body: str  # Текст поста
    author_id: int  # ID автора поста


# Модель данных для создания нового пользователя
class UserCreate(BaseModel):
    # Используем Annotated для добавления метаданных и валидации
    # Имя пользователя (от 2 до 20 символов), Имя пользователя (от 2 до 20 символов)
    name: Annotated[str, Field(..., title="Имя пользователя", min_length=2, max_length=20)]
    # Возраст пользователя (от 5 до 120 лет)
    age: Annotated[int, Field(..., title="Возраст пользователя", ge=5, le=120)]


# Инициализация данных: список пользователей
users = [
    {'id': 1, 'name': 'Jonn', 'age': 20},
    {'id': 2, 'name': 'Pen', 'age': 30},
    {'id': 3, 'name': 'Tom', 'age': 40},
]

# Инициализация данных: список постов
posts = [
    {'id': 1, 'title': 'News1', 'body': 'Text1', 'author': users[1]},
    {'id': 2, 'title': 'News2', 'body': 'Text2', 'author': users[2]},
    {'id': 3, 'title': 'News3', 'body': 'Text3', 'author': users[0]},
]


# Эндпоинт для получения всех постов
@app.get("/items")
async def items() -> List[Post]:
    return [Post(**post) for post in posts]


# Эндпоинт для добавления нового поста
@app.post("/items/add")
async def add_item(post: PostCreate) -> Post:
    # Поиск автора поста по ID
    author = next((user for user in users if user['id'] == post.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail="User not found")  # Если автор не найден, возвращаем ошибку 404

    # Генерация нового ID для поста
    new_post_id = len(posts) + 1

    # Создание нового поста
    new_post = {'id': new_post_id, 'title': post.title, 'body': post.body, 'author': author}
    posts.append(new_post)  # Добавление поста в список

    return Post(**new_post)  # Возвращаем созданный пост


# Эндпоинт для добавления нового пользователя
@app.post("/user/add")
async def user_add(user: UserCreate) -> User:
    # Генерация нового ID для пользователя
    new_user_id = len(users) + 1

    # Создание нового пользователя
    new_user = {'id': new_user_id, 'name': user.name, 'age': user.age}
    users.append(new_user)  # Добавление пользователя в список

    return User(**new_user)  # Возвращаем созданного пользователя


# Эндпоинт для получения поста по ID
@app.get("/items/{id}")
async def items(id: Annotated[int, Path(..., title='Здесь указывается id поста', ge=1)]) -> Post:
    # Поиск поста по ID
    for post in posts:
        if post['id'] == id:
            return Post(**post)  # Возвращаем найденный пост
    # Если пост не найден, возвращаем ошибку 404
    raise HTTPException(status_code=404, detail="Input number: not more 3!!!")


# Эндпоинт для поиска поста по ID через query-параметр
@app.get("/search")
async def search(post_id: Annotated[
    Optional[int],
    Query(title="ID of post to search for", ge=1, le=50)
]) -> Dict[str, Optional[Post]]:
    if post_id:
        # Поиск поста по ID
        for post in posts:
            if post['id'] == post_id:
                return {"data": Post(**post)}  # Возвращаем найденный пост
        # Если пост не найден, возвращаем ошибку 404
        raise HTTPException(status_code=404, detail="Input number: not more 3!!!")
    else:
        return {'data': None}  # Если post_id не указан, возвращаем None
