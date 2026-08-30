# -*- coding: utf-8 -*-
"""
Lấy kết quả trong ngày từ kqxs.vn — cho Power 6/55 và Mega 6/45.

Vì sao có file này: đo tận nơi ngày 30/08/2026 thì vietlott.vn nấp sau dịch vụ
chống bot, trả 403 cho máy chủ GitHub (IP Azure, Mỹ) ở MỌI đường. Không phải
chặn theo nước — IP nhà dân Việt Nam vẫn qua. Nhờ trung gian gọi hộ cũng tắc
(r.jina.ai trả về trang "Performing security verification").

kqxs.vn thì máy chủ GitHub gọi được, và có kết quả ngay trong ngày. Đổi lại:
  - Chỉ có 4 sản phẩm, KHÔNG có Lotto 5/35 và Max 3D Pro
    (ba sản phẩm còn lại vẫn đi đường dự phòng, chậm 1-2 ngày)
  - KHÔNG in mã kỳ — phải tự suy ra bằng "kỳ cuối cộng một"

Chỗ tự suy mã kỳ là chỗ nguy hiểm nhất: sai một cái là dò vé sai mà nhìn vẫn như
thật. Nên mỗi kỳ lấy về đây đều đóng dấu `"nguon": "kqxs"`, và khi kho dự phòng
bắt kịp 1-2 ngày sau, `lay_du_phong.py` đối chiếu lại — lệch thì nó ghi đè bằng
số của kho kia và KÊU LÊN.

Cách chạy:
    python cua-chi/lay_kqxs.py
"""

import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from thu_vien import SAN_PHAM, THU_MUC_DATA, bat_utf8, ngay_viet  # noqa: E402

bat_utf8()

GOC = "https://www.kqxs.vn/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
CHO = 25

# Thứ trong tuần theo Python: Thứ 2 = 0 ... Chủ nhật = 6
NGUON = {
    # mã       đường trên kqxs      số phải có   ngày quay
    "power_655": ("xo-so-power655", 7, {1, 3, 5}),   # Thứ 3, 5, 7
    "power_645": ("xo-so-mega645",  6, {2, 4, 6}),   # Thứ 4, 6, Chủ nhật
}

# Không lùi quá xa: chỗ này chỉ để bù vài ngày, phần lịch sử đã có sẵn rồi.
TOI_DA_NGAY = 45


def hom_nay():
    return datetime.now(timezone(timedelta(hours=7))).date()


def tai(duong):
    req = urllib.request.Request(GOC + duong, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=CHO) as r:
        return r.read().decode("utf-8", errors="replace")


def boc(html):
    """
    Bóc các cặp (ngày, dãy số) khỏi trang.

    Trang có dạng:
        <h2>... Xổ số Power 6/55 &nbsp; Thứ Bảy &nbsp; 29-08-2026 </h2>
        <div class="vietlott"><ul><li data-value="05" ...>05</li> ... </ul>

    Ngày không có kỳ quay thì trang trả về 0 khối — đã thử, không đoán bừa.
    """
    ngay = [m.group(1) for m in re.finditer(r"<h2>(.*?)</h2>", html, re.S)]
    ngay = [re.search(r"(\d{2})-(\d{2})-(\d{4})", x) for x in ngay]
    khoi = re.findall(r'<div class="vietlott">(.*?)</ul>', html, re.S)

    ra = []
    for m, k in zip(ngay, khoi):
        if not m:
            continue
        d, t, n = m.groups()
        so = [int(x) for x in re.findall(r'data-value="(\d+)"', k)]
        ra.append((n + "-" + t + "-" + d, so))
    return ra


