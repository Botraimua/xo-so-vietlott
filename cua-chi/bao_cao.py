# -*- coding: utf-8 -*-
"""
Dựng báo cáo thống kê Vietlott thành 1 file HTML tự chứa.
Mở bằng trình duyệt bất kỳ, không cần mạng, không cần Claude.

Cách chạy:
    python cua-chi/bao_cao.py
"""

import html
import json
import math
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bieu_do import CSS_BIEU_DO, cot, khung  # noqa: E402
from thu_vien import (  # noqa: E402
    SAN_PHAM, THU_MUC_BAO_CAO, bat_utf8, doc_du_lieu, doc_ve, do_mot_ve,
    kiem_lo, ngay_viet, tach_so, thong_ke,
)

bat_utf8()

CSS = """
:root{--nen:#f6f7f9;--the:#fff;--chu:#1b1f26;--mo:#6b7280;--vien:#e3e6ea;
--nhan:#c81e1e;--nhandiu:#fdecec;--lanh:#1d4ed8;--lanhdiu:#e8eefc;
--gan:#b45309;--gandiu:#fdf1e0;--xanh:#047857;--xanhdiu:#e6f4ef}
@media (prefers-color-scheme:dark){:root{--nen:#14161a;--the:#1c1f25;--chu:#e8eaed;
--mo:#9aa1ab;--vien:#2b2f36;--nhandiu:#3a1c1c;--nhan:#f87171;--lanhdiu:#1a2436;
--lanh:#93b4fb;--gandiu:#33260f;--gan:#f0b45f;--xanhdiu:#12291f;--xanh:#5ad6a4}}
*{box-sizing:border-box}
body{margin:0;padding:0 16px 64px;background:var(--nen);color:var(--chu);
font-family:"Segoe UI",Roboto,system-ui,sans-serif;line-height:1.55;font-size:15px}
.bao{max-width:1080px;margin:0 auto}
header{padding:28px 0 8px}
h1{margin:0 0 4px;font-size:26px;letter-spacing:-.3px}
h2{font-size:19px;margin:32px 0 12px;padding-top:8px}
h3{font-size:15px;margin:22px 0 8px;color:var(--mo);text-transform:uppercase;
letter-spacing:.6px;font-weight:600}
.mo{color:var(--mo);font-size:13px}
.the{background:var(--the);border:1px solid var(--vien);border-radius:12px;
padding:16px 18px;margin-bottom:14px}
.luoi{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}
.bi{display:inline-flex;align-items:center;justify-content:center;min-width:34px;
height:34px;padding:0 6px;border-radius:50%;background:var(--nhandiu);color:var(--nhan);
font-weight:700;font-size:14px;margin:2px 3px 2px 0;border:1px solid transparent}
.bi.db{background:var(--gandiu);color:var(--gan);border-color:var(--gan)}
.bi.lanh{background:var(--lanhdiu);color:var(--lanh)}
.bi.gan{background:var(--gandiu);color:var(--gan)}
.bi.trung{background:var(--xanhdiu);color:var(--xanh);border-color:var(--xanh)}
.bi.nho{min-width:28px;height:28px;font-size:12px}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th,td{text-align:left;padding:7px 9px;border-bottom:1px solid var(--vien)}
th{color:var(--mo);font-weight:600;font-size:12px;text-transform:uppercase;
letter-spacing:.4px;white-space:nowrap}
th.sx{cursor:pointer;user-select:none}
th.sx:hover{color:var(--chu)}
td.so{text-align:right;font-variant-numeric:tabular-nums}
th.so{text-align:right}
.cuon{overflow-x:auto;-webkit-overflow-scrolling:touch}
.thanh{height:6px;border-radius:3px;background:var(--nhan);opacity:.75;min-width:2px}
nav{position:sticky;top:0;background:var(--nen);padding:10px 0;z-index:5;
border-bottom:1px solid var(--vien);margin-bottom:8px}
nav a{display:inline-block;padding:6px 12px;margin:2px 4px 2px 0;border-radius:20px;
background:var(--the);border:1px solid var(--vien);color:var(--chu);
text-decoration:none;font-size:13px}
nav a:hover{border-color:var(--mo)}
.nhan-nho{display:inline-block;padding:2px 8px;border-radius:12px;font-size:11.5px;
font-weight:600;background:var(--vien);color:var(--mo)}
.nhan-nho.thang{background:var(--xanhdiu);color:var(--xanh)}
.nhan-nho.sai{background:var(--nhandiu);color:var(--nhan)}
.canh a{color:inherit}
.luoi-goi{grid-template-columns:repeat(auto-fit,minmax(250px,1fr))}
.bo-so{cursor:pointer;padding:4px 6px;margin:2px -6px;border-radius:8px;
border:1px solid transparent;transition:background .12s,border-color .12s}
.bo-so:hover{background:var(--nen);border-color:var(--vien)}
.bo-so.chep-roi{border-color:var(--xanh);background:var(--xanhdiu)}
.bo-so.chep-roi::after{content:" đã chép";font-size:11.5px;color:var(--xanh);
font-weight:600;vertical-align:middle}
.canh{border-left:3px solid var(--gan);background:var(--gandiu);padding:12px 16px;
border-radius:0 8px 8px 0;margin:24px 0;font-size:13.5px}
footer{margin-top:40px;padding-top:16px;border-top:1px solid var(--vien);
color:var(--mo);font-size:12.5px}
""" + CSS_BIEU_DO

