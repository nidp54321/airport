# Airport Assets Management System

A comprehensive web application for managing airport assets, locations, maintenance schedules, and reports. Built with FastAPI (backend) and React + TypeScript (frontend).

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Database Setup](#database-setup)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)

## ✨ Features

- **User Authentication** - Secure login with JWT tokens and role-based access control
- **Asset Management** - Track and manage airport assets across multiple locations
- **Location Management** - Organize assets by terminal, runway, cargo areas, etc.
- **Maintenance Tracking** - Schedule and monitor maintenance activities
- **Reporting** - Generate and view operational reports
- **Real-time Updates** - Live data synchronization between frontend and backend

## 🛠 Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation using Python type hints
- **Passlib + Bcrypt** - Password hashing and security
- **SQLite** - Lightweight database (can be upgraded to PostgreSQL)

### Frontend
- **React 19** - UI library with latest features
- **TypeScript** - Type-safe JavaScript
- **Vite** - Lightning-fast build tool
- **Axios** - HTTP client for API requests
- **React Router** - Client-side routing

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/)

## 🚀 Installation

### Step 1: Navigate to Project Root

```bash
cd D:\My Library\Python\DFW
```

### Step 2: Setup Python Backend

#### 2.1 Create a Virtual Environment
```bash
# On Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Or on Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate.bat
```

#### 2.2 Install Python Dependencies

Create a `requirements.txt` file (if not already present) with:

```
fastapi==0.109.0
uvicorn==0.27.0
sqlalchemy==2.0.27
pydantic==2.5.3
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
```

Then install:

```bash
pip install -r requirements.txt
```

**Note:** If you encounter bcrypt version issues, reinstall:
```bash
pip install --upgrade bcrypt passlib
```

### Step 3: Setup Frontend

#### 3.1 Navigate to Frontend Directory
```bash
cd frontend
```

#### 3.2 Install Node Dependencies
```bash
npm install
```

#### 3.3 Return to Root Directory
```bash
cd ..
```

## 📊 Database Setup

### Option 1: Quick Setup with Seeding Script (Recommended)

This will create the database and populate it with sample data:

```bash
# Make sure your Python virtual environment is activated
.\venv\Scripts\Activate.ps1

# Run the seeding script
python seed_db_direct.py
```

**Sample Data Created:**
- ✓ Test User: `testuser` / `testpass123` (Admin role)
- ✓ 4 Locations (Terminal 1, Terminal 2, Runway 1, Cargo Terminal)
- ✓ 4 Assets (X-Ray Machine, Conveyor Belt, Ground Support Vehicle, Cargo Loader)
- ✓ 3 Maintenance Records
- ✓ 3 Reports

### Option 2: Manual Database Creation

```bash
# Activate virtual environment first
.\venv\Scripts\Activate.ps1

# Run the FastAPI server (it will create tables automatically)
cd app
uvicorn main:app --reload
```

The database will be created automatically at `test.db` when the backend starts.

## ▶️ Running the Application

### Start Backend Server

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Navigate to app directory
cd app

# Start FastAPI with auto-reload
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The backend will be available at: `http://127.0.0.1:8000`

**Swagger API Documentation:** `http://127.0.0.1:8000/docs`

### Start Frontend Development Server

In a new terminal/PowerShell window:

```bash
# Navigate to frontend directory
cd frontend

# Start Vite development server
npm run dev
```

The frontend will typically be available at: `http://localhost:5173`

### Quick Start with Batch File (Windows)

A `quickstart.bat` script is provided for convenience:

```bash
quickstart.bat
```

## 📁 Project Structure

```
airport-assets-management/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── users.py         # User management endpoints
│   │   ├── assets.py        # Asset management endpoints
│   │   ├── locations.py     # Location management endpoints
│   │   ├── maintenance.py   # Maintenance endpoints
│   │   └── reports.py       # Reporting endpoints
│   ├── auth.py              # Authentication logic & password hashing
│   ├── crud.py              # Database operations (CRUD)
│   ├── database.py          # Database configuration & session
│   ├── main.py              # FastAPI application setup
│   ├── models.py            # SQLAlchemy models
│   └── schemas.py           # Pydantic schemas for validation
├── frontend/
│   ├── src/
│   │   ├── pages/           # Page components
│   │   │   ├── AllAssets.tsx
│   │   │   ├── Locations.tsx
│   │   │   ├── Maintenance.tsx
│   │   │   ├── Reports.tsx
│   │   │   └── UserManagement.tsx
│   │   ├── App.tsx          # Main app component
│   │   ├── Dashboard.tsx    # Dashboard layout
│   │   ├── Login.tsx        # Login page
│   │   └── main.tsx         # Entry point
│   ├── package.json
│   └── vite.config.ts       # Vite configuration
├── seed_db_direct.py        # Database seeding script
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔌 API Endpoints

### Authentication
- `POST /auth/login` - Login with credentials
- `POST /auth/logout` - Logout (invalidate token)

### Users
- `GET /users/` - List all users
- `POST /users/` - Create new user
- `GET /users/{user_id}` - Get user details
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Assets
- `GET /assets/` - List all assets
- `POST /assets/` - Create new asset
- `GET /assets/{asset_id}` - Get asset details
- `PUT /assets/{asset_id}` - Update asset
- `DELETE /assets/{asset_id}` - Delete asset

### Locations
- `GET /locations/` - List all locations
- `POST /locations/` - Create new location
- `GET /locations/{location_id}` - Get location details
- `PUT /locations/{location_id}` - Update location
- `DELETE /locations/{location_id}` - Delete location

### Maintenance
- `GET /maintenance/` - List all maintenance records
- `POST /maintenance/` - Create maintenance record
- `GET /maintenance/{maintenance_id}` - Get maintenance details
- `PUT /maintenance/{maintenance_id}` - Update maintenance
- `DELETE /maintenance/{maintenance_id}` - Delete maintenance

### Reports
- `GET /reports/` - List all reports
- `POST /reports/` - Create new report
- `GET /reports/{report_id}` - Get report details
- `PUT /reports/{report_id}` - Update report
- `DELETE /reports/{report_id}` - Delete report

## 🔐 Default Test Credentials

After running the seed script:
- **Username:** `testuser`
- **Password:** `testpass123`
- **Role:** Admin

## 🐛 Troubleshooting

### CORS Errors
If you see CORS policy errors in the browser console, ensure:
1. FastAPI backend is running on `http://127.0.0.1:8000`
2. Frontend is running on `http://localhost:5173`
3. CORS middleware is configured in `app/main.py`

### Bcrypt Errors
If you encounter bcrypt version errors:
```bash
pip uninstall bcrypt passlib
pip install bcrypt==4.1.2 passlib==1.7.4
```

### Database Locked
If you see database lock errors:
1. Stop all running instances
2. Delete `test.db` file
3. Run `python seed_db_direct.py` again

### Port Already in Use
- **Backend port 8000:** Find and kill process: `netstat -ano | findstr :8000`
- **Frontend port 5173:** Vite will use the next available port automatically

## 📝 Notes

- Application uses SQLite (`test.db`) for development
- All passwords are hashed using bcrypt for security
- JWT tokens are used for API authentication
- Frontend communicates with backend via REST API
- All data is validated using Pydantic schemas

## 🤝 Contributing

When making changes:
1. Update models in `app/models.py`
2. Add CRUD operations in `app/crud.py`
3. Create API endpoints in `app/api/`
4. Update frontend components to call new endpoints

## 📄 License

This project is part of the Airport Assets Management System.

---

**Happy coding!** 🚀

