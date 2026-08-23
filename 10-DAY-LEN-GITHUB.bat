@echo off
chcp 65001 >nul
pushd "%~dp0"
title Day thay doi len GitHub

echo.
echo ==============================================================
echo   DAY THAY DOI LEN GITHUB
echo ==============================================================
echo.
echo   Repo cua chi:  https://github.com/Botraimua/xo-so-vietlott
echo.
echo   Chi can bam file nay khi chi (hoac Claude) sua ma nguon
echo   tren may. Con du lieu xo so thi GitHub tu cap nhat 2 lan
echo   moi ngay, khong phai bam gi.
echo.

git remote get-url origin >nul 2>&1
if errorlevel 1 (
  git remote add origin https://github.com/Botraimua/xo-so-vietlott.git
)

echo   [1/3] Xem co gi thay doi khong...
git add -A
git diff --staged --quiet
if not errorlevel 1 (
  echo         Khong co gi moi. Khong can day len.
  goto xong
)
git diff --staged --stat

echo.
echo   [2/3] Ghi lai thay doi...
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set NGAY=%%a %%b %%c
git commit -q -m "Cap nhat tu may cua chi %NGAY%"
if errorlevel 1 goto loi

echo   [3/3] Day len GitHub...
git push
if errorlevel 1 goto loi_push

echo.
echo   XONG. Vercel se tu dang lai trang sau khoang 1 phut.

:xong
echo.
popd
pause
exit /b 0

:loi_push
echo.
echo   Day len khong duoc. Thu lan luot:
echo     - Kiem tra mang
echo     - Neu bao "rejected" hoac "non-fast-forward": GitHub co ban ghi
echo       moi hon may chi. Go lenh nay roi bam lai nut 10:
echo         git pull --rebase
echo.
echo   Van khong duoc thi chup man hinh nay lai roi hoi Claude.
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
