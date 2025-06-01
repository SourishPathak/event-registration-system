@echo off
echo Setting up virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Installing requirements...
pip install -r requirements.txt

echo Running main program...
python main.py

pause
