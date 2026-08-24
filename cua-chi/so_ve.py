# -*- coding: utf-8 -*-
"""
Sổ vé — ghi lại những bộ số chị ĐÃ MUA, rồi tự chấm kết quả khi kỳ quay xong.

Khác với ve-cua-chi.txt (bộ số đang chơi, dò với kỳ mới nhất), sổ vé là nhật ký:
mỗi tờ vé gắn với đúng MỘT kỳ quay, chấm xong thì đóng sổ, cộng dồn lãi/lỗ thật.

File sổ: cua-chi/so-ve.txt — mỗi dòng một tờ vé:
    2026-08-24 | power: 2 20 23 33 44 52          # gợi ý Số nóng
    2026-08-24 | lotto: 4 9 17 22 31 | 5 @843     # @843 = mã kỳ, cho 5/35 quay 2 lần/ngày

Cách chạy:
    python cua-chi/so_ve.py                  -> chấm sổ, in kết quả
    python cua-chi/so_ve.py ghi "power: 2 20 23 33 44 52 # ghi chú"
                                             -> thêm vé, tự đóng ngày hôm nay
"""

import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from thu_vien import (  # noqa: E402
    SAN_PHAM, bat_utf8, chuan_hoa_ma, doc_du_lieu, ngay_viet, tach_so,
)

bat_utf8()

FILE_SO = Path(__file__).resolve().parent / "so-ve.txt"
GIA_VE = 10_000

# Giá trị giải cố định theo công bố của Vietlott. Jackpot ghi mức TỐI THIỂU —
# thực tế lũy tiến cao hơn, nên nếu trúng thì con số thật chỉ có hơn.
GIAI = {
    "power_655": {
        "jackpot1": ("JACKPOT 1", 30_000_000_000, True),
        "jackpot2": ("JACKPOT 2", 3_000_000_000, True),
        "nhat": ("Giải nhất", 40_000_000, False),
        "nhi": ("Giải nhì", 500_000, False),
        "ba": ("Giải ba", 50_000, False),
    },
    "power_645": {
        "jackpot1": ("JACKPOT", 12_000_000_000, True),
        "nhat": ("Giải nhất", 10_000_000, False),
        "nhi": ("Giải nhì", 300_000, False),
        "ba": ("Giải ba", 30_000, False),
    },
}


def xep_hang(ma, trung, trung_db):
    """Trả về khóa hạng giải, hoặc None nếu trượt / sản phẩm không có bảng giải."""
    if ma == "power_655":
        if trung == 6:
            return "jackpot1"
        if trung == 5 and trung_db:
            return "jackpot2"
        return {5: "nhat", 4: "nhi", 3: "ba"}.get(trung)
    if ma == "power_645":
        if trung == 6:
            return "jackpot1"
        return {5: "nhat", 4: "nhi", 3: "ba"}.get(trung)
    return None


MAU_DONG = """# =====================================================================
#  SỔ VÉ — những bộ số chị ĐÃ MUA, để theo dõi kết quả thật
#
#  Mỗi dòng một tờ vé:  <ngày mua> | <sản phẩm>: <các số>  # ghi chú
#     2026-08-24 | power: 2 20 23 33 44 52       # gợi ý Số nóng
#     2026-08-24 | lotto: 4 9 17 22 31 | 5 @843  # @843 = mã kỳ (5/35 quay 2 lần/ngày)
#
#  Cách nhanh nhất: trong báo cáo HTML, bấm vào bộ số ở mục "Bộ số gợi ý"
#  (nó tự chép), rồi bấm 11-GHI-VE-DA-MUA.bat — vé tự vào sổ với ngày hôm nay.
#
#  Vé chưa tới kỳ quay sẽ hiện "chờ quay", quay xong tự chấm.
# =====================================================================
"""


