class Book:
    id: int
    title: str
    author: str
    published_date: int
    description: str
    rating: int

    def __init__(self, id, title, author, published_date, description, rating): # type: ignore
        self.id = id
        self.title = title
        self.author = author
        self.published_date = published_date
        self.description = description
        self.rating = rating