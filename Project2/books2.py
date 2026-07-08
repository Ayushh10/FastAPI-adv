from fastapi import FastAPI
from class_books import Books

app = FastAPI()

Books = [
    Books(1, "Book One", "Author One", "About book one", 4),
    Books(2, "Book Two", "Author Two", "About book Two", 2),
    Books(3, "Book Three", "Author Three", "About book Three", 5),
    Books(4, "Book Four", "Author Four", "About book Four", 1),
    Books(5, "Book Five", "Author Five", "About book Five", 3),
    Books(6, "Book Six", "Author Six", "About book Six", 4)
]

@app.get("/books")
async def get_all_books():
    return Books