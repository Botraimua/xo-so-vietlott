# -*- coding: utf-8 -*-
"""
Gợi bộ số cho kỳ tới — mỗi sản phẩm, mỗi chiến lược vài bộ.

ĐỌC CHỖ NÀY TRƯỚC: bàn kiểm thử (kiem_thu.py) đã chứng minh không cách chọn số
nào ăn được — tất cả lỗ 78–92%, kể cả bốc bừa. Mọi bộ 6 số đều có xác suất trúng
y hệt nhau. File này chỉ giúp chị khỏi phải ngồi nghĩ số, không phải để dự đoán.

Bộ số đổi theo NGÀY: cùng một ngày chạy bao nhiêu lần cũng ra y nhau,
sang ngày mới thì ra bộ khác.

Cách chạy:
    python cua-chi/goi_so.py           -> 4 bộ mỗi chiến lược
    python cua-chi/goi_so.py 5         -> 5 bộ mỗi chiến lược
    python cua-chi/goi_so.py 3 power   -> 3 bộ, chỉ Power 6/55
"""

import json
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chien_luoc import CHIEN_LUOC, boc_ve, w_lau_chua_ve  # noqa: E402
from thu_vien import (  # noqa: E402
    SAN_PHAM, THU_MUC_BAO_CAO, bat_utf8, chuan_hoa_ma, doc_du_lieu, ngay_viet, tach_so,
)

bat_utf8()

# Sản phẩm mà người chơi tự chọn số theo một khuôn cố định.
# so_chon   : người chơi chọn bao nhiêu số chính
# dai_chon  : chọn trong dải nào
# db_dai    : nếu người chơi chọn cả số đặc biệt thì dải của nó, không thì None
KHUON = {
    "power_655": {"so_chon": 6, "dai_chon": 55, "db_dai": None,
                  "ghi_chu": "Số đặc biệt do Vietlott quay, người chơi không chọn."},
    "power_645": {"so_chon": 6, "dai_chon": 45, "db_dai": None, "ghi_chu": ""},
    "power_535": {"so_chon": 5, "dai_chon": 35, "db_dai": 12,
                  "ghi_chu": "Số sau dấu | là số đặc biệt, chọn trong 1–12."},
    "keno": {"so_chon": 10, "dai_chon": 80, "db_dai": None,
             "ghi_chu": "Keno cho chọn từ 1 đến 10 số; đây là bộ 10 số, chị lấy bớt cũng được."},
}


def _lich_su_chinh(ma, rows):
    """[(tập số chính, số đặc biệt hoặc None), ...] theo thứ tự cũ -> mới."""
    ra = []
    for r in rows:
        chinh, db = tach_so(r, ma)
        if chinh:
            ra.append((set(chinh), db))
    return ra


def _lich_su_db(rows, ma):
    """Coi mỗi số đặc biệt như một kỳ quay 1 số, để dùng lại đúng 9 chiến lược đó."""
    ra = []
    for r in rows:
        _chinh, db = tach_so(r, ma)
        if db is not None:
            ra.append(({db}, None))
    return ra


def goi_cho_san_pham(ma, so_bo, ngay_hom_nay):
    rows = doc_du_lieu(ma)
    if not rows:
        return None
    k = KHUON[ma]
    lich = _lich_su_chinh(ma, rows)
    if len(lich) < 30:
        return None
    dai = list(range(1, k["dai_chon"] + 1))

    lich_db, dai_db = None, None
    if k["db_dai"]:
        lich_db = _lich_su_db(rows, ma)
        dai_db = list(range(1, k["db_dai"] + 1))

    ra = {"ma": ma, "ten": SAN_PHAM[ma]["ten"], "lich": SAN_PHAM[ma]["lich"],
          "ghi_chu": k["ghi_chu"], "so_chon": k["so_chon"],
          "ky_cuoi": rows[-1].get("date"),
          "ky_cuoi_id": str(rows[-1].get("id", "")), "chien_luoc": []}

    for ten, ham, mo_ta in CHIEN_LUOC:
        # hạt giống cố định theo ngày + sản phẩm + chiến lược
        rng = random.Random(ngay_hom_nay + "|" + ma + "|" + ten)

        # "Lâu chưa về" mặc định chỉ bốc trong 10 số. Với sản phẩm chọn nhiều số
        # (Keno chọn 10) thì rổ đó chỉ đẻ ra đúng 1 bộ -> nới rổ ra cho đủ chỗ xoay.
        kw = {}
        if ham is w_lau_chua_ve and k["so_chon"] >= 8:
            kw["top_n"] = k["so_chon"] + 8
            mo_ta = "chỉ bốc trong " + str(kw["top_n"]) + " số vắng lâu nhất"

        ts = ham(lich, dai, **kw)
        ts_db = ham(lich_db, dai_db) if lich_db else None
        bo = []
        da_co = set()
        lan = 0
        while len(bo) < so_bo and lan < so_bo * 40:
            lan += 1
            so = boc_ve(ts, rng, k["so_chon"], dai)
            khoa = tuple(so)
            if khoa in da_co:
                continue
            da_co.add(khoa)
            mot = {"so": so}
            if ts_db:
                mot["so_db"] = boc_ve(ts_db, rng, 1, dai_db)[0]
            bo.append(mot)
        ra["chien_luoc"].append({"ten": ten, "mo_ta": mo_ta, "bo": bo})
    return ra