def doc_so():
    """Đọc sổ vé, trả về (danh sách vé hợp lệ, danh sách lỗi)."""
    if not FILE_SO.exists():
        return [], []
    ve, loi = [], []
    for so_dong, line in enumerate(FILE_SO.read_text(encoding="utf-8").splitlines(), 1):
        raw = line.strip()
        if not raw or raw.startswith("#"):
            continue
        ghi_chu = ""
        if "#" in raw:
            raw, ghi_chu = raw.split("#", 1)
            ghi_chu = ghi_chu.strip()
        raw = raw.strip()
        m = re.match(r"^(\d{4}-\d{2}-\d{2})\s*\|\s*(.+)$", raw)
        if not m:
            loi.append("Dòng " + str(so_dong) + ": thiếu ngày mua (dạng 2026-08-24 | ...)")
            continue
        ngay_mua, phan = m.group(1), m.group(2)
        ky_chon = None
        mk = re.search(r"@\s*(\d+)", phan)
        if mk:
            ky_chon = int(mk.group(1))
            phan = phan[:mk.start()] + phan[mk.end():]
        if ":" not in phan:
            loi.append("Dòng " + str(so_dong) + ": thiếu dấu hai chấm sau tên sản phẩm")
            continue
        ten, phan_so = phan.split(":", 1)
        ma = chuan_hoa_ma(ten)
        if ma is None:
            loi.append("Dòng " + str(so_dong) + ": không hiểu sản phẩm " + ten.strip())
            continue
        so_db = None
        if "|" in phan_so:
            phan_so, phan_db = phan_so.split("|", 1)
            mieng = phan_db.replace(",", " ").split()
            if mieng:
                try:
                    so_db = int(mieng[0])
                except ValueError:
                    so_db = None
        try:
            so = sorted(int(x) for x in phan_so.replace(",", " ").replace(";", " ").split())
        except ValueError:
            loi.append("Dòng " + str(so_dong) + ": có ký tự không phải số")
            continue
        cfg = SAN_PHAM[ma]
        n_can = cfg["so_chinh"] if ma != "keno" else None
        if ma == "keno":
            if not (1 <= len(so) <= 10):
                loi.append("Dòng " + str(so_dong) + ": Keno chọn 1-10 số, chị ghi " + str(len(so)))
                continue
        elif len(so) != n_can:
            loi.append("Dòng " + str(so_dong) + ": " + cfg["ten"] + " cần " + str(n_can)
                       + " số, chị ghi " + str(len(so)))
            continue
        ve.append({"ngay_mua": ngay_mua, "ma": ma, "so": so, "so_db": so_db,
                   "ky_chon": ky_chon, "ghi_chu": ghi_chu, "dong": so_dong})
    return ve, loi


def tim_ky(ve, rows):
    """Tờ vé mua ngày D dự kỳ quay ĐẦU TIÊN có ngày >= D (hoặc đúng mã kỳ nếu có @)."""
    if ve["ky_chon"] is not None:
        for r in rows:
            try:
                if int(str(r.get("id", "")).lstrip("#").lstrip("0") or "0") == ve["ky_chon"]:
                    return r, False
            except ValueError:
                continue
        return None, False
    ung = [r for r in rows if str(r.get("date", "")) >= ve["ngay_mua"]]
    if not ung:
        return None, True          # chưa quay
    # 5/35 quay 2 kỳ cùng một ngày -> mặc định lấy kỳ đầu (13h), nhắc bằng cờ
    nhieu = len([r for r in ung if r.get("date") == ung[0].get("date")]) > 1
    return ung[0], nhieu


def cham(ve, rows):
    ky, cho_hoac_nhieu = tim_ky(ve, rows)
    if ky is None:
        return {"ve": ve, "trang_thai": "cho", "ky": None}
    if isinstance(cho_hoac_nhieu, bool) and ky is None:
        return {"ve": ve, "trang_thai": "cho", "ky": None}
    chinh, db = tach_so(ky, ve["ma"])
    tap = set(ve["so"])
    trung = len(tap & set(chinh))
    trung_db = (ve["so_db"] is not None and db is not None and ve["so_db"] == db)
    hang = xep_hang(ve["ma"], trung, trung_db)
    tien = 0
    ten_giai = ""
    toi_thieu = False
    if hang:
        ten_giai, tien, toi_thieu = GIAI[ve["ma"]][hang]
    return {"ve": ve, "trang_thai": "xong", "ky": ky, "so_ky": sorted(chinh),
            "db_ky": db, "trung": trung, "trung_db": trung_db,
            "ten_giai": ten_giai, "tien": tien, "toi_thieu": toi_thieu,
            "nhieu_ky_cung_ngay": (ve["ky_chon"] is None and cho_hoac_nhieu is True)}


def danh_gia():
    """Chấm toàn bộ sổ. Trả về (kết quả từng vé, tổng hợp, lỗi)."""
    ve_list, loi = doc_so()
    bo_nho = {}
    kq = []
    for v in ve_list:
        ma = v["ma"]
        if ma not in bo_nho:
            bo_nho[ma] = doc_du_lieu(ma)
        kq.append(cham(v, bo_nho[ma]))
    da_quay = [k for k in kq if k["trang_thai"] == "xong"]
    tinh_tien = [k for k in da_quay if k["ve"]["ma"] in GIAI]
    tong = {
        "so_ve": len(kq),
        "cho_quay": len(kq) - len(da_quay),
        "da_quay": len(da_quay),
        "tien_ve": len(kq) * GIA_VE,
        "tien_trung": sum(k["tien"] for k in tinh_tien),
        "so_ve_trung": sum(1 for k in tinh_tien if k["tien"] > 0),
        "ve_khong_tinh_tien": len(da_quay) - len(tinh_tien),
    }
    tong["lai_lo"] = tong["tien_trung"] - tong["tien_ve"]
    return kq, tong, loi


