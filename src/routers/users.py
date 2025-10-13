from fastapi import APIRouter, status

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user():
    return {"message": "User created"}