from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import authenticate_user, get_all_assets, get_all_users, get_all_maintenance
from pydantic import BaseModel

router = APIRouter()

# ========================
# Schemas
# ========================

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    user: dict

class DashboardStats(BaseModel):
    message: str
    user: dict | None
    stats: dict
    status: str

# ========================
# Authentication Endpoints (no tokens)
# ========================

@router.post("/login")
def login_json(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Login endpoint (JSON body) - Returns user info without token
    """
    user = authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    return {"user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active
        }}

@router.post("/token")
def token_compat(form_data: dict = None, db: Session = Depends(get_db)):
    """
    Compatibility endpoint: accepts form data (username & password) and returns same as /login
    """
    # Try to read username/password from form-data-like dict
    username = None
    password = None
    if form_data:
        username = form_data.get("username")
        password = form_data.get("password")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Use /auth/login JSON endpoint with username and password")

@router.post("/logout")
def logout():
    """
    Logout endpoint - client should clear local state; server does not maintain session
    """
    return {"message": "Logout acknowledged"}

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    """
    Dashboard endpoint - Returns system stats (no authentication)
    """
    total_assets = len(get_all_assets(db))
    total_users = len(get_all_users(db))
    total_maintenance = len(get_all_maintenance(db))

    return {
        "message": "Welcome to Dashboard!",
        "user": None,
        "stats": {
            "total_assets": total_assets,
            "total_users": total_users,
            "total_maintenance": total_maintenance,
            "system_health": "operational"
        },
        "status": "ok"
    }

@router.get("/verify")
def verify():
    return {"valid": True}

@router.get("/me")
def me():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active session")
