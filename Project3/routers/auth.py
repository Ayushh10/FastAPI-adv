from fastapi import APIRouter
from models import Users
from Requests import CreateUserRequest
from routers.todos import db_dependency

router = APIRouter()



# @router.get("/auth/")
# async def get_users():
#     return {"User": "Authenticated"}

@router.post("/auth")
async def create_user(create_user_request: CreateUserRequest):
    create_new_user = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,           
        hashed_password = create_user_request.password,
        is_active = True
    )
    return create_new_user
