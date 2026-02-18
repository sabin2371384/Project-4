from fastapi import FastAPI, Query, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import shutil
import os
import uuid

app = FastAPI()


if not os.path.exists("images"):
    os.makedirs("images")


app.mount("/images", StaticFiles(directory="images"), name="images")

books_db = []


class Book(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    image_url: str


@app.post("/books")
def add_book(
    title: str = Form(..., min_length=3, max_length=100),
    image: UploadFile = File(...)
):
   
    file_extension = image.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"

    file_path = f"images/{unique_filename}"

    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    
    image_url = f"http://127.0.0.1:8000/images/{unique_filename}"

    
    book = Book(
        title=title,
        image_url=image_url
    )

    books_db.append(book)

    return {
        "message": "Book added successfully",
        "book": book
    }


@app.get("/search")
def search_books(
    q: str = Query(..., min_length=3, max_length=100),
    skip: int = 0,
    limit: int = 10
):
    results = []

    for book in books_db:
        if q.lower() in book.title.lower():
            results.append(book)

    return results[skip: skip + limit]
