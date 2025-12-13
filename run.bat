@echo off
echo ========================================
echo ZION APOSTOLIC SWAZILAND CHURCH
echo ========================================
echo NPO: 2023/757388/08
echo Youth President: 072 276 7670
echo ========================================
python --version
if errorlevel 1 (
    echo ERROR: Python not installed!
    pause
    exit /b 1
)
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo ========================================
echo Starting Church Management System...
echo Website: http://localhost:5000
echo API: http://localhost:5000/api/health
echo ========================================
python app.py
pause
