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

@app.get("/books/{search_by_book_id}")
async def search_by_book_id(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return {f"Found book with {book_id}": book}
    return "No Record found"

@app.get("/books/")
async def fetch_by_rating(book_rating: int):                            # type: ignore
    new_book = []
    for book in BOOKS:
        if book.rating == book_rating:
        #     return f"Books with ratings {book_rating} NOT FOUND"
        # else:
            new_book.append(book)                                       # type: ignore
    return {f"Here are the books with ratings {book_rating}": new_book} # type: ignore

@app.post("/books/create_new")
async def create_new_book(book_request: RequestBody):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return new_book

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.put("/books/update_book_info")
async def update_book_info(book: RequestBody):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book                             # type: ignore
            return {"Information updated": BOOKS[i]}
    return "Record not FOUND"

@app.delete("/books/{book_id}")
async def delete_by_id(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return "ITEM REMOVED"
