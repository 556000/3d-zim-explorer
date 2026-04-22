@echo off
chcp 65001 >nul
title 3D ZIM Explorer

echo.
echo =====================================
echo     3D ZIM Explorer - 正在启动...
echo =====================================
echo.

:: 检查是否首次运行
if not exist "data" mkdir data
if not exist "data\在这里放置ZIM文件.txt" (
    echo 请将 ZIM 文件放在 data 文件夹中 > "data\在这里放置ZIM文件.txt"
    echo 或者在应用中点击「加载 ZIM」选择文件位置 >> "data\在这里放置ZIM文件.txt"
)

:: 启动服务器
echo 正在启动本地服务器...
start "" python server.py

:: 等待服务器启动
timeout /t 2 /nobreak >nul

:: 打开浏览器
echo 正在打开浏览器...
start http://localhost:8765

echo.
echo =====================================
echo   服务已启动！
echo   访问地址：http://localhost:8765
echo   
echo   按 Ctrl+C 停止服务器
echo =====================================
echo.

:: 保持窗口打开
pause
