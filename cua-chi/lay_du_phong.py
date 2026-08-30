# -*- coding: utf-8 -*-
"""
Đường dự phòng: lấy kết quả từ kho dữ liệu của tác giả gốc trên GitHub.

Vì sao cần: vietlott.vn không trả dữ liệu cho máy chủ GitHub (phát hiện 30/08/2026 —
bot chạy 8 ngày liền báo thành công mà không lấy được kỳ nào). Máy ở Việt Nam thì
gọi bình thường. Nên bot cần một đường khác.

Kho `vietvudanh/vietlott-data` nằm ngay trên GitHub, cập nhật hằng ngày, và
`raw.githubusercontent.com` thì máy chủ GitHub luôn gọi được. Chậm hơn nguồn gốc
khoảng 1-2 ngày, nhưng có còn hơn đứng im.

Chỉ THÊM kỳ mình chưa có, không bao giờ xoá — nên phần lịch sử mình đã lấy bù
(278 kỳ mà kho gốc thiếu) vẫn giữ nguyên.

Cách chạy:
    python cua-chi/lay_du_phong.py
"""

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from thu_vien import SAN_PHAM, THU_MUC_DATA, bat_utf8, ngay_viet  # noqa: E402

bat_utf8()

GOC = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/"

# Chỉ lấy các sản phẩm quay theo ngày. Bỏ Keno/Bingo18: file của họ hàng chục MB
# mà mình cũng không theo dõi hai cái đó.
LAY = ("power_655", "power_645", "power_535", "3d", "3d_pro")


def tai(ten_file):
    url = GOC + ten_file
    req = urllib.request.Request(url, headers={"User-Agent": "vietlott-cua-chi"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def _ma(r):
    return str(r.get("id", "")).strip()


def gop_mot(ma):
    """Trả về (số kỳ thêm được, ghi chú)."""
    cfg = SAN_PHAM[ma]
    dich = THU_MUC_DATA / cfg["file"]

    cu = []
    if dich.exists():
        with open(dich, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        cu.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    da_co = {_ma(r) for r in cu}

    try:
        noi_dung = tai(cfg["file"])
    except urllib.error.HTTPError as e:
        return 0, "không tải được (HTTP " + str(e.code) + ")"
    except Exception as e:
        return 0, "không tải được (" + str(e)[:60] + ")"

    them = []
    for line in noi_dung.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if _ma(r) and _ma(r) not in da_co:
            da_co.add(_ma(r))
            them.append(r)

    if not them:
        return 0, "đã đủ"

    tat_ca = cu + them
    tat_ca.sort(key=lambda r: (str(r.get("date", "")), _ma(r)))
    with open(dich, "w", encoding="utf-8", newline="\n") as f:
        for r in tat_ca:
            json.dump(r, f, ensure_ascii=False)
            f.write("\n")
    return len(them), "kỳ cuối " + ngay_viet(tat_ca[-1].get("date"), kem_thu=False)


def main():
    print()
    print("=" * 62)
    print("  ĐƯỜNG DỰ PHÒNG — lấy từ kho dữ liệu trên GitHub")
    print("=" * 62)
    print("  Dùng khi vietlott.vn không trả dữ liệu cho máy đang chạy.")
    print()
    tong = 0
    for ma in LAY:
        n, ghi = gop_mot(ma)
        tong += n
        print("  " + SAN_PHAM[ma]["ten"].ljust(13)
              + (("thêm " + str(n) + " kỳ") if n else "đã đủ").ljust(14)
              + "  " + ghi)
    print()
    if tong:
        print("  Bù được " + str(tong) + " kỳ từ đường dự phòng.")
    else:
        print("  Không có kỳ nào để bù — dữ liệu đang ngang hoặc mới hơn kho kia.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
