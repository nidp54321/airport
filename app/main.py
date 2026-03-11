from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import users, auth, assets, locations, maintenance, reports
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Assets Management API")

origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost",
    "http://127.0.0.1",
    "http://backend:80",
]

# Add CORS middleware FIRST, before routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(assets.router, prefix="/assets", tags=["assets"])
app.include_router(locations.router, prefix="/locations", tags=["locations"])
app.include_router(maintenance.router, prefix="/maintenance", tags=["maintenance"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])

# ========================
# Root Health Check Endpoints
# ========================

@app.get("/")
def root():
    """Root endpoint - API is running"""
    return {"message": "Airport Assets Management API", "status": "operational"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Airport API"}


