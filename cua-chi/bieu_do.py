# -*- coding: utf-8 -*-
"""
Vẽ biểu đồ bằng SVG thuần, nhúng thẳng vào file HTML.
Không dùng thư viện ngoài -> báo cáo vẫn là 1 file tự chứa, mở offline được.

Hệ toạ độ SVG rộng 1000 x cao 400. Thẻ chứa biểu đồ thường rộng ~500px nên
mọi thứ bị thu còn một nửa -> cỡ chữ phải đặt to gấp đôi mức mong muốn.
"""

import html


def _e(s):
    return html.escape(str(s if s is not None else ""))


CHU = 20        # cỡ chữ trục, tính trong hệ toạ độ SVG
CAO_MAC_DINH = 400


def cot(gia_tri, nhan=None, cao=CAO_MAC_DINH, mau="var(--nhan)", ky_vong=None,
        don_vi="", nhan_moi=5, tieu_de_cot=None):
    """
    Biểu đồ cột đứng.

    gia_tri : list số
    nhan    : list nhãn trục ngang (mặc định 1..n)
    ky_vong : nếu có, vẽ đường ngang đứt nét ở mức này
    nhan_moi: cứ mấy cột thì ghi 1 nhãn cho đỡ rối
    """
    n = len(gia_tri)
    if n == 0:
        return ""
    if nhan is None:
        nhan = [str(i + 1) for i in range(n)]

    lien = 1000.0
    le_trai, le_phai = 78, 18
    le_tren, le_duoi = 22, 50
    vung_rong = lien - le_trai - le_phai
    vung_cao = cao - le_tren - le_duoi

    dinh = max(list(gia_tri) + ([ky_vong] if ky_vong else [0]))
    if dinh <= 0:
        dinh = 1
    dinh *= 1.08

    buoc = vung_rong / n
    rong_cot = max(1.5, buoc * 0.74)

    p = ['<svg class="bd" viewBox="0 0 ' + str(int(lien)) + " " + str(int(cao))
         + '" role="img">']

    # lưới ngang + số trên trục dọc
    for k in range(0, 5):
        gt = dinh * k / 4
        y = le_tren + vung_cao - (gt / dinh) * vung_cao
        p.append('<line x1="' + str(le_trai) + '" y1="' + format(y, ".1f")
                 + '" x2="' + str(int(lien - le_phai)) + '" y2="' + format(y, ".1f")
                 + '" stroke="var(--vien)" stroke-width="1.6"/>')
        p.append('<text x="' + str(le_trai - 10) + '" y="' + format(y + CHU * 0.36, ".1f")
                 + '" text-anchor="end" font-size="' + str(CHU) + '" fill="var(--mo)">'
                 + (format(gt, ".0f") if dinh >= 8 else format(gt, ".1f")) + "</text>")

    # cột
    for i, v in enumerate(gia_tri):
        h = max(0.0, (v / dinh) * vung_cao)
        x = le_trai + i * buoc + (buoc - rong_cot) / 2
        y = le_tren + vung_cao - h
        tt = (tieu_de_cot(i, v) if tieu_de_cot else (str(nhan[i]) + ": " + str(v) + don_vi))
        p.append('<rect x="' + format(x, ".1f") + '" y="' + format(y, ".1f")
                 + '" width="' + format(rong_cot, ".1f") + '" height="' + format(h, ".1f")
                 + '" fill="' + mau + '" opacity="0.82"><title>' + _e(tt) + "</title></rect>")

    # đường kỳ vọng
    if ky_vong:
        y = le_tren + vung_cao - (ky_vong / dinh) * vung_cao
        p.append('<line x1="' + str(le_trai) + '" y1="' + format(y, ".1f")
                 + '" x2="' + str(int(lien - le_phai)) + '" y2="' + format(y, ".1f")
                 + '" stroke="var(--lanh)" stroke-width="3" stroke-dasharray="14 9"/>')

    # nhãn trục ngang
    for i in range(n):
        if i % nhan_moi != 0 and i != n - 1:
            continue
        x = le_trai + i * buoc + buoc / 2
        p.append('<text x="' + format(x, ".1f") + '" y="' + str(int(cao - 16))
                 + '" text-anchor="middle" font-size="' + str(CHU) + '" fill="var(--mo)">'
                 + _e(nhan[i]) + "</text>")

    p.append("</svg>")
    return "".join(p)


def khung(tieu_de, svg, chu_thich="", co_ky_vong=False):
    """Bọc 1 biểu đồ vào thẻ có tiêu đề và lời giải thích."""
    ghi = ""
    if co_ky_vong:
        ghi = ('<span class="chu-thich"><span class="vach"></span>'
               "mức kỳ vọng nếu quay hoàn toàn ngẫu nhiên</span>")
    return ('<div class="the">'
            + '<div class="ten-bd">' + _e(tieu_de) + ghi + "</div>"
            + svg
            + ('<div class="mo" style="margin-top:6px">' + chu_thich + "</div>" if chu_thich else "")
            + "</div>")


CSS_BIEU_DO = """
svg.bd{width:100%;height:auto;display:block;margin-top:8px}
.ten-bd{font-size:13.5px;font-weight:600;display:flex;justify-content:space-between;
align-items:center;flex-wrap:wrap;gap:6px}
.chu-thich{font-size:11.5px;font-weight:400;color:var(--mo);display:inline-flex;
align-items:center;gap:5px}
.vach{display:inline-block;width:18px;height:0;border-top:2px dashed var(--lanh)}
.luoi-bd{grid-template-columns:repeat(auto-fit,minmax(330px,1fr))}
@media (max-width:400px){.luoi-bd{grid-template-columns:1fr}}
"""
