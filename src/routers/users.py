from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
async def create_user():
    return {"message": "User created"}