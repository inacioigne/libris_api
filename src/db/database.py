import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+asyncmy://appuser:secret@localhost:3306/libris_db")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_session():
    async with SessionLocal() as session:
        yield session