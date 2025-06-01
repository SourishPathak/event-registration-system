@echo off

rem Request MySQL username
set /p MYSQL_USER=Enter your MySQL username: 

rem Request MySQL password (input visible)
set /p MYSQL_PASS=Enter your MySQL password: 

rem Set environment variables
set MYSQL_USER=%MYSQL_USER%
set MYSQL_PASS=%MYSQL_PASS%

echo Installing required Python packages...
pip install -r requirements.txt

echo.
echo Running faker_data.py to generate fake data...
"C:\Users\souri\AppData\Local\Programs\Python\Python313\python.exe" faker_data.py

echo.
echo Starting main.py...
"C:\Users\souri\AppData\Local\Programs\Python\Python313\python.exe" main.py

pause
