from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import create_access_token, get_current_user
from src.routers import users
from src.db.database import engine, Base
from src.models import User
from src.lib.users import get_by_email
from src.db.database import get_session
from src.core.security import verify_password

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
async def read_root(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permissions'
        )

    return {'mgs': current_user.name}
    

@app.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_session)
    ):

    user = await get_by_email(form_data.username, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User does not exists",
                            headers={"WWW-Authenticate": "Bearer"})
        
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect password",
                            headers={"WWW-Authenticate": "Bearer"})
    

    access_token = create_access_token({"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}