@echo off
chcp 65001 >nul
pushd "%~dp0"
title Dua bao cao len mang - Vietlott cua Sep
set PYTHONIOENCODING=utf-8
set PYTHONPATH=%~dp0src

if not exist ".venv\Scripts\python.exe" goto chua_cai

echo.
echo   [1/4] Kiem tra dang nhap Vercel...
call npx --yes vercel whoami >nul 2>&1
if errorlevel 1 goto chua_dang_nhap
echo         OK.

echo.
echo   [2/4] Cap nhat du lieu moi nhat...
".venv\Scripts\python.exe" "cua-chi\cap_nhat.py"

echo.
echo   [3/4] Dung ban cong khai (KHONG kem ve cua Sep)...
".venv\Scripts\python.exe" "cua-chi\goi_so.py" >nul
".venv\Scripts\python.exe" "cua-chi\bao_cao.py" web
if errorlevel 1 goto loi

echo.
echo   [4/4] Dang len Vercel...
rem Chay tu thu muc goc: tren Vercel, Root Directory da dat la "web"
call npx --yes vercel deploy --prod --yes
if errorlevel 1 goto loi_mang

echo.
echo   XONG. Trang cua Sep:  https://vietlott-thongke.vercel.app
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

:chua_dang_nhap
echo.
echo   May nay chua dang nhap Vercel nen chua dang len mang duoc.
echo   Sep chay 8-DANG-NHAP-VERCEL.bat mot lan, roi quay lai bam nut 7 nay.
echo.
echo   (Trang cu van con o https://vietlott-thongke.vercel.app,
echo    chi la chua cap nhat du lieu moi thoi.)
echo.
popd
pause
exit /b 1

:loi_mang
echo.
echo   Khong dang duoc. Chup man hinh nay lai roi hoi Claude.
echo.
popd
pause
exit /b 1

:loi
echo.
echo   Co loi khi dung bao cao. Chup man hinh nay lai roi hoi Claude.
echo.
popd
pause
exit /b 1
