@echo off
echo Starting WhatsApp AI Bot...
echo.
echo Starting WhatsApp Service...
start cmd /k "npm start"
timeout /t 3 /nobreak >nul
echo.
echo Starting Django Server...
start cmd /k "python manage.py runserver"
echo.
echo Both services started!
echo Scan QR code in WhatsApp Service window.
