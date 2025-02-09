from fastapi import FastAPI, HTTPException, Path, Query
from typing import Optional, List, Dict, Annotated
from pydantic import BaseModel

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


class PostCreate(BaseModel):
    title: str
    body: str
    author_id: int


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



# @app.put("/items/edit/{id}")  # редактирование запросов, put запрос
# async def add_item(post: PostCreate) -> Post:
#     author = next((user for user in users if user['id'] == post.author_id), None)
#     if not author:
#         raise HTTPException(status_code=404, detail="User not found")
#
#     new_post_id = len(posts) + 1
#
#     new_post = {'id': new_post_id, 'title': post.title, 'body': post.body, 'author': author}
#     posts.append(new_post)
#
#     return Post(**new_post)

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


