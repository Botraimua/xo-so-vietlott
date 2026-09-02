# -*- coding: utf-8 -*-
"""
Canh chừng dữ liệu có cũ đi không — và báo ĐỘNG nếu có.

Vì sao có file này: cuối tháng 8/2026 bot chạy 8 ngày liền, lần nào cũng báo
"thành công", mà thật ra không lấy được kỳ mới nào từ vietlott.vn. Mỗi commit
chỉ đổi đúng một dòng giờ trong trang. Nhìn từ ngoài không ai biết — chỉ tới khi
chị hỏi "vé mua không tự dò" mới lộ.

Hỏng mà im lặng còn tệ hơn hỏng mà kêu. File này làm cho nó kêu: dữ liệu quá cũ
thì thoát với mã lỗi, GitHub gửi mail báo hỏng.

Cách chạy:
    python cua-chi/kiem_du_lieu.py
"""

import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from thu_vien import SAN_PHAM, bat_utf8, doc_du_lieu, ngay_viet  # noqa: E402

bat_utf8()

# Cách nhau mấy ngày thì coi là cũ. Tính theo lịch quay, cộng 1 ngày phòng
# Vietlott công bố muộn hoặc bot chạy trễ.
# Đã cộng thêm 1-2 ngày cho đường dự phòng: kho của tác giả gốc thường
# chậm hơn vietlott.vn chừng đó. Trần này vẫn đủ chặt để bắt kiểu hỏng
# 8 ngày liền như lần trước.
TRAN_NGAY_CU = {
    "power_655": 5,    # quay Thứ 3-5-7, cách nhau nhiều nhất 3 ngày
    "power_645": 5,    # quay Thứ 4-6-CN
    "power_535": 3,    # quay hằng ngày, 2 kỳ
    "3d": 5,           # quay Thứ 2-4-6
    "3d_pro": 5,       # quay Thứ 3-5-7
}


# Số con số mà một kỳ PHẢI có (số chính + số đặc biệt). Sản phẩm 3D trả về
# dict các mức giải nên không tính ở đây.
SO_PHAI_CO = {"power_655": 7, "power_645": 6, "power_535": 6}


def kiem_toan_ven():
    """
    Bắt bản ghi hỏng: thiếu số, số ngoài dải, hoặc mã kỳ và ngày đi ngược nhau.

    Vì sao có: ngày 02/09/2026 phát hiện kỳ 00944 của Power 6/55 ghi ngày
    23/09/2022 (đúng ra là 14/10/2023) và chỉ có 6 số thay vì 7 — sai từ repo
    gốc, nằm im suốt. Hai kho dự phòng cũng sai y hệt vì đều là nhánh của nó.
    Chỉ lộ ra khi đối chiếu với một kho dựng độc lập.

    Kiểu hỏng này nguy hơn hỏng-không-lấy-được-dữ-liệu: nó làm dò vé và thống kê
    sai mà nhìn vẫn như thật.
    """
    loi = []
    for ma in list(SO_PHAI_CO) + ["3d", "3d_pro"]:
        rows = doc_du_lieu(ma)
        if not rows:
            continue
        ten = SAN_PHAM[ma]["ten"]
        n = SO_PHAI_CO.get(ma)
        for r in rows:
            kq = r.get("result")
            if n is None:
                if not isinstance(kq, dict) or not kq:
                    loi.append(ten + " kỳ " + str(r.get("id")) + ": không có bảng giải")
                continue
            if not isinstance(kq, list) or len(kq) != n:
                loi.append(ten + " kỳ " + str(r.get("id")) + " ngày " + str(r.get("date"))[:10]
                           + ": có " + str(len(kq) if isinstance(kq, list) else 0)
                           + " số, phải có " + str(n))
            elif any(not (1 <= x <= SAN_PHAM[ma]["max_chinh"]) for x in kq[:6]):
                loi.append(ten + " kỳ " + str(r.get("id")) + ": có số ngoài dải 1-"
                           + str(SAN_PHAM[ma]["max_chinh"]))
        # mã kỳ tăng thì ngày cũng phải tăng
        try:
            sap = sorted(rows, key=lambda r: int(str(r.get("id", "0")).lstrip("#") or 0))
        except ValueError:
            continue
        for a, b in zip(sap, sap[1:]):
            if str(a.get("date"))[:10] > str(b.get("date"))[:10]:
                loi.append(ten + ": kỳ " + str(a.get("id")) + " (" + str(a.get("date"))[:10]
                           + ") lại đứng sau kỳ " + str(b.get("id"))
                           + " (" + str(b.get("date"))[:10] + ") — ngày đi ngược")
    return loi