JS = """
document.querySelectorAll('table.sapxep').forEach(function(t){
  t.querySelectorAll('th.sx').forEach(function(th,i){
    th.addEventListener('click',function(){
      var tb=t.tBodies[0], rows=Array.from(tb.rows);
      var giam = th.dataset.chieu !== 'giam';
      t.querySelectorAll('th.sx').forEach(function(o){o.dataset.chieu='';
        o.textContent=o.textContent.replace(/ [\\u2191\\u2193]$/,'');});
      th.dataset.chieu = giam ? 'giam' : 'tang';
      th.textContent = th.textContent.replace(/ [\\u2191\\u2193]$/,'') + (giam?' \\u2193':' \\u2191');
      rows.sort(function(a,b){
        var x=a.cells[i].dataset.v, y=b.cells[i].dataset.v;
        var nx=parseFloat(x), ny=parseFloat(y);
        if(!isNaN(nx)&&!isNaN(ny)){return giam? ny-nx : nx-ny;}
        return giam ? String(y).localeCompare(String(x)) : String(x).localeCompare(String(y));
      });
      rows.forEach(function(r){tb.appendChild(r);});
    });
  });
});

document.querySelectorAll('.bo-so').forEach(function(el){
  el.addEventListener('click', function(){
    var t = el.dataset.chep || '';
    function xong(){
      document.querySelectorAll('.bo-so.chep-roi').forEach(function(o){
        o.classList.remove('chep-roi');});
      el.classList.add('chep-roi');
      setTimeout(function(){el.classList.remove('chep-roi');}, 1800);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(t).then(xong, function(){});
    } else {
      var ta = document.createElement('textarea');
      ta.value = t; ta.style.position='fixed'; ta.style.opacity='0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); xong(); } catch(e) {}
      document.body.removeChild(ta);
    }
  });
});
"""


def e(s):
    return html.escape(str(s if s is not None else ""))


def bi(n, lop=""):
    return '<span class="bi ' + lop + '">' + str(n).zfill(2) + "</span>"


def day_bi(ds, db=None, tap_trung=None):
    ra = []
    for n in ds:
        lop = "trung" if (tap_trung and n in tap_trung) else ""
        ra.append(bi(n, lop))
    if db is not None:
        ra.append(bi(db, "db"))
    return "".join(ra)


# ---------- Khối vé của chị ----------

def khoi_ve(du_lieu):
    ve_list = doc_ve()
    if not ve_list:
        return ""
    p = ['<h2 id="ve">Vé của chị</h2>']
    hop_le = [v for v in ve_list if "loi" not in v]
    loi = [v for v in ve_list if "loi" in v]

    for v in hop_le:
        ma = v["ma"]
        rows = du_lieu.get(ma) or []
        if not rows:
            continue
        kq = do_mot_ve(v, rows)
        cfg = SAN_PHAM[ma]
        moi = kq["ky_moi_nhat"]
        tap = set(v["so"])

        p.append('<div class="the">')
        p.append("<div><strong>" + e(cfg["ten"]) + "</strong>"
                 + ('  <span class="mo">' + e(v["ghi_chu"]) + "</span>" if v["ghi_chu"] else "")
                 + "</div>")
        p.append("<div style='margin:8px 0'>" + day_bi(v["so"], v["so_db"]) + "</div>")

        if moi:
            trung = moi["trung"]
            giai = moi["giai"]
            thang = giai not in ("—", "")
            p.append('<div style="margin-top:10px;padding-top:10px;border-top:1px solid var(--vien)">')
            p.append('<div class="mo">Kỳ mới nhất &middot; ' + e(ngay_viet(moi["ky"].get("date")))
                     + " &middot; kỳ #" + e(moi["ky"].get("id")) + "</div>")
            p.append("<div style='margin:6px 0'>"
                     + day_bi(moi["so_ky"], moi["so_db_ky"], tap_trung=tap) + "</div>")
            dong = "Trùng <strong>" + str(trung) + "/" + str(cfg["so_chinh"]) + " số</strong>"
            if v["so_db"] is not None and cfg["co_so_db"]:
                dong += " &middot; số đặc biệt: " + ("<strong>trúng</strong>" if moi["trung_db"] else "không")
            if giai:
                nhan = giai if thang else "Chưa có giải"
                dong += ' &middot; <span class="nhan-nho' + (" thang" if thang else "") + '">' + e(nhan) + "</span>"
            p.append("<div>" + dong + "</div>")
            p.append("</div>")

        tn = kq["tot_nhat"]
        if tn:
            ky, t, tdb = tn
            p.append('<div class="mo" style="margin-top:10px">Trong ' + str(kq["tong_ky"])
                     + " kỳ đã quay, bộ số này khớp cao nhất <strong>" + str(t)
                     + " số</strong> vào ngày " + e(ngay_viet(ky.get("date"), kem_thu=False))
                     + (" (trúng cả số đặc biệt)" if tdb else "") + ".</div>")
        if kq["so_lan_trung_giai"]:
            p.append('<div class="mo">Số kỳ bộ số này đủ điều kiện có giải: <strong>'
                     + str(kq["so_lan_trung_giai"]) + "</strong> lần.</div>")
        p.append("</div>")

    if loi:
        p.append('<div class="canh"><strong>Vài dòng trong ve-cua-chi.txt chưa đọc được:</strong><ul>')
        for l in loi:
            p.append("<li>" + e(l["loi"]) + " &mdash; <code>" + e(l["raw"]) + "</code></li>")
        p.append("</ul></div>")
    return "\n".join(p)


def dong_chat_luong(rows):
    """Một dòng cho biết dữ liệu có liền mạch không. Soi bằng mã kỳ."""
    lo = kiem_lo(rows)
    if not lo:
        return ""
    if lo["hut"] == 0:
        return ('<div class="mo">Dữ liệu liền mạch: mã kỳ chạy đủ từ '
                + str(lo["ma_dau"]) + " đến " + str(lo["ma_cuoi"]) + ", không thiếu kỳ nào.</div>")
    ty = lo["hut"] / lo["le_ra"] * 100
    return ('<div class="canh" style="margin:10px 0">Dữ liệu <strong>chưa đầy đủ</strong>: '
            "trong khoảng mã kỳ " + str(lo["ma_dau"]) + "&ndash;" + str(lo["ma_cuoi"])
            + " lẽ ra có " + format(lo["le_ra"], ",").replace(",", ".") + " kỳ, hiện có "
            + format(lo["co"], ",").replace(",", ".") + " kỳ &mdash; <strong>hụt "
            + format(lo["hut"], ",").replace(",", ".") + " kỳ (" + format(ty, ".0f")
            + "%)</strong>. Bảng tần suất vẫn dùng được vì mẫu đủ lớn và phần hụt là "
            "một quãng thời gian, không thiên về con số nào; nhưng đừng đọc nó như thể "
            "đã bao trọn mọi kỳ quay.</div>")


