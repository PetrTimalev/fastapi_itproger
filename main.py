from fastapi import FastAPI, HTTPException
from typing import Optional, List, Dict
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


@app.get("/items/{id}")
async def items(id: int) -> Post:
    for post in posts:
        if post['id'] == id:
            return Post(**post)
    raise HTTPException(status_code=404, detail="Input number: not more 3!!!")


@app.get("/search")
async def search(post_id: Optional[int] = None) -> Dict[str, Optional[Post]]:
    if post_id:
        for post in posts:
            if post['id'] == post_id:
                return {"data": Post(**post)}
        raise HTTPException(status_code=404, detail="Input number: not more 3!!!")
    else:
        return {'data': None}

