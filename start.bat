@echo off
title AdLens - Starting...
color 0A

echo.
echo   ====================================
echo      AdLens - AI Ad Intelligence
echo   ====================================
echo.

cd /d "%~dp0"

REM Kill any existing instances
taskkill /f /fi "WINDOWTITLE eq AdLens Backend*" >nul 2>&1
taskkill /f /fi "WINDOWTITLE eq AdLens Frontend*" >nul 2>&1

REM Install frontend deps if needed
if not exist "frontend\node_modules" (
    echo [1/4] Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
) else (
    echo [1/4] Frontend deps OK
)

REM Install backend deps if needed
echo [2/4] Checking backend dependencies...
pip install -q fastapi uvicorn python-multipart opencv-python-headless numpy Pillow scikit-learn 2>nul

REM Start backend
echo [3/4] Starting backend server on port 8000...
start "AdLens Backend" /min cmd /c "cd /d %~dp0backend && python server.py"

REM Wait for backend
timeout /t 3 /nobreak >nul

REM Start frontend
echo [4/4] Starting frontend on port 3000...
start "AdLens Frontend" /min cmd /c "cd /d %~dp0frontend && npx vite --host 0.0.0.0"

REM Wait for frontend to be ready
echo Waiting for servers...
timeout /t 5 /nobreak >nul

REM Open browser
start http://localhost:3000

echo.
echo   ====================================
echo      AdLens is RUNNING!
echo   ====================================
echo.
echo   Browser: http://localhost:3000
echo   Backend: http://localhost:8000
echo.
echo   Close this window freely.
echo   To STOP: close the AdLens Backend
echo   and AdLens Frontend windows.
echo.
pause
