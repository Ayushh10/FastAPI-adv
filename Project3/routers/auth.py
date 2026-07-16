from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette import status
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from Requests import CreateUserRequest, Token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET_KEY = 'c5319bd1930daa5388097b61a024d3dd'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')          # Client will send this URL to our fastAPI app; 
                                                                # we need it to vrify our Token as a dependency in our API request

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
    if not bcrypt_context.verify(password, user.hashed_password):                           # type: ignore
        return False
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}                                 # type: ignore
    expires = datetime.now(timezone.utc) + expires_delta   # when JWT will expire
    encode.update({'exp': expires})                                                         # type: ignore
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)                              # type: ignore

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):                  # type: ignore
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')                                                  # type: ignore
        user_id: int = payload.get('id')                                                    # type: ignore
        if username is None and user_id is None:                                            # type: ignore
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
        return {'username': username, 'id': user_id}                                        # type: ignore
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

@router.get("/all")
async def get_all_users(db: db_dependency):
    return db.query(Users).all()

@router.post("/", status_code=status.HTTP_201_CREATED)
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    token = create_access_token(user.username , user.id, user.role, timedelta(minutes=20))  # type: ignore
    return {"access_token": token, "token_type": "bearer"}