def khoi_so_ve():
    """Sổ vé đã mua — nhật ký lãi/lỗ thật. Chỉ có ở bản trên máy."""
    try:
        from so_ve import FILE_SO, danh_gia
    except ImportError:
        return ""
    if not FILE_SO.exists():
        return ""
    kq, tong, loi = danh_gia()
    if not kq and not loi:
        return ""

    def vnd(x):
        return format(x, ",").replace(",", ".") + "đ"

    p = ['<h2 id="so-ve">Sổ vé đã mua</h2>']
    p.append('<div class="mo">Mỗi tờ vé gắn với đúng một kỳ quay. Ghi thêm vé: bấm vào một '
             "bộ số gợi ý (nó tự chép) rồi bấm <code>11-GHI-VE-DA-MUA.bat</code>.</div>")

    lai = tong["lai_lo"]
    p.append('<div class="the"><div class="cuon"><table><thead><tr>'
             '<th class="so">Số vé</th><th class="so">Tiền mua vé</th>'
             '<th class="so">Tiền trúng</th><th class="so">Lãi / lỗ</th></tr></thead><tbody>'
             '<tr><td class="so">' + str(tong["so_ve"])
             + ('<span class="mo"> (' + str(tong["cho_quay"]) + " chờ quay)</span>" if tong["cho_quay"] else "")
             + '</td><td class="so">' + vnd(tong["tien_ve"])
             + '</td><td class="so">' + vnd(tong["tien_trung"])
             + '</td><td class="so"><strong style="color:var(--' + ("xanh" if lai >= 0 else "nhan")
             + ')">' + ("+" if lai >= 0 else "") + vnd(lai) + "</strong></td></tr>"
             "</tbody></table></div></div>")

    p.append('<div class="the"><div class="cuon"><table><thead><tr>'
             "<th>Ngày mua</th><th>Vé</th><th>Kỳ quay</th><th>Kết quả</th></tr></thead><tbody>")
    for k in reversed(kq):
        v = k["ve"]
        ten = SAN_PHAM[v["ma"]]["ten"]
        so_html = day_bi(v["so"], v["so_db"])
        o_ve = "<strong>" + e(ten) + "</strong><div>" + so_html + "</div>"
        if v["ghi_chu"]:
            o_ve += '<div class="mo">' + e(v["ghi_chu"]) + "</div>"
        if k["trang_thai"] == "cho":
            p.append("<tr><td>" + e(ngay_viet(v["ngay_mua"], kem_thu=False)) + "</td><td>" + o_ve
                     + '</td><td class="mo">&mdash;</td><td><span class="nhan-nho">chờ quay</span></td></tr>')
            continue
        ky = k["ky"]
        o_ky = e(ngay_viet(ky.get("date"), kem_thu=False)) + '<div class="mo">kỳ ' + e(ky.get("id")) + "</div>"
        tap = set(v["so"])
        o_kq = "<div>" + day_bi(k["so_ky"], k["db_ky"], tap_trung=tap) + "</div>"
        dong = "Trùng <strong>" + str(k["trung"]) + " số</strong>"
        if v["so_db"] is not None and k["db_ky"] is not None and k["trung_db"]:
            dong += " + số đặc biệt"
        if k["tien"] > 0:
            dong += ('  <span class="nhan-nho thang">' + e(k["ten_giai"]) + " " + vnd(k["tien"]) + "</span>")
            if k["toi_thieu"]:
                dong += '<div class="mo">mức tối thiểu — jackpot thực tế lũy tiến cao hơn</div>'
        elif v["ma"] in ("power_655", "power_645"):
            dong += '  <span class="nhan-nho">trượt</span>'
        else:
            dong += '<div class="mo">sản phẩm này chỉ báo số trùng, không tính tiền</div>'
        if k.get("nhieu_ky_cung_ngay"):
            dong += ('<div class="mo">ngày này quay nhiều kỳ — đang chấm kỳ đầu tiên; '
                     "muốn kỳ khác, thêm @&lt;mã kỳ&gt; vào dòng vé</div>")
        o_kq += "<div>" + dong + "</div>"
        p.append("<tr><td>" + e(ngay_viet(v["ngay_mua"], kem_thu=False)) + "</td><td>" + o_ve
                 + "</td><td>" + o_ky + "</td><td>" + o_kq + "</td></tr>")
    p.append("</tbody></table></div></div>")

    if loi:
        p.append('<div class="canh"><strong>Vài dòng trong so-ve.txt chưa đọc được:</strong><ul>'
                 + "".join("<li>" + e(x) + "</li>" for x in loi) + "</ul></div>")
    return chr(10).join(p)


# ---------- Bộ số gợi ý ----------

