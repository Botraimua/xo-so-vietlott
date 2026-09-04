# -*- coding: utf-8 -*-
"""
Dò bộ số của Sếp với kỳ mới nhất và với toàn bộ lịch sử.

Cách chạy:
    python cua-chi/do_ve.py                          -> dò mọi vé trong ve-cua-chi.txt
    python cua-chi/do_ve.py power_655 5 10 14 23 24 38   -> dò nhanh 1 bộ số
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from thu_vien import (  # noqa: E402
    FILE_VE, SAN_PHAM, bat_utf8, chuan_hoa_ma, do_mot_ve, doc_du_lieu, doc_ve, ngay_viet, tach_so,
)

bat_utf8()


def in_so(ds, db=None, tap_trung=None):
    ra = []
    for n in ds:
        s = str(n).zfill(2)
        ra.append("[" + s + "]" if (tap_trung and n in tap_trung) else " " + s + " ")
    if db is not None:
        ra.append(" +" + str(db).zfill(2))
    return " ".join(ra)


def in_ket_qua(kq):
    v = kq["ve"]
    cfg = SAN_PHAM[v["ma"]]
    tap = set(v["so"])

    print()
    print("-" * 62)
    tieu_de = cfg["ten"] + ":  " + in_so(v["so"], v["so_db"])
    print("  " + tieu_de + ("   # " + v["ghi_chu"] if v["ghi_chu"] else ""))
    print("-" * 62)

    moi = kq["ky_moi_nhat"]
    if moi:
        print("  Kỳ mới nhất: " + ngay_viet(moi["ky"].get("date")) + "  (kỳ " + str(moi["ky"].get("id")) + ")")
        print("  Kết quả:     " + in_so(moi["so_ky"], moi["so_db_ky"], tap_trung=tap))
        dong = "  Sếp trùng:   " + str(moi["trung"]) + "/" + str(cfg["so_chinh"]) + " số"
        if v["so_db"] is not None and cfg["co_so_db"]:
            dong += " | số đặc biệt: " + ("TRÚNG" if moi["trung_db"] else "không")
        print(dong)
        if moi["giai"] and moi["giai"] != "—":
            print("  >>> " + moi["giai"] + " <<<")
        elif moi["giai"] == "—":
            print("  Kỳ này chưa có giải.")

    tn = kq["tot_nhat"]
    if tn:
        ky, t, tdb = tn
        print("  Lịch sử:     trong " + str(kq["tong_ky"]) + " kỳ, khớp cao nhất " + str(t)
              + " số vào " + ngay_viet(ky.get("date"), kem_thu=False)
              + (" (trúng cả số đặc biệt)" if tdb else ""))
    if kq["so_lan_trung_giai"]:
        print("               bộ số này đủ điều kiện có giải " + str(kq["so_lan_trung_giai"]) + " lần:")
        for ky, t, tdb, giai in kq["ky_trung_giai"]:
            print("                 - " + ngay_viet(ky.get("date"), kem_thu=False)
                  + ": trùng " + str(t) + " số -> " + giai)

    pb = kq["phan_bo"]
    if pb:
        tom = ", ".join(str(k) + " số: " + str(v2) + " kỳ" for k, v2 in list(pb.items())[:4])
        print("  Phân bố:     " + tom)


def main():
    tham_so = sys.argv[1:]

    if tham_so:
        ma = chuan_hoa_ma(tham_so[0])
        if ma is None:
            print("  Không hiểu sản phẩm: " + tham_so[0])
            print("  Chọn một trong: " + ", ".join(SAN_PHAM.keys()))
            return 1
        phan = " ".join(tham_so[1:]).replace(",", " ")
        so_db = None
        if "|" in phan:
            phan, pdb = phan.split("|", 1)
            mieng = pdb.split()
            if mieng:
                try:
                    so_db = int(mieng[0])
                except ValueError:
                    so_db = None
        try:
            so = [int(x) for x in phan.split()]
        except ValueError:
            print("  Bộ số có ký tự không phải số.")
            return 1
        cfg = SAN_PHAM[ma]
        if len(so) != cfg["so_chinh"]:
            print("  " + cfg["ten"] + " cần " + str(cfg["so_chinh"]) + " số, Sếp ghi " + str(len(so)) + " số.")
            return 1
        ve_list = [{"ma": ma, "so": sorted(so), "so_db": so_db, "ghi_chu": "", "raw": ""}]
    else:
        ve_list = doc_ve()
        if not ve_list:
            print()
            print("  Chưa có vé nào. Mở file này rồi ghi bộ số của Sếp vào:")
            print("     " + str(FILE_VE))
            print()
            return 0

    print()
    print("=" * 62)
    print("  DÒ VÉ CỦA CHỊ")
    print("=" * 62)

    bo_nho = {}
    co_ve = False
    for v in ve_list:
        if "loi" in v:
            print()
            print("  (bỏ qua) " + v["loi"] + "  ->  " + v["raw"])
            continue
        co_ve = True
        ma = v["ma"]
        if ma not in bo_nho:
            bo_nho[ma] = doc_du_lieu(ma)
        rows = bo_nho[ma]
        if not rows:
            print()
            print("  Chưa có dữ liệu cho " + SAN_PHAM[ma]["ten"] + ". Chạy cập nhật dữ liệu trước.")
            continue
        in_ket_qua(do_mot_ve(v, rows))

    if co_ve:
        print()
        print("-" * 62)
        print("  Lưu ý: mỗi kỳ quay độc lập với kỳ trước. Bảng lịch sử ở trên")
        print("  để nhìn lại cho vui, không dự đoán được kỳ sau.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
