# app/api/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import create_user, get_user_by_username
from app.auth import oauth2_scheme, decode_access_token
from app.models import User
from pydantic import BaseModel
import jwt
from app.auth import SECRET_KEY, ALGORITHM

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str
    email: str | None = None
    full_name: str | None = None
    role: str = "user"

class UserOut(BaseModel):
    id: int
    username: str
    email: str | None = None
    full_name: str | None = None
    role: str

    class Config:
        orm_mode = True

# Register new user
@router.post("/", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    db_user = create_user(db, user)
    return db_user

# Helper to get current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user




# Get current user
@router.get("/me", response_model=UserOut)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    username = payload.get("sub")
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Get All Users
@router.get("/")
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = db.query(User).all()
    return users
