@echo off
chcp 65001 >nul
pushd "%~dp0"
title Kiem thu chien luoc - Vietlott cua chi
set PYTHONIOENCODING=utf-8
set PYTHONPATH=%~dp0src

if not exist ".venv\Scripts\python.exe" goto chua_cai

echo.
echo   Dang chay 9 chien luoc chon so tren toan bo lich su Power 6/55.
echo   Mat khoang 20 giay.
echo.
".venv\Scripts\python.exe" "cua-chi\kiem_thu.py" %*
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
