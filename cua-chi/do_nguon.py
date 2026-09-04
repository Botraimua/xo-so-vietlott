# -*- coding: utf-8 -*-
"""
Máy dò nguồn: xem từ CHỖ ĐANG CHẠY thì gọi được những nguồn nào.

Vì sao cần: nguồn nào thử từ máy Sếp (ở Việt Nam) cũng chạy, nên thử ở đây
không chứng minh được gì về máy chủ GitHub. Đúng cái bẫy đã làm bot hỏng im
lặng 8 ngày cuối tháng 8/2026. File này chạy ở đâu thì đo ở đó, rồi GHI KẾT QUẢ
RA FILE để đọc lại — vì nhật ký lần chạy trên GitHub không xem được nếu không
đăng nhập (403).

Cách chạy:
    python cua-chi/do_nguon.py            -> in ra màn hình + ghi file
"""

import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from thu_vien import bat_utf8  # noqa: E402

bat_utf8()

FILE_KQ = Path(__file__).resolve().parent / "ket-qua-do-nguon.md"
CHO = 25

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) "
      "Gecko/20100101 Firefox/128.0")

# Bảng ajaxpro của chính vietlott.vn — đúng đường mà bộ crawler gốc dùng
# Mỗi sản phẩm một mã Key riêng — lấy đúng từ repo gốc, dùng nhầm thì
# vietlott.vn vẫn trả HTTP 200 nhưng bảng rỗng (chỉ ~700 byte).
AJAX = {
    "power_655": ("Game655CompareWebPart", "23bbd667"),
    "power_645": ("Game645CompareWebPart", "8290fce2"),
    "power_535": ("Game535CompareWebPart", "d0ea794f"),
}

# Vài trang kết quả xổ số khác, phòng khi vietlott.vn chặn
TRANG_KHAC = [
    ("kqxs.vn",      "https://www.kqxs.vn/vietlott/power-655"),
    ("minhngoc",     "https://www.minhngoc.net.vn/ket-qua-xo-so/vietlott/power-655.html"),
    ("xosodaiphat",  "https://xosodaiphat.com/xs-power-655.html"),
    ("xoso.me",      "https://xoso.me/power-655-xsvl.html"),
    ("ketqua1",      "https://ketqua1.net/vietlott-power-655"),
]

# Các kho dữ liệu sẵn trên GitHub — máy chủ GitHub chắc chắn gọi được
KHO_GITHUB = [
    ("vietvudanh", "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/"),
    ("googlesky",  "https://raw.githubusercontent.com/googlesky/vietlott-data/main/data/"),
]

ghi = []


def d(s=""):
    print(s)
    ghi.append(s)


def _mo(req):
    ctx = ssl.create_default_context()
    return urllib.request.urlopen(req, timeout=CHO, context=ctx)


def lay(url, du_lieu=None, headers=None):
    """Trả (mã, số byte, nội dung, lỗi). Không ném ngoại lệ ra ngoài."""
    h = {"User-Agent": UA, "Accept": "*/*"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=du_lieu, headers=h,
                                 method="POST" if du_lieu else "GET")
    t = time.time()
    try:
        with _mo(req) as r:
            b = r.read()
            return r.status, len(b), b, None, time.time() - t
    except urllib.error.HTTPError as e:
        try:
            b = e.read()
        except Exception:
            b = b""
        return e.code, len(b), b, "HTTP " + str(e.code), time.time() - t
    except Exception as e:
        return None, 0, b"", type(e).__name__ + ": " + str(e)[:110], time.time() - t


def _dong(ten, ma, cd, loi, giay, them=""):
    dau = "  ✗" if loi or not ma else "  ✓"
    d(dau + " " + ten.ljust(22)
      + (("HTTP " + str(ma)) if ma else "không nối được").ljust(16)
      + str(cd).rjust(8) + " byte"
      + ("  " + format(giay, ".1f") + "s")
      + (("   " + them) if them else "")
      + (("   " + loi) if loi and ma is None else ""))


# ---------------------------------------------------------------- 1. chỗ đứng
def cho_dung():
    d("## 1. Máy đang chạy đứng ở đâu")
    d()
    for ten, u in (("ip", "https://api.ipify.org?format=json"),
                   ("quốc gia", "https://ipinfo.io/json")):
        ma, cd, b, loi, giay = lay(u)
        if ma == 200:
            try:
                j = json.loads(b.decode("utf-8", "replace"))
                if ten == "ip":
                    d("  Địa chỉ IP: " + str(j.get("ip")))
                else:
                    d("  Quốc gia  : " + str(j.get("country"))
                      + "   nhà mạng: " + str(j.get("org"))[:60])
            except Exception:
                pass
        else:
            d("  " + ten + ": không hỏi được (" + str(loi) + ")")
    d()


