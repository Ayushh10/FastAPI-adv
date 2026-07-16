from typing import Annotated
from starlette import status
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from Requests import TodoRequest
from models import Todos, Users
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]     #Dependency Injection
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all(user: user_dependency, db : db_dependency):                  #Dependency Injection
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()



@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todos_id_by_users(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None: 
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todos_model = db.query(Todos).filter(Todos.owner_id == user.get('id')).filter(Todos.id == todo_id).first()
    if todos_model is None:
        raise HTTPException(status_code=404, detail=f"User {user.get('id')} has NO RECORDS of ID {todo_id}")
    return todos_model

@router.post("/create_record", status_code=status.HTTP_201_CREATED)
async def create_record(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None: 
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = Todos(**todo_request.model_dump(), owner_id = user.get('id'))
    db.add(todo_model)
    db.commit()
    return {"Todo added": todo_model}

@router.put("/{todo_id}", status_code=status.HTTP_201_CREATED)
# async def update_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail=f"Todo ID {todo_id} does not exist")
    
async def update_todos_by_user(user: user_dependency, todo_request: TodoRequest, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None: 
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.owner_id == user.get('id')).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail=f"Todo ID {todo_id} does not exist for User {user.get('id')}")
    
    todo_model.title = todo_request.title                   # type: ignore
    todo_model.description = todo_request.description       # type: ignore
    todo_model.priority = todo_request.priority             # type: ignore
    todo_model.complete = todo_request.complete             # type: ignore
    # todo_model.owner_id == user.get('id')
    db.add(todo_model)
    db.commit()
    return {f"Record updated for OwnerID {user.get('id')} and TodoID {todo_id}": todo_model}

@router.delete("/{delete_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db : db_dependency, delete_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == delete_id).first()
    if todo_model is None: 
        raise HTTPException(status_code=404, detail="RECORD NOT FOUND")
    db.query(Todos).filter(Todos.id == delete_id).delete()
    db.commit()