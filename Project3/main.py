from fastapi import FastAPI
import models
from routers import auth, todos
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)













# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# db_dependency = Annotated[Session, Depends(get_db)]     #Dependency Injection

# @app.get("/", status_code=status.HTTP_200_OK)
# async def get_all(db : db_dependency):                  #Dependency Injection
#     return db.query(Todos).all()

# @app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
# async def get_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
#     todos_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todos_model is not None:
#         return todos_model
#     raise HTTPException(status_code=404, detail="XXX Record not Found XXX")

# @app.post("/todos/create_record", status_code=status.HTTP_201_CREATED)
# async def create_record(db: db_dependency, todo_request: TodoRequest):
#     todo_model = Todos(**todo_request.model_dump())
#     db.add(todo_model)
#     db.commit()

# @app.put("/todos/{todo_id}", status_code=status.HTTP_201_CREATED)
# async def update_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail=f"Todo ID {todo_id} does not exist")
    
#     todo_model.title = todo_request.title                   # type: ignore
#     todo_model.description = todo_request.description       # type: ignore
#     todo_model.priority = todo_request.priority             # type: ignore
#     todo_model.complete = todo_request.complete             # type: ignore

#     db.add(todo_model)
#     db.commit()

# @app.delete("/todos/{delete_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_todo(db : db_dependency, delete_id: int = Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id == delete_id).first()
#     if todo_model is None: 
#         raise HTTPException(status_code=404, detail="RECORD NOT FOUND")
#     db.query(Todos).filter(Todos.id == delete_id).delete()
#     db.commit()