@echo off
setlocal
set SCRIPT_DIR=%~dp0
set SERVICE_NAME=IPCatcher

REM Use full path to nssm.exe
set NSSM_EXE="C:\Program Files\NSSM\nssm.exe"
if not exist %NSSM_EXE% set NSSM_EXE="%SCRIPT_DIR%nssm.exe"

REM Check if NSSM exists
if not exist %NSSM_EXE% (
    echo ERROR: nssm.exe not found in either "C:\Program Files\NSSM" or script directory: %SCRIPT_DIR%
    pause
    exit /b 1
)

echo Attempting to stop service %SERVICE_NAME%...
sc query %SERVICE_NAME% | find "STATE" | find /I "PAUSED"
if %errorlevel%==0 (
    echo Service is PAUSED. Attempting to continue...
    sc continue %SERVICE_NAME%
    timeout /t 2 >nul
)

%NSSM_EXE% stop %SERVICE_NAME%
if %errorlevel% neq 0 (
    echo Service may not be running or already stopped. Continuing...
)

%NSSM_EXE% remove %SERVICE_NAME% confirm
if %errorlevel% neq 0 (
    echo Service may not exist or could not be removed. Continuing...
)

rmdir /s /q "C:\Program Files\IPCatcher"
rmdir /s /q "C:\Program Files\NSSM"
echo Service and files removed.

REM Set the service to run as Local System (admin privileges)
sc config IPCatcher obj= "LocalSystem" password= ""

"C:\Program Files\NSSM\nssm.exe" install IPCatcher "%PYTHON_PATH%" "C:\Program Files\IPCatcher\IPCatcher.py"
sc config IPCatcher obj= "LocalSystem" password= ""
"C:\Program Files\NSSM\nssm.exe" start IPCatcher
sc config IPCatcher start= auto

pause
endlocal