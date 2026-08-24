# Vietlott của chị — hướng dẫn dùng

Bộ công cụ tải toàn bộ kết quả xổ số Vietlott về máy chị, dựng bảng thống kê và dò vé.
Chạy hoàn toàn dưới máy, **không cần Claude, không cần tài khoản, không tốn tiền**.

Thư mục: `E:\Claude-Brain\xo-so-vietlott`

---

## Dùng hằng ngày — chỉ 1 nút

Mở thư mục, bấm đúp vào:

**`0-LAM-MOI-VA-XEM.bat`**

Nó làm liền 3 việc: tải kỳ mới về → dò vé của chị → mở báo cáo trên trình duyệt.
Mất khoảng 20 giây. Xong là chị có mọi thứ.

---

## Mười một nút bấm

| Nút | Làm gì | Khi nào bấm |
|---|---|---|
| `0-LAM-MOI-VA-XEM.bat` | Cập nhật + dò vé + mở báo cáo | **Hằng ngày.** Nút chính |
| `1-CAI-DAT.bat` | Cài môi trường Python | Chỉ 1 lần, hoặc khi chuyển máy |
| `2-CAP-NHAT-DU-LIEU.bat` | Chỉ tải kỳ mới về máy | Khi chỉ muốn tải, chưa muốn xem |
| `3-XEM-BAO-CAO.bat` | Dựng báo cáo HTML rồi mở | Khi đã có dữ liệu, chỉ muốn xem lại |
| `4-DO-VE-CUA-CHI.bat` | Dò vé, in ra cửa sổ đen | Khi chỉ cần biết trúng/trượt cho nhanh |
| `5-SUA-VE-CUA-CHI.bat` | Mở Notepad để sửa bộ số | Khi mua vé mới |
| `6-KIEM-THU-CHIEN-LUOC.bat` | Chạy 9 cách chọn số trên toàn bộ lịch sử | Khi tò mò "có mẹo nào ăn không" |
| `7-DUA-LEN-MANG.bat` | Đăng bản công khai lên Vercel | Khi muốn xem từ điện thoại |
| `8-DANG-NHAP-VERCEL.bat` | Đăng nhập Vercel | **Một lần duy nhất**, trước khi dùng nút 7 |
| `9-GOI-BO-SO.bat` | In bộ số gợi ý ra cửa sổ đen | Khi muốn xem nhanh, khỏi mở báo cáo |
| `10-DAY-LEN-GITHUB.bat` | Đẩy thay đổi mã nguồn lên GitHub | Khi sửa mã trên máy. Dữ liệu thì GitHub tự lo |

> Máy chị đã cài sẵn rồi, `1-CAI-DAT.bat` không cần chạy lại.
> Nút 6 mất khoảng 20 giây, chạy xong thì kết quả tự hiện trong báo cáo HTML.

---

## Ghi bộ số của chị vào

Bấm `5-SUA-VE-CUA-CHI.bat`, Notepad hiện ra. Mỗi dòng một bộ số:

```
power: 3 12 19 27 41 52 | 8      # Power 6/55, số sau dấu | là số đặc biệt
mega: 5 11 18 24 33 45           # Mega 6/45, không có số đặc biệt
lotto: 4 9 17 22 31 | 5          # Lotto 5/35, số sau dấu | từ 1 đến 12
```

Quy tắc:
- Tên sản phẩm gõ sao cũng được: `power` / `655` / `power_655` đều hiểu.
- Số cách nhau bằng dấu cách hoặc dấu phẩy.
- Số đặc biệt ngăn bằng dấu gạch đứng `|`.
- Dòng bắt đầu bằng `#` là ghi chú, chương trình bỏ qua.
- Ghi bao nhiêu bộ cũng được, dò hết một lượt.

Lưu lại bằng `Ctrl+S`, đóng Notepad, rồi bấm `0-LAM-MOI-VA-XEM.bat`.

### Dò nhanh một bộ không cần ghi vào file

Mở cửa sổ lệnh trong thư mục này rồi gõ:

```bash
.venv\Scripts\python.exe cua-chi\do_ve.py power 3 12 19 27 41 52 ^| 8
```

---

## Báo cáo có gì

File `bao-cao\thong-ke-vietlott.html`. Đây là **file tự chứa** — chị copy sang USB,
gửi Zalo, mở trên điện thoại đều được, không cần mạng.

Trong đó:

- **Vé của chị** — mỗi bộ số so với kỳ mới nhất; số nào trùng được tô xanh.
  Kèm cả lịch sử: bộ số này từng khớp cao nhất mấy con, vào ngày nào, đã từng
  đủ điều kiện có giải bao nhiêu lần.
