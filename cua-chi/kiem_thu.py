# -*- coding: utf-8 -*-
"""
Bàn kiểm thử chiến lược chọn số Power 6/55 — chấm điểm ĐÚNG LUẬT.

Vì sao có file này: repo gốc có sẵn 9 chiến lược, nhưng phần chấm điểm của họ
có 2 lỗi làm mọi chiến lược trông như đang lãi to:
  1. So vé với cả 7 số (6 số chính + số đặc biệt) thay vì 6 số chính
     -> "trùng 4 chính + số đặc biệt" bị đếm thành "trùng 5".
  2. Bảng giá gán "trùng 5" = 5 tỷ (Jackpot 2), trong khi trùng 5 số chính
     là giải nhất 40 triệu. Jackpot 2 phải là 5 số chính CỘNG số đặc biệt.

File này dựng lại 9 chiến lược đó, sinh vé y hệt nhau, rồi chấm bằng HAI thước:
thước đúng luật và thước sai của repo gốc. Cùng một bộ vé, chỉ khác cách chấm.

Cách chạy:
    python cua-chi/kiem_thu.py            -> 30 vé/kỳ như repo gốc
    python cua-chi/kiem_thu.py 5          -> 5 vé/kỳ, chạy nhanh hơn
"""

import json
import math
import random
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chien_luoc import CHIEN_LUOC, boc_ve  # noqa: E402
from thu_vien import THU_MUC_BAO_CAO, bat_utf8, doc_du_lieu  # noqa: E402

bat_utf8()

MIN_SO, MAX_SO = 1, 55
SO_MOI_VE = 6
GIA_VE = 10_000
KY_KHOI_DONG = 200          # số kỳ đầu dùng làm dữ liệu mồi, không đem chấm

# Giá trị giải Power 6/55. Hai Jackpot lấy mức TỐI THIỂU theo công bố của Vietlott;
# thực tế Jackpot lũy tiến nên đây đã là con số rộng rãi cho các chiến lược.
GIAI_DUNG = {
    "jackpot1": 30_000_000_000,   # trùng 6 số chính
    "jackpot2": 3_000_000_000,    # trùng 5 số chính + số đặc biệt
    "nhat": 40_000_000,           # trùng 5 số chính
    "nhi": 500_000,               # trùng 4 số chính
    "ba": 50_000,                 # trùng 3 số chính
}
# Bảng giá sai của repo gốc, ánh xạ thẳng từ "số con trùng trong 7 số"
GIAI_REPO_GOC = {6: 40_000_000_000, 5: 5_000_000_000, 4: 500_000, 3: 50_000}

# Xác suất lý thuyết cho MỘT tờ vé bất kỳ. Tổng số bộ 6 số: C(55,6) = 28.989.675.
# Xổ số công bằng thì chọn số kiểu gì cũng ra đúng mấy con số này — đó là lý do
# không chiến lược nào có thể hơn chiến lược nào.
TONG_BO = math.comb(55, 6)
SO_CACH = {
    "jackpot1": 1,                                    # trùng cả 6 số chính
    "jackpot2": math.comb(6, 5) * 1,                  # 5 số chính + đúng số đặc biệt
    "nhat": math.comb(6, 5) * 48,                     # 5 số chính, số thứ 6 không phải số đặc biệt
    "nhi": math.comb(6, 4) * math.comb(49, 2),        # đúng 4 số chính
    "ba": math.comb(6, 3) * math.comb(49, 3),         # đúng 3 số chính
}
XAC_SUAT = {k: v / TONG_BO for k, v in SO_CACH.items()}
GIA_TRI_KY_VONG = sum(XAC_SUAT[k] * GIAI_DUNG[k] for k in GIAI_DUNG)
ROI_LY_THUYET = (GIA_TRI_KY_VONG - GIA_VE) / GIA_VE * 100


def cham_dung(ve, chinh, db):
    """Chấm đúng luật: chỉ so với 6 số chính, số đặc biệt chỉ dùng cho Jackpot 2."""
    t = len(ve & chinh)
    if t == 6:
        return "jackpot1", GIAI_DUNG["jackpot1"], t
    if t == 5:
        if db in ve:
            return "jackpot2", GIAI_DUNG["jackpot2"], t
        return "nhat", GIAI_DUNG["nhat"], t
    if t == 4:
        return "nhi", GIAI_DUNG["nhi"], t
    if t == 3:
        return "ba", GIAI_DUNG["ba"], t
    return "truot", 0, t


