from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.routers import users
from src.db.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Aplicação iniciando...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    print("Aplicação finalizando...")
    await engine.dispose()

app = FastAPI(title="Libris API", version="0.1.0", lifespan=lifespan)

app.include_router(users.router)



@app.get("/")
async def read_root():
    return {"Hello": "World"}