def doc_hien_co(ma):
    f = THU_MUC_DATA / SAN_PHAM[ma]["file"]
    ra = []
    if f.exists():
        with open(f, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    try:
                        ra.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return ra


def ngay_can_lay(ma, da_co_ngay, den):
    """Các ngày CÓ quay mà mình chưa có, từ sau kỳ cuối tới hôm nay."""
    _, _, thu = NGUON[ma]
    if da_co_ngay:
        bat_dau = max(da_co_ngay)
    else:
        return []
    d = datetime.strptime(bat_dau, "%Y-%m-%d").date() + timedelta(days=1)
    som_nhat = den - timedelta(days=TOI_DA_NGAY)
    if d < som_nhat:
        d = som_nhat
    ra = []
    while d <= den:
        if d.weekday() in thu and d.isoformat() not in da_co_ngay:
            ra.append(d)
        d += timedelta(days=1)
    return ra


def gop_mot(ma):
    """Trả (số kỳ thêm, ghi chú)."""
    duong, can_bao_nhieu, _ = NGUON[ma]
    cu = doc_hien_co(ma)
    if not cu:
        return 0, "chưa có dữ liệu nền, bỏ qua"

    da_co_ngay = {str(r.get("date"))[:10] for r in cu}
    try:
        ma_ky_cuoi = max(int(str(r.get("id")).lstrip("#") or 0) for r in cu)
    except ValueError:
        return 0, "mã kỳ đọc không ra, bỏ qua"

    can = ngay_can_lay(ma, da_co_ngay, hom_nay())
    if not can:
        return 0, "đã đủ"

    them = []
    for d in can:
        dm = d.strftime("%d-%m-%Y")
        try:
            html = tai(duong + "/ngay-" + dm)
        except urllib.error.HTTPError as e:
            print("    " + dm + ": không tải được (HTTP " + str(e.code) + ")")
            continue
        except Exception as e:
            print("    " + dm + ": không tải được (" + str(e)[:50] + ")")
            continue

        cap = boc(html)
        # Trang phải trả về ĐÚNG ngày mình hỏi. Không khớp thì bỏ, không đoán.
        khop = [(n, so) for n, so in cap if n == d.isoformat()]
        if not khop:
            continue
        n, so = khop[0]
        if len(so) != can_bao_nhieu:
            print("    " + dm + ": bốc được " + str(len(so)) + " số, cần "
                  + str(can_bao_nhieu) + " — bỏ qua")
            continue
        # 6 số chính phải khác nhau (số thứ 7 của 6/55 là số đặc biệt,
        # Vietlott quay từ các quả còn lại nên cũng không trùng)
        if len(set(so[:6])) != 6:
            print("    " + dm + ": 6 số chính có số trùng nhau — bỏ qua")
            continue
        tran = SAN_PHAM[ma]["max_chinh"]
        if any(not (1 <= x <= tran) for x in so):
            print("    " + dm + ": có số ngoài dải 1-" + str(tran) + " — bỏ qua")
            continue

        ma_ky_cuoi += 1
        them.append({
            "date": n,
            "id": str(ma_ky_cuoi).zfill(5),
            "result": so,
            "process_time": datetime.now().isoformat(),
            # Dấu này để lay_du_phong biết kỳ nào là mã kỳ TỰ SUY, còn đối chiếu
            # lại được khi kho dự phòng bắt kịp.
            "nguon": "kqxs",
        })
        print("    " + dm + ": " + " ".join(str(x).zfill(2) for x in so)
              + "   -> đặt mã kỳ " + str(ma_ky_cuoi).zfill(5) + " (tự suy)")

    if not them:
        return 0, "chưa có kỳ mới"

    tat_ca = cu + them
    tat_ca.sort(key=lambda r: (str(r.get("date", "")), str(r.get("id", ""))))
    f = THU_MUC_DATA / SAN_PHAM[ma]["file"]
    with open(f, "w", encoding="utf-8", newline="\n") as fh:
        for r in tat_ca:
            json.dump(r, fh, ensure_ascii=False)
            fh.write("\n")
    return len(them), "kỳ cuối " + ngay_viet(tat_ca[-1].get("date"), kem_thu=False)


def main():
    print()
    print("=" * 66)
    print("  LẤY KẾT QUẢ TRONG NGÀY TỪ kqxs.vn")
    print("=" * 66)
    print("  Dùng khi vietlott.vn chặn máy đang chạy (chống bot).")
    print("  Chỉ có Power 6/55 và Mega 6/45 — ba sản phẩm kia đi đường dự phòng.")
    print()
    tong = 0
    for ma in NGUON:
        print("  " + SAN_PHAM[ma]["ten"])
        n, ghi = gop_mot(ma)
        tong += n
        print("    -> " + (("thêm " + str(n) + " kỳ") if n else "không thêm")
              + "   " + ghi)
    print()
    if tong:
        print("  Lấy được " + str(tong) + " kỳ trong ngày từ kqxs.vn.")
        print("  Mã kỳ là TỰ SUY — sẽ được đối chiếu lại khi kho dự phòng bắt kịp.")
    else:
        print("  Không có kỳ mới nào.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
