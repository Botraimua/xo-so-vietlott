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
TRAN_NGAY_CU = {
    "power_655": 4,    # quay Thứ 3-5-7, cách nhau nhiều nhất 3 ngày
    "power_645": 4,    # quay Thứ 4-6-CN
    "power_535": 2,    # quay hằng ngày, 2 kỳ
    "3d": 4,           # quay Thứ 2-4-6
    "3d_pro": 4,       # quay Thứ 3-5-7
}


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
    if not cu:
        print("  Mọi sản phẩm đều mới. Không có gì phải lo.")
        print()
        return 0

    print("-" * 66)
    print("  DỮ LIỆU ĐANG CŨ — nhiều khả năng không lấy được từ vietlott.vn.")
    print()
    do_mang()
    print()
    print("  Nếu chạy trên máy chủ GitHub mà dòng trên báo không gọi được,")
    print("  thì Vietlott chặn máy chủ nước ngoài. Cách chữa: để MÁY CỦA CHỊ")
    print("  tải dữ liệu (bấm nút 0 hoặc nút 7), bot chỉ lo dựng trang.")
    print()
    for ten, cach, tran in cu:
        print("  - " + ten + ": " + (("cách " + str(cach) + " ngày") if cach else "không có dữ liệu")
              + " (trần " + str(tran) + ")")
    print()
    return 1


if __name__ == "__main__":
    sys.exit(main())
