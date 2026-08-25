# -*- coding: utf-8 -*-
"""
Chấm lại toàn bộ những bộ số đã đề xuất — để biết mục gợi ý trúng thật ra sao.

Mỗi bộ trong kho neo vào MÃ KỲ CUỐI CÙNG mà nó biết lúc sinh ra (`sau_ky`).
Kỳ nó nhắm tới là kỳ kế tiếp ngay sau mã đó. Kỳ chưa quay thì để đó, chờ.

Đây là bàn cân trung thực cho chính mục gợi ý: bao nhiêu bộ đã chấm, trúng
được mấy, và tỉ lệ đó so với lý thuyết xác suất thì cao hay thấp hơn.

Cách chạy:
    python cua-chi/cham_goi_so.py
"""

import json
import sys
from math import comb, sqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import goi_so  # noqa: E402
from goi_so import FILE_KHO  # noqa: E402
from so_ve import GIA_VE, GIAI, xep_hang  # noqa: E402
from thu_vien import SAN_PHAM, THU_MUC_BAO_CAO, bat_utf8, doc_du_lieu, tach_so  # noqa: E402

bat_utf8()

# Xác suất lý thuyết trúng "từ 3 số chính trở lên" của MỘT bộ bất kỳ.
# Dùng làm mốc: tỉ lệ thật của mục gợi ý phải bám quanh con số này.
XS_CO_GIAI = {
    "power_655": (comb(6, 6) + comb(6, 5) * 49 + comb(6, 4) * comb(49, 2)
                  + comb(6, 3) * comb(49, 3)) / comb(55, 6),
    "power_645": (comb(6, 6) + comb(6, 5) * comb(39, 1) + comb(6, 4) * comb(39, 2)
                  + comb(6, 3) * comb(39, 3)) / comb(45, 6),
    "power_535": (1 + comb(5, 4) * comb(30, 1) + comb(5, 3) * comb(30, 2)) / comb(35, 5),
}


def _so_ky(x):
    """Mã kỳ về dạng số để so sánh. Keno có dạng #0293043."""
    t = str(x).lstrip("#").lstrip("0")
    return int(t) if t.isdigit() else None


