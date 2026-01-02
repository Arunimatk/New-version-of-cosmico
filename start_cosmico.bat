@echo off
echo Starting COSMICO Backend and Frontend...
start cmd /k "cd backend && python manage.py runserver"
start cmd /k "cd frontend && npm run dev"
echo Servers started! Open http://localhost:5173
pause
