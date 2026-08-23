@echo off
chcp 65001 >nul
pushd "%~dp0"
title Day len GitHub - lam 1 lan duy nhat

set REPO=https://github.com/Botraimua/xo-so-vietlott.git

echo.
echo ==============================================================
echo   DAY BO CONG CU LEN GITHUB
echo ==============================================================
echo.
echo   Truoc khi chay file nay, chi phai tao repo rong tren GitHub:
echo.
echo     1. Mo  https://github.com/new
echo     2. Repository name:  xo-so-vietlott
echo     3. Chon  Public
echo     4. KHONG tich "Add a README file"
echo        KHONG chon .gitignore, KHONG chon license
echo        (tich vao la lat nua day len se bi ket)
echo     5. Bam  Create repository
echo.
echo   Tao xong roi thi bam phim bat ky de tiep tuc.
echo   Chua tao thi dong cua so nay lai.
echo.
pause

echo.
echo   [1/3] Gan dia chi repo...
git remote remove origin >nul 2>&1
git remote add origin %REPO%
if errorlevel 1 goto loi

echo   [2/3] Dat nhanh chinh la main...
git branch -M main

echo   [3/3] Day len GitHub...
echo         (lan dau co the hien cua so dang nhap GitHub - chi bam dong y)
echo.
git push -u origin main
if errorlevel 1 goto loi_push

echo.
echo ==============================================================
echo   XONG. Repo cua chi:
echo     https://github.com/Botraimua/xo-so-vietlott
echo.
echo   Con 1 buoc cuoi: noi Vercel voi repo nay.
echo   Xem muc "Tu chay moi ngay" trong HUONG-DAN.md
echo ==============================================================
echo.
popd
pause
exit /b 0

:loi_push
echo.
echo   Day len khong duoc. Vai nguyen nhan hay gap:
echo     - Chua tao repo tren GitHub, hoac dat ten khac "xo-so-vietlott"
echo     - Luc tao co tich "Add a README file" -^> repo khong rong
echo       Cach chua: xoa repo do di, tao lai cho that rong
echo     - Chua dang nhap GitHub tren may
echo.
echo   Chup man hinh nay lai roi hoi Claude.
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
