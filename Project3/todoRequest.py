from pydantic import BaseModel, Field

class TodoRequest(BaseModel):
    __tablename__ = 'todos'

    # id: Optional[int] = None
    title: str = Field(min_length=2, max_length=15)
    description: str = Field(min_length=3, max_length=50)
    priority: int = Field(gt=0, lt=6)
    complete: bool

    # def __init__(self, title, description, priority, complete):      # type: ignore
    #     self.id = id
    #     self.title = title
    #     self.description = description
    #     self. priority = priority
    #     self.complete = complete