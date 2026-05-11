@echo off
echo Stopping AdLens...
taskkill /f /fi "WINDOWTITLE eq AdLens Backend*" >nul 2>&1
taskkill /f /fi "WINDOWTITLE eq AdLens Frontend*" >nul 2>&1
echo AdLens stopped.
timeout /t 2 /nobreak >nul