def cham_kieu_repo(ve, ca_7_so):
    """Chấm y như repo gốc: so với cả 7 số rồi tra bảng giá sai."""
    t = len(ve & ca_7_so)
    return GIAI_REPO_GOC.get(t, 0), t


DAI = list(range(MIN_SO, MAX_SO + 1))


def chay(ve_moi_ky=30):
    rows = doc_du_lieu("power_655")
    lich = []
    for r in rows:
        kq = r.get("result") or []
        if len(kq) < 7:
            continue
        lich.append((set(int(x) for x in kq[:6]), int(kq[6]), r.get("date")))

    if len(lich) <= KY_KHOI_DONG + 10:
        print("  Chưa đủ dữ liệu. Chạy cập nhật trước.")
        return None

    ngay_cham = lich[KY_KHOI_DONG:]
    print()
    print("=" * 68)
    print("  BÀN KIỂM THỬ CHIẾN LƯỢC — POWER 6/55")
    print("=" * 68)
    print("  " + str(len(ngay_cham)) + " kỳ được chấm (bỏ " + str(KY_KHOI_DONG)
          + " kỳ đầu làm dữ liệu mồi) · " + str(ve_moi_ky) + " vé/kỳ · vé "
          + format(GIA_VE, ",") + "đ")
    print("  Mỗi chiến lược chỉ được xem dữ liệu TRƯỚC kỳ đang đoán.")
    print()

    ket_qua = []
    for ten, ham, mo_ta in CHIEN_LUOC:
        t0 = time.time()
        chi_phi = 0
        thu_dung = 0
        thu_repo = 0
        pb_dung = Counter()
        pb_repo = Counter()
        giai_dung = Counter()
        rng = random.Random(20260823)

        for i in range(KY_KHOI_DONG, len(lich)):
            truoc = [(c, d) for c, d, _ in lich[:i]]
            chinh, db, _ngay = lich[i]
            ca_7 = set(chinh) | {db}
            ts = ham(truoc, DAI)
            for _ in range(ve_moi_ky):
                ve = boc_ve(ts, rng, SO_MOI_VE, DAI)
                chi_phi += GIA_VE
                ve = set(ve)
                ten_giai, tien, t = cham_dung(ve, chinh, db)
                thu_dung += tien
                pb_dung[t] += 1
                if ten_giai != "truot":
                    giai_dung[ten_giai] += 1
                tien_r, tr = cham_kieu_repo(ve, ca_7)
                thu_repo += tien_r
                pb_repo[tr] += 1

        roi_dung = (thu_dung - chi_phi) / chi_phi * 100
        roi_repo = (thu_repo - chi_phi) / chi_phi * 100
        ket_qua.append({
            "ten": ten, "mo_ta": mo_ta,
            "chi_phi": chi_phi, "thu_dung": thu_dung, "thu_repo": thu_repo,
            "roi_dung": roi_dung, "roi_repo": roi_repo,
            "giai": dict(giai_dung),
            "pb_dung": dict(pb_dung), "pb_repo": dict(pb_repo),
        })
        print("  " + ten.ljust(15) + " chấm đúng ROI " + format(roi_dung, "+7.1f")
              + "%   |  chấm kiểu repo gốc " + format(roi_repo, "+9.1f") + "%"
              + "   (" + format(time.time() - t0, ".0f") + "s)")

    ket_qua.sort(key=lambda r: -r["roi_dung"])
    so_ve = ket_qua[0]["chi_phi"] // GIA_VE
    kv_ba = so_ve * XAC_SUAT["ba"]
    kv_nhi = so_ve * XAC_SUAT["nhi"]
    kv_lon = so_ve * (XAC_SUAT["nhat"] + XAC_SUAT["jackpot1"] + XAC_SUAT["jackpot2"])

    print()
    print("-" * 68)
    print("  SO VỚI LÝ THUYẾT XÁC SUẤT")
    print("-" * 68)
    print("  Mỗi chiến lược mua " + format(so_ve, ",") + " tờ. Nếu bộ quay công bằng thì")
    print("  DÙ CHỌN SỐ KIỂU GÌ cũng phải ra quanh mức này:")
    print("     giải ba  (trùng 3): " + format(kv_ba, ".0f") + " tờ  (±"
          + format(2 * math.sqrt(kv_ba), ".0f") + " là nhiễu bình thường)")
    print("     giải nhì (trùng 4): " + format(kv_nhi, ".1f") + " tờ  (±"
          + format(2 * math.sqrt(kv_nhi), ".1f") + ")")
    print("     giải nhất trở lên : " + format(kv_lon, ".2f") + " tờ")
    print()
    print("  " + "Chiến lược".ljust(15) + "giải ba".rjust(9) + "giải nhì".rjust(10)
          + "nhất+".rjust(7) + "ROI thật".rjust(11) + "ROI kiểu repo".rjust(15))
    for r in ket_qua:
        g = r["giai"]
        lon = g.get("nhat", 0) + g.get("jackpot1", 0) + g.get("jackpot2", 0)
        print("  " + r["ten"].ljust(15)
              + str(g.get("ba", 0)).rjust(9)
              + str(g.get("nhi", 0)).rjust(10)
              + str(lon).rjust(7)
              + format(r["roi_dung"], "+10.1f") + "%"
              + format(r["roi_repo"], "+14.1f") + "%")

    print()
    print("  ROI kỳ vọng lý thuyết của MỌI cách chọn số: "
          + format(ROI_LY_THUYET, "+.1f") + "%")
    print("  (một tờ 10.000đ có giá trị kỳ vọng khoảng "
          + format(GIA_TRI_KY_VONG, ",.0f") + "đ)")
    print()
    print("  Điều này KHÔNG phải kết quả thực nghiệm may rủi, mà là toán:")
    print("  với bộ quay công bằng, mọi bộ 6 số có xác suất trúng y hệt nhau.")
    print("  Nên giá trị kỳ vọng của mọi chiến lược bằng nhau, bằng " + format(GIA_TRI_KY_VONG, ",.0f") + "đ/tờ.")
    print("  Chênh lệch trong bảng trên là dao động, không phải kỹ năng.")
    print()
    lech = [r for r in ket_qua
            if abs(r["giai"].get("ba", 0) - kv_ba) > 2 * math.sqrt(kv_ba)]
    if lech:
        print("  Lệch quá 2 lần sai số ở giải ba: " + ", ".join(r["ten"] for r in lech) + ".")
        print("  Đọc kỹ chỗ này: dải ±2 sai số chỉ đúng khi các tờ vé độc lập nhau.")
        print("  Chiến lược bốc trong một rổ số hẹp (vd Lâu chưa về chỉ bốc trong 10 số,")
        print("  cả rổ chỉ có 210 bộ vé khác nhau) thì 30 tờ mỗi kỳ trùng lặp nhau nhiều,")
        print("  nên biên độ dao động rộng hơn hẳn. Lệch ở đây là do vé bị dồn cục,")
        print("  KHÔNG phải do chọn được số dễ trúng hơn.")
    else:
        print("  Không chiến lược nào lệch khỏi lý thuyết quá mức nhiễu thống kê.")
    print()
    print("  Cột ROI cuối cùng mới là điều đáng nhìn: CÙNG một bộ vé, chỉ đổi cách chấm,")
    print("  con số nhảy từ khoảng -80% lên +4.130%. Đó chính là lỗi của repo gốc.")
    print()

    THU_MUC_BAO_CAO.mkdir(parents=True, exist_ok=True)
    dich = THU_MUC_BAO_CAO / "kiem-thu.json"
    with open(dich, "w", encoding="utf-8") as f:
        json.dump({
            "ve_moi_ky": ve_moi_ky,
            "so_ky_cham": len(ngay_cham),
            "tu_ngay": ngay_cham[0][2],
            "den_ngay": ngay_cham[-1][2],
            "gia_ve": GIA_VE,
            "giai_dung": GIAI_DUNG,
            "xac_suat": XAC_SUAT,
            "roi_ly_thuyet": ROI_LY_THUYET,
            "gia_tri_ky_vong": GIA_TRI_KY_VONG,
            "so_ve_moi_chien_luoc": ket_qua[0]["chi_phi"] // GIA_VE,
            "ket_qua": ket_qua,
        }, f, ensure_ascii=False, indent=1)
    print("  Đã ghi " + str(dich))
    print("  Chạy 3-XEM-BAO-CAO.bat để xem bảng này trong báo cáo HTML.")
    print()
    return ket_qua


if __name__ == "__main__":
    n = 30
    if len(sys.argv) > 1:
        try:
            n = max(1, int(sys.argv[1]))
        except ValueError:
            pass
    chay(n)
