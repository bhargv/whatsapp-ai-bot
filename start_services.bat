@echo off
echo Starting WhatsApp AI Bot Services...
echo.

echo Starting Django Server on port 8080...
start "Django Server" cmd /k "cd /d C:\Users\Lenovo\whatsapp-ai-bot && python manage.py runserver 8080"

timeout /t 3 /nobreak >nul

echo Starting WhatsApp Service...
start "WhatsApp Service" cmd /k "cd /d C:\Users\Lenovo\whatsapp-ai-bot && node whatsapp_service.js"

echo.
echo Both services are starting...
echo Django Dashboard: http://localhost:8080/
echo WhatsApp Service: Port 3000
echo.
echo Press any key to exit this window (services will continue running)...
pause >nul
