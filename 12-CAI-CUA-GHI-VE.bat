@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
pushd "%~dp0"
title Cai cua ghi ve - lam 1 lan duy nhat

echo.
echo ==============================================================
echo   CAI CUA GHI VE   (de nhap ve ngay tren trang web)
echo ==============================================================
echo.
echo   Chi lam 1 lan. Chay lai luc nao cung duoc neu muon doi
echo   mat khau hoac doi chia khoa GitHub.
echo.
echo   TRUOC KHI BAT DAU can co san chia khoa GitHub:
echo.
echo     1. Mo:  https://github.com/settings/personal-access-tokens/new
echo     2. Token name:        vietlott-ghi-ve
echo     3. Expiration:        No expiration
echo     4. Repository access: Only select repositories
echo                           -^> chon  xo-so-vietlott
echo     5. Permissions -^> Repository permissions, dat DUNG 2 muc:
echo           Contents  =  Read and write
echo           Actions   =  Read and write
echo     6. Bam Generate token roi COPY chuoi hien ra
echo        (bat dau bang  github_pat_...  , chi hien 1 lan)
echo.
echo   Co chuoi do roi thi bam phim bat ky de tiep tuc.
echo   Chua co thi dong cua so nay, lam xong roi quay lai.
echo.
pause

echo.
echo   [1/5] Kiem tra dang nhap Vercel...
call npx --yes vercel whoami >nul 2>&1
if errorlevel 1 goto chua_dang_nhap
echo         OK.

echo.
echo --------------------------------------------------------------
echo   [2/5] Nhap hai gia tri
echo --------------------------------------------------------------
echo.
echo   1) CHIA KHOA GITHUB - bam chuot phai vao cua so nay de DAN.
echo.
set "TOKEN="
set /p "TOKEN=   Chia khoa GitHub: "
if "!TOKEN!"=="" goto trong_token

echo.
echo   2) MAT KHAU - Sep tu nghi, chi de chan nguoi la ghi ve vao so.
echo      Nen dung CHU va SO thoi, tranh ky tu la nhu ^& ^| ^^ ^!
echo.
set "MK="
set /p "MK=   Mat khau Sep tu nghi: "
if "!MK!"=="" goto trong_mk

echo.
echo   [3/5] Dang luu len Vercel...
call npx --yes vercel env rm GITHUB_TOKEN production --yes >nul 2>&1
echo(!TOKEN!| call npx --yes vercel env add GITHUB_TOKEN production >nul 2>&1
if errorlevel 1 goto loi
call npx --yes vercel env rm MAT_KHAU production --yes >nul 2>&1
echo(!MK!| call npx --yes vercel env add MAT_KHAU production >nul 2>&1
if errorlevel 1 goto loi
set "TOKEN="
set "MK="
echo         Da luu ca hai.

echo.
echo   [4/5] Kiem lai hai bien da vao chua...
call npx --yes vercel env ls production 2>nul | findstr /C:"GITHUB_TOKEN" >nul
if errorlevel 1 goto thieu_bien
call npx --yes vercel env ls production 2>nul | findstr /C:"MAT_KHAU" >nul
if errorlevel 1 goto thieu_bien
echo         Ca hai bien deu co.

echo.
echo   [5/5] Dang lai trang de nhan bien moi...
if exist ".venv\Scripts\python.exe" ".venv\Scripts\python.exe" "cua-chi\bao_cao.py" web >nul 2>&1
call npx --yes vercel deploy --prod --yes >nul 2>&1
if errorlevel 1 goto loi_dang

echo.
echo   Dang thu cua ghi (co tinh go mat khau sai)...
echo.
curl -s -X POST https://vietlott-thongke.vercel.app/api/ghi-ve -H "Content-Type: application/json" -d "{\"matKhau\":\"co-y-go-sai\",\"dong\":\"2026-01-01 | power: 1 2 3 4 5 6\"}"
echo.
echo.
echo ==============================================================
echo   Doc dong vua hien o tren:
echo.
echo     "Mat khau khong dung"        -^> CAI XONG. Ngon roi.
echo     "May chu chua duoc cai dat"  -^> chua nhan bien. Doi 1 phut
echo                                     roi bam 7-DUA-LEN-MANG.bat
echo.
echo   Gio mo https://vietlott-thongke.vercel.app
echo   keo xuong muc "So ve da mua" de nhap ve.
echo ==============================================================
echo.
popd
pause
exit /b 0

:trong_token
echo.
echo   Chua dan gi ca. Chay lai nut nay khi co chia khoa trong tay.
echo.
popd
pause
exit /b 1

:trong_mk
echo.
echo   Chua go mat khau. Chay lai nut nay nhe.
echo.
popd
pause
exit /b 1

:thieu_bien
echo.
echo   Luu roi ma kiem lai khong thay. Chup man hinh nay lai roi hoi Claude.
echo.
popd
pause
exit /b 1

:chua_dang_nhap
echo.
echo   Chua dang nhap Vercel. Chay 8-DANG-NHAP-VERCEL.bat truoc nhe.
echo.
popd
pause
exit /b 1

:loi_dang
echo.
echo   Da luu bien nhung dang lai trang khong duoc.
echo   Thu bam 7-DUA-LEN-MANG.bat.
echo.
popd
pause
exit /b 1

:loi
echo.
echo   Chua luu duoc. Chup man hinh nay lai roi hoi Claude.
echo.
popd
pause
exit /b 1
