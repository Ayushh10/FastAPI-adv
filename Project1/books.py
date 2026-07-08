from fastapi import Body, FastAPI

app = FastAPI()

Books = [
    {"title": "Title One", "Author": "Author One", "category": "Category One"},
    {"title": "Title Two", "Author": "Author Two", "category": "Category Two"},
    {"title": "Title Three", "Author": "Author Three", "category": "Category Three"},
    {"title": "Title Four", "Author": "Author Four", "category": "Science"},
    {"title": "Title Five", "Author": "Author Four", "category": "Maths"},
    {"title": "Title Five", "Author": "Author Four", "category": "History"},
    {"title": "Title Five", "Author": "Author Four", "category": "Geo"}
]

@app.get("/books")
async def get_all_books():
    return Books

@app.get("/books/{book_title}")
async def get_book(book_title: str):
    for book in Books:
        if book.get("title").casefold() == book_title.casefold():
            return {"Requested Book": book }
    return {"Book Tiltle": "Not found"}

@app.get("/books/byauthor/")
async def search_by_author(author_name: str):
    author_books = []
    for i in range(len(Books)):
        if Books[i].get("Author").casefold() == author_name.casefold():
            author_books.append(Books[i])
    return {f"All books by {author_name}": author_books}
        

@app.get("/books/{author_name}/")
async def get_books_by_category_query(author_name: str, category: str):
    books_to_return = []
    for book in Books:
        if book.get('Author').casefold() == author_name.casefold() and \
            book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.post("/books/create_book")
async def create_book(new_book = Body()):
    Books.append(new_book)
    return {"new record added": new_book}

@app.put("/books/update_book")
async def update_books(updated_book = Body()):
    for i in range(len(Books)):
        if Books[i].get("title").casefold() == updated_book.get("title").casefold():
            Books[i] == updated_book
    return {"updated Records": Books}

@app.delete("/books/delete_books/{delete_book_title}")
async def delete_book(delete_book_title: str):
    for i in range(len(Books)):
        if Books[i].get('title').casefold() == delete_book_title.casefold():
            Books.pop(i)
            break
    return {"Book deleted": delete_book_title}

