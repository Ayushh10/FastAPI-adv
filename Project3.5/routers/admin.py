from fastapi import APIRouter, HTTPException

from models import Todos
from .todos import user_dependency, db_dependency

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@router.get("/")
async def get_all_todos(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail="Authentication FAILED")
    todo_model = db.query(Todos).all()
    return todo_model

@router.delete("/{delete_id}")
async def delete_todo(user: user_dependency, db: db_dependency, delete_id: int):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail="Authentication FAILED")
    db.query(Todos).filter(Todos.id == delete_id).delete()
    db.commit()
    return {f"User {user.get('id')} DELETED TodoID{delete_id} SUCCESSFULLY"}