def vnd(x):
    return format(x, ",").replace(",", ".") + "đ"


def in_bao_cao():
    kq, tong, loi = danh_gia()
    print()
    print("=" * 66)
    print("  SỔ VÉ CỦA CHỊ")
    print("=" * 66)
    if not kq and not loi:
        print("  Sổ đang trống. Ghi vé bằng 11-GHI-VE-DA-MUA.bat, hoặc mở")
        print("  " + str(FILE_SO) + " mà ghi tay.")
        print()
        return
    for k in kq:
        v = k["ve"]
        ten = SAN_PHAM[v["ma"]]["ten"]
        so = " ".join(str(x).zfill(2) for x in v["so"])
        if v["so_db"] is not None:
            so += " |" + str(v["so_db"]).zfill(2)
        dau = "  " + v["ngay_mua"] + "  " + ten.ljust(11) + so
        if k["trang_thai"] == "cho":
            print(dau + "   -> chờ quay")
            continue
        ky = k["ky"]
        duoi = "trùng " + str(k["trung"]) + " số"
        if v["so_db"] is not None and k["db_ky"] is not None:
            duoi += "+ĐB" if k["trung_db"] else ""
        if k["tien"] > 0:
            duoi += "  >>> " + k["ten_giai"] + " " + vnd(k["tien"])
            if k["toi_thieu"]:
                duoi += " (mức tối thiểu — thực tế lũy tiến cao hơn)"
        elif v["ma"] in GIAI:
            duoi += "  (trượt)"
        else:
            duoi += "  (sản phẩm này không tính tiền, chỉ báo số trùng)"
        print(dau + "   -> kỳ " + str(ky.get("id")) + " ngày "
              + ngay_viet(ky.get("date"), kem_thu=False) + ": " + duoi)
        if k.get("nhieu_ky_cung_ngay"):
            print(" " * 14 + "(ngày này quay nhiều kỳ — đang chấm kỳ ĐẦU TIÊN trong ngày;"
                  + " muốn chấm kỳ khác, thêm @<mã kỳ> vào dòng vé)")
        if v["ghi_chu"]:
            print(" " * 14 + "# " + v["ghi_chu"])
    print()
    print("-" * 66)
    print("  Tổng: " + str(tong["so_ve"]) + " vé"
          + (" (" + str(tong["cho_quay"]) + " chờ quay)" if tong["cho_quay"] else ""))
    print("  Tiền mua vé : " + vnd(tong["tien_ve"]))
    print("  Tiền trúng  : " + vnd(tong["tien_trung"])
          + ("  (" + str(tong["so_ve_trung"]) + " vé có giải)" if tong["so_ve_trung"] else ""))
    print("  LÃI / LỖ    : " + ("+" if tong["lai_lo"] >= 0 else "") + vnd(tong["lai_lo"]))
    if tong["ve_khong_tinh_tien"]:
        print("  (" + str(tong["ve_khong_tinh_tien"]) + " vé Lotto/Keno chỉ báo số trùng,"
              + " không tính tiền — cơ cấu giải không đủ nguồn công khai)")
    if loi:
        print()
        for x in loi:
            print("  (bỏ qua) " + x)
    print()


def ghi(cac_dong):
    """Thêm vé vào sổ. Dòng chưa có ngày thì tự đóng ngày hôm nay."""
    if not FILE_SO.exists():
        FILE_SO.write_text(MAU_DONG, encoding="utf-8")
    hom_nay = date.today().isoformat()
    them = 0
    with open(FILE_SO, "a", encoding="utf-8") as f:
        for dong in cac_dong:
            dong = dong.strip()
            if not dong:
                continue
            if not re.match(r"^\d{4}-\d{2}-\d{2}\s*\|", dong):
                dong = hom_nay + " | " + dong
            f.write(dong + "\n")
            them += 1
            print("  Đã ghi: " + dong)
    if them == 0:
        print("  Không có gì để ghi. Bấm vào một bộ số trong báo cáo trước đã.")
    return them


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "ghi":
        noi_dung = " ".join(sys.argv[2:])
        # cho phép dán nhiều dòng một lúc
        cac_dong = [d for d in noi_dung.replace("\r", "\n").split("\n") if d.strip()]
        print()
        if ghi(cac_dong):
            in_bao_cao()
        return 0
    in_bao_cao()
    return 0


if __name__ == "__main__":
    sys.exit(main())
