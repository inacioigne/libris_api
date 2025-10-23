from typing import Annotated, Optional
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from http import HTTPStatus
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError

from src.db.database import get_session
from src.models.users import User



SECRET_KEY = 'your-secret-key' 
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta]=None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

class UserFAKE(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    
def fake_decode_token(token):
    return UserFAKE(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Session = Depends(get_session)
):
    
    credentials_email = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Email não encontrado',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    
    credentials_user = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Usuário não encontrado',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject_email = payload.get('sub')

        if not subject_email:
            raise credentials_email

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Assinatura inválida")
    except DecodeError:
        raise HTTPException(status_code=401, detail="Token malformado")


    user = await session.scalar(
        select(User).where(User.email == subject_email)
    )

    if not user:
        raise credentials_user

    return user