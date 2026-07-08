from typing import Optional

from pydantic import BaseModel, Field

class RequestBody(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3, max_length=10)
    author: str = Field(min_length=2)
    description: str = Field(min_length=5, max_length=100)
    rating: int = Field(gt=0, lt=6)

    model_config = {
        "json_schema_extra": {
            "example" :{
                "title": "Add Title",
                "author": "Author Name",
                "description": "Give description",
                "rating": "Add rating (0-5)"
            }
        }
    }