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

REM Check if the service exists
sc query %SERVICE_NAME% >nul 2>&1
if %errorlevel% neq 0 (
    echo Service %SERVICE_NAME% does not exist. Skipping stop and remove steps.
) else (
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
)

REM Remove directories if they exist
if exist "C:\Program Files\IPCatcher" (
    rmdir /s /q "C:\Program Files\IPCatcher"
    echo Removed C:\Program Files\IPCatcher
) else (
    echo Directory C:\Program Files\IPCatcher does not exist.
)

if exist "C:\Program Files\NSSM" (
    rmdir /s /q "C:\Program Files\NSSM"
    echo Removed C:\Program Files\NSSM
) else (
    echo Directory C:\Program Files\NSSM does not exist.
)

echo Uninstall process completed.
pause
endlocal