FILE_KHO = Path(__file__).resolve().parent / "kho-goi-so.jsonl"


def luu_kho(tat_ca, hom_nay):
    """
    Cất mọi bộ số đã đề xuất vào kho, để sau này dò lại xem tỉ lệ trúng thật ra sao.

    Mỗi bộ được neo vào MÃ KỲ CUỐI CÙNG mà nó biết lúc sinh ra ("sau_ky").
    Nhờ vậy biết chính xác nó nhắm vào kỳ nào: kỳ kế tiếp sau mã đó.
    Chạy lại cùng ngày với cùng dữ liệu -> trùng khoá -> không ghi thêm.
    """
    da_co = set()
    if FILE_KHO.exists():
        with open(FILE_KHO, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                da_co.add((r.get("ma"), r.get("chien_luoc"), r.get("sau_ky"),
                           tuple(r.get("so") or []), r.get("so_db")))

    them = 0
    with open(FILE_KHO, "a", encoding="utf-8") as f:
        for sp in tat_ca:
            for cl in sp["chien_luoc"]:
                for b in cl["bo"]:
                    khoa = (sp["ma"], cl["ten"], sp["ky_cuoi_id"],
                            tuple(b["so"]), b.get("so_db"))
                    if khoa in da_co:
                        continue
                    da_co.add(khoa)
                    json.dump({"ngay": hom_nay, "ma": sp["ma"],
                               "chien_luoc": cl["ten"], "so": b["so"],
                               "so_db": b.get("so_db"), "sau_ky": sp["ky_cuoi_id"]},
                              f, ensure_ascii=False)
                    f.write(chr(10))
                    them += 1
    return them


def in_ra(kq):
    k = KHUON[kq["ma"]]
    print()
    print("=" * 68)
    print("  " + kq["ten"].upper() + "   (" + kq["lich"] + ")")
    print("=" * 68)
    if kq["ghi_chu"]:
        print("  " + kq["ghi_chu"])
        print()
    for cl in kq["chien_luoc"]:
        print("  " + cl["ten"] + " — " + cl["mo_ta"])
        for b in cl["bo"]:
            dong = "      " + "  ".join(str(x).zfill(2) for x in b["so"])
            if "so_db" in b:
                dong += "   |  " + str(b["so_db"]).zfill(2)
            print(dong)
        print()


def main():
    so_bo = 4
    loc = []
    for a in sys.argv[1:]:
        if a.isdigit():
            so_bo = max(1, min(10, int(a)))
        else:
            ma = chuan_hoa_ma(a)
            if ma in KHUON:
                loc.append(ma)
            else:
                print("  Không gợi số cho: " + a)
                print("  Chỉ làm được: " + ", ".join(KHUON.keys()))
                return 1

    danh_sach = loc or list(KHUON.keys())
    # Theo giờ Việt Nam, không theo giờ máy chủ chạy bot
    hom_nay = datetime.now(timezone(timedelta(hours=7))).date().isoformat()

    print()
    print("  BỘ SỐ GỢI Ý CHO NGÀY " + ngay_viet(hom_nay))
    print("  " + str(so_bo) + " bộ cho mỗi chiến lược. Cùng ngày chạy lại ra y nhau.")

    tat_ca = []
    for ma in danh_sach:
        kq = goi_cho_san_pham(ma, so_bo, hom_nay)
        if kq:
            tat_ca.append(kq)
            in_ra(kq)

    print("-" * 68)
    print("  Nhắc lại cho rõ: mọi bộ số ở trên có xác suất trúng Y HỆT NHAU,")
    print("  và y hệt bất kỳ bộ nào chị tự nghĩ ra. Bàn kiểm thử (nút 6) cho thấy")
    print("  cả 9 chiến lược đều lỗ 78–92%. Đây là công cụ khỏi phải nghĩ số,")
    print("  không phải công cụ dự đoán.")
    print()

    them = luu_kho(tat_ca, hom_nay)
    print("  Đã cất " + str(them) + " bộ mới vào kho để sau dò lại"
          + " (kho: " + str(FILE_KHO.name) + ")")

    THU_MUC_BAO_CAO.mkdir(parents=True, exist_ok=True)
    dich = THU_MUC_BAO_CAO / "goi-so.json"
    with open(dich, "w", encoding="utf-8") as f:
        json.dump({"ngay": hom_nay, "so_bo": so_bo, "san_pham": tat_ca},
                  f, ensure_ascii=False, indent=1)
    print("  Đã ghi " + str(dich))
    print("  Chạy 3-XEM-BAO-CAO.bat để xem trong báo cáo HTML (bấm vào bộ số là chép được).")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
