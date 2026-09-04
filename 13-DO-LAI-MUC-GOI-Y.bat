@echo off
chcp 65001 >nul
pushd "%~dp0"
title Do lai muc goi y - Vietlott cua Sep
set PYTHONIOENCODING=utf-8
set PYTHONPATH=%~dp0src

if not exist ".venv\Scripts\python.exe" goto chua_cai

rem Keo ve kho goi so tu tren mang truoc da
git pull --rebase --autostash >nul 2>&1

echo.
echo   [1/2] Cham nhung bo so DA de xuat that...
".venv\Scripts\python.exe" "cua-chi\cham_goi_so.py"

echo.
echo   [2/2] Dung lai qua khu de co so ngay (khoang 10 giay)...
".venv\Scripts\python.exe" "cua-chi\cham_goi_so.py" nap 400

echo.
echo   Ket qua da vao bao cao. Bam 3-XEM-BAO-CAO.bat de xem bang day du.
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
