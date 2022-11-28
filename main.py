from typing import List

from fastapi import FastAPI, status, HTTPException
from sqlmodel import Session, select

from models import Book
from database import engine



app = FastAPI(
    title = "Book API",
    version = "v 1.0",
    description = "A simple Book API using FastAPI and SQLModel"
)

session = Session(bind=engine)


@app.get("/books", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books():
    statement = select(Book)
    results = session.exec(statement).all()

    return results


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_a_book(book: Book):
    new_book = Book(title=book.title, description=book.description)
    session.add(new_book)
    session.commit()

    return new_book


@app.get("/books/{book_id}", response_model=Book)
async def get_a_book(book_id: int):
    statement = select(Book).where(Book.id == book_id)
    result = session.exec(statement).first()

    if result == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Book associated with ID '{book_id}' not found")

    return result


@app.put("/books/{book_id}", response_model=Book)
async def update_a_book(book_id: int, book: Book):
    statement = select(Book).where(Book.id == book_id)
    result = session.exec(statement).first()

    result.title = book.title
    result.description = book.description

    session.commit()

    return result


@app.delete("/books/{book_id}")
async def delete_a_book(book_id: int):
    statement = select(Book).where(Book.id == book_id)
    result = session.exec(statement).one_or_none()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Book found with ID '{book_id}'"
        )
    
    session.delete(result)

    return f"successfully deleted"