# -*- coding: utf-8 -*-
"""
Thư viện dùng chung cho bộ công cụ Vietlott của chị.
Chỉ dùng thư viện chuẩn của Python -> chạy được ở bất cứ máy nào có Python.
"""

import json
import os
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
THU_MUC_DATA = GOC / "data"
THU_MUC_BAO_CAO = GOC / "bao-cao"
FILE_VE = Path(__file__).resolve().parent / "ve-cua-chi.txt"

# Mô tả từng sản phẩm: bao nhiêu số chính, có số đặc biệt không, dải số tới đâu
SAN_PHAM = {
    "power_655": {
        "ten": "Power 6/55",
        "file": "power655.jsonl",
        "so_chinh": 6,
        "max_chinh": 55,
        "co_so_db": True,
        "max_db": 55,
        "lich": "Thứ 3 - Thứ 5 - Thứ 7, 18h00",
        "phan_tich_day_du": True,
    },
    "power_645": {
        "ten": "Mega 6/45",
        "file": "power645.jsonl",
        "so_chinh": 6,
        "max_chinh": 45,
        "co_so_db": False,
        "max_db": 0,
        "lich": "Thứ 4 - Thứ 6 - Chủ nhật, 18h00",
        "phan_tich_day_du": True,
    },
    "power_535": {
        "ten": "Lotto 5/35",
        "file": "power535.jsonl",
        "so_chinh": 5,
        "max_chinh": 35,
        "co_so_db": True,
        "max_db": 12,
        "lich": "Hằng ngày 2 kỳ — 13h00 và 21h00",
        "phan_tich_day_du": True,
    },
    "keno": {
        "ten": "Keno",
        "file": "keno.jsonl",
        "so_chinh": 20,
        "max_chinh": 80,
        "co_so_db": False,
        "max_db": 0,
        "lich": "Mỗi 10 phút, 6h00 - 21h55",
        "phan_tich_day_du": True,
    },
    "bingo18": {
        "ten": "Bingo18",
        "file": "bingo18.jsonl",
        "so_chinh": 3,
        "max_chinh": 9,
        "co_so_db": False,
        "max_db": 0,
        "lich": "Mỗi 10 phút",
        "phan_tich_day_du": False,
    },
    "3d": {
        "ten": "Max 3D",
        "file": "3d.jsonl",
        "so_chinh": 0,
        "max_chinh": 999,
        "co_so_db": False,
        "max_db": 0,
        "lich": "Thứ 2 - Thứ 4 - Thứ 6, 18h00",
        "phan_tich_day_du": False,
    },
    "3d_pro": {
        "ten": "Max 3D Pro",
        "file": "3d_pro.jsonl",
        "so_chinh": 0,
        "max_chinh": 999,
        "co_so_db": False,
        "max_db": 0,
        "lich": "Thứ 3 - Thứ 5 - Thứ 7, 18h00",
        "phan_tich_day_du": False,
    },
}

# Tên gọi khác chị hay gõ -> mã sản phẩm chuẩn
BIET_DANH = {
    "power": "power_655", "power655": "power_655", "655": "power_655",
    "power6/55": "power_655", "6/55": "power_655",
    "mega": "power_645", "mega645": "power_645", "645": "power_645",
    "power645": "power_645", "6/45": "power_645", "mega6/45": "power_645",
    "lotto": "power_535", "lotto535": "power_535", "535": "power_535",
    "power535": "power_535", "5/35": "power_535", "lotto5/35": "power_535",
    "keno": "keno",
    "bingo": "bingo18", "bingo18": "bingo18",
    "3d": "3d", "max3d": "3d",
    "3dpro": "3d_pro", "max3dpro": "3d_pro",
}


def bat_utf8():
    """Cho tiếng Việt hiện đúng trong cửa sổ đen của Windows."""
    if os.name == "nt":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass


def chuan_hoa_ma(ten):
    key = ten.strip().lower().replace("-", "_").replace(" ", "")
    if key in SAN_PHAM:
        return key
    if key in BIET_DANH:
        return BIET_DANH[key]
    return None