def khoi_goi_so():
    f = THU_MUC_BAO_CAO / "goi-so.json"
    if not f.exists():
        return ""
    try:
        with open(f, "r", encoding="utf-8") as fh:
            d = json.load(fh)
    except (json.JSONDecodeError, OSError):
        return ""
    sp = d.get("san_pham") or []
    if not sp:
        return ""

    p = ['<h2 id="goi-so">Bộ số gợi ý &mdash; ' + e(ngay_viet(d.get("ngay"))) + "</h2>"]
    p.append('<div class="mo">' + str(d.get("so_bo", 0))
             + " bộ cho mỗi cách chọn số. Bấm vào một bộ là chép được, dán thẳng vào "
             + "<code>ve-cua-chi.txt</code>. Sang ngày mới thì ra bộ khác.</div>")
    p.append('<div class="canh" style="margin:14px 0">Mấy bộ số này <strong>không dễ '
             "trúng hơn</strong> bộ chị tự nghĩ. Bảng kiểm thử ngay bên dưới cho thấy "
             "cả 9 cách đều lỗ 78&ndash;92%, kể cả bốc bừa. Đây là công cụ đỡ phải ngồi "
             "nghĩ số, không phải công cụ dự đoán.</div>")

    for s in sp:
        ma = s.get("ma")
        p.append('<h3 style="margin-top:24px">' + e(s.get("ten")) + " &middot; "
                 + e(s.get("lich")) + "</h3>")
        if s.get("ghi_chu"):
            p.append('<div class="mo" style="margin-bottom:8px">' + e(s["ghi_chu"]) + "</div>")
        p.append('<div class="luoi luoi-goi">')
        for cl in s.get("chien_luoc", []):
            p.append('<div class="the">')
            p.append("<div><strong>" + e(cl.get("ten")) + "</strong></div>")
            p.append('<div class="mo" style="margin-bottom:8px">' + e(cl.get("mo_ta")) + "</div>")
            for b in cl.get("bo", []):
                so = b.get("so", [])
                db = b.get("so_db")
                chep = ma + ": " + " ".join(str(x) for x in so)
                if db is not None:
                    chep += " | " + str(db)
                chep += "   # gợi ý " + cl.get("ten", "") + " " + ngay_viet(d.get("ngay"), kem_thu=False)
                p.append('<div class="bo-so" data-chep="' + e(chep) + '" title="Bấm để chép">'
                         + day_bi(so, db) + "</div>")
            p.append("</div>")
        p.append("</div>")
    return "\n".join(p)


def khoi_xac_suat():
    """Xác suất trúng của MỘT bộ số. Tính thẳng từ tổ hợp, không phải ước lượng."""
    C = math.comb

    def n(x):
        return format(x, ",").replace(",", ".")

    def hang(ten, cach, tong):
        return ("<tr><td>" + e(ten) + '</td><td class="so">1 trên <strong>'
                + n(round(tong / cach)) + "</strong></td>"
                + '<td class="so">' + format(cach / tong * 100, ".7f").rstrip("0").rstrip(".")
                + "%</td></tr>")

    sp = []

    # Power 6/55
    T = C(55, 6)
    d = [("Jackpot 1 — trùng 6 số", 1),
         ("Jackpot 2 — trùng 5 số + số đặc biệt", C(6, 5)),
         ("Giải nhất — trùng 5 số", C(6, 5) * 48),
         ("Giải nhì — trùng 4 số", C(6, 4) * C(49, 2)),
         ("Giải ba — trùng 3 số", C(6, 3) * C(49, 3))]
    sp.append(("Power 6/55", "chọn 6 số trong 55 &middot; " + n(T) + " bộ khác nhau",
               d, sum(x for _, x in d), T, "Có giải bất kỳ"))

    # Mega 6/45
    T = C(45, 6)
    d = [("Jackpot — trùng 6 số", 1),
         ("Giải nhất — trùng 5 số", C(6, 5) * C(39, 1)),
         ("Giải nhì — trùng 4 số", C(6, 4) * C(39, 2)),
         ("Giải ba — trùng 3 số", C(6, 3) * C(39, 3))]
    sp.append(("Mega 6/45", "chọn 6 số trong 45 &middot; " + n(T) + " bộ khác nhau",
               d, sum(x for _, x in d), T, "Có giải bất kỳ"))

    # Lotto 5/35 — chỉ nói xác suất KHỚP SỐ, vì cơ cấu giải không có nguồn công khai
    T = C(35, 5)
    d = [("Trùng 5 số chính + số đặc biệt", T / (T * 12) * T),
         ("Trùng 5 số chính", 1),
         ("Trùng 4 số chính", C(5, 4) * C(30, 1)),
         ("Trùng 3 số chính", C(5, 3) * C(30, 2))]
    sp.append(("Lotto 5/35", "chọn 5 số trong 35 + 1 số đặc biệt trong 12",
               d, 1 + C(5, 4) * C(30, 1) + C(5, 3) * C(30, 2), T, "Trùng từ 3 số trở lên"))

    # Keno bộ 10 số
    T = C(80, 20)
    d = [("Trùng " + str(k) + "/10 số", C(10, k) * C(70, 20 - k)) for k in range(10, 4, -1)]
    sp.append(("Keno — bộ 10 số", "mỗi kỳ quay 20 số trong 80", d, None, T, None))

    p = ['<h2 id="xac-suat">Xác suất trúng của một bộ số</h2>']
    p.append('<div class="mo">Tính thẳng từ tổ hợp, không phải ước lượng. '
             "Con số này đúng cho <strong>mọi</strong> bộ số &mdash; bộ gợi ý, bộ chị tự nghĩ, "
             "hay bộ bốc bừa đều y hệt nhau.</div>")
    p.append('<div class="luoi luoi-bd">')
    for ten, mo, d, co_giai, T, nhan_tong in sp:
        p.append('<div class="the"><div class="ten-bd">' + e(ten) + "</div>")
        p.append('<div class="mo" style="margin-bottom:6px">' + mo + "</div>")
        p.append('<div class="cuon"><table><thead><tr><th>Mức trúng</th>'
                 '<th class="so">Cơ hội</th><th class="so">Tỷ lệ</th></tr></thead><tbody>')
        for ten_h, cach in d:
            p.append(hang(ten_h, cach, T))
        if co_giai:
            p.append('<tr style="font-weight:600"><td>' + e(nhan_tong)
                     + '</td><td class="so">1 trên <strong>' + n(round(T / co_giai))
                     + "</strong></td>" + '<td class="so">'
                     + format(co_giai / T * 100, ".3f") + "%</td></tr>")
        p.append("</tbody></table></div></div>")
    p.append("</div>")

    p.append('<div class="the"><div class="ten-bd">Mua mỗi kỳ thì bao lâu mới trúng?</div>'
             '<div class="cuon" style="margin-top:8px"><table><thead><tr><th></th>'
             '<th class="so">Jackpot</th><th class="so">Giải bất kỳ</th>'
             "</tr></thead><tbody>"
             '<tr><td>Power 6/55 <span class="mo">(156 kỳ/năm)</span></td>'
             '<td class="so">185.831 năm</td><td class="so">2,1 lần/năm</td></tr>'
             '<tr><td>Mega 6/45 <span class="mo">(156 kỳ/năm)</span></td>'
             '<td class="so">52.212 năm</td><td class="so">3,7 lần/năm</td></tr>'
             "</tbody></table></div>"
             '<div class="mo" style="margin-top:8px">Mua mỗi kỳ một tờ, tính trung bình. '
             "Mua 10 bộ thì cơ hội nhân 10 &mdash; và tiền bỏ ra cũng nhân 10, nên giá trị "
             "kỳ vọng mỗi đồng vẫn y nguyên.</div></div>")

    p.append('<div class="canh">Cơ cấu giải của Lotto 5/35 theo số con trùng không có nguồn '
             "công khai nào nói rõ, nên bảng trên chỉ ghi xác suất <strong>khớp số</strong>, "
             "không đặt tên hạng giải. Power 6/55 và Mega 6/45 thì có bảng giải đầy đủ.</div>")
    return chr(10).join(p)


