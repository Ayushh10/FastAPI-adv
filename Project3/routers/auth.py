from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from starlette import status
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from Requests import CreateUserRequest, Token

router = APIRouter()

SECRET_KEY = 'c5319bd1930daa5388097b61a024d3dd'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]     #Dependency Injection

def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if not user :
        return False
    if not bcrypt_context.verify(password, user.hashed_password):        # type: ignore
        return False
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}             # type: ignore
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})                                     # type: ignore
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)          # type: ignore

@router.get("/auth/all")
async def get_all_users(db: db_dependency):
    return db.query(Users).all()

# def hash_password(userPassword: str):
#     password = userPassword.encode('utf-8')
# # Generate a salt with a specific work factor (default is 12)
#     salt = bcrypt.gensalt(rounds=12)
# # Hash the password
#     hashed_password = bcrypt.hashpw(password, salt)
#     return hashed_password

@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest, db: db_dependency):
    create_new_user = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,           
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True
    )
    db.add(create_new_user)
    db.commit()
    return {"New User Added": create_new_user}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db : db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user: 
        return "Authentication Failed"
    token = create_access_token(user.username , user.id, user.role, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}