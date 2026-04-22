@echo off
chcp 65001 >nul
title 3D Wiki Explorer

echo.
echo =====================================
echo     3D Wiki Explorer - Starting...
echo =====================================
echo.

if not exist 'data' mkdir data
if not exist 'data\put_zim_files_here.txt' (
    echo Place ZIM files here or use Load ZIM button in app > 'data\put_zim_files_here.txt'
)

echo Starting server...
start '' 3d-wiki-explorer.exe

timeout /t 2 /nobreak >nul

echo Opening browser...
start http://localhost:8765

echo.
echo =====================================
echo   Server running at: http://localhost:8765
echo   Press Ctrl+C to stop
echo =====================================
echo.

pause
