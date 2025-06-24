@echo off
set SERVICE_NAME=IPCatcher
echo Stopping and removing service %SERVICE_NAME%...
nssm stop %SERVICE_NAME%
nssm remove %SERVICE_NAME% confirm
echo Service removed.
pause