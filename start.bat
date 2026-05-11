@echo off
REM AdLens - Start both backend and frontend

cd /d "%~dp0"

echo Starting AdLens Backend...
start "AdLens Backend" cmd /c "cd backend && pip install -r requirements.txt && python server.py"

echo Starting AdLens Frontend...
start "AdLens Frontend" cmd /c "cd frontend && npm run dev"

timeout /t 4 /nobreak >nul
start http://localhost:3000

echo.
echo AdLens is running!
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:8000
echo.
pause