# ---------- Bàn kiểm thử chiến lược ----------

def khoi_kiem_thu():
    f = THU_MUC_BAO_CAO / "kiem-thu.json"
    if not f.exists():
        return ""
    try:
        with open(f, "r", encoding="utf-8") as fh:
            d = json.load(fh)
    except (json.JSONDecodeError, OSError):
        return ""

    kq = d.get("ket_qua") or []
    if not kq:
        return ""
    so_ve = d.get("so_ve_moi_chien_luoc", 0)
    xs = d.get("xac_suat", {})
    kv_ba = so_ve * xs.get("ba", 0)
    kv_nhi = so_ve * xs.get("nhi", 0)

    p = ['<h2 id="kiem-thu">Có chiến lược chọn số nào ăn được không?</h2>']
    p.append('<div class="mo">Kiểm thử ' + str(len(kq)) + " cách chọn số trên "
             + str(d.get("so_ky_cham", 0)) + " kỳ Power 6/55 ("
             + e(ngay_viet(d.get("tu_ngay"), kem_thu=False)) + " &rarr; "
             + e(ngay_viet(d.get("den_ngay"), kem_thu=False)) + "), mỗi chiến lược mua "
             + format(so_ve, ",").replace(",", ".") + " tờ. "
             + "Mỗi chiến lược chỉ được xem dữ liệu trước kỳ nó đoán.</div>")

    p.append('<div class="the"><div class="cuon"><table class="sapxep"><thead><tr>'
             '<th class="sx" data-chieu="">Cách chọn số</th>'
             '<th class="sx so" data-chieu="">Giải ba</th>'
             '<th class="sx so" data-chieu="">Giải nhì</th>'
             '<th class="sx so" data-chieu="">Nhất trở lên</th>'
             '<th class="sx so" data-chieu="">ROI chấm đúng luật</th>'
             '<th class="sx so" data-chieu="">ROI chấm kiểu repo gốc</th>'
             "</tr></thead><tbody>")
    for r in kq:
        g = r.get("giai", {})
        lon = g.get("nhat", 0) + g.get("jackpot1", 0) + g.get("jackpot2", 0)
        sai = r["roi_repo"] > 0
        p.append(
            "<tr>"
            + '<td data-v="' + e(r["ten"]) + '"><strong>' + e(r["ten"])
            + '</strong><div class="mo">' + e(r.get("mo_ta", "")) + "</div></td>"
            + '<td class="so" data-v="' + str(g.get("ba", 0)) + '">' + str(g.get("ba", 0)) + "</td>"
            + '<td class="so" data-v="' + str(g.get("nhi", 0)) + '">' + str(g.get("nhi", 0)) + "</td>"
            + '<td class="so" data-v="' + str(lon) + '">' + str(lon) + "</td>"
            + '<td class="so" data-v="' + format(r["roi_dung"], ".1f") + '">'
            + format(r["roi_dung"], "+.1f") + "%</td>"
            + '<td class="so" data-v="' + format(r["roi_repo"], ".1f") + '">'
            + '<span class="nhan-nho' + (" sai" if sai else "") + '">'
            + format(r["roi_repo"], "+.1f") + "%</span></td>"
            + "</tr>"
        )
    p.append("</tbody></table></div></div>")

    p.append('<div class="the"><div class="ten-bd">Nếu bộ quay công bằng thì phải ra bao nhiêu</div>'
             '<div class="mo" style="margin-top:8px">Với ' + format(so_ve, ",").replace(",", ".")
             + " tờ, lý thuyết xác suất nói mọi cách chọn số đều phải ra quanh mức "
             + "<strong>" + format(kv_ba, ".0f") + " tờ giải ba</strong> và <strong>"
             + format(kv_nhi, ".0f") + " tờ giải nhì</strong>. Nhìn cột giải ba trong bảng: "
             + "tất cả đều bám quanh mức đó.</div>"
             + '<div class="mo" style="margin-top:8px">Đây không phải kết quả may rủi mà là toán. '
             + "Với bộ quay công bằng, <strong>mọi bộ 6 số đều có xác suất trúng y hệt nhau</strong>, "
             + "nên giá trị kỳ vọng của mọi chiến lược bằng nhau: khoảng <strong>"
             + format(d.get("gia_tri_ky_vong", 0), ",.0f").replace(",", ".")
             + "đ cho mỗi tờ vé " + format(d.get("gia_ve", 10000), ",").replace(",", ".")
             + "đ</strong>. Chênh lệch trong bảng là dao động, không phải kỹ năng.</div></div>")

    p.append('<div class="canh"><strong>Cột cuối cùng mới là chuyện đáng nói.</strong> '
             "Repo gốc mà bộ công cụ này lấy dữ liệu có sẵn phần dự đoán, và "
             '<a href="https://vietvudanh.github.io/vietlott-data/" target="_blank" '
             'rel="noopener">trang web của nó</a> công bố các chiến lược lãi tới +3.647%. '
             "Cột cuối là kết quả khi chấm <strong>cùng bộ vé này</strong> bằng đúng cách chấm của họ "
             "&mdash; con số nhảy từ khoảng &minus;80% lên hơn +4.000%. "
             "Hai lỗi: họ so vé với cả 7 số (6 số chính + số đặc biệt) nên "
             '"trùng 4 chính + số đặc biệt" bị đếm thành "trùng 5"; rồi bảng giá của họ trả '
             "5 tỷ cho mỗi tờ trùng 5, trong khi trùng 5 số chính chỉ là giải nhất 40 triệu. "
             "Kết quả: mỗi tờ giải nhì 500.000đ được ghi sổ 5 tỷ.</div>")
    return "\n".join(p)