def hom_nay():
    return datetime.now(timezone(timedelta(hours=7))).date()


def do_mang():
    """Xem từ máy đang chạy có gọi được vietlott.vn không. In ra để đọc log."""
    dia_chi = "https://vietlott.vn/vi"
    try:
        req = urllib.request.Request(dia_chi, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=25) as r:
            print("  Gọi thử " + dia_chi + " -> mã " + str(r.status)
                  + ", nhận " + str(len(r.read(4096))) + " byte đầu")
            return True
    except urllib.error.HTTPError as e:
        print("  Gọi thử " + dia_chi + " -> LỖI HTTP " + str(e.code))
    except Exception as e:
        print("  Gọi thử " + dia_chi + " -> KHÔNG GỌI ĐƯỢC: " + str(e)[:120])
    return False


def main():
    print()
    print("=" * 66)
    print("  KIỂM DỮ LIỆU CÓ CŨ KHÔNG")
    print("=" * 66)
    n = hom_nay()
    print("  Hôm nay: " + ngay_viet(n.isoformat()))
    print()

    cu = []
    for ma, tran in TRAN_NGAY_CU.items():
        rows = doc_du_lieu(ma)
        ten = SAN_PHAM[ma]["ten"]
        if not rows:
            print("  " + ten.ljust(13) + " KHÔNG CÓ DỮ LIỆU")
            cu.append((ten, None, tran))
            continue
        try:
            d = datetime.strptime(str(rows[-1].get("date"))[:10], "%Y-%m-%d").date()
        except (ValueError, TypeError):
            print("  " + ten.ljust(13) + " ngày kỳ cuối đọc không ra")
            cu.append((ten, None, tran))
            continue
        cach = (n - d).days
        dau = "  " + ten.ljust(13) + " kỳ cuối " + ngay_viet(d.isoformat(), kem_thu=False) \
              + "  (cách " + str(cach) + " ngày, " + str(len(rows)) + " kỳ)"
        if cach > tran:
            print(dau + "   <-- CŨ QUÁ (trần " + str(tran) + " ngày)")
            cu.append((ten, cach, tran))
        else:
            print(dau)

    print()
    hong = kiem_toan_ven()
    if hong:
        print("-" * 66)
        print("  BẢN GHI HỎNG — dò vé và thống kê sẽ sai mà nhìn vẫn như thật:")
        for x in hong[:12]:
            print("   - " + x)
        if len(hong) > 12:
            print("   ... còn " + str(len(hong) - 12) + " chỗ nữa")
        print()
    else:
        print("  Toàn vẹn: mọi kỳ đều đủ số, mã kỳ và ngày đi cùng chiều.")
        print()

    if not cu and not hong:
        print("  Mọi sản phẩm đều mới. Không có gì phải lo.")
        print()
        return 0
    if not cu:
        return 1

    print("-" * 66)
    print("  DỮ LIỆU ĐANG CŨ — nhiều khả năng không lấy được từ vietlott.vn.")
    print()
    do_mang()
    print()
    print("  Bot đã có đường dự phòng (kho vietvudanh trên GitHub). Cũ tới mức này")
    print("  nghĩa là CẢ HAI đường đều tắc. Chữa nhanh: bấm nút 0 trên máy chị —")
    print("  máy ở Việt Nam gọi vietlott.vn bình thường.")
    print()
    for ten, cach, tran in cu:
        print("  - " + ten + ": " + (("cách " + str(cach) + " ngày") if cach else "không có dữ liệu")
              + " (trần " + str(tran) + ")")
    print()
    return 1


if __name__ == "__main__":
    sys.exit(main())
