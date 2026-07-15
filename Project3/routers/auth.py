from typing import Annotated
from starlette import status
import bcrypt
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from Requests import CreateUserRequest

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]     #Dependency Injection

@router.get("/auth/all")
async def get_all_users(db: db_dependency):
    return db.query(Users).all()

def hash_password(userPassword: str):
    password = userPassword.encode('utf-8')
# Generate a salt with a specific work factor (default is 12)
    salt = bcrypt.gensalt(rounds=12)
# Hash the password
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password

@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest, db: db_dependency):
    create_new_user = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,           
        hashed_password = str(hash_password(create_user_request.password)),
        is_active = True
    )
    db.add(create_new_user)
    db.commit()
    return {"New User Added": create_new_user}



