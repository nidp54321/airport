from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users, auth, assets, locations, maintenance, reports
from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Assets Management API")

# Add CORS middleware FIRST, before routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost",
        "http://127.0.0.1",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(assets.router, prefix="/assets", tags=["assets"])
app.include_router(locations.router, prefix="/locations", tags=["locations"])
app.include_router(maintenance.router, prefix="/maintenance", tags=["maintenance"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])