# ---------- Biểu đồ của 1 sản phẩm ----------

def khoi_bieu_do(ma, tk):
    cfg = SAN_PHAM[ma]
    tong_ky = tk["tong_ky"] or 1
    n_chinh, n_max = cfg["so_chinh"], cfg["max_chinh"]
    ra = ['<div class="luoi luoi-bd">']

    # 1. Tần suất từng số + đường kỳ vọng
    lan = [r["lan"] for r in tk["bang"]]
    kv = tong_ky * n_chinh / n_max
    lech = max(abs(x - kv) for x in lan) / kv * 100 if kv else 0
    ra.append(khung(
        "Mỗi số đã về bao nhiêu lần",
        cot(lan, [str(r["so"]) for r in tk["bang"]], ky_vong=kv, nhan_moi=5, don_vi=" lần"),
        "Nếu quay hoàn toàn ngẫu nhiên, mỗi số về khoảng <strong>" + format(kv, ".0f")
        + " lần</strong>. Cột cao thấp lệch nhau là chuyện bình thường của ngẫu nhiên — "
        "số lệch nhiều nhất ở đây cách mức kỳ vọng " + format(lech, ".0f") + "%.",
        co_ky_vong=True))

    # 2. Số kỳ chưa về
    gan = [r["gan"] for r in tk["bang"]]
    ra.append(khung(
        "Mỗi số đã bao nhiêu kỳ chưa về",
        cot(gan, [str(r["so"]) for r in tk["bang"]], mau="var(--gan)", nhan_moi=5, don_vi=" kỳ"),
        "Cột càng cao là càng lâu chưa thấy. Điều này <strong>không</strong> làm số đó dễ về hơn "
        "ở kỳ sau — quả cầu không nhớ kỳ trước."))

    # 3. Bao nhiêu số chẵn mỗi kỳ, so với kỳ vọng
    chan = tk["chan_moi_ky"]
    if chan:
        so_chan_co = n_max // 2
        so_le_co = n_max - so_chan_co
        gt, kvs, nh = [], [], []
        for k in range(0, n_chinh + 1):
            gt.append(chan.get(k, 0))
            nh.append(str(k))
            try:
                xs = (math.comb(so_chan_co, k) * math.comb(so_le_co, n_chinh - k)
                      / math.comb(n_max, n_chinh))
            except ValueError:
                xs = 0
            kvs.append(tong_ky * xs)
        ra.append(khung(
            "Mỗi kỳ có bao nhiêu số chẵn",
            cot(gt, nh, mau="var(--lanh)", nhan_moi=1, don_vi=" kỳ",
                tieu_de_cot=lambda i, v, _k=kvs, _n=nh: (_n[i] + " số chẵn: " + str(v)
                                                         + " kỳ (kỳ vọng " + format(_k[i], ".0f") + ")")),
            "Thực tế bám rất sát lý thuyết xác suất: hay gặp nhất là "
            + str(max(range(len(kvs)), key=lambda i: kvs[i]))
            + " số chẵn. Đây là dấu hiệu bộ quay chạy sòng phẳng."))

    # 4. Tổng các số mỗi kỳ
    tong = tk["tong_moi_ky"]
    if tong:
        nho, lon = min(tong), max(tong)
        so_o = 24
        buoc = max(1, math.ceil((lon - nho + 1) / so_o))
        thung, nhan_t = [], []
        v = nho
        while v <= lon:
            thung.append(sum(tong.get(x, 0) for x in range(v, v + buoc)))
            nhan_t.append(str(v))
            v += buoc
        tb = sum(k * c for k, c in tong.items()) / tong.total()
        ra.append(khung(
            "Tổng các số trong một kỳ",
            cot(thung, nhan_t, mau="var(--xanh)", nhan_moi=4, don_vi=" kỳ"),
            "Cộng cả " + str(n_chinh) + " số của mỗi kỳ lại. Dồn thành hình chuông quanh mức "
            "trung bình <strong>" + format(tb, ".0f") + "</strong> — tổng quá thấp hay quá cao "
            "đều hiếm, vì phải trúng toàn số bé hoặc toàn số lớn."))

    ra.append("</div>")
    return "".join(ra)


