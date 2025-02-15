from fastapi import FastAPI, HTTPException, Path, Query, Body
from typing import Optional, List, Dict, Annotated

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    age: int


class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User


class PostCreate(BaseModel): # для добавления нового поста
    title: str
    body: str
    author_id: int


class UserCreate(BaseModel):   # для добавления нового пользователя
    # используем Annotated[Field]
    name: Annotated[str, Field(..., title="Имя пользователя", min_length=2, max_length=20)]
    age: Annotated[int, Field(..., title="Возраст пользователя", ge=5, le=120)]


users = [
    {'id': 1, 'name': 'Jonn', 'age': 20},
    {'id': 2, 'name': 'Pen', 'age': 30},
    {'id': 3, 'name': 'Tom', 'age': 40},
]

posts = [
    {'id': 1, 'title': 'News1', 'body': 'Text1', 'author': users[1]},
    {'id': 2, 'title': 'News2', 'body': 'Text2', 'author': users[2]},
    {'id': 3, 'title': 'News3', 'body': 'Text3', 'author': users[0]},
]


@app.get("/items")
async def items() -> List[Post]:
    return [Post(**post) for post in posts]


@app.post("/items/add")
async def add_item(post: PostCreate) -> Post:
    author = next((user for user in users if user['id'] == post.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail="User not found")

    new_post_id = len(posts) + 1

    new_post = {'id': new_post_id, 'title': post.title, 'body': post.body, 'author': author}
    posts.append(new_post)

    return Post(**new_post)


@app.post("/user/add") # добавление нового user
async def user_add(user: Annotated[
    UserCreate,
    Body(..., example={
        'name': 'UserName',
        'age': 10
    })

]) -> User: # используем Annotated[Body]
    new_user_id = len(users) + 1

    new_user = {'id': new_user_id, 'name': user.name, 'age': user.age}
    users.append(new_user)

    return User(**new_user)

@app.get("/items/{id}")  # используем Annotated[..., Path] в динамике{}
async def items(id: Annotated[int, Path(..., title='Здесь указывается id поста', ge=1)]) -> Post:
    for post in posts:
        if post['id'] == id:
            return Post(**post)
    raise HTTPException(status_code=404, detail="Input number: not more 3!!!")


@app.get("/search")  # используем Annotated[..., Query] после апперсандов(?, &)
async def search(post_id: Annotated[
    Optional[int],
    Query(title="ID of post to search for", ge=1, le=50)
]) -> Dict[str, Optional[Post]]:
    if post_id:
        for post in posts:
            if post['id'] == post_id:
                return {"data": Post(**post)}
        raise HTTPException(status_code=404, detail="Input number: not more 3!!!")
    else:
        return {'data': None}


