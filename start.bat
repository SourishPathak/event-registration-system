@echo off
echo ============================================
echo     Welcome to the Event Registration System
echo ============================================

:: Set the full path to your Python interpreter
set PYTHON_EXE="C:\Users\souri\AppData\Local\Programs\Python\Python313\python.exe"

:: Step 1: Install required packages
echo Installing required Python packages...
%PYTHON_EXE% -m pip install -r requirements.txt

:: Step 2: Launch the GUI application
echo Launching the GUI application...
start "" %PYTHON_EXE% main.py

exit
