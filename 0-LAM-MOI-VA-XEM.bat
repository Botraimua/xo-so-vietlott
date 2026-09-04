@echo off
chcp 65001 >nul
pushd "%~dp0"
title Vietlott cua Sep
set PYTHONIOENCODING=utf-8
set PYTHONPATH=%~dp0src

if not exist ".venv\Scripts\python.exe" goto chua_cai

rem Keo ve nhung ve Sep da nhap tren trang web
git pull --rebase --autostash >nul 2>&1

".venv\Scripts\python.exe" "cua-chi\cap_nhat.py"
".venv\Scripts\python.exe" "cua-chi\do_ve.py"
".venv\Scripts\python.exe" "cua-chi\goi_so.py" >nul
".venv\Scripts\python.exe" "cua-chi\cham_goi_so.py" >nul
".venv\Scripts\python.exe" "cua-chi\bao_cao.py"
if errorlevel 1 goto loi

start "" "bao-cao\thong-ke-vietlott.html"
echo.
echo   Da mo bao cao tren trinh duyet. Cua so nay dong duoc roi.
echo.
popd
pause
exit /b 0

:chua_cai
echo.
echo   Chua cai dat. Sep chay 1-CAI-DAT.bat truoc nhe.
echo.
popd
pause
exit /b 1

:loi
echo.
echo   Co loi. Chup man hinh nay lai roi hoi Claude.
echo.
popd
pause
exit /b 1
