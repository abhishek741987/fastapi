
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter,  Depends, HTTPException, Path, Query
from models import Todos
from database import SessionLocal, engine
from starlette import status
from routers.auth import get_current_user


router = APIRouter(
    prefix='/todo',
    tags=['todo']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get("/")
async def read_all(user: user_dependency, db: db_dependency):
    if user is not None:
        current_role = user.get('user_role')

        if current_role == 'Admin':
            return db.query(Todos).all()
        else:
            return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()
    else:
        raise HTTPException(401, "No Todos Found")


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_data = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_data is not None:
        return todo_data
    raise HTTPException(404, "Todo not found")


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_tooo(user: user_dependency, db: db_dependency, model: TodoRequest):

    if user is None:
        raise HTTPException(401, "Authentication Failed")

    new_model = Todos(**model.model_dump(), owner_id=user.get('id'))
    db.add(new_model)
    db.commit()


@router.put("/update", status_code=status.HTTP_200_OK)
async def update_todo(db: db_dependency,  todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    print(todo_model)
    if todo_model is not None:

        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete

        db.add(todo_model)
        db.commit()

    else:
        raise HTTPException(404, "Todo not found")


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(404, "Todo not found")

    db.delete(todo_model)
    db.commit()