# ---------- Khối 1 sản phẩm ----------

def khoi_san_pham(ma, rows):
    cfg = SAN_PHAM[ma]
    tk = thong_ke(ma, rows)
    p = ['<h2 id="' + ma + '">' + e(cfg["ten"]) + "</h2>"]
    p.append('<div class="mo">' + e(cfg["lich"]) + " &middot; " + str(tk["tong_ky"])
             + " kỳ &middot; " + e(ngay_viet(tk["tu_ngay"], kem_thu=False)) + " &rarr; "
             + e(ngay_viet(tk["den_ngay"], kem_thu=False)) + "</div>")
    p.append(dong_chat_luong(rows))

    # --- kỳ gần nhất
    so_ky_hien = 8 if ma == "keno" else 10
    p.append("<h3>Kết quả " + str(so_ky_hien) + " kỳ gần nhất</h3>")
    p.append('<div class="the"><div class="cuon"><table><thead><tr>'
             "<th>Ngày</th><th>Kỳ</th><th>Kết quả</th></tr></thead><tbody>")
    for ky in reversed(rows[-so_ky_hien:]):
        chinh, db = tach_so(ky, ma)
        p.append("<tr><td>" + e(ngay_viet(ky.get("date"))) + "</td><td>" + e(ky.get("id"))
                 + "</td><td>" + day_bi(chinh, db) + "</td></tr>")
    p.append("</tbody></table></div></div>")

    # --- nóng / lạnh / gan
    theo_lan = sorted(tk["bang"], key=lambda r: (-r["lan"], r["so"]))
    theo_gan = sorted(tk["bang"], key=lambda r: (-r["gan"], r["so"]))
    n = 6
    p.append('<div class="luoi">')
    p.append('<div class="the"><h3 style="margin-top:0">Về nhiều nhất</h3><div>'
             + "".join(bi(r["so"]) for r in theo_lan[:n]) + '</div><div class="mo">'
             + ", ".join(str(r["lan"]) + " lần" for r in theo_lan[:n]) + "</div></div>")
    p.append('<div class="the"><h3 style="margin-top:0">Về ít nhất</h3><div>'
             + "".join(bi(r["so"], "lanh") for r in theo_lan[-n:][::-1]) + '</div><div class="mo">'
             + ", ".join(str(r["lan"]) + " lần" for r in theo_lan[-n:][::-1]) + "</div></div>")
    p.append('<div class="the"><h3 style="margin-top:0">Lâu chưa về nhất</h3><div>'
             + "".join(bi(r["so"], "gan") for r in theo_gan[:n]) + '</div><div class="mo">'
             + ", ".join(str(r["gan"]) + " kỳ" for r in theo_gan[:n]) + "</div></div>")
    p.append("</div>")

    # --- biểu đồ
    p.append("<h3>Nhìn bằng biểu đồ</h3>")
    p.append(khoi_bieu_do(ma, tk))

    # --- bảng đầy đủ
    max_lan = max((r["lan"] for r in tk["bang"]), default=1) or 1
    p.append("<h3>Bảng đầy đủ &mdash; bấm tiêu đề cột để sắp xếp</h3>")
    p.append('<div class="the"><div class="cuon"><table class="sapxep"><thead><tr>'
             '<th class="sx so" data-chieu="">Số</th>'
             '<th class="sx so" data-chieu="">Số lần về</th>'
             '<th class="sx so" data-chieu="">Tỷ lệ</th>'
             "<th>Mức độ</th>"
             '<th class="sx" data-chieu="">Về gần nhất</th>'
             '<th class="sx so" data-chieu="">Số kỳ chưa về</th>'
             "</tr></thead><tbody>")
    for r in tk["bang"]:
        rong = max(2, round(r["lan"] / max_lan * 100))
        p.append(
            "<tr>"
            + '<td class="so" data-v="' + str(r["so"]) + '">' + bi(r["so"], "nho") + "</td>"
            + '<td class="so" data-v="' + str(r["lan"]) + '">' + str(r["lan"]) + "</td>"
            + '<td class="so" data-v="' + str(round(r["ty_le"], 2)) + '">'
            + format(r["ty_le"], ".2f") + "%</td>"
            + '<td><div class="thanh" style="width:' + str(rong) + '%"></div></td>'
            + '<td data-v="' + e(r["ngay_cuoi"]) + '">' + e(ngay_viet(r["ngay_cuoi"], kem_thu=False)) + "</td>"
            + '<td class="so" data-v="' + str(r["gan"]) + '">' + str(r["gan"]) + "</td>"
            + "</tr>"
        )
    p.append("</tbody></table></div></div>")

    # --- số đặc biệt
    if tk["bang_db"]:
        top_db = sorted(tk["bang_db"], key=lambda r: (-r["lan"], r["so"]))[:8]
        p.append("<h3>Số đặc biệt &mdash; hay về nhất</h3>")
        p.append('<div class="the"><div>' + "".join(bi(r["so"], "db") for r in top_db)
                 + '</div><div class="mo">' + ", ".join(str(r["lan"]) + " lần" for r in top_db)
                 + "</div></div>")

    # --- cặp số
    if tk["cap_hay_gap"]:
        p.append("<h3>Cặp số hay về cùng nhau</h3>")
        p.append('<div class="the"><div class="cuon"><table><thead><tr>'
                 "<th>Cặp</th><th class='so'>Số kỳ về cùng</th><th class='so'>Tỷ lệ</th>"
                 "</tr></thead><tbody>")
        for (a, b), lan in tk["cap_hay_gap"]:
            p.append("<tr><td>" + bi(a, "nho") + bi(b, "nho") + '</td><td class="so">'
                     + str(lan) + '</td><td class="so">'
                     + format(lan / tk["tong_ky"] * 100, ".2f") + "%</td></tr>")
        p.append("</tbody></table></div></div>")

    return "\n".join(p)


