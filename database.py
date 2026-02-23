from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# اتصال به دیتابیس PostgreSQL
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/library"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# تعریف جدول books مطابق کد FastAPI
class BookDB(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    author_name = Column(String(100), nullable=False)
    image_url = Column(String(255), nullable=False)

# ساخت جدول در دیتابیس (اگر موجود نبود)
Base.metadata.create_all(engine)