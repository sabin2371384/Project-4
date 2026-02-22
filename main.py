from fastapi import FastAPI, Query, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from database import SessionLocal, BookDB
import shutil
import os
import uuid

app = FastAPI()

# ساخت پوشه تصاویر در صورت عدم وجود
if not os.path.exists("images"):
    os.makedirs("images")

app.mount("/images", StaticFiles(directory="images"), name="images")


# مدل Pydantic برای پاسخ API
class Book(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    image_url: str


# اضافه کردن کتاب
@app.post("/books")
def add_book(
    title: str = Form(..., min_length=3, max_length=100),
    image: UploadFile = File(...)
):
    # ساخت نام یکتا برای تصویر
    file_extension = image.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = f"images/{unique_filename}"

    # ذخیره فایل تصویر
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # آدرس تصویر
    image_url = f"http://127.0.0.1:8000/images/{unique_filename}"

    # ذخیره اطلاعات در دیتابیس PostgreSQL
    db: Session = SessionLocal()
    book = BookDB(title=title, image_url=image_url)
    db.add(book)
    db.commit()
    db.refresh(book)
    db.close()

    return {
        "message": "Book added successfully",
        "book": {"id": book.id, "title": book.title, "image_url": book.image_url}
    }


# جستجوی کتاب‌ها
@app.get("/search")
def search_books(
    q: str = Query(..., min_length=3, max_length=100),
    skip: int = 0,
    limit: int = 10
):
    db = SessionLocal()
    results = (
        db.query(BookDB)
        .filter(BookDB.title.ilike(f"%{q}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )
    db.close()
    return results