def doc_du_lieu(ma):
    """Đọc file .jsonl của 1 sản phẩm, trả về list các kỳ quay, cũ -> mới."""
    duong_dan = THU_MUC_DATA / SAN_PHAM[ma]["file"]
    if not duong_dan.exists():
        return []
    rows = []
    with open(duong_dan, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    rows.sort(key=lambda r: (str(r.get("date", "")), str(r.get("id", ""))))
    return rows


def tach_so(ky, ma):
    """Tách 1 kỳ thành (danh sách số chính, số đặc biệt hoặc None)."""
    cfg = SAN_PHAM[ma]
    kq = ky.get("result")
    if not isinstance(kq, list):
        return [], None
    try:
        so = [int(x) for x in kq]
    except (TypeError, ValueError):
        return [], None
    n = cfg["so_chinh"]
    if cfg["co_so_db"] and len(so) > n:
        return so[:n], so[n]
    return (so[:n] if n else so), None


THU_TRONG_TUAN = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]


def ngay_viet(s, kem_thu=True):
    """2026-08-22 -> 22/08/2026 (Thứ 7)"""
    try:
        d = datetime.strptime(str(s)[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return str(s)
    if kem_thu:
        return d.strftime("%d/%m/%Y") + " (" + THU_TRONG_TUAN[d.weekday()] + ")"
    return d.strftime("%d/%m/%Y")


def thong_ke(ma, rows):
    """Tính tần suất, lần cuối xuất hiện, số kỳ chưa về (gan) cho từng con số."""
    cfg = SAN_PHAM[ma]
    tong_ky = len(rows)
    dem = Counter()
    dem_db = Counter()
    ky_cuoi = {}
    ngay_cuoi = {}
    cap = Counter()
    tong_moi_ky = Counter()
    chan_moi_ky = Counter()

    for i, ky in enumerate(rows):
        chinh, db = tach_so(ky, ma)
        for s in chinh:
            dem[s] += 1
            ky_cuoi[s] = i
            ngay_cuoi[s] = ky.get("date")
        if db is not None:
            dem_db[db] += 1
        if chinh:
            tong_moi_ky[sum(chinh)] += 1
            chan_moi_ky[sum(1 for x in chinh if x % 2 == 0)] += 1
        if 2 <= len(chinh) <= 8:
            sc = sorted(set(chinh))
            for a in range(len(sc)):
                for b in range(a + 1, len(sc)):
                    cap[(sc[a], sc[b])] += 1

    bang = []
    for s in range(1, cfg["max_chinh"] + 1):
        lan = dem.get(s, 0)
        idx = ky_cuoi.get(s)
        gan = (tong_ky - 1 - idx) if idx is not None else tong_ky
        bang.append({
            "so": s,
            "lan": lan,
            "ty_le": (lan / tong_ky * 100) if tong_ky else 0.0,
            "ngay_cuoi": ngay_cuoi.get(s),
            "gan": gan,
        })

    bang_db = []
    if cfg["co_so_db"]:
        tong_db = sum(dem_db.values()) or 1
        for s in range(1, cfg["max_db"] + 1):
            bang_db.append({
                "so": s,
                "lan": dem_db.get(s, 0),
                "ty_le": dem_db.get(s, 0) / tong_db * 100,
            })

    return {
        "ma": ma,
        "tong_ky": tong_ky,
        "tu_ngay": rows[0].get("date") if rows else None,
        "den_ngay": rows[-1].get("date") if rows else None,
        "bang": bang,
        "bang_db": bang_db,
        "cap_hay_gap": cap.most_common(12),
        "tong_moi_ky": tong_moi_ky,
        "chan_moi_ky": chan_moi_ky,
    }


# ---------- Đọc & dò vé của chị ----------

def doc_ve():
    """Đọc file ve-cua-chi.txt. Mỗi dòng: <san pham>: <cac so>  # ghi chu"""
    if not FILE_VE.exists():
        return []
    ve = []
    with open(FILE_VE, "r", encoding="utf-8") as f:
        for so_dong, line in enumerate(f, 1):
            raw = line.strip()
            if not raw or raw.startswith("#"):
                continue
            ghi_chu = ""
            if "#" in raw:
                raw, ghi_chu = raw.split("#", 1)
                ghi_chu = ghi_chu.strip()
            raw = raw.strip()
            if not raw:
                continue
            if ":" not in raw:
                ve.append({"loi": "Dòng " + str(so_dong) + ": thiếu dấu hai chấm", "raw": line.strip()})
                continue
            ten, phan_so = raw.split(":", 1)
            ma = chuan_hoa_ma(ten)
            if ma is None:
                ve.append({"loi": "Dòng " + str(so_dong) + ": không hiểu sản phẩm " + ten.strip(),
                           "raw": line.strip()})
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
                so = [int(x) for x in phan_so.replace(",", " ").replace(";", " ").split()]
            except ValueError:
                ve.append({"loi": "Dòng " + str(so_dong) + ": có ký tự không phải số", "raw": line.strip()})
                continue
            cfg = SAN_PHAM[ma]
            if len(so) != cfg["so_chinh"]:
                ve.append({"loi": "Dòng " + str(so_dong) + ": " + cfg["ten"] + " cần " + str(cfg["so_chinh"])
                                  + " số, chị ghi " + str(len(so)) + " số", "raw": line.strip()})
                continue
            ngoai_dai = [x for x in so if x < 1 or x > cfg["max_chinh"]]
            if ngoai_dai:
                ve.append({"loi": "Dòng " + str(so_dong) + ": số " + str(ngoai_dai)
                                  + " nằm ngoài dải 1-" + str(cfg["max_chinh"]), "raw": line.strip()})
                continue
            ve.append({"ma": ma, "so": sorted(so), "so_db": so_db, "ghi_chu": ghi_chu, "raw": line.strip()})
    return ve


def xep_giai(ma, trung, trung_db):
    """Tên hạng giải theo số con trùng. Chỉ khẳng định với 6/55 và 6/45."""
    if ma == "power_655":
        if trung == 6:
            return "JACKPOT 1"
        if trung == 5 and trung_db:
            return "JACKPOT 2"
        if trung == 5:
            return "Giải nhất"
        if trung == 4:
            return "Giải nhì"
        if trung == 3:
            return "Giải ba"
        return "—"
    if ma == "power_645":
        if trung == 6:
            return "JACKPOT"
        if trung == 5:
            return "Giải nhất"
        if trung == 4:
            return "Giải nhì"
        if trung == 3:
            return "Giải ba"
        return "—"
    return ""


def do_mot_ve(ve, rows):
    """So 1 bộ số với toàn bộ lịch sử + kỳ mới nhất."""
    ma = ve["ma"]
    tap = set(ve["so"])
    phan_bo = Counter()
    ky_tot_nhat = None
    diem_tot_nhat = -1
    ky_trung_giai = []

    for ky in rows:
        chinh, db = tach_so(ky, ma)
        if not chinh:
            continue
        trung = len(tap & set(chinh))
        trung_db = (ve["so_db"] is not None and db is not None and ve["so_db"] == db)
        phan_bo[trung] += 1
        diem = trung * 10 + (1 if trung_db else 0)
        if diem > diem_tot_nhat:
            diem_tot_nhat = diem
            ky_tot_nhat = (ky, trung, trung_db)
        giai = xep_giai(ma, trung, trung_db)
        if giai not in ("—", ""):
            ky_trung_giai.append((ky, trung, trung_db, giai))

    kq_moi = None
    if rows:
        ky_moi = rows[-1]
        chinh, db = tach_so(ky_moi, ma)
        trung = len(tap & set(chinh))
        trung_db = (ve["so_db"] is not None and db is not None and ve["so_db"] == db)
        kq_moi = {
            "ky": ky_moi,
            "trung": trung,
            "trung_db": trung_db,
            "giai": xep_giai(ma, trung, trung_db),
            "so_ky": sorted(chinh),
            "so_db_ky": db,
        }

    return {
        "ve": ve,
        "ky_moi_nhat": kq_moi,
        "phan_bo": dict(sorted(phan_bo.items(), reverse=True)),
        "tot_nhat": ky_tot_nhat,
        "so_lan_trung_giai": len(ky_trung_giai),
        "ky_trung_giai": list(reversed(ky_trung_giai[-5:])),
        "tong_ky": len(rows),
    }