def khoi_gon(ma, rows):
    """Sản phẩm không phân tích tần suất (Max 3D / 3D Pro / Bingo18): chỉ nêu kỳ gần nhất."""
    cfg = SAN_PHAM[ma]
    if not rows:
        return ""
    ky = rows[-1]
    kq = ky.get("result")
    if isinstance(kq, dict):
        noi_dung = "".join(
            "<div style='margin:4px 0'><span class='mo'>" + e(k) + ":</span> "
            + "".join('<span class="bi nho">' + e(x) + "</span>" for x in v) + "</div>"
            for k, v in kq.items()
        )
    else:
        chinh, db = tach_so(ky, ma)
        noi_dung = day_bi(chinh, db)
    return ('<div class="the"><div><strong>' + e(cfg["ten"]) + '</strong> <span class="mo">&middot; '
            + format(len(rows), ",").replace(",", ".") + " kỳ</span></div>"
            + '<div class="mo">' + e(ngay_viet(ky.get("date"))) + " &middot; kỳ " + e(ky.get("id"))
            + "</div><div style='margin-top:6px'>" + noi_dung + "</div>"
            + dong_chat_luong(rows) + "</div>")


def main(che_do_web=False):
    """che_do_web=True: bỏ phần 'Vé của chị' và ghi ra web/index.html để đăng lên mạng."""
    print()
    print("  Đang đọc dữ liệu và dựng báo cáo"
          + (" (bản công khai, không kèm vé của chị)..." if che_do_web else "..."))
    du_lieu = {}
    for ma in SAN_PHAM:
        du_lieu[ma] = doc_du_lieu(ma)

    day_du = [ma for ma, c in SAN_PHAM.items() if c["phan_tich_day_du"] and du_lieu.get(ma)]
    gon = [ma for ma, c in SAN_PHAM.items() if not c["phan_tich_day_du"] and du_lieu.get(ma)]

    bay_gio = datetime.now().strftime("%H:%M ngày %d/%m/%Y")
    p = []
    p.append('<!doctype html><html lang="vi"><head><meta charset="utf-8">')
    p.append('<meta name="viewport" content="width=device-width,initial-scale=1">')
    p.append("<title>Thống kê Vietlott</title><style>" + CSS + "</style></head><body><div class='bao'>")
    p.append("<header><h1>Thống kê Vietlott</h1>")
    p.append('<div class="mo">Dựng lúc ' + e(bay_gio) + " &middot; dữ liệu lấy từ vietlott.vn</div></header>")

    p.append("<nav>")
    if doc_ve():
        p.append('<a href="#ve">Vé của chị</a>')
    so_ve_html = khoi_so_ve()
    if so_ve_html:
        p.append('<a href="#so-ve">Sổ vé</a>')
    for ma in day_du:
        p.append('<a href="#' + ma + '">' + e(SAN_PHAM[ma]["ten"]) + "</a>")
    if (THU_MUC_BAO_CAO / "goi-so.json").exists():
        p.append('<a href="#goi-so">Bộ số gợi ý</a>')
    p.append('<a href="#xac-suat">Xác suất trúng</a>')
    if (THU_MUC_BAO_CAO / "kiem-thu.json").exists():
        p.append('<a href="#kiem-thu">Chiến lược có ăn không?</a>')
    if gon:
        p.append('<a href="#khac">Sản phẩm khác</a>')
    p.append("</nav>")

    # Cả hai mục vé lên web — chị chọn công khai (24/08/2026)
    p.append(khoi_ve(du_lieu))
    # Sổ vé lên cả bản web — chị chọn công khai (24/08/2026)
    p.append(so_ve_html)

    for ma in day_du:
        p.append(khoi_san_pham(ma, du_lieu[ma]))

    p.append(khoi_goi_so())
    p.append(khoi_xac_suat())
    p.append(khoi_kiem_thu())

    if gon:
        p.append('<h2 id="khac">Sản phẩm khác &mdash; kỳ gần nhất</h2>')
        p.append('<div class="luoi">')
        for ma in gon:
            p.append(khoi_gon(ma, du_lieu[ma]))
        p.append("</div>")

    p.append('<div class="canh"><strong>Đọc bảng này cho đúng.</strong> '
             "Mỗi kỳ quay là độc lập: quả cầu không nhớ kỳ trước. Một con số "
             '"lâu chưa về" không vì thế mà dễ về hơn ở kỳ sau, và số "về nhiều" '
             "cũng không nóng hơn. Bảng ở đây để nhìn lại lịch sử cho vui và để dò vé, "
             "không phải công cụ dự đoán. Chơi trong khoản tiền chị sẵn sàng mất.</div>")

    p.append("<footer>Dữ liệu thô nằm trong thư mục <code>data/</code>, định dạng .jsonl. "
             "Bộ crawl gốc: dự án nguồn mở vietlott-data (giấy phép MIT). "
             "File báo cáo này tự chứa &mdash; copy đi đâu cũng mở được, không cần mạng.</footer>")
    p.append("</div><script>" + JS + "</script></body></html>")

    if che_do_web:
        thu_muc = THU_MUC_BAO_CAO.parent / "web"
        thu_muc.mkdir(parents=True, exist_ok=True)
        dich = thu_muc / "index.html"
    else:
        THU_MUC_BAO_CAO.mkdir(parents=True, exist_ok=True)
        dich = THU_MUC_BAO_CAO / "thong-ke-vietlott.html"
    with open(dich, "w", encoding="utf-8") as f:
        f.write("\n".join(x for x in p if x))

    kb = dich.stat().st_size / 1024
    print("  Xong: " + str(dich))
    print("  Kích thước " + format(kb, ".0f") + " KB")
    print()
    return str(dich)


if __name__ == "__main__":
    main(che_do_web=(len(sys.argv) > 1 and sys.argv[1].lower() in ("web", "--web")))