def doc_kho():
    if not FILE_KHO.exists():
        return []
    ra = []
    with open(FILE_KHO, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                ra.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return ra


def _ky_ke_tiep(rows_sap, sau):
    """Kỳ đầu tiên có mã LỚN HƠN `sau`. Trả None nếu chưa quay."""
    for so, r in rows_sap:
        if so > sau:
            return r
    return None


def cham():
    kho = doc_kho()
    if not kho:
        return None

    # Sắp mỗi sản phẩm theo mã kỳ, chỉ làm một lần cho nhanh
    bo_nho = {}
    for ma in {r.get("ma") for r in kho}:
        if ma not in SAN_PHAM:
            continue
        rows = doc_du_lieu(ma)
        cap = [(_so_ky(r.get("id")), r) for r in rows]
        bo_nho[ma] = sorted([(s, r) for s, r in cap if s is not None], key=lambda t: t[0])

    theo_cl = {}       # chiến lược -> thống kê gộp mọi sản phẩm
    theo_sp = {}       # sản phẩm  -> thống kê gộp mọi chiến lược
    tong = {"da_cham": 0, "cho_quay": 0, "co_giai": 0, "tien_ve": 0, "tien_trung": 0,
            "ky_vong_co_giai": 0.0}

    def o(kho_luu, khoa):
        if khoa not in kho_luu:
            kho_luu[khoa] = {"da_cham": 0, "cho_quay": 0, "co_giai": 0,
                             "tien_ve": 0, "tien_trung": 0, "ky_vong_co_giai": 0.0,
                             "hang": {}}
        return kho_luu[khoa]

    for r in kho:
        ma = r.get("ma")
        if ma not in bo_nho:
            continue
        a = o(theo_cl, r.get("chien_luoc", "?"))
        b = o(theo_sp, ma)

        sau = _so_ky(r.get("sau_ky"))
        ky = _ky_ke_tiep(bo_nho[ma], sau) if sau is not None else None
        if ky is None:
            a["cho_quay"] += 1
            b["cho_quay"] += 1
            tong["cho_quay"] += 1
            continue

        chinh, db = tach_so(ky, ma)
        tap = set(r.get("so") or [])
        trung = len(tap & set(chinh))
        trung_db = (r.get("so_db") is not None and db is not None and r["so_db"] == db)
        hang = xep_hang(ma, trung, trung_db)
        tien = GIAI[ma][hang][1] if (hang and ma in GIAI) else 0

        # "Có giải" = trùng từ 3 số chính trở lên (mốc chung, so được với lý thuyết)
        co_giai = trung >= 3
        xs = XS_CO_GIAI.get(ma, 0.0)

        for x in (a, b, tong):
            x["da_cham"] += 1
            x["tien_ve"] += GIA_VE
            x["tien_trung"] += tien
            x["ky_vong_co_giai"] += xs
            if co_giai:
                x["co_giai"] += 1
        for x in (a, b):
            if hang:
                x["hang"][hang] = x["hang"].get(hang, 0) + 1

    def don(d):
        n = d["da_cham"] or 1
        d["ty_le_co_giai"] = d["co_giai"] / n * 100
        d["ty_le_ky_vong"] = d["ky_vong_co_giai"] / n * 100
        d["roi"] = (d["tien_trung"] - d["tien_ve"]) / (d["tien_ve"] or 1) * 100
        # Sai số chuẩn của số lần có giải, để biết lệch bao nhiêu là bình thường
        d["sai_so"] = sqrt(max(d["ky_vong_co_giai"], 1e-9))
        d["lech_sai_so"] = ((d["co_giai"] - d["ky_vong_co_giai"]) / d["sai_so"]
                            if d["sai_so"] > 0 else 0.0)
        return d

    for d in list(theo_cl.values()) + list(theo_sp.values()):
        don(d)
    don(tong)

    return {
        "tong": tong,
        "theo_chien_luoc": dict(sorted(theo_cl.items(), key=lambda kv: -kv[1]["ty_le_co_giai"])),
        "theo_san_pham": theo_sp,
        "tu_ngay": min((r.get("ngay") or "") for r in kho) or None,
        "den_ngay": max((r.get("ngay") or "") for r in kho) or None,
        "tong_bo_trong_kho": len(kho),
    }


def nap_qua_khu(so_ky=60, so_bo=4):
    """
    Dựng lại xem mục gợi ý ĐÃ đề xuất gì trong quá khứ, để có số ngay thay vì đợi.

    Với mỗi kỳ đã quay, cho chương trình xem đúng phần lịch sử TRƯỚC kỳ đó rồi
    hỏi nó gợi ý gì — y như nó đã chạy hôm ấy.

    KHÔNG ghi vào kho: phần này dựng lại được bất cứ lúc nào từ dữ liệu, cất vào
    chỉ tổ phình repo và chạy hai lần là đếm trùng. Kho chỉ giữ đề xuất THẬT.
    """
    goc = goi_so.doc_du_lieu
    ra = []
    try:
        for ma in ("power_655", "power_645", "power_535"):
            rows = goc(ma)
            if len(rows) < 260:
                continue
            for i in range(max(200, len(rows) - so_ky), len(rows)):
                truoc = rows[:i]                      # chỉ biết tới kỳ i-1
                goi_so.doc_du_lieu = (lambda r: (lambda m: r if m == ma else goc(m)))(truoc)
                ngay = str(truoc[-1].get("date"))     # "hôm nay" của lần chạy đó
                kq = goi_so.goi_cho_san_pham(ma, so_bo, ngay)
                if not kq:
                    continue
                for cl in kq["chien_luoc"]:
                    for b in cl["bo"]:
                        ra.append({"ngay": ngay, "ma": ma, "chien_luoc": cl["ten"],
                                   "so": b["so"], "so_db": b.get("so_db"),
                                   "sau_ky": kq["ky_cuoi_id"]})
    finally:
        goi_so.doc_du_lieu = goc
    return ra


def cham_nap(kho):
    """Chấm phần nạp lại quá khứ (danh sách trong bộ nhớ, không đụng kho)."""
    if not kho:
        return None
    bo_nho = {}
    for ma in {r.get("ma") for r in kho}:
        if ma not in SAN_PHAM:
            continue
        cap = [(_so_ky(r.get("id")), r) for r in doc_du_lieu(ma)]
        bo_nho[ma] = sorted([(s, r) for s, r in cap if s is not None], key=lambda t: t[0])

    theo_cl = {}
    tong = {"da_cham": 0, "co_giai": 0, "tien_ve": 0, "tien_trung": 0,
            "ky_vong_co_giai": 0.0, "giai_lon": 0}
    for r in kho:
        ma = r.get("ma")
        if ma not in bo_nho:
            continue
        ten = r.get("chien_luoc", "?")
        d = theo_cl.setdefault(ten, {"da_cham": 0, "co_giai": 0, "tien_ve": 0,
                                     "tien_trung": 0, "ky_vong_co_giai": 0.0,
                                     "giai_lon": 0})
        sau = _so_ky(r.get("sau_ky"))
        ky = _ky_ke_tiep(bo_nho[ma], sau) if sau is not None else None
        if ky is None:
            continue
        chinh, db = tach_so(ky, ma)
        trung = len(set(r.get("so") or []) & set(chinh))
        trung_db = (r.get("so_db") is not None and db is not None and r["so_db"] == db)
        hang = xep_hang(ma, trung, trung_db)
        tien = GIAI[ma][hang][1] if (hang and ma in GIAI) else 0
        for x in (d, tong):
            x["da_cham"] += 1
            x["tien_ve"] += GIA_VE
            x["tien_trung"] += tien
            x["ky_vong_co_giai"] += XS_CO_GIAI.get(ma, 0.0)
            if trung >= 3:
                x["co_giai"] += 1
            # Giải nhất trở lên: hiếm, nhưng một tờ là đủ lật ngược cột ROI
            if hang in ("nhat", "jackpot1", "jackpot2"):
                x["giai_lon"] += 1

    def don(x):
        n = x["da_cham"] or 1
        x["ty_le_co_giai"] = x["co_giai"] / n * 100
        x["ty_le_ky_vong"] = x["ky_vong_co_giai"] / n * 100
        x["roi"] = (x["tien_trung"] - x["tien_ve"]) / (x["tien_ve"] or 1) * 100
        ss = sqrt(max(x["ky_vong_co_giai"], 1e-9))
        x["lech_sai_so"] = (x["co_giai"] - x["ky_vong_co_giai"]) / ss if ss > 0 else 0.0
        return x

    for x in theo_cl.values():
        don(x)
    don(tong)
    return {"tong": tong,
            "theo_chien_luoc": dict(sorted(theo_cl.items(),
                                           key=lambda kv: -kv[1]["ty_le_co_giai"]))}


def vnd(x):
    return format(int(x), ",").replace(",", ".") + "đ"


def in_ra(kq):
    t = kq["tong"]
    print()
    print("=" * 72)
    print("  MỤC GỢI Ý TRÚNG THẬT RA SAO")
    print("=" * 72)
    print("  Kho có " + format(kq["tong_bo_trong_kho"], ",").replace(",", ".") + " bộ ("
          + str(kq["tu_ngay"]) + " → " + str(kq["den_ngay"]) + ")")
    print("  Đã chấm " + format(t["da_cham"], ",").replace(",", ".") + " bộ, "
          + format(t["cho_quay"], ",").replace(",", ".") + " bộ chờ quay")
    if t["da_cham"] == 0:
        print()
        print("  Chưa bộ nào tới kỳ quay. Quay xong rồi chạy lại.")
        print()
        return
    print()
    print("  Trúng từ 3 số trở lên : " + str(t["co_giai"]) + " bộ  ("
          + format(t["ty_le_co_giai"], ".2f") + "%)")
    print("  Lý thuyết nói phải là : " + format(t["ky_vong_co_giai"], ".1f") + " bộ  ("
          + format(t["ty_le_ky_vong"], ".2f") + "%)")
    print("  Lệch                  : " + format(t["lech_sai_so"], "+.1f")
          + " lần sai số chuẩn" + ("   <- trong mức nhiễu bình thường"
                                   if abs(t["lech_sai_so"]) <= 2 else "   <- đáng để ý"))
    print()
    print("  Nếu mua hết: bỏ ra " + vnd(t["tien_ve"]) + ", thu về " + vnd(t["tien_trung"])
          + "  ->  ROI " + format(t["roi"], "+.1f") + "%")
    print()
    print("-" * 72)
    print("  " + "Chiến lược".ljust(15) + "đã chấm".rjust(9) + "có giải".rjust(9)
          + "tỉ lệ".rjust(9) + "kỳ vọng".rjust(10) + "lệch".rjust(8))
    for ten, d in kq["theo_chien_luoc"].items():
        if d["da_cham"] == 0:
            continue
        print("  " + ten.ljust(15) + str(d["da_cham"]).rjust(9) + str(d["co_giai"]).rjust(9)
              + (format(d["ty_le_co_giai"], ".2f") + "%").rjust(9)
              + (format(d["ty_le_ky_vong"], ".2f") + "%").rjust(10)
              + format(d["lech_sai_so"], "+.1f").rjust(8))
    print()
    print("  Cột 'lệch' tính theo lần sai số chuẩn. Trong khoảng ±2 là nhiễu bình thường,")
    print("  không có ý nghĩa gì. Xổ số công bằng thì mọi chiến lược đều phải bám kỳ vọng.")
    print()


def in_nap(kq):
    t = kq["tong"]
    print()
    print("=" * 72)
    print("  NẠP LẠI QUÁ KHỨ — mục gợi ý ĐÃ đề xuất gì và trúng ra sao")
    print("=" * 72)
    print("  " + format(t["da_cham"], ",").replace(",", ".") + " bộ, mỗi bộ chấm với đúng kỳ nó nhắm tới")
    print()
    print("  Trúng từ 3 số trở lên : " + str(t["co_giai"]) + " bộ  ("
          + format(t["ty_le_co_giai"], ".2f") + "%)")
    print("  Lý thuyết nói phải là : " + format(t["ky_vong_co_giai"], ".1f") + " bộ  ("
          + format(t["ty_le_ky_vong"], ".2f") + "%)")
    print("  Lệch                  : " + format(t["lech_sai_so"], "+.1f") + " lần sai số chuẩn"
          + ("   <- trong mức nhiễu" if abs(t["lech_sai_so"]) <= 2 else "   <- đáng để ý"))
    print("  Mua hết thì ROI       : " + format(t["roi"], "+.1f") + "%")
    print()
    print("  " + "Chiến lược".ljust(15) + "đã chấm".rjust(9) + "có giải".rjust(9)
          + "tỉ lệ".rjust(9) + "kỳ vọng".rjust(10) + "lệch".rjust(8)
          + "nhất+".rjust(7) + "ROI".rjust(10))
    for ten, d in kq["theo_chien_luoc"].items():
        if not d["da_cham"]:
            continue
        print("  " + ten.ljust(15) + str(d["da_cham"]).rjust(9) + str(d["co_giai"]).rjust(9)
              + (format(d["ty_le_co_giai"], ".2f") + "%").rjust(9)
              + (format(d["ty_le_ky_vong"], ".2f") + "%").rjust(10)
              + format(d["lech_sai_so"], "+.1f").rjust(8)
              + str(d.get("giai_lon", 0)).rjust(7)
              + (format(d["roi"], "+.0f") + "%").rjust(10))
    print()
    print("  Đọc cột ROI cho đúng: nó bị cột 'nhất+' chi phối. Một tờ giải nhất 40 triệu")
    print("  đủ kéo ROI của cả 4.800 tờ lên hàng chục điểm phần trăm. Cột đáng tin là")
    print("  'tỉ lệ' và 'lệch' — trong khoảng ±2 sai số chuẩn thì là nhiễu, không phải tài.")
    print()


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "nap":
        n = 60
        if len(sys.argv) > 2 and sys.argv[2].isdigit():
            n = max(5, min(400, int(sys.argv[2])))
        print()
        print("  Đang dựng lại " + str(n) + " kỳ gần nhất của 3 sản phẩm chính...")
        ds = nap_qua_khu(n)
        print("  Dựng lại được " + format(len(ds), ",").replace(",", ".") + " bộ.")
        kqn = cham_nap(ds)
        if kqn:
            in_nap(kqn)
            THU_MUC_BAO_CAO.mkdir(parents=True, exist_ok=True)
            with open(THU_MUC_BAO_CAO / "cham-goi-so-nap.json", "w", encoding="utf-8") as f:
                json.dump(kqn, f, ensure_ascii=False, indent=1)
        return 0

    kq = cham()
    if kq is None:
        print()
        print("  Kho gợi ý còn trống. Chạy 9-GOI-BO-SO.bat vài ngày rồi quay lại.")
        print()
        return 0
    in_ra(kq)
    THU_MUC_BAO_CAO.mkdir(parents=True, exist_ok=True)
    dich = THU_MUC_BAO_CAO / "cham-goi-so.json"
    with open(dich, "w", encoding="utf-8") as f:
        json.dump(kq, f, ensure_ascii=False, indent=1)
    print("  Đã ghi " + str(dich))
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