# ------------------------------------------------------- 2. chính vietlott.vn
def do_vietlott():
    d("## 2. Chính vietlott.vn — đường mà bộ crawler gốc dùng")
    d()

    ma, cd, b, loi, giay = lay("https://vietlott.vn/vi")
    _dong("trang chủ", ma, cd, loi, giay)

    # Cookie: mọi sản phẩm trong repo gốc đều đặt use_cookies=False, nên bước
    # này KHÔNG bắt buộc. Vẫn đo để biết, nhưng thiếu nó thì cứ gọi tiếp.
    ma, cd, b, loi, giay = lay("https://vietlott.vn/ajaxpro/")
    m = re.search(r'document\.cookie="(.*?)"', b.decode("utf-8", "replace"))
    _dong("thử lấy cookie", ma, cd, loi, giay,
          "có cookie" if m else "không có cookie (không sao, crawler không cần)")
    cookie = m.group(1) if m else None

    orender = {
        "ExtraParam1": "", "ExtraParam2": "", "ExtraParam3": "",
        "FullPageAlias": None, "IsPageDesign": False, "OrgPageAlias": None,
        "PageAlias": None, "RefKey": None, "SiteAlias": "main.vi",
        "SiteId": "main.frontend.vi", "SiteLang": "vi", "SiteName": "Vietlott",
        "SiteURL": "", "System": 1, "UserSessionId": "", "WebPage": None,
    }
    duoc = False
    for ma_sp, (phan, khoa) in AJAX.items():
        than = json.dumps({
            "ORenderInfo": orender, "Key": khoa, "GameDrawId": "",
            "ArrayNumbers": [["" for _ in range(18)] for _ in range(5)],
            "CheckMulti": False, "PageIndex": 0,
        }).encode("utf-8")
        url = ("https://vietlott.vn/ajaxpro/Vietlott.PlugIn.WebParts."
               + phan + ",Vietlott.PlugIn.WebParts.ashx")
        h = {
            "Content-Type": "text/plain; charset=utf-8",
            "X-AjaxPro-Method": "ServerSideDrawResult",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://vietlott.vn",
            "Referer": "https://vietlott.vn/vi/trung-thuong/ket-qua-trung-thuong/winning-number-645",
        }
        if cookie:
            h["Cookie"] = cookie
        ma, cd, b, loi, giay = lay(url, than, h)
        them = ""
        if ma == 200:
            t = b.decode("utf-8", "replace")
            co = "HtmlContent" in t
            ngay = re.findall(r"\d{2}/\d{2}/20\d\d", t)
            them = ("có bảng kết quả, ngày mới nhất "
                    + (sorted(set(ngay), reverse=True)[0] if ngay else "?")) \
                if co else "trả về nhưng KHÔNG có bảng kết quả"
            # 6/45 va 5/35 hay tra bang RONG (~700 byte) du dung Key — chua ro
            # vi sao, nhung khong can: chi can 6/55 co bang la biet may nay goi
            # duoc vietlott.vn hay khong.
            if co and not ngay:
                them = "trả về bảng RỖNG (" + str(cd) + " byte)"
            duoc = duoc or co
        _dong(ma_sp, ma, cd, loi, giay, them)
    d()
    return duoc


# --------------------------------------------------------- 3. các trang khác
def do_trang_khac():
    d("## 3. Các trang kết quả xổ số khác")
    d()
    hom_nay = datetime.now(timezone(timedelta(hours=7))).strftime("%d/%m/%Y")
    hn2 = hom_nay.replace("/", "-")
    for ten, u in TRANG_KHAC:
        ma, cd, b, loi, giay = lay(u)
        them = ""
        if ma == 200 and cd > 2000:
            t = b.decode("utf-8", "replace")
            ngay = re.findall(r"\d{2}[/-]\d{2}[/-]20\d\d", t)
            moi = sorted(set(x.replace("-", "/") for x in ngay), reverse=True)
            them = ("ngày mới nhất " + moi[0]) if moi else "không thấy ngày nào"
            if hom_nay in t or hn2 in t:
                them += "  (CÓ hôm nay)"
        _dong(ten, ma, cd, loi, giay, them)
    d()


# ------------------------------------------------------- 4. kho sẵn trên GitHub
def do_kho_github():
    d("## 4. Kho dữ liệu sẵn trên GitHub (đường dự phòng)")
    d()
    for ten, goc in KHO_GITHUB:
        for f in ("power655", "power645", "power535"):
            ma, cd, b, loi, giay = lay(goc + f + ".jsonl")
            them = ""
            if ma == 200 and b:
                dong = [x for x in b.decode("utf-8", "replace").splitlines() if x.strip()]
                if dong:
                    try:
                        j = json.loads(dong[-1])
                        them = ("kỳ cuối " + str(j.get("id"))
                                + " ngày " + str(j.get("date"))
                                + "  (" + str(len(dong)) + " kỳ)")
                    except Exception:
                        them = str(len(dong)) + " dòng, đọc không ra"
            _dong(ten + "/" + f, ma, cd, loi, giay, them)
    d()


def main():
    n = datetime.now(timezone(timedelta(hours=7)))
    d("# Kết quả dò nguồn")
    d()
    d("Đo lúc **" + n.strftime("%H:%M ngày %d/%m/%Y") + "** (giờ Việt Nam).")
    d()
    d("```")
    cho_dung()
    ok = do_vietlott()
    do_trang_khac()
    do_kho_github()
    d("```")
    d()
    d("## Kết luận")
    d()
    if ok:
        d("**Máy này gọi được thẳng vietlott.vn.** Không cần đường vòng.")
    else:
        d("**Máy này KHÔNG gọi được vietlott.vn.** Phải đi đường khác — xem "
          "mục 3 và 4 ở trên xem đường nào còn sống.")
    d()

    FILE_KQ.write_text("\n".join(ghi) + "\n", encoding="utf-8")
    print()
    print("  Đã ghi " + str(FILE_KQ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