- **Từng sản phẩm** (Power 6/55, Mega 6/45, Lotto 5/35, Keno):
  - Kết quả 10 kỳ gần nhất
  - Ba nhóm: số về nhiều nhất / về ít nhất / lâu chưa về nhất
  - **Bốn biểu đồ**: mỗi số về bao nhiêu lần (có vạch đứt là mức kỳ vọng nếu quay
    hoàn toàn ngẫu nhiên) · mỗi số đã bao nhiêu kỳ chưa về · mỗi kỳ có bao nhiêu
    số chẵn · tổng các số trong một kỳ. Rê chuột lên cột để xem con số cụ thể.
  - Bảng đầy đủ mọi con số — **bấm vào tiêu đề cột để sắp xếp lại**
  - Cặp số hay về cùng nhau
- **Bộ số gợi ý** — mỗi sản phẩm, mỗi cách chọn số 4 bộ. **Bấm vào một bộ là chép được**,
  dán thẳng vào `ve-cua-chi.txt`. Xem mục dưới
- **Có chiến lược chọn số nào ăn được không?** — kết quả của nút 6, xem mục dưới
- **Sản phẩm khác** — Max 3D, Max 3D Pro, Bingo18: kỳ gần nhất

---

## Dữ liệu chị đang có

| Sản phẩm | Số kỳ | Từ ngày | Lịch quay |
|---|---:|---|---|
| Power 6/55 | 1.388 | 01/08/2017 | Thứ 3 – 5 – 7, 18h |
| Mega 6/45 | 1.355 | 25/10/2017 | Thứ 4 – 6 – CN, 18h |
| Lotto 5/35 | 767 | 29/06/2025 | Hằng ngày, 21h |
| Keno | 81.861 | 04/12/2022 | Mỗi 10 phút |
| Bingo18 | 87.059 | 03/12/2024 | Mỗi 10 phút |
| Max 3D | 1.118 | 22/04/2019 | Thứ 2 – 4 – 6, 18h |
| Max 3D Pro | 765 | 14/09/2021 | Thứ 3 – 5 – 7, 18h |

Dữ liệu thô nằm trong `data\*.jsonl` — mỗi dòng một kỳ quay, mở bằng Notepad
hay Excel đều đọc được.

**Keno và Bingo18 không tự cập nhật** khi bấm nút 0 (mỗi ngày cả trăm kỳ, tải lâu).
Muốn cập nhật hai cái này thì mở cửa sổ lệnh trong thư mục rồi gõ:

```bash
.venv\Scripts\python.exe cua-chi\cap_nhat.py tat-ca
```

---

## Bộ số gợi ý (nút 9)

Mỗi sản phẩm, mỗi cách chọn số cho ra 4 bộ:

| Sản phẩm | Bộ số gồm |
|---|---|
| Power 6/55 | 6 số từ 1–55 *(số đặc biệt do Vietlott quay, chị không chọn)* |
| Mega 6/45 | 6 số từ 1–45 |
| Lotto 5/35 | 5 số từ 1–35 **+ 1 số đặc biệt từ 1–12** |
| Keno | 10 số từ 1–80 *(Keno cho chọn 1–10 số, chị lấy bớt cũng được)* |

Tổng cộng **144 bộ** mỗi ngày (4 sản phẩm × 9 cách chọn × 4 bộ).

Bộ số **đổi theo ngày**: hôm nay chạy bao nhiêu lần cũng ra y nhau, sang ngày mai ra bộ khác.
Nhờ vậy chị không bị cám dỗ bấm đi bấm lại đến khi ra bộ "ưng mắt".

Trong báo cáo HTML, **bấm vào một bộ số là chép luôn** ở dạng dán được thẳng vào
`ve-cua-chi.txt`, ví dụ `power_655: 2 20 23 33 44 52`.

Muốn nhiều hay ít bộ hơn, hoặc chỉ một sản phẩm, thì mở cửa sổ lệnh rồi gõ:

```bash
.venv\Scripts\python.exe cua-chi\goi_so.py 5 power
```

> **Nói thẳng một lần cho rõ:** mấy bộ số này **không dễ trúng hơn** bộ chị tự nghĩ,
> cũng không dễ trúng hơn bộ bốc bừa. Mọi bộ 6 số đều có xác suất y hệt nhau —
> mục ngay dưới đây là bằng chứng. Đây là công cụ đỡ phải ngồi nghĩ số, thế thôi.

---

## Bàn kiểm thử chiến lược (nút 6)

Repo gốc có sẵn 9 cách chọn số — số nóng, số lạnh, số lâu chưa về, chuỗi Markov, v.v.
Nút 6 chạy lại cả 9 cách đó trên toàn bộ lịch sử Power 6/55, mỗi cách mua 30 tờ mỗi kỳ,
và **chỉ cho mỗi chiến lược xem dữ liệu trước kỳ nó đoán**.

