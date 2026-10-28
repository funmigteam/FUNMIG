@echo off
cd /d D:\funmig
powershell -NoProfile -Command "if (Get-NetTCPConnection -LocalPort 8003 -State Listen -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }"
if %errorlevel% equ 0 exit /b 0
if not exist logs mkdir logs
D:\funmig\.venv\Scripts\daphne.exe -b 127.0.0.1 -p 8003 myproject.asgi:application >> D:\funmig\logs\daphne.log 2>&1
