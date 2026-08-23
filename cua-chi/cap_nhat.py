# -*- coding: utf-8 -*-
"""
Cập nhật dữ liệu Vietlott mới nhất về máy.
Gọi lại bộ crawler gốc cho từng sản phẩm, rồi báo cáo bằng tiếng Việt.

Cách chạy:
    python cua-chi/cap_nhat.py              -> cập nhật các sản phẩm chính
    python cua-chi/cap_nhat.py tat-ca       -> cập nhật cả Keno + Bingo18 (lâu hơn)
    python cua-chi/cap_nhat.py power_655    -> chỉ 1 sản phẩm
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from thu_vien import GOC, SAN_PHAM, THU_MUC_DATA, bat_utf8, chuan_hoa_ma, ngay_viet  # noqa: E402

bat_utf8()

# Mặc định: các sản phẩm quay theo ngày. Keno/Bingo18 quay 10 phút/lần nên để riêng.
MAC_DINH = ["power_655", "power_645", "power_535", "3d", "3d_pro"]
NHIEU_KY = ["keno", "bingo18"]


def dem_dong(ma):
    f = THU_MUC_DATA / SAN_PHAM[ma]["file"]
    if not f.exists():
        return 0
    with open(f, "r", encoding="utf-8") as fh:
        return sum(1 for line in fh if line.strip())


def ky_cuoi(ma):
    f = THU_MUC_DATA / SAN_PHAM[ma]["file"]
    if not f.exists():
        return None
    cuoi = None
    with open(f, "r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                cuoi = line
    if not cuoi:
        return None
    import json
    try:
        return json.loads(cuoi).get("date")
    except json.JSONDecodeError:
        return None


def chay_mot(ma):
    truoc = dem_dong(ma)
    lenh = [sys.executable, str(GOC / "src" / "vietlott" / "cli" / "crawl.py"), ma]
    import os
    moi_truong = dict(os.environ)
    moi_truong["PYTHONPATH"] = str(GOC / "src")
    moi_truong["LOGURU_LEVEL"] = "ERROR"
    moi_truong["PYTHONIOENCODING"] = "utf-8"
    try:
        kq = subprocess.run(lenh, cwd=str(GOC), env=moi_truong, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", timeout=600)
    except subprocess.TimeoutExpired:
        return ma, truoc, truoc, "QUÁ GIỜ (mạng chậm hoặc trang Vietlott không phản hồi)"
    sau = dem_dong(ma)
    loi = ""
    if kq.returncode != 0:
        loi = (kq.stderr or kq.stdout or "").strip().splitlines()
        loi = loi[-1] if loi else "lỗi không rõ"
    return ma, truoc, sau, loi


def main():
    tham_so = [a for a in sys.argv[1:] if a.strip()]
    if not tham_so:
        danh_sach = MAC_DINH
    elif tham_so[0].lower() in ("tat-ca", "tatca", "all"):
        danh_sach = MAC_DINH + NHIEU_KY
    else:
        danh_sach = []
        for t in tham_so:
            ma = chuan_hoa_ma(t)
            if ma is None:
                print("  Không hiểu sản phẩm: " + t)
                print("  Chọn một trong: " + ", ".join(SAN_PHAM.keys()))
                return 1
            danh_sach.append(ma)

    print()
    print("=" * 62)
    print("  CẬP NHẬT DỮ LIỆU VIETLOTT")
    print("=" * 62)
    print()

    tong_moi = 0
    co_loi = False
    for ma in danh_sach:
        ten = SAN_PHAM[ma]["ten"]
        print("  " + ten.ljust(14) + " ... ", end="", flush=True)
        _, truoc, sau, loi = chay_mot(ma)
        if loi:
            co_loi = True
            print("LỖI: " + str(loi)[:80])
            continue
        them = sau - truoc
        tong_moi += them
        if them > 0:
            print("thêm " + str(them) + " kỳ  (tổng " + str(sau) + ", mới nhất "
                  + ngay_viet(ky_cuoi(ma), kem_thu=False) + ")")
        else:
            print("đã đủ    (tổng " + str(sau) + ", mới nhất "
                  + ngay_viet(ky_cuoi(ma), kem_thu=False) + ")")

    print()
    if tong_moi:
        print("  Xong. Có " + str(tong_moi) + " kỳ mới về máy.")
    else:
        print("  Xong. Dữ liệu đã là mới nhất, không có kỳ nào thêm.")
    if co_loi:
        print("  Có sản phẩm lỗi ở trên - thường do mạng. Chạy lại sau ít phút.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
