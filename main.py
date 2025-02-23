from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from typing import Optional, List, Dict, Annotated
from sqlalchemy.orm import Session

from models import Base, User, Post
from database import engine, session_local
from schemas import UserCreate, User as DbUser, PostCreate, PostResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():  # подключение к базе
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.post("/user/", response_model=DbUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


