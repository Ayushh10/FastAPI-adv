from pydantic import BaseModel, Field

class CreateUserRequest(BaseModel):

    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserVerification(BaseModel):
    old_password: str
    new_password: str

class TodoRequest(BaseModel):

    # id: Optional[int] = None
    title: str = Field(min_length=2, max_length=15)
    description: str = Field(min_length=3, max_length=50)
    priority: int = Field(gt=0, lt=6)
    complete: bool
