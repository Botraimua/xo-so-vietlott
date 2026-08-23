@echo off
chcp 65001 >nul
pushd "%~dp0"
title Bao cao thong ke - Vietlott cua chi
set PYTHONIOENCODING=utf-8
set PYTHONPATH=%~dp0src

if not exist ".venv\Scripts\python.exe" goto chua_cai
".venv\Scripts\python.exe" "cua-chi\bao_cao.py"
if errorlevel 1 goto loi

start "" "bao-cao\thong-ke-vietlott.html"
echo   Da mo bao cao tren trinh duyet.
echo.
popd
ping -n 5 127.0.0.1 >nul
exit /b 0

:chua_cai
echo.
echo   Chua cai dat. Chi chay 1-CAI-DAT.bat truoc nhe.
echo.
popd
pause
exit /b 1

:loi
echo.
echo   Khong dung duoc bao cao. Chup man hinh nay lai roi hoi Claude.
echo.
popd
pause
exit /b 1
