from datetime import timedelta

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from uvicorn.config import HTTPProtocolType

from app import models
from app.database import SessionLocal
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.routers.dependencies import (
    get_password_hash,
    authenticate_user,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", status_code=201)
def register_user(
        username: str,
        password: str,
        db:Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.username == username).fisrt()
    if user:
        raise HTTPException(status_code=400, detail="User already excist")

    hashed_password = get_password_hash(password)

    new_user = models.User(
        username=username,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return{"detail":"User created"}

@router.post("/token")
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )

    return{
        "access_token": access_token,
        "token_type":"bearer",
    }