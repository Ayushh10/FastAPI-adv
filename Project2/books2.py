from fastapi import FastAPI, Path, Query, HTTPException
from starlette import status
from BookRequest import RequestBody
from book_model import Book

app = FastAPI()

BOOKS = [
    Book(1, "Book One", "Author One", 1999, "About book one", 4),
    Book(2, "Book Two", "Author Two", 2000, "About book Two", 2),
    Book(3, "Book Three", "Author Three", 2000, "About book Three", 5),
    Book(4, "Book Four", "Author Four", 2000, "About book Four", 1),
    Book(5, "Book Five", "Author Five", 2003 ,"About book Five", 3),
    Book(6, "Book Six", "Author Six", 2004, "About book Six", 4)
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def get_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def search_by_book_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return {f"Found book with {book_id}": book}
    raise HTTPException(status_code=404, detail="RECORD NOT FOUND")

@app.get("/books/", status_code=status.HTTP_200_OK)
async def fetch_by_rating(book_rating: int = Query(gt=0, lt=6)):                            # type: ignore
    new_book = []
    for book in BOOKS:
        if book.rating == book_rating:
            new_book.append(book)                                       # type: ignore
    return {f"Here are the books with ratings {book_rating}": new_book} # type: ignore

@app.get("/books/published_date/", status_code=status.HTTP_200_OK)
async def filter_by_date(published_date: int = Query(gt=1999, lt=2050)):                          # type: ignore
    book_list = []
    for book in BOOKS:
        if book.published_date == published_date:
            book_list.append(book)                                      # type: ignore
    return {f"Book with published_date {published_date} are": book_list}# type: ignore

@app.post("/books/create_new", status_code=status.HTTP_201_CREATED)
async def create_new_book(book_request: RequestBody):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return new_book

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.put("/books/update_book_info", status_code=status.HTTP_204_NO_CONTENT)
async def update_book_info(book: RequestBody):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book                 # type: ignore
            book_changed = True             # type: ignore
            return {"Information updated": BOOKS[i]}
    if not book_changed:
        raise HTTPException(status_code=404, detail="RECORD NOT FOUND")

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            return "ITEM REMOVED"
    if not book_changed:
        raise HTTPException(status_code=404, detail="RECORD NOT FOUND")
