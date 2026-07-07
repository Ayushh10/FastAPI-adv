from fastapi import FastAPI

app = FastAPI()

Books = [
    {"title": "Title One", "Author": "Author One", "category": "Category One"},
    {"title": "Title Two", "Author": "Author Two", "category": "Category Two"},
    {"title": "Title Three", "Author": "Author Three", "category": "Category Three"},
    {"title": "Title Four", "Author": "Author Four", "category": "Category Four"},
    {"title": "Title Five", "Author": "Author Five", "category": "Category Five"}
]

@app.get("/book")
async def first_call():
    return {"message": "Hello, Ayush!"}

@app.get("/books")
async def get_all_books():
    return Books