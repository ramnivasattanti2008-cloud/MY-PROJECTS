"""
Python GraphQL API using Strawberry
A simple GraphQL API with queries and mutations for managing books.
"""

import strawberry
from datetime import datetime
from uuid import uuid4
from typing import Optional, List
from dataclasses import dataclass, field


# In-memory database
books_db: dict = {
    "1": {
        "id": "1",
        "title": "The Pragmatic Programmer",
        "author": "David Thomas & Andrew Hunt",
        "isbn": "978-0135957059",
        "published_year": 2019,
        "genre": "Technology",
        "rating": 4.8,
        "available": True,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    },
    "2": {
        "id": "2",
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "978-0132350884",
        "published_year": 2008,
        "genre": "Technology",
        "rating": 4.6,
        "available": True,
        "created_at": "2024-01-02T00:00:00",
        "updated_at": "2024-01-02T00:00:00"
    }
}


# Strawberry Types
@strawberry.type
class Book:
    id: str
    title: str
    author: str
    isbn: str
    published_year: int
    genre: str
    rating: float
    available: bool
    created_at: str
    updated_at: str


@strawberry.type
class BookList:
    books: List[Book]
    total: int


@strawberry.type
class DeleteResponse:
    success: bool
    message: str
    id: str


@strawberry.type
class Stats:
    total_books: int
    total_authors: int
    average_rating: float
    available_count: int
    genres: List[str]


# Input Types
@strawberry.input
class BookInput:
    title: str
    author: str
    isbn: str
    published_year: int
    genre: str
    rating: float = 0.0
    available: bool = True


@strawberry.input
class BookUpdateInput:
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    published_year: Optional[int] = None
    genre: Optional[str] = None
    rating: Optional[float] = None
    available: Optional[bool] = None


@strawberry.input
class BookFilterInput:
    genre: Optional[str] = None
    author: Optional[str] = None
    published_year: Optional[int] = None
    min_rating: Optional[float] = None
    available_only: Optional[bool] = None


# Queries
@strawberry.type
class Query:
    @strawberry.field
    def book(self, id: str) -> Optional[Book]:
        """Get a single book by ID."""
        book_data = books_db.get(id)
        if book_data:
            return Book(**book_data)
        return None

    @strawberry.field
    def books(
        self,
        filter: Optional[BookFilterInput] = None,
        limit: int = 10,
        offset: int = 0
    ) -> BookList:
        """List all books with optional filtering and pagination."""
        result = list(books_db.values())

        # Apply filters
        if filter:
            if filter.genre:
                result = [b for b in result if b["genre"].lower() == filter.genre.lower()]
            if filter.author:
                result = [b for b in result if filter.author.lower() in b["author"].lower()]
            if filter.published_year:
                result = [b for b in result if b["published_year"] == filter.published_year]
            if filter.min_rating:
                result = [b for b in result if b["rating"] >= filter.min_rating]
            if filter.available_only is not None:
                result = [b for b in result if b["available"] == filter.available_only]

        total = len(result)

        # Apply pagination
        result = result[offset:offset + limit]

        return BookList(
            books=[Book(**b) for b in result],
            total=total
        )

    @strawberry.field
    def search_books(self, query: str) -> List[Book]:
        """Search books by title or author."""
        q = query.lower()
        results = [
            b for b in books_db.values()
            if q in b["title"].lower() or q in b["author"].lower()
        ]
        return [Book(**b) for b in results]

    @strawberry.field
    def book_by_isbn(self, isbn: str) -> Optional[Book]:
        """Get a book by ISBN."""
        for book_data in books_db.values():
            if book_data["isbn"] == isbn:
                return Book(**book_data)
        return None

    @strawberry.field
    def genres(self) -> List[str]:
        """Get all unique genres."""
        return list(set(b["genre"] for b in books_db.values()))

    @strawberry.field
    def authors(self) -> List[str]:
        """Get all unique authors."""
        return list(set(b["author"] for b in books_db.values()))

    @strawberry.field
    def stats(self) -> Stats:
        """Get library statistics."""
        all_books = list(books_db.values())
        return Stats(
            total_books=len(all_books),
            total_authors=len(set(b["author"] for b in all_books)),
            average_rating=round(sum(b["rating"] for b in all_books) / len(all_books), 2) if all_books else 0,
            available_count=sum(1 for b in all_books if b["available"]),
            genres=list(set(b["genre"] for b in all_books))
        )


# Mutations
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_book(self, input: BookInput) -> Book:
        """Create a new book."""
        now = datetime.utcnow().isoformat()

        # Check for duplicate ISBN
        for b in books_db.values():
            if b["isbn"] == input.isbn:
                raise ValueError(f"Book with ISBN {input.isbn} already exists")

        book_id = str(uuid4())
        book_data = {
            "id": book_id,
            "title": input.title,
            "author": input.author,
            "isbn": input.isbn,
            "published_year": input.published_year,
            "genre": input.genre,
            "rating": max(0, min(5, input.rating)),
            "available": input.available,
            "created_at": now,
            "updated_at": now
        }

        books_db[book_id] = book_data
        return Book(**book_data)

    @strawberry.mutation
    def update_book(self, id: str, input: BookUpdateInput) -> Optional[Book]:
        """Update an existing book."""
        if id not in books_db:
            return None

        book_data = books_db[id]

        # Check for duplicate ISBN if being updated
        if input.isbn and input.isbn != book_data["isbn"]:
            for b in books_db.values():
                if b["isbn"] == input.isbn and b["id"] != id:
                    raise ValueError(f"Book with ISBN {input.isbn} already exists")

        # Update fields
        updates = {}
        if input.title is not None:
            updates["title"] = input.title
        if input.author is not None:
            updates["author"] = input.author
        if input.isbn is not None:
            updates["isbn"] = input.isbn
        if input.published_year is not None:
            updates["published_year"] = input.published_year
        if input.genre is not None:
            updates["genre"] = input.genre
        if input.rating is not None:
            updates["rating"] = max(0, min(5, input.rating))
        if input.available is not None:
            updates["available"] = input.available

        if updates:
            updates["updated_at"] = datetime.utcnow().isoformat()
            books_db[id].update(updates)

        return Book(**books_db[id])

    @strawberry.mutation
    def delete_book(self, id: str) -> DeleteResponse:
        """Delete a book."""
        if id not in books_db:
            return DeleteResponse(success=False, message="Book not found", id=id)

        del books_db[id]
        return DeleteResponse(success=True, message="Book deleted successfully", id=id)

    @strawberry.mutation
    def toggle_availability(self, id: str) -> Optional[Book]:
        """Toggle book availability."""
        if id not in books_db:
            return None

        books_db[id]["available"] = not books_db[id]["available"]
        books_db[id]["updated_at"] = datetime.utcnow().isoformat()

        return Book(**books_db[id])


# Create schema
schema = strawberry.Schema(query=Query, mutation=Mutation)


# FastAPI app for serving
try:
    from fastapi import FastAPI
    from strawberry.fastapi import GraphQLRouter

    fastapi_app = FastAPI(title="Book GraphQL API")
    graphql_app = GraphQLRouter(schema)
    fastapi_app.include_router(graphql_app, prefix="/graphql")

    def get_app():
        return fastapi_app

except ImportError:
    # Fallback: use Flask-Strawberry or standalone server
    fastapi_app = None

    def get_app():
        return None


if __name__ == "__main__" and fastapi_app:
    import uvicorn
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
