@echo off
setlocal

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Try to auto-detect python.exe
for /f "delims=" %%P in ('where python 2^>nul') do set PYTHON_PATH=%%P & goto :foundpython
set PYTHON_PATH=
:foundpython
if "%PYTHON_PATH%"=="" (
    echo ERROR: python.exe not found in PATH. Please install Python and add it to your PATH.
    pause
    exit /b 1
)

REM Check for nssm.exe and IPCatcher.py in the script directory
if not exist "%SCRIPT_DIR%nssm.exe" (
    echo ERROR: nssm.exe not found in script directory: %SCRIPT_DIR%
    pause
    exit /b 1
)
if not exist "%SCRIPT_DIR%IPCatcher.py" (
    echo ERROR: IPCatcher.py not found in script directory: %SCRIPT_DIR%
    pause
    exit /b 1
)

REM Check for requirements.txt and install dependencies if present
if exist "%SCRIPT_DIR%..\requirements.txt" (
    echo Installing Python dependencies from requirements.txt...
    "%PYTHON_PATH%" -m pip install -r "%SCRIPT_DIR%..\requirements.txt"
)

REM Create directories if they don't exist
if not exist "C:\Program Files\IPCatcher" mkdir "C:\Program Files\IPCatcher"
if not exist "C:\Program Files\NSSM" mkdir "C:\Program Files\NSSM"

REM Copy files
copy /Y "%SCRIPT_DIR%nssm.exe" "C:\Program Files\NSSM\"
copy /Y "%SCRIPT_DIR%IPCatcher.py" "C:\Program Files\IPCatcher\"
copy /Y "%SCRIPT_DIR%.env" "C:\Program Files\IPCatcher\"

REM Use full path to nssm.exe and python.exe
"C:\Program Files\NSSM\nssm.exe" install IPCatcher "%PYTHON_PATH%" "C:\Program Files\IPCatcher\IPCatcher.py"
"C:\Program Files\NSSM\nssm.exe" start IPCatcher
sc config IPCatcher start= auto

echo Service Running...
pause
endlocal