Kết quả: mọi cách đều lỗ **khoảng 78–92%**. Cách bốc bừa không nhìn lịch sử lỗ 89,7% —
nằm giữa đám đông. Không cách nào ăn được.

Đây không phải kết luận từ may rủi mà là toán: với bộ quay công bằng, **mọi bộ 6 số
đều có xác suất trúng y hệt nhau**, nên giá trị kỳ vọng của mọi chiến lược bằng nhau,
khoảng 2.993đ cho mỗi tờ vé 10.000đ. Chênh lệch trong bảng chỉ là dao động.

### Vì sao trang web của tác giả lại nói khác

Trang `vietvudanh.github.io/vietlott-data` công bố các chiến lược lãi tới **+3.647%**.
Con số đó sai, do 2 lỗi trong phần chấm điểm của họ:

1. Họ so vé với **cả 7 số** (6 số chính + số đặc biệt) thay vì 6 số chính, nên
   "trùng 4 chính + số đặc biệt" bị đếm thành "trùng 5".
2. Bảng giá của họ trả **5 tỷ** cho mỗi tờ "trùng 5". Nhưng trùng 5 số chính là
   giải nhất 40 triệu; 5 tỷ là Jackpot 2, phải trùng 5 số chính **cộng** số đặc biệt.

Cộng lại: mỗi tờ giải nhì 500.000đ được ghi sổ 5 tỷ.

Cột cuối cùng trong bảng kiểm thử là bằng chứng — nó chấm **cùng bộ vé đó** bằng đúng
cách chấm của họ, và con số nhảy từ khoảng −80% lên hơn +4.000%.

---

## Xem từ điện thoại (nút 7)

**Trang của chị đã lên rồi:** https://vietlott-thongke.vercel.app

Mở bằng điện thoại, máy tính bảng, máy nào cũng được — không cần bật máy tính ở nhà.

`7-DUA-LEN-MANG.bat` làm 4 việc: kiểm tra đăng nhập → tải kỳ mới → dựng **bản công khai**
→ đăng đè lên trang cũ (giữ nguyên đường dẫn).

### Lần đầu phải đăng nhập một lần

Em đăng bản đầu tiên từ phiên làm việc của em. Nhưng cửa sổ lệnh trên máy chị thì
Vercel chưa nhận đăng nhập, nên **lần đầu chị phải bấm `8-DANG-NHAP-VERCEL.bat`**.
Nó mở trình duyệt cho chị bấm xác nhận, xong là thôi, không phải làm lại.

Nếu chị bấm nút 7 mà nó báo "chua dang nhap Vercel" thì đúng là chuyện này.

Bản công khai **không kèm vé của chị** — chỉ có thống kê và kết quả xổ số, là dữ liệu
ai cũng xem được. Bộ số riêng chỉ nằm trên máy chị.

Trang đặt cờ `noindex` nên Google không đưa vào kết quả tìm kiếm; ai có đường dẫn thì
vẫn mở được.

Muốn đăng lại sau khi có kỳ mới thì bấm lại nút 7 — vẫn giữ nguyên đường dẫn cũ.

---

## Tự chạy mỗi ngày — GitHub Actions

Mặc định bộ công cụ **không tự chạy**: máy tắt là mọi thứ đứng yên, trang web giữ nguyên
số liệu của lần đăng cuối.

Muốn nó tự cập nhật kể cả khi máy chị tắt thì để GitHub chạy hộ — **và việc này đã bật rồi.**

### Đã xong hết — không còn việc gì phải làm

- ✅ Repo: **https://github.com/Botraimua/xo-so-vietlott** (công khai).
  Bộ số riêng trong `ve-cua-chi.txt` **không** lên mạng — đã chặn và đã kiểm chứng.
- ✅ **GitHub Actions đã chạy thật** (00h20 ngày 24/08/2026): tự tải kỳ mới, dựng lại trang,
  ghi vào repo.
- ✅ **Vercel đã nối với repo** (chị nối đêm 23/08).
- ✅ **Root Directory** = `web`.
- ✅ Đã kiểm cả dây chuyền: đẩy lên GitHub → Vercel tự đăng lại trang trong vòng 1 phút.

> **Một lỗi đã xảy ra và đã chữa:** lúc đặt Root Directory bị gõ thành `wed`.
> Suốt 12 tiếng sau đó, mọi lần Vercel tự đăng đều thất bại — kể cả lần bot GitHub
> cập nhật dữ liệu — mà nhìn bên ngoài không biết, vì trang vẫn hiện bản cũ.
> Bài học: nếu thấy trang không đổi dù GitHub đã có bản mới, vào
> https://vercel.com/psd6/vietlott-thongke/deployments xem có dòng nào **Error** không.

