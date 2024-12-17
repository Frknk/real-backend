from src.routes.auth.models import UserLogin, User
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from src.database import get_session
from sqlmodel import Session
from datetime import timedelta

from src.routes.auth.operations import get_user_by_username, create_user, authenticate_user, create_access_token, verify_token, get_current_user
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register")
def register_user(user: UserLogin, session: Session = Depends(get_session)):
    db_user = get_user_by_username(user.username, session)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(user, session)

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    db_user = authenticate_user(form_data.username, form_data.password, session)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(data={"sub": db_user.username, "role": db_user.role}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify_token/{token}")
def verify_token_route(token: str):
    verify_token(token)
    return {"message": "Token is valid"}

@router.get("/test")
def test(current_user: Annotated[User, Depends(get_current_user)]):
   return current_user