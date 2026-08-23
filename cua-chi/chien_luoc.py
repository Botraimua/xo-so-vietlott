# -*- coding: utf-8 -*-
"""
9 cách chọn số, viết lại từ repo gốc bằng Python thuần.

Mỗi hàm nhận lịch sử các kỳ TRƯỚC kỳ đang xét, trả về trọng số cho từng con số
trong dải hợp lệ. Trọng số càng cao thì càng dễ được bốc. Trọng số 0 = không bốc.

Dùng chung cho:
  - kiem_thu.py  (chấm điểm 9 chiến lược trên lịch sử)
  - goi_so.py    (đề xuất bộ số cho kỳ tới)

LƯU Ý: không cách nào trong đây ăn được. Xem kết quả kiểm thử ở kiem_thu.py.
Chúng có mặt ở đây để so sánh và để chọn số cho vui, không phải để dự đoán.
"""

import math
from collections import Counter, defaultdict


def _dem_trong_cua_so(lich_su, so_ky):
    d = Counter()
    for chinh, _db in lich_su[-so_ky:]:
        for s in chinh:
            d[s] += 1
    return d


def w_ngau_nhien(lich_su, dai):
    return {s: 1.0 for s in dai}


def w_so_nong(lich_su, dai, so_ky=180):
    d = _dem_trong_cua_so(lich_su, so_ky)
    return {s: 1.0 + 3.0 * d.get(s, 0) for s in dai}


def w_so_lanh(lich_su, dai, so_ky=180):
    d = _dem_trong_cua_so(lich_su, so_ky)
    dinh = max(d.values()) if d else 0
    return {s: 1.0 + 3.0 * (dinh - d.get(s, 0)) for s in dai}


def w_lau_chua_ve(lich_su, dai, top_n=10):
    cuoi = {}
    for i, (chinh, _db) in enumerate(lich_su):
        for s in chinh:
            cuoi[s] = i
    gan = {s: len(lich_su) - cuoi.get(s, -1) for s in dai}
    tap = set(sorted(dai, key=lambda s: -gan[s])[:top_n])
    return {s: (1.0 if s in tap else 0.0) for s in dai}


def w_khong_lap_lai(lich_su, dai, so_ky=15, avoid=0.8):
    gan_day = set()
    for chinh, _db in lich_su[-so_ky:]:
        gan_day.update(chinh)
    return {s: (1.0 - avoid if s in gan_day else 1.0) for s in dai}


def w_suy_giam_mu(lich_su, dai, ban_ky=45):
    diem = defaultdict(float)
    n = len(lich_su)
    for i, (chinh, _db) in enumerate(lich_su):
        w = math.exp(-math.log(2) * (n - i) / ban_ky)
        for s in chinh:
            diem[s] += w
    return {s: 1.0 + 3.0 * diem.get(s, 0.0) for s in dai}


def w_tan_suat_cap(lich_su, dai, so_ky=180):
    """Số hay đi cùng với các số vừa về ở kỳ liền trước."""
    cung = defaultdict(float)
    for chinh, _db in lich_su[-so_ky:]:
        sc = sorted(chinh)
        for a in range(len(sc)):
            for b in range(a + 1, len(sc)):
                cung[(sc[a], sc[b])] += 1
                cung[(sc[b], sc[a])] += 1
    truoc = lich_su[-1][0] if lich_su else []
    return {s: 1.0 + sum(cung.get((t, s), 0.0) for t in truoc) for s in dai}


def w_markov(lich_su, dai, so_ky=180, lam_min=0.5):
    """Số hay xuất hiện ở kỳ SAU, khi kỳ trước có các số đang có."""
    chuyen = defaultdict(float)
    cua = lich_su[-so_ky:]
    for i in range(len(cua) - 1):
        for a in cua[i][0]:
            for b in cua[i + 1][0]:
                chuyen[(a, b)] += 1
    truoc = lich_su[-1][0] if lich_su else []
    return {s: lam_min + sum(chuyen.get((t, s), 0.0) for t in truoc) for s in dai}


def w_mau_hinh(lich_su, dai, so_ky=90):
    """Theo phân bố 5 khoảng của dải số trong cửa sổ gần đây."""
    lon_nhat = max(dai)
    rong = lon_nhat / 5.0

    def o(s):
        return min(4, int((s - 1) // rong))

    khoang = Counter()
    for chinh, _db in lich_su[-so_ky:]:
        for s in chinh:
            khoang[o(s)] += 1
    tong = sum(khoang.values()) or 1
    return {s: 1.0 + 5.0 * khoang.get(o(s), 0) / tong for s in dai}


# (tên hiển thị, hàm, mô tả ngắn)
CHIEN_LUOC = [
    ("Ngẫu nhiên", w_ngau_nhien, "bốc bừa, không nhìn lịch sử — mốc so sánh"),
    ("Số nóng", w_so_nong, "ưu tiên số hay về trong ~180 kỳ gần đây"),
    ("Số lạnh", w_so_lanh, "ưu tiên số ít về trong ~180 kỳ gần đây"),
    ("Lâu chưa về", w_lau_chua_ve, "chỉ bốc trong 10 số vắng lâu nhất"),
    ("Không lặp lại", w_khong_lap_lai, "né các số vừa về 15 kỳ gần đây"),
    ("Suy giảm mũ", w_suy_giam_mu, "số nóng nhưng kỳ càng cũ càng nhẹ ký"),
    ("Tần suất cặp", w_tan_suat_cap, "số hay đi cùng các số của kỳ liền trước"),
    ("Chuỗi Markov", w_markov, "số hay về ở kỳ SAU khi kỳ trước có các số đó"),
    ("Mẫu hình", w_mau_hinh, "theo phân bố 5 khoảng của dải số"),
]


def boc_ve(trong_so, rng, so_luong, dai):
    """Bốc `so_luong` số khác nhau theo trọng số."""
    con = dict(trong_so)
    ve = set()
    while len(ve) < so_luong:
        ung = [s for s, w in con.items() if w > 0]
        if not ung:
            con = {s: 1.0 for s in dai if s not in ve}
            continue
        s = rng.choices(ung, weights=[con[x] for x in ung], k=1)[0]
        ve.add(s)
        con.pop(s, None)
    return sorted(ve)
