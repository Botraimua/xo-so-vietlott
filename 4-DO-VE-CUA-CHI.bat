@echo off
chcp 65001 >nul
pushd "%~dp0"
title Do ve - Vietlott cua chi
set PYTHONIOENCODING=utf-8
set PYTHONPATH=%~dp0src

if not exist ".venv\Scripts\python.exe" goto chua_cai
".venv\Scripts\python.exe" "cua-chi\do_ve.py" %*
popd
pause
exit /b 0

:chua_cai
echo.
echo   Chua cai dat. Chi chay 1-CAI-DAT.bat truoc nhe.
echo.
popd
pause
exit /b 1
