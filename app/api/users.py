from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import create_user, get_user_by_username, update_user, get_user_by_id
from app.models import User
from pydantic import BaseModel
from typing import Optional

from app.schemas import UserUpdate

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str  # Plain text
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: str = "user"

class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: str
    is_active: bool

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    db_user = create_user(db, user)
    return db_user

# Get all users
@router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Authenticate user
@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"username": db_user.username, "role": db_user.role}

@router.get("/me", response_model=UserOut)
def read_users_me(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_user(username: str, db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user by ID
@router.put("/{user_id}", response_model=UserOut)
def update_user_route(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return update_user(db, db_user, user_data)

# Delete user by ID (admin only)
@router.delete("/{user_id}", status_code=200)
def delete_user_route(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Prevent non-admins from deleting
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete users")

    # Prevent deleting self
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")

    # Fetch user to delete
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if not user_to_delete:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Delete user
    db.delete(user_to_delete)
    db.commit()

    return {"message": f"User {user_to_delete.username} deleted successfully"}