---

## Lịch tự chạy

Từ đó GitHub tự chạy **2 lần mỗi ngày**:

| Giờ Việt Nam | Sau khi quay |
|---|---|
| ~18h45 | Power 6/55, Mega 6/45, Max 3D, Max 3D Pro |
| ~21h45 | Lotto 5/35 |

Mỗi lần nó tải kỳ mới → chạy lại bàn kiểm thử → sinh bộ số mới cho ngày → dựng lại trang →
ghi vào repo. Vercel thấy repo đổi thì tự đăng lại trang. Máy chị không cần bật.

> GitHub hay chạy trễ 5–30 phút so với giờ hẹn, chuyện bình thường.
> Muốn chạy ngay không đợi: vào tab **Actions**, bấm **Run workflow**.

Sau khi bật cái này thì **nút 7 thành tuỳ chọn** — chỉ dùng khi chị muốn đẩy ngay lập tức
chứ không đợi tới giờ.

### Muốn tắt tự chạy

Vào repo trên GitHub → tab **Actions** → chọn "Cập nhật Vietlott" → menu `...` bên phải →
**Disable workflow**.

---

## Nếu có trục trặc

**Cửa sổ đen hiện chữ loạn xạ** — máy đang dùng bảng mã cũ. Không sao, kết quả vẫn đúng;
cứ xem bản HTML thay vì cửa sổ đen.

**Báo "Chưa cài đặt"** — chạy `1-CAI-DAT.bat` một lần.

**Báo LỖI ở một sản phẩm** — gần như luôn là mạng chập chờn hoặc trang vietlott.vn
đang bận. Đợi vài phút rồi bấm lại nút 2.

**Không có kỳ mới dù đã tới giờ quay** — Vietlott thường đăng kết quả sau giờ quay
khoảng 15–30 phút. Bấm lại sau.

---

## Cấu trúc thư mục

```
xo-so-vietlott\
├── 0-LAM-MOI-VA-XEM.bat        <- nút chính
├── 1..10-*.bat                  <- các nút phụ
├── HUONG-DAN.md                 <- file chị đang đọc
├── cua-chi\                     <- phần em viết riêng cho chị
│   ├── ve-cua-chi.txt              bộ số của chị
│   ├── thu_vien.py                 hàm dùng chung
│   ├── cap_nhat.py                 tải kỳ mới
│   ├── bao_cao.py                  dựng HTML
│   ├── bieu_do.py                  vẽ biểu đồ SVG
│   ├── chien_luoc.py               9 cách chọn số, dùng chung
│   ├── kiem_thu.py                 bàn kiểm thử 9 chiến lược
│   ├── goi_so.py                   sinh bộ số gợi ý
│   └── do_ve.py                    dò vé
├── bao-cao\
│   ├── thong-ke-vietlott.html   <- báo cáo, mở bằng trình duyệt
│   ├── kiem-thu.json               kết quả nút 6, báo cáo tự đọc vào
│   └── goi-so.json                 bộ số gợi ý của ngày hôm nay
├── web\index.html               <- bản công khai, Vercel lấy từ đây
├── .github\workflows\           <- lịch tự chạy 2 lần/ngày trên GitHub
├── data\*.jsonl                 <- dữ liệu thô
└── src\                         <- bộ crawler gốc (không cần đụng tới)
```

Phần `src\` là mã nguồn mở của dự án `vietvudanh/vietlott-data` (giấy phép MIT) —
em giữ nguyên để sau này còn kéo bản vá về được. Mọi thứ trong `cua-chi\` và các
file `.bat` là của riêng chị, em viết thêm.

Muốn kéo bản mới của tác giả gốc về: `git pull goc main`.

---

## Một điều cần nói thẳng

Bảng thống kê trong báo cáo là **nhìn lại quá khứ**, không phải dự đoán tương lai.

Mỗi kỳ quay hoàn toàn độc lập: quả cầu không nhớ kỳ trước. Con số "lâu chưa về"
không vì thế mà dễ về hơn ở kỳ sau — đó là cái bẫy suy nghĩ nổi tiếng, gọi là
*ngộ nhận của con bạc*. Số "về nhiều nhất" cũng không nóng hơn số khác.

Xác suất trúng Jackpot Power 6/55 là 1 trên 28.989.675. Bộ công cụ này để dò vé
cho nhanh và nhìn lịch sử cho vui. Chị chơi trong khoản tiền sẵn sàng mất là được.
