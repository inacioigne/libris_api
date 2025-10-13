from fastapi import FastAPI
from src.routers import users

app = FastAPI()

app.include_router(users.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}