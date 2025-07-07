from src.routes.auth.models import UserLogin, User

import datetime
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.database import get_session
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select
from fastapi import Depends, HTTPException
from src.config import SECRET_KEY, ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(user: UserLogin, session=Depends(get_session)):
    _hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=_hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return "complete"


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    role: str = payload.get("role")
    if username is None:
        raise HTTPException(status_code=400, detail="Invalid token")
    return username, role


def get_user_by_username(username: str, session=Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()
    return user


def authenticate_user(username: str, password: str, session=Depends(get_session)):
    user = get_user_by_username(username, session)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            minutes=15
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        return payload
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
