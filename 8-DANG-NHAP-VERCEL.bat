@echo off
chcp 65001 >nul
pushd "%~dp0"
title Dang nhap Vercel - lam 1 lan duy nhat

echo.
echo ==============================================================
echo   DANG NHAP VERCEL
echo ==============================================================
echo.
echo   Chi lam 1 lan duy nhat tren may nay.
echo.
echo   Lat nua se hien menu chon cach dang nhap - Sep chon dong
echo   "Continue with GitHub" hoac "Continue with Email" tuy Sep
echo   dang ky bang gi, roi bam Enter. Trinh duyet se tu mo ra
echo   de Sep bam xac nhan.
echo.
echo   Tai khoan cua Sep:  botraimua
echo.
pause

call npx --yes vercel login
if errorlevel 1 goto loi

echo.
echo   Kiem tra lai...
call npx --yes vercel whoami
if errorlevel 1 goto loi

echo.
echo ==============================================================
echo   XONG. Gio Sep bam 7-DUA-LEN-MANG.bat duoc roi.
echo ==============================================================
echo.
popd
pause
exit /b 0

:loi
echo.
echo   Chua dang nhap duoc. Chup man hinh nay lai roi hoi Claude.
echo.
popd
pause
exit /b 1
