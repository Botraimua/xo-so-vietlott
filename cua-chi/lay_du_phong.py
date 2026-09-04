# -*- coding: utf-8 -*-
"""
Đường dự phòng: lấy kết quả từ các kho dữ liệu Vietlott khác trên GitHub.

Vì sao cần: vietlott.vn nấp sau dịch vụ chống bot, trả 403 cho máy chủ GitHub
(đo tận nơi 30/08/2026). Máy Sếp ở Việt Nam thì gọi bình thường. Nên bot cần
đường khác, mà `raw.githubusercontent.com` thì máy chủ GitHub luôn gọi được.

Vì sao có NHIỀU kho chứ không một: ngày 02/09/2026 kho `vietvudanh` — lúc đó là
kho duy nhất — **ngừng cập nhật từ 29/08**. Lotto 5/35, Max 3D và Max 3D Pro mất
sạch nguồn, chuông báo dữ liệu cũ phải kêu. Một kho là một điểm chết. Giờ có ba,
thử lần lượt, kho nào chết thì kho khác gánh.

Chỉ THÊM kỳ mình chưa có, không bao giờ xoá — nên phần lịch sử đã lấy bù vẫn giữ.
Riêng kỳ nào mang dấu mã-kỳ-tự-suy (xem `lay_kqxs.py`) mà lệch với kho thì bị
ghi đè lại theo kho và KÊU LÊN.

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

# Chỉ lấy các sản phẩm quay theo ngày. Bỏ Keno/Bingo18: file của họ hàng chục MB
# mà mình cũng không theo dõi hai cái đó.
LAY = ("power_655", "power_645", "power_535", "3d", "3d_pro")


# Số con số mà một kỳ PHẢI có (số chính + số đặc biệt). Kho nào trả thiếu là
# dữ liệu hỏng — bỏ qua, đừng để nó chui vào. Đã dính một lần: hai kho là nhánh
# của cùng repo gốc nên cùng thiếu số đặc biệt ở 11 kỳ Power 6/55.
SO_PHAI_CO = {"power_655": 7, "power_645": 6, "power_535": 6}

# Kho pqminh-4 viết "Giải Ba", mình viết "Giải ba". Chỉ khác chữ hoa — số y hệt.
DOI_TEN_GIAI = {"Giải Ba": "Giải ba"}


def _hop_le(ma, ket):
    """Bản ghi có đủ số không. Sản phẩm 3D trả dict nên bỏ qua khoản này."""
    n = SO_PHAI_CO.get(ma)
    if n is None:
        return isinstance(ket, dict) and bool(ket)
    return isinstance(ket, list) and len(ket) == n


def _chuan(r):
    """Kho dùng đúng lược đồ của repo gốc — giữ nguyên."""
    if not r.get("id") or r.get("result") is None:
        return None
    return {"date": str(r.get("date"))[:10], "id": str(r["id"]).strip(),
            "result": r["result"], "process_time": r.get("process_time", "")}


def _canonical(r):
    """
    Kho pqminh-4 dùng lược đồ riêng, phải đổi hình:

        {"draw_date": "...", "draw_id": "00860",
         "result": {"main_numbers": [...], "bonus_numbers": [...]}}          -> số
        {"result": {"tiers": [{"name": "Giải Nhất", "numbers": [...]}, ...]}} -> 3D
    """
    kq = r.get("result") or {}
    if not r.get("draw_id"):
        return None
    if kq.get("kind") == "three_digit_tiers":
        ket = {DOI_TEN_GIAI.get(t["name"], t["name"]): t["numbers"]
               for t in kq.get("tiers", []) if t.get("name")}
        if not ket:
            return None
    else:
        chinh = kq.get("main_numbers")
        if not chinh:
            return None
        ket = list(chinh) + list(kq.get("bonus_numbers") or [])
    return {"date": str(r.get("draw_date"))[:10], "id": str(r["draw_id"]).strip(),
            "result": ket, "process_time": r.get("retrieved_at", "")}


# Thử lần lượt từ trên xuống. Mỗi kho khai báo: tên file cho từng sản phẩm nó có,
# và hàm đổi hình về lược đồ của mình.
KHO = [
    {
        "ten": "pqminh-4",
        "goc": "https://raw.githubusercontent.com/pqminh-4/vietlott-data/main/data/canonical/",
        "file": {"power_655": "power655.jsonl", "power_535": "lotto535.jsonl",
                 "3d": "max3d.jsonl", "3d_pro": "max3d_pro.jsonl"},
        "doi": _canonical,
    },
    {
        "ten": "googlesky",
        "goc": "https://raw.githubusercontent.com/googlesky/vietlott-data/main/data/",
        "file": {"power_655": "power655.jsonl", "power_645": "power645.jsonl"},
        "doi": _chuan,
    },
    {
        # Kho của tác giả repo gốc. Ngừng cập nhật từ 29/08/2026 nhưng vẫn để đây:
        # nếu sống lại thì dùng được ngay, mà chết thì cũng chỉ tốn một lần gọi.
        "ten": "vietvudanh",
        "goc": "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/",
        "file": {m: SAN_PHAM[m]["file"] for m in LAY},
        "doi": _chuan,
    },
]


def tai(url):
    req = urllib.request.Request(url, headers={"User-Agent": "vietlott-cua-chi"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def _ma(r):
    return str(r.get("id", "")).strip()


def doc_kho(kho, ma):
    """Đọc một sản phẩm từ một kho. Trả (danh sách bản ghi, ghi chú)."""
    ten_file = kho["file"].get(ma)
    if not ten_file:
        return [], "không có sản phẩm này"
    try:
        noi_dung = tai(kho["goc"] + ten_file)
    except urllib.error.HTTPError as e:
        return [], "HTTP " + str(e.code)
    except Exception as e:
        return [], str(e)[:40]

    ra, bo_qua = [], 0
    for line in noi_dung.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        x = kho["doi"](r)
        if x and _hop_le(ma, x["result"]):
            ra.append(x)
        elif x:
            bo_qua += 1
    ghi = (str(len(ra)) + " kỳ, mới nhất " + ra[-1]["date"]) if ra else "rỗng"
    if bo_qua:
        ghi += "  (bỏ " + str(bo_qua) + " kỳ thiếu số)"
    return ra, ghi


def gop_mot(ma):
    """Trả về (số kỳ thêm được, ghi chú)."""
    dich = THU_MUC_DATA / SAN_PHAM[ma]["file"]

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

    theo_ma = {_ma(r): r for r in cu if _ma(r)}
    theo_ngay = {str(r.get("date"))[:10]: r for r in cu}

    them, sua, keu, nguon_da_dung = [], [], [], []
    for kho in KHO:
        ban_ghi, ghi = doc_kho(kho, ma)
        if not ban_ghi:
            continue
        nguon_da_dung.append(kho["ten"])
        for r in ban_ghi:
            ngay = r["date"]
            cua_minh = theo_ma.get(_ma(r)) or theo_ngay.get(ngay)

            if cua_minh is None:
                theo_ma[_ma(r)] = r
                theo_ngay[ngay] = r
                them.append(r)
                continue

            # Đã có kỳ này. Khớp cả mã, ngày lẫn số thì thôi.
            if (str(cua_minh.get("date"))[:10] == ngay
                    and cua_minh.get("result") == r["result"]
                    and _ma(cua_minh) == _ma(r)):
                continue

            # Lệch. Kho là chuẩn — kỳ nào mình TỰ SUY mã thì sửa lại theo kho.
            if cua_minh.get("nguon") == "kqxs":
                sua.append((cua_minh, r, kho["ten"]))
            else:
                keu.append((cua_minh, r, kho["ten"]))

    if sua:
        print()
        print("  !! Có " + str(len(sua)) + " kỳ mã tự suy bị lệch — đang sửa theo kho:")
        for a, b, ten in sua:
            print("     ngày " + str(a.get("date"))[:10]
                  + "   mình: mã " + _ma(a) + " " + str(a.get("result"))
                  + "   ->  " + ten + ": mã " + _ma(b) + " " + str(b["result"]))
        bo = {id(a) for a, _, _ in sua}
        cu = [r for r in cu if id(r) not in bo]
        them.extend(b for _, b, _ in sua)

    if keu:
        print()
        print("  !! CẢNH BÁO: " + str(len(keu)) + " kỳ lệch mà KHÔNG phải mã tự suy.")
        print("     Đây là chuyện không nên xảy ra — giữ nguyên bản của mình, Sếp xem lại:")
        for a, b, ten in keu[:10]:
            print("     ngày " + str(a.get("date"))[:10]
                  + "   mình: mã " + _ma(a) + " " + str(a.get("result"))
                  + "   " + ten + ": mã " + _ma(b) + " " + str(b["result"]))

    ghi_chu = ("nguồn: " + ", ".join(nguon_da_dung)) if nguon_da_dung else "không kho nào có"
    if not them:
        return 0, "đã đủ  (" + ghi_chu + ")"

    tat_ca = cu + them
    tat_ca.sort(key=lambda r: (str(r.get("date", "")), _ma(r)))
    with open(dich, "w", encoding="utf-8", newline="\n") as f:
        for r in tat_ca:
            json.dump(r, f, ensure_ascii=False)
            f.write("\n")
    return len(them), "kỳ cuối " + ngay_viet(tat_ca[-1].get("date"), kem_thu=False)


def main():
    print()
    print("=" * 66)
    print("  ĐƯỜNG DỰ PHÒNG — lấy từ các kho dữ liệu trên GitHub")
    print("=" * 66)
    print("  Dùng khi vietlott.vn không trả dữ liệu cho máy đang chạy.")
    print("  Thử lần lượt: " + " -> ".join(k["ten"] for k in KHO))
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
        print("  Không có kỳ nào để bù — dữ liệu đang ngang hoặc mới hơn các kho kia.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
