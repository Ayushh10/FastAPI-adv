from fastapi import FastAPI
from BookRequest import RequestBody
from book_model import Book

app = FastAPI()

BOOKS = [
    Book(1, "Book One", "Author One", "About book one", 4),
    Book(2, "Book Two", "Author Two", "About book Two", 2),
    Book(3, "Book Three", "Author Three", "About book Three", 5),
    Book(4, "Book Four", "Author Four", "About book Four", 1),
    Book(5, "Book Five", "Author Five", "About book Five", 3),
    Book(6, "Book Six", "Author Six", "About book Six", 4)
]

@app.get("/books")
async def get_all_books():
    return BOOKS

@app.post("/books/create_new")
async def create_new_book(book_request: RequestBody):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return new_book

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


