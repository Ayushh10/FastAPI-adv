from fastapi import APIRouter, HTTPException
from Requests import UserVerification
from models import Users
from .todos import user_dependency, db_dependency
from .auth import bcrypt_context

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.get("/")
async def get_current_user_info(user: user_dependency, db: db_dependency):
    if user is None: 
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    return user_model

@router.put("/update_password")
async def change_password(user: user_dependency, db: db_dependency, password: UserVerification):
    if user is None: 
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(password.old_password, user_model.hashed_password):                           # type: ignore
        raise HTTPException(status_code=401, detail="OLD PASSWORD MISMATCH")

    # print(f"old hash {todo_model.hashed_password}")
    user_model.hashed_password = bcrypt_context.hash(password.new_password)
    # print(f"new hash {todo_model.hashed_password}")
    db.add(user_model)
    db.commit()
    return "Password Updated successfully"
    