@echo off
REM Quick Start Script for Airport Assets Management System
REM This script automates the startup process

echo.
echo ======================================
echo  Airport Assets Management System
echo  Quick Start Script
echo ======================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [1/5] Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment exists
)

REM Activate virtual environment
echo.
echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated

REM Install backend dependencies
echo.
echo [3/5] Installing backend dependencies...
pip install fastapi uvicorn sqlalchemy passlib python-multipart bcrypt pyjwt python-dotenv requests -q
echo ✓ Backend dependencies installed

REM Check if node_modules exists
cd frontend
if not exist "node_modules" (
    echo.
    echo [4/5] Installing frontend dependencies...
    call npm install -q
    echo ✓ Frontend dependencies installed
) else (
    echo.
    echo ✓ Frontend dependencies exist
)
cd ..

echo.
echo [5/5] Setup complete!
echo.
echo ======================================
echo  NEXT STEPS
echo ======================================
echo.
echo 1. Start Backend Server:
echo    python -m uvicorn app.main:app --reload
echo.
echo 2. Start Frontend Dev Server (in new terminal):
echo    cd frontend
echo    npm run dev
echo.
echo 3. Seed Database (in new terminal - OPTIONAL):
echo    python seed_database.py
echo.
echo 4. Access the application:
echo    Frontend: http://localhost:5173
echo    API Docs: http://127.0.0.1:8000/docs
echo.
echo ======================================
echo.
echo Default Test Credentials:
echo Username: testuser
echo Password: testpass123
echo.
echo See SETUP_GUIDE.md for detailed instructions
echo.
pause

