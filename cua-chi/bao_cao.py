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
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bieu_do import CSS_BIEU_DO, cot, khung  # noqa: E402
from goi_so import KHUON as KHUON_NHAP  # noqa: E402
from thu_vien import (  # noqa: E402
    SAN_PHAM, THU_MUC_BAO_CAO, bat_utf8, doc_du_lieu, doc_ve, do_mot_ve,
    kiem_lo, ngay_viet, tach_so, thong_ke,
)

bat_utf8()

CSS = """
:root{--nen:#f6f7f9;--the:#fff;--chu:#1b1f26;--mo:#6b7280;--vien:#e3e6ea;
--nhan:#c81e1e;--nhandiu:#fdecec;--lanh:#1d4ed8;--lanhdiu:#e8eefc;
--gan:#b45309;--gandiu:#fdf1e0;--xanh:#047857;--xanhdiu:#e6f4ef;--chinh:#2563eb}
@media (prefers-color-scheme:dark){:root{--nen:#14161a;--the:#1c1f25;--chu:#e8eaed;
--mo:#9aa1ab;--vien:#2b2f36;--nhandiu:#3a1c1c;--nhan:#f87171;--lanhdiu:#1a2436;
--lanh:#93b4fb;--gandiu:#33260f;--gan:#f0b45f;--xanhdiu:#12291f;--xanh:#5ad6a4;--chinh:#3b82f6}}
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

/* ---------- khối nhập vé ---------- */
/* Trước 30/08/2026 khối này không có lấy một dòng CSS nào — trình duyệt vẽ bằng
   kiểu mặc định nên trông thô hẳn so với phần còn lại của trang. Class .an cũng
   chưa có, nên lệnh giấu ô "Số đặc biệt" của Power 6/55 không hề chạy. */
.an{display:none !important}
.nhap-ve input,.nhap-ve select{font:inherit;width:100%;padding:9px 11px;border-radius:8px;
border:1px solid var(--vien);background:var(--nen);color:var(--chu);
transition:border-color .12s,box-shadow .12s}
.nhap-ve input::placeholder{color:var(--mo);opacity:.75}
.nhap-ve input:focus,.nhap-ve select:focus{outline:none;border-color:var(--chinh);
box-shadow:0 0 0 3px rgba(37,99,235,.22)}
.luoi-nv{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}
.o-nv{display:flex;flex-direction:column;gap:5px;min-width:0}
.o-nv>.nhan{font-size:11px;text-transform:uppercase;letter-spacing:.5px;
color:var(--mo);font-weight:650}
.rong2{grid-column:span 2}
.nut{font:inherit;font-weight:650;padding:10px 22px;border-radius:8px;
border:1px solid transparent;background:var(--chinh);color:#fff;cursor:pointer;
transition:filter .12s}
.nut:hover{filter:brightness(1.08)}
.nut:disabled{opacity:.55;cursor:progress}
.nut.phu{background:transparent;color:var(--chu);border-color:var(--vien);
font-weight:600;padding:9px 14px}
.nut.phu:hover{border-color:var(--mo);filter:none}
.nut-xoa{font:inherit;font-size:12.5px;font-weight:600;padding:4px 11px;border-radius:6px;
border:1px solid var(--vien);background:transparent;color:var(--mo);cursor:pointer}
.nut-xoa:hover{border-color:var(--nhan);color:var(--nhan);background:var(--nhandiu)}
.nut-xoa:disabled{opacity:.5;cursor:default}
.hang-nut{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-top:14px;
padding-top:14px;border-top:1px solid var(--vien)}
.nv-bao{font-size:13px;color:var(--mo)}
.nv-bao.ok{color:var(--xanh);font-weight:600}
.nv-bao.loi{color:var(--nhan);font-weight:600}
.pad{border:1px solid var(--vien);border-radius:10px;padding:12px;
background:var(--nen);margin-top:12px}
.pad-dau{display:flex;align-items:center;justify-content:space-between;gap:10px;
margin-bottom:10px}
.pad-ten{font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:var(--mo);
font-weight:650}
.dem{font-variant-numeric:tabular-nums;font-weight:700;font-size:13px;padding:2px 10px;
border-radius:20px;background:var(--the);border:1px solid var(--vien);color:var(--mo)}
.dem.du{background:var(--xanhdiu);color:var(--xanh);border-color:var(--xanh)}
.o-so{display:grid;grid-template-columns:repeat(auto-fill,minmax(40px,1fr));gap:6px}
.vien-so{font:inherit;font-weight:650;font-size:13.5px;height:38px;border-radius:8px;
border:1px solid var(--vien);background:var(--the);color:var(--chu);cursor:pointer;
font-variant-numeric:tabular-nums;transition:background .1s,border-color .1s,color .1s}
.vien-so:hover{border-color:var(--chinh)}
.vien-so.chon{background:var(--chinh);border-color:var(--chinh);color:#fff}
.vien-so:disabled{opacity:.32;cursor:not-allowed}
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
    dienVaoO(t);
  });
});

// ----- Nhap ve ngay tren trang -----
var KHUON = __KHUON_JSON__;

function o(id){ return document.getElementById(id); }

// Cac so dang duoc chon. Go tay va bam bang so luon khop nhau qua bien nay.
var CHON = [];

function viDuSo(k){
  var con = [], ra = [];
  for(var i = 1; i <= k.dai_chon; i++) con.push(i);
  for(var j = 0; j < k.so_chon; j++)
    ra.push(con.splice(Math.floor(con.length * (j + 1) / (k.so_chon + 1)), 1)[0]);
  return ra.sort(function(x, y){ return x - y; }).join(' ');
}

function veBangSo(){
  var sp = o('nv-sp'), khung = o('nv-oso');
  if(!sp || !khung) return;
  var k = KHUON[sp.value] || {};
  var ten = o('nv-padten');
  if(ten) ten.textContent = 'Chọn ' + k.so_chon + ' số  (1-' + k.dai_chon + ')';
  khung.innerHTML = '';
  for(var i = 1; i <= k.dai_chon; i++){
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'vien-so'; b.textContent = i; b.dataset.v = i;
    b.addEventListener('click', bamVienSo);
    khung.appendChild(b);
  }
}

function bamVienSo(e){
  var k = KHUON[o('nv-sp').value] || {};
  var v = +e.currentTarget.dataset.v, i = CHON.indexOf(v);
  if(i >= 0) CHON.splice(i, 1);
  else if(CHON.length < k.so_chon) CHON.push(v);
  else return;
  dongBoSo(false);
}

// tuO = true  : doc so tu o go tay, KHONG ghi de lai o (con de chi go tiep)
// tuO = false : doc so tu CHON, ghi nguoc ra o
function dongBoSo(tuO){
  var sp = o('nv-sp'); if(!sp) return;
  var k = KHUON[sp.value] || {};
  if(tuO){
    var raw = (o('nv-so').value.match(/[0-9]+/g) || []).map(Number);
    CHON = raw.filter(function(v, i, a){
      return v >= 1 && v <= k.dai_chon && a.indexOf(v) === i;
    }).slice(0, k.so_chon);
  }
  CHON.sort(function(a, b){ return a - b; });
  var du = CHON.length === k.so_chon, khung = o('nv-oso');
  if(khung) khung.querySelectorAll('.vien-so').forEach(function(b){
    var c = CHON.indexOf(+b.dataset.v) >= 0;
    b.classList.toggle('chon', c);
    b.disabled = (!c && du);
  });
  var dm = o('nv-dem');
  if(dm){ dm.textContent = CHON.length + '/' + k.so_chon; dm.classList.toggle('du', du); }
  if(!tuO) o('nv-so').value = CHON.join(' ');
}

function capNhatODacBiet(){
  var sp = o('nv-sp'); if(!sp) return;
  var k = KHUON[sp.value] || {};
  // Power 6/55 va Mega 6/45 khong cho nguoi choi chon so dac biet - Vietlott tu quay.
  var oDb = document.querySelector('.nv-db');
  if(oDb) oDb.classList.toggle('an', !k.db_dai);
  var i = o('nv-so');
  if(i) i.placeholder = 'ví dụ  ' + viDuSo(k);
  var d = o('nv-db');
  if(d && k.db_dai) d.placeholder = '1-' + k.db_dai;
  veBangSo();
  dongBoSo(true);
}

// Bam vao bo so goi y -> tu dien vao o nhap
function dienVaoO(chuoi){
  if(!o('nv-sp')) return;
  var m = /^([a-z_0-9]+):\\s*([\\d\\s]+?)(?:\\|\\s*(\\d+))?\\s*(?:#\\s*(.*))?$/.exec(chuoi.trim());
  if(!m) return;
  var sp = o('nv-sp');
  if([].some.call(sp.options, function(x){ return x.value === m[1]; })) sp.value = m[1];
  capNhatODacBiet();
  o('nv-so').value = m[2].trim();
  dongBoSo(true);
  if(m[3]) o('nv-db').value = m[3];
  if(m[4]) o('nv-ghi').value = m[4].trim();
  var t = o('nv-gui');
  if(t) t.scrollIntoView({behavior:'smooth', block:'center'});
}

(function(){
  var nut = o('nv-gui');
  if(!nut) return;
  var sp = o('nv-sp'), bao = o('nv-bao'), mk = o('nv-mk'), ngay = o('nv-ngay');
  sp.addEventListener('change', function(){
    o('nv-so').value = '';
    if(o('nv-db')) o('nv-db').value = '';
    CHON = [];
    capNhatODacBiet();
  });
  o('nv-so').addEventListener('input', function(){ dongBoSo(true); });
  var mopad = o('nv-mopad');
  if(mopad) mopad.addEventListener('click', function(){
    var dangAn = o('nv-pad').classList.toggle('an');
    mopad.textContent = dangAn ? 'Bảng số' : 'Đóng bảng';
    if(!dangAn) o('nv-pad').scrollIntoView({behavior:'smooth', block:'nearest'});
  });
  var xoahet = o('nv-xoahet');
  if(xoahet) xoahet.addEventListener('click', function(){
    CHON = []; dongBoSo(false); o('nv-so').focus();
  });
  capNhatODacBiet();
  try { mk.value = localStorage.getItem('vietlott_mk') || ''; } catch(e){}
  if(!ngay.value) ngay.value = new Date().toISOString().slice(0,10);

  function noi(t, lop){ bao.textContent = t; bao.className = 'nv-bao ' + (lop || ''); }

  nut.addEventListener('click', function(){
    var k = KHUON[sp.value] || {};
    var so = (o('nv-so').value || '').trim().replace(/[,;]+/g, ' ').replace(/\\s+/g, ' ');
    var mang = so ? so.split(' ') : [];
    if(mang.length !== k.so_chon){
      noi('Cần đúng ' + k.so_chon + ' số, đang có ' + mang.length + '.', 'loi'); return;
    }
    for(var i = 0; i < mang.length; i++){
      var v = parseInt(mang[i], 10);
      if(!(v >= 1 && v <= k.dai_chon)){
        noi('Số ' + mang[i] + ' ngoài dải 1-' + k.dai_chon + '.', 'loi'); return;
      }
    }
    var tap = {};
    for(var q = 0; q < mang.length; q++){
      if(tap[mang[q]]){ noi('Có số bị trùng.', 'loi'); return; }
      tap[mang[q]] = 1;
    }
    var db = (o('nv-db').value || '').trim();
    if(k.db_dai){
      var dv = parseInt(db, 10);
      if(!(dv >= 1 && dv <= k.db_dai)){
        noi('Số đặc biệt phải từ 1 đến ' + k.db_dai + '.', 'loi'); return;
      }
    }
    var matKhau = (mk.value || '').trim();
    if(!matKhau){ noi('Chưa nhập mật khẩu.', 'loi'); return; }

    var dong = ngay.value + ' | ' + sp.value + ': ' + so + (k.db_dai ? ' | ' + db : '');
    var gc = (o('nv-ghi').value || '').trim().replace(/[#|\\n\\r]/g, ' ');
    if(gc) dong += '   # ' + gc;

    nut.disabled = true; noi('Đang ghi...', '');
    fetch('/api/ghi-ve', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({matKhau: matKhau, dong: dong})
    }).then(function(r){
      return r.json().then(function(j){ return {ok: r.ok, ma: r.status, j: j}; });
    }).then(function(kq){
      if(kq.ok && kq.j.ok){
        try { localStorage.setItem('vietlott_mk', matKhau); } catch(e){}
        noi(kq.j.thong_bao || 'Đã ghi vào sổ.', 'ok');
        o('nv-so').value = ''; o('nv-db').value = ''; o('nv-ghi').value = '';
        CHON = []; dongBoSo(false);
      } else {
        noi(kq.j.loi || ('Lỗi ' + kq.ma), 'loi');
      }
    }).catch(function(){
      noi('Không gọi được máy chủ. Nhap ve chi chay tren trang vietlott-thongke.vercel.app, '
        + 'khong chay khi mo file HTML tu may.', 'loi');
    }).then(function(){ nut.disabled = false; });
  });
})();

// ----- Xoa mot to ve khoi so -----
document.querySelectorAll('.nut-xoa').forEach(function(nut){
  nut.addEventListener('click', function(){
    var dong = nut.dataset.dong || '';
    if(!dong) return;
    if(!confirm('Xoá tờ vé này khỏi sổ?   [ ' + dong + ' ]   Xoá rồi không lấy lại được.')) return;

    var mk = '';
    try { mk = localStorage.getItem('vietlott_mk') || ''; } catch(e){}
    if(!mk){
      mk = prompt('Nhập mật khẩu để xoá vé:') || '';
      if(!mk) return;
    }

    var cu = nut.textContent;
    nut.disabled = true; nut.textContent = 'Đang xoá...';
    fetch('/api/ghi-ve', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({viec: 'xoa', matKhau: mk, dong: dong})
    }).then(function(r){
      return r.json().then(function(j){ return {ok: r.ok, ma: r.status, j: j}; });
    }).then(function(kq){
      if(kq.ok && kq.j.ok){
        try { localStorage.setItem('vietlott_mk', mk); } catch(e){}
        var tr = nut.closest('tr');
        if(tr){ tr.style.opacity = '.35'; tr.style.textDecoration = 'line-through'; }
        nut.textContent = 'Đã xoá';
        alert(kq.j.thong_bao || 'Đã xoá khỏi sổ.');
      } else {
        nut.disabled = false; nut.textContent = cu;
        alert(kq.j.loi || ('Lỗi ' + kq.ma));
      }
    }).catch(function(){
      nut.disabled = false; nut.textContent = cu;
      alert('Không gọi được máy chủ. Xoa ve chi chay tren trang vietlott-thongke.vercel.app, '
        + 'khong chay khi mo file HTML tu may.');
    });
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
        from so_ve import GIA_VE, GIAI, FILE_SO, danh_gia
    except ImportError:
        return ""
    kq, tong, loi = ([], None, []) if not FILE_SO.exists() else danh_gia()

    def vnd(x):
        return format(x, ",").replace(",", ".") + "đ"

    p = ['<h2 id="so-ve">Sổ vé đã mua</h2>']
    p.append('<div class="mo">Mỗi tờ vé gắn với đúng một kỳ quay. Nhập vé ngay bên dưới, '
             "hoặc trên máy tính thì bấm một bộ số gợi ý rồi bấm "
             "<code>11-GHI-VE-DA-MUA.bat</code>.</div>")
    p.append(khung_nhap_ve())

    if not kq and not loi:
        return chr(10).join(p)

    lai = tong["lai_lo"]

    # Gom theo sản phẩm để biết lỗ ở loại nào, chứ một dòng gộp thì không nói
    # được gì khi chị mua nhiều loại.
    nhom = {}
    for k in kq:
        ma = k["ve"]["ma"]
        o = nhom.setdefault(ma, {"so_ve": 0, "cho_quay": 0, "tien_ve": 0,
                                 "tien_trung": 0, "tinh_tien": ma in GIAI})
        o["so_ve"] += 1
        o["tien_ve"] += GIA_VE
        if k["trang_thai"] != "xong":
            o["cho_quay"] += 1
        elif o["tinh_tien"]:
            o["tien_trung"] += k["tien"]

    def o_so(x):
        return '<td class="so">' + x + "</td>"

    def o_lai(x, dam=False):
        mau = "xanh" if x >= 0 else "nhan"
        t = ("+" if x >= 0 else "") + vnd(x)
        t = "<strong>" + t + "</strong>" if dam else t
        return '<td class="so" style="color:var(--' + mau + ')">' + t + "</td>"

    def hang(ten, o, dam=False):
        dem = str(o["so_ve"])
        if o["cho_quay"]:
            dem += '<span class="mo"> (' + str(o["cho_quay"]) + " chờ quay)</span>"
        r = "<tr><td>" + ("<strong>" + ten + "</strong>" if dam else ten) + "</td>"
        r += o_so(dem) + o_so(vnd(o["tien_ve"]))
        r += o_so(vnd(o["tien_trung"]) if o["tinh_tien"]
                  else '<span class="mo">không tính</span>')
        r += o_lai(o["tien_trung"] - o["tien_ve"], dam)
        return r + "</tr>"

    # Câu trả lời trước, số liệu sau — nhìn một dòng là biết đang lãi hay lỗ.
    p.append('<div class="the">')
    p.append("<div style='font-size:17px;margin-bottom:2px'>Tới giờ chị "
             + ("<strong style='color:var(--xanh)'>lãi " if lai >= 0
                else "<strong style='color:var(--nhan)'>lỗ ")
             + vnd(abs(lai)) + "</strong> trên " + str(tong["so_ve"]) + " tờ vé.</div>")
    if tong["ve_khong_tinh_tien"]:
        p.append('<div class="mo">' + str(tong["ve_khong_tinh_tien"])
                 + " tờ thuộc sản phẩm chỉ báo số trùng, không tính tiền thưởng — "
                 "tiền mua vẫn tính đủ, nên nếu có trúng thì con số trên đang thiệt cho chị.</div>")
    p.append('<div class="cuon" style="margin-top:12px"><table><thead><tr>'
             '<th>Sản phẩm</th><th class="so">Số vé</th><th class="so">Tiền mua vé</th>'
             '<th class="so">Tiền trúng</th><th class="so">Lãi / lỗ</th></tr></thead><tbody>')
    if len(nhom) > 1:
        for ma in sorted(nhom, key=lambda m: -nhom[m]["so_ve"]):
            p.append(hang(e(SAN_PHAM[ma]["ten"]), nhom[ma]))
    tong_o = {"so_ve": tong["so_ve"], "cho_quay": tong["cho_quay"],
              "tien_ve": tong["tien_ve"], "tien_trung": tong["tien_trung"],
              "tinh_tien": True}
    p.append(hang("Tổng" if len(nhom) > 1 else e(SAN_PHAM[next(iter(nhom))]["ten"]),
                  tong_o, dam=len(nhom) > 1))
    p.append("</tbody></table></div></div>")

    p.append('<div class="the"><div class="cuon"><table><thead><tr>'
             "<th>Ngày mua</th><th>Vé</th><th>Kỳ quay</th><th>Kết quả</th>"
             "<th></th></tr></thead><tbody>")
    for k in reversed(kq):
        v = k["ve"]
        ten = SAN_PHAM[v["ma"]]["ten"]
        so_html = day_bi(v["so"], v["so_db"])
        o_ve = "<strong>" + e(ten) + "</strong><div>" + so_html + "</div>"
        if v["ghi_chu"]:
            o_ve += '<div class="mo">' + e(v["ghi_chu"]) + "</div>"
        if k["trang_thai"] == "cho":
            p.append("<tr><td>" + e(ngay_viet(v["ngay_mua"], kem_thu=False)) + "</td><td>" + o_ve
                     + '</td><td class="mo">&mdash;</td><td><span class="nhan-nho">chờ quay</span></td>'
                     + o_xoa(v) + "</tr>")
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
                 + "</td><td>" + o_ky + "</td><td>" + o_kq + "</td>" + o_xoa(v) + "</tr>")
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


def o_xoa(v):
    """Ô chứa nút xoá một tờ vé. Xoá theo NGUYÊN VĂN dòng nên không sợ lệch số dòng."""
    return ('<td><button class="nut-xoa" data-dong="' + e(v.get("raw", ""))
            + '" title="Xoá tờ vé này khỏi sổ">Xoá</button></td>')


def khung_nhap_ve():
    """Ô nhập vé ngay trên trang. Gửi lên /api/ghi-ve, cửa ghi phía máy chủ."""
    chon = "".join(
        '<option value="' + ma + '">' + e(SAN_PHAM[ma]["ten"]) + " &mdash; "
        + str(c["so_chon"]) + " số 1-" + str(c["dai_chon"])
        + (" + số đặc biệt 1-" + str(c["db_dai"]) if c["db_dai"] else "")
        + "</option>"
        for ma, c in KHUON_NHAP.items())
    return (
        '<div class="the nhap-ve">'
        '<div class="ten-bd">Ghi một tờ vé vào sổ</div>'
        '<div class="mo" style="margin:4px 0 14px">Gõ số vào ô, hoặc bấm '
        '<b>Bảng số</b> để chọn bằng cách bấm. Bấm vào bộ số ở mục '
        '<a href="#goi-so">Bộ số gợi ý</a> thì ô này tự điền hộ.</div>'
        '<div class="luoi-nv">'
        '<div class="o-nv rong2"><label class="nhan" for="nv-sp">Sản phẩm</label>'
        '<select id="nv-sp">' + chon + "</select></div>"
        '<div class="o-nv rong2"><label class="nhan" for="nv-so">Các số</label>'
        '<span style="display:flex;gap:8px">'
        '<input id="nv-so" inputmode="numeric" style="flex:1">'
        '<button type="button" id="nv-mopad" class="nut phu" '
        'style="white-space:nowrap">Bảng số</button></span></div>'
        '<div class="o-nv nv-db"><label class="nhan" for="nv-db">Số đặc biệt</label>'
        '<input id="nv-db" inputmode="numeric"></div>'
        '<div class="o-nv"><label class="nhan" for="nv-ngay">Ngày mua</label>'
        '<input id="nv-ngay" type="date"></div>'
        '<div class="o-nv"><label class="nhan" for="nv-ghi">Ghi chú</label>'
        '<input id="nv-ghi" placeholder="tuỳ ý"></div>'
        '<div class="o-nv"><label class="nhan" for="nv-mk">Mật khẩu</label>'
        '<input id="nv-mk" type="password" placeholder="nhớ sau lần đầu"></div>'
        "</div>"
        '<div class="pad an" id="nv-pad">'
        '<div class="pad-dau"><span class="pad-ten" id="nv-padten">Chọn số</span>'
        '<span><span class="dem" id="nv-dem">0/6</span>'
        '<button type="button" class="nut phu" id="nv-xoahet" '
        'style="margin-left:6px">Xoá hết</button></span></div>'
        '<div class="o-so" id="nv-oso"></div>'
        "</div>"
        '<div class="hang-nut">'
        '<button id="nv-gui" class="nut">Ghi vào sổ</button>'
        '<span id="nv-bao" class="nv-bao"></span></div>'
        "</div>")


def _ten_hang(h, ma):
    if h:
        from so_ve import GIAI as _G
        if ma in _G and h in _G[ma]:
            return _G[ma][h][0]
    return ""


def _o_bo(so, so_db, so_ky=None, db_ky=None):
    """
    Bộ số dạng chữ, số trúng in đậm xanh. Bảng chi tiết có hàng nghìn dòng nên
    dùng viên bi tròn thì trang phình lên gần 1 MB — chữ thường vừa đủ đọc.
    """
    tap = set(so_ky or [])
    ra = []
    for x in (so or []):
        t = str(x).zfill(2)
        ra.append('<b class="tr">' + t + "</b>" if x in tap else t)
    out = " ".join(ra)
    if so_db is not None:
        d = str(so_db).zfill(2)
        out += " | " + ('<b class="tr">' + d + "</b>" if db_ky == so_db else d)
    return '<span class="so-gon">' + out + "</span>"


def bang_chi_tiet_that(that):
    """Từng bộ đề xuất THẬT: ngày, sản phẩm, bộ số, kỳ nhắm tới, trúng bao nhiêu."""
    ct = (that or {}).get("chi_tiet") or []
    if not ct:
        return ""
    p = ['<details class="the gap"><summary>Chi tiết từng bộ đã đề xuất thật ('
         + format(len(ct), ",").replace(",", ".") + " bộ)</summary>"]
    p.append('<div class="cuon" style="margin-top:10px"><table class="sapxep"><thead><tr>'
             '<th class="sx" data-chieu="">Ngày</th>'
             '<th class="sx" data-chieu="">Sản phẩm</th>'
             '<th class="sx" data-chieu="">Cách chọn</th>'
             "<th>Bộ số</th><th>Kỳ nhắm tới</th>"
             '<th class="sx so" data-chieu="">Trúng</th>'
             '<th class="sx so" data-chieu="">Được</th></tr></thead><tbody>')
    for x in ct:
        ma = x.get("ma")
        ten_sp = SAN_PHAM.get(ma, {}).get("ten", ma)
        cho = x.get("trang_thai") == "cho"
        p.append("<tr>"
                 + '<td data-v="' + e(x.get("ngay")) + '">'
                 + e(ngay_viet(x.get("ngay"), kem_thu=False)) + "</td>"
                 + '<td data-v="' + e(ten_sp) + '">' + e(ten_sp) + "</td>"
                 + '<td data-v="' + e(x.get("chien_luoc")) + '">' + e(x.get("chien_luoc")) + "</td>"
                 + "<td>" + _o_bo(x.get("so") or [], x.get("so_db"),
                                  x.get("so_ky"), x.get("db_ky")) + "</td>")
        if cho:
            p.append('<td class="mo">chưa quay</td>'
                     '<td class="so mo" data-v="-1">&mdash;</td>'
                     '<td class="so mo">&mdash;</td></tr>')
            continue
        giai = _ten_hang(x.get("hang"), ma)
        duoc = (vnd_(x["tien"]) if x.get("tien") else
                ('<span class="mo">không tính tiền</span>' if ma not in ("power_655", "power_645")
                 else '<span class="mo">0đ</span>'))
        p.append("<td>" + e(ngay_viet(x.get("ky_ngay"), kem_thu=False))
                 + '<div class="mo">kỳ ' + e(x.get("ky_id")) + "</div></td>"
                 + '<td class="so" data-v="' + str(x.get("trung", 0)) + '"><strong>'
                 + str(x.get("trung", 0)) + "</strong>"
                 + (" +ĐB" if x.get("trung_db") else "")
                 + (' <div class="mo">' + e(giai) + "</div>" if giai else "") + "</td>"
                 + '<td class="so">' + duoc + "</td></tr>")
    p.append("</tbody></table></div></details>")
    return chr(10).join(p)


def bang_theo_ngay(nap):
    """Từng ngày, từng sản phẩm: đề xuất mấy bộ, trúng mấy, được bao nhiêu."""
    dn = (nap or {}).get("theo_ngay") or []
    if not dn:
        return ""
    tong_dong = len(dn)
    dn = dn[:250]          # 250 ngày gần nhất; cũ hơn thì bảng gộp đã nói đủ
    p = ['<details class="the gap"><summary>Tách theo từng ngày và từng loại ('
         + format(len(dn), ",").replace(",", ".")
         + (" dòng gần nhất trong " + format(tong_dong, ",").replace(",", ".")
            if tong_dong > len(dn) else " dòng") + ")</summary>"]
    p.append('<div class="mo" style="margin-top:8px">Mỗi dòng là một ngày quay của một sản '
             "phẩm: hôm đó mục gợi ý đưa ra mấy bộ, trúng mấy bộ, được bao nhiêu tiền.</div>")
    p.append('<div class="cuon" style="margin-top:8px"><table class="sapxep"><thead><tr>'
             '<th class="sx" data-chieu="">Ngày quay</th>'
             '<th class="sx" data-chieu="">Sản phẩm</th>'
             '<th class="sx so" data-chieu="">Số bộ</th>'
             '<th class="sx so" data-chieu="">Trúng ≥3 số</th>'
             '<th class="sx so" data-chieu="">Tiền trúng</th></tr></thead><tbody>')
    for x in dn:
        ma = x.get("ma")
        ten_sp = SAN_PHAM.get(ma, {}).get("ten", ma)
        p.append("<tr>"
                 + '<td data-v="' + e(x.get("ngay")) + '">'
                 + e(ngay_viet(x.get("ngay"), kem_thu=False)) + "</td>"
                 + '<td data-v="' + e(ten_sp) + '">' + e(ten_sp) + "</td>"
                 + '<td class="so" data-v="' + str(x["so_bo"]) + '">' + str(x["so_bo"]) + "</td>"
                 + '<td class="so" data-v="' + str(x["trung"]) + '">'
                 + (("<strong>" + str(x["trung"]) + "</strong>") if x["trung"] else
                    '<span class="mo">0</span>') + "</td>"
                 + '<td class="so" data-v="' + str(x["tien"]) + '">'
                 + (vnd_(x["tien"]) if x["tien"] else '<span class="mo">0đ</span>')
                 + "</td></tr>")
    p.append("</tbody></table></div></details>")
    return chr(10).join(p)


def bang_bo_trung(nap):
    """Danh sách từng bộ đã trúng, kèm kỳ nào và được bao nhiêu."""
    bt = (nap or {}).get("bo_trung") or []
    if not bt:
        return ""
    tong_bo = len(bt)
    bt = bt[:400]          # 400 bộ trúng gần nhất
    p = ['<details class="the gap"><summary>Những bộ đã trúng ('
         + format(len(bt), ",").replace(",", ".")
         + (" bộ gần nhất trong " + format(tong_bo, ",").replace(",", ".")
            if tong_bo > len(bt) else " bộ") + ")</summary>"]
    p.append('<div class="cuon" style="margin-top:10px"><table class="sapxep"><thead><tr>'
             '<th class="sx" data-chieu="">Ngày quay</th>'
             '<th class="sx" data-chieu="">Sản phẩm</th>'
             '<th class="sx" data-chieu="">Cách chọn</th>'
             "<th>Bộ số &mdash; xanh là trúng</th>"
             '<th class="sx so" data-chieu="">Trúng</th>'
             '<th class="sx so" data-chieu="">Được</th></tr></thead><tbody>')
    for x in bt:
        ma = x.get("ma")
        ten_sp = SAN_PHAM.get(ma, {}).get("ten", ma)
        giai = _ten_hang(x.get("hang"), ma)
        duoc = (vnd_(x["tien"]) if x.get("tien") else
                '<span class="mo">không tính tiền</span>')
        p.append("<tr>"
                 + '<td data-v="' + e(x.get("ngay")) + '">'
                 + e(ngay_viet(x.get("ngay"), kem_thu=False))
                 + '<div class="mo">kỳ ' + e(x.get("ky_id")) + "</div></td>"
                 + '<td data-v="' + e(ten_sp) + '">' + e(ten_sp) + "</td>"
                 + '<td data-v="' + e(x.get("chien_luoc")) + '">' + e(x.get("chien_luoc")) + "</td>"
                 + "<td>" + _o_bo(x.get("so") or [], x.get("so_db"),
                                  x.get("so_ky"), x.get("db_ky")) + "</td>"
                 + '<td class="so" data-v="' + str(x.get("trung", 0)) + '"><strong>'
                 + str(x.get("trung", 0)) + "</strong>"
                 + (" +ĐB" if x.get("trung_db") else "")
                 + (' <div class="mo">' + e(giai) + "</div>" if giai else "") + "</td>"
                 + '<td class="so" data-v="' + str(x.get("tien", 0)) + '">' + duoc + "</td></tr>")
    p.append("</tbody></table></div></details>")
    return chr(10).join(p)


def vnd_(x):
    return format(int(x), ",").replace(",", ".") + "đ"


def pt(x, n=2):
    """Phần trăm kiểu Việt: 1,74% chứ không phải 1.74%"""
    return format(x, "." + str(n) + "f").replace(".", ",") + "%"


def _thanh_so_sanh(that, ky_vong, nhan_trai="", nhan_phai=""):
    """
    Thanh so sánh: vạch giữa là mức may rủi, thanh màu là kết quả thật.
    Bám giữa nghĩa là ngang may rủi. Đọc bằng mắt, khỏi cần hiểu sai số chuẩn.
    """
    if ky_vong <= 0:
        return ""
    ty = min(1.0, that / (ky_vong * 2)) * 100
    return ('<div class="thanh-ss"><div class="thanh-ss-nen"></div>'
            '<div class="thanh-ss-day" style="width:' + format(ty, ".1f") + '%"></div>'
            '<div class="thanh-ss-moc"></div></div>'
            + ('<div class="thanh-ss-nhan"><span>' + nhan_trai + "</span><span>"
               + nhan_phai + "</span></div>" if (nhan_trai or nhan_phai) else ""))


def _loi_phan(d):
    """Một cụm từ thay cho con số sigma."""
    if not d.get("du_mau"):
        return ("cho", "chưa đủ dữ liệu")
    l = d.get("lech_sai_so", 0)
    if abs(l) <= 2:
        return ("ngang", "ngang mức may rủi")
    return ("lech", "cao hơn may rủi" if l > 0 else "thấp hơn may rủi")


def khoi_cham_goi_y():
    """Mục gợi ý tự chấm chính nó — trả lời trước, số liệu sau."""
    f1 = THU_MUC_BAO_CAO / "cham-goi-so.json"
    f2 = THU_MUC_BAO_CAO / "cham-goi-so-nap.json"
    that = nap = None
    for f, ten in ((f1, "that"), (f2, "nap")):
        if f.exists():
            try:
                with open(f, "r", encoding="utf-8") as fh:
                    d = json.load(fh)
                if ten == "that":
                    that = d
                else:
                    nap = d
            except (json.JSONDecodeError, OSError):
                pass
    if not that and not nap:
        return ""

    def n(x):
        return format(int(x), ",").replace(",", ".")

    p = ['<h2 id="cham-goi-y">Mục gợi ý có ăn không?</h2>']

    # ---------- 1. Câu trả lời, to và rõ ----------
    if nap:
        t = nap["tong"]
        _, cum = _loi_phan(t)
        ngang = cum == "ngang mức may rủi"
        p.append('<div class="the tra-loi">')
        p.append('<div class="tl-to">' + ("Không." if ngang else "Có dấu hiệu lệch.")
                 + '</div><div class="tl-phu">'
                 + ("Chọn số kiểu gì cũng trúng ngang nhau, và ngang cả bốc bừa."
                    if ngang else "Kết quả lệch khỏi mức may rủi, xem bảng bên dưới.")
                 + "</div>")
        p.append('<div class="tl-so">'
                 '<div><span class="tl-nhan">Đã thử</span>'
                 '<span class="tl-lon">' + n(t["da_cham"]) + "</span>"
                 '<span class="tl-nhan">bộ số</span></div>'
                 '<div><span class="tl-nhan">Trúng ≥3 số</span>'
                 '<span class="tl-lon">' + n(t["co_giai"]) + "</span>"
                 '<span class="tl-nhan">bộ &middot; ' + pt(t["ty_le_co_giai"])
                 + "</span></div>"
                 '<div><span class="tl-nhan">Nếu bốc bừa thì khoảng</span>'
                 '<span class="tl-lon mo">' + n(round(t["ky_vong_co_giai"])) + "</span>"
                 '<span class="tl-nhan">bộ &middot; ' + pt(t["ty_le_ky_vong"])
                 + "</span></div></div>")
        p.append(_thanh_so_sanh(t["ty_le_co_giai"], t["ty_le_ky_vong"],
                                "trúng ít hơn", "trúng nhiều hơn"))
        p.append('<div class="mo" style="margin-top:6px">Vạch đứng ở giữa là mức may rủi. '
                 "Thanh dừng ngay giữa nghĩa là kết quả đúng bằng may rủi.</div>")
        p.append("</div>")

    # ---------- 2. Từng cách chọn số ----------
    if nap:
        p.append("<h3>Từng cách chọn số</h3>")
        p.append('<div class="the"><div class="cuon"><table><thead><tr>'
                 "<th>Cách chọn số</th>"
                 '<th class="so">Trúng</th>'
                 "<th>So với may rủi</th>"
                 "<th></th></tr></thead><tbody>")
        for ten, d in nap["theo_chien_luoc"].items():
            if not d["da_cham"]:
                continue
            lop, cum = _loi_phan(d)
            p.append("<tr>"
                     + "<td><strong>" + e(ten) + "</strong></td>"
                     + '<td class="so">' + n(d["co_giai"]) + "/" + n(d["da_cham"])
                     + '<div class="mo">' + pt(d["ty_le_co_giai"]) + "</div></td>"
                     + '<td style="min-width:170px">'
                     + _thanh_so_sanh(d["ty_le_co_giai"], d["ty_le_ky_vong"]) + "</td>"
                     + '<td><span class="cum ' + lop + '">' + cum + "</span></td></tr>")
        p.append("</tbody></table></div>")
        p.append('<div class="mo" style="margin-top:10px">Cả '
                 + str(len(nap["theo_chien_luoc"])) + " cách đều bám vạch giữa. "
                 "Không cách nào giỏi hơn cách nào &mdash; chênh lệch là dao động ngẫu nhiên, "
                 "không phải tài.</div></div>")

    # ---------- 3. Kho đề xuất thật ----------
    if that:
        t = that["tong"]
        p.append("<h3>Kho đề xuất thật đang tới đâu</h3>")
        p.append('<div class="the"><div class="tl-so">'
                 '<div><span class="tl-nhan">Đã cất</span><span class="tl-lon">'
                 + n(that.get("tong_bo_trong_kho", 0)) + '</span><span class="tl-nhan">bộ</span></div>'
                 '<div><span class="tl-nhan">Đã chấm</span><span class="tl-lon">'
                 + n(t["da_cham"]) + '</span><span class="tl-nhan">bộ</span></div>'
                 '<div><span class="tl-nhan">Chờ quay</span><span class="tl-lon mo">'
                 + n(t["cho_quay"]) + '</span><span class="tl-nhan">bộ</span></div>'
                 + ('<div><span class="tl-nhan">Trúng ≥3 số</span><span class="tl-lon">'
                    + n(t["co_giai"]) + '</span><span class="tl-nhan">bộ</span></div>'
                    if t["da_cham"] else "")
                 + "</div>")
        if not t["da_cham"]:
            p.append('<div class="mo" style="margin-top:8px">Chưa bộ nào tới kỳ quay. '
                     "Bảng phía trên là kết quả dựng lại từ quá khứ, để có số ngay.</div>")
        elif not t.get("du_mau"):
            p.append('<div class="mo" style="margin-top:8px">Kho còn nhỏ nên chưa kết luận '
                     "được gì. Mỗi ngày kho một lớn; khoảng vài tháng nữa mới đủ để so.</div>")
        else:
            _, cum = _loi_phan(t)
            p.append('<div style="margin-top:8px">Kết quả từ đề xuất thật: <strong>'
                     + cum + "</strong>.</div>")
        p.append("</div>")

    # ---------- 4. Chi tiết, gói lại ----------
    p.append(bang_chi_tiet_that(that))
    if nap:
        p.append(bang_bo_trung(nap))
        p.append(bang_theo_ngay(nap))

    # ---------- 5. Ghi chú ----------
    p.append('<div class="canh">'
             "<strong>Vài điều để đọc cho đúng.</strong> "
             '<div style="margin-top:6px">&middot; "Trúng" ở đây là trùng từ <strong>3 số '
             "chính trở lên</strong> &mdash; mức thấp nhất có giải của Power 6/55 và Mega 6/45."
             "</div>"
             '<div style="margin-top:4px">&middot; Chỉ theo dõi Power 6/55, Mega 6/45 và '
             "Lotto 5/35. <strong>Keno không tính</strong>: chọn 10 số trong 80 mà quay tới "
             "20 số nên trúng ≥3 số xảy ra tới 47,9%, gộp chung thì con số tổng vô nghĩa."
             "</div>"
             '<div style="margin-top:4px">&middot; Bảng lớn lấy từ phần <strong>dựng lại quá '
             "khứ</strong>: cho chương trình xem đúng phần lịch sử trước mỗi kỳ rồi hỏi nó gợi "
             "ý gì, y như nó đã chạy hôm ấy. Nhờ vậy có số ngay thay vì đợi vài tháng.</div>"
             "</div>")
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

    # Bot GitHub chạy trên máy giờ UTC -> phải quy về giờ Việt Nam,
    # không thì trang ghi lệch 7 tiếng.
    bay_gio = datetime.now(timezone(timedelta(hours=7))).strftime("%H:%M ngày %d/%m/%Y")
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
    if (THU_MUC_BAO_CAO / "cham-goi-so-nap.json").exists() or (THU_MUC_BAO_CAO / "cham-goi-so.json").exists():
        p.append('<a href="#cham-goi-y">Gợi ý trúng ra sao</a>')
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
    p.append(khoi_cham_goi_y())
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
    p.append("</div><script>"
             + JS.replace("__KHUON_JSON__", json.dumps(KHUON_NHAP, ensure_ascii=False))
             + "</script></body></html>")

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
