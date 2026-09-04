# Vietlott của Sếp — hướng dẫn dùng

Bộ công cụ tải toàn bộ kết quả xổ số Vietlott về máy Sếp, dựng bảng thống kê và dò vé.
Chạy hoàn toàn dưới máy, **không cần Claude, không cần tài khoản, không tốn tiền**.

Thư mục: `E:\Claude-Brain\xo-so-vietlott`

---

## Dùng hằng ngày — chỉ 1 nút

Mở thư mục, bấm đúp vào:

**`0-LAM-MOI-VA-XEM.bat`**

Nó làm liền 3 việc: tải kỳ mới về → dò vé của Sếp → mở báo cáo trên trình duyệt.
Mất khoảng 20 giây. Xong là Sếp có mọi thứ.

---

## Mười bốn nút bấm

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
| `11-GHI-VE-DA-MUA.bat` | Ghi vé vừa mua vào sổ | Ngay sau khi bấm chép một bộ số gợi ý |
| `12-CAI-CUA-GHI-VE.bat` | Cài để nhập vé được trên web | **Một lần duy nhất** |
| `13-DO-LAI-MUC-GOI-Y.bat` | Chấm lại mọi bộ số đã đề xuất | Khi muốn biết mục gợi ý trúng ra sao |

> Máy Sếp đã cài sẵn rồi, `1-CAI-DAT.bat` không cần chạy lại.
> Nút 6 mất khoảng 20 giây, chạy xong thì kết quả tự hiện trong báo cáo HTML.

---

## Ghi bộ số của Sếp vào

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

Muốn bộ số này hiện luôn trên trang web thì bấm thêm `10-DAY-LEN-GITHUB.bat` — khoảng
1 phút sau là có, và bot tự dò lại 3 lần mỗi ngày.

### Dò nhanh một bộ không cần ghi vào file

Mở cửa sổ lệnh trong thư mục này rồi gõ:

```bash
.venv\Scripts\python.exe cua-chi\do_ve.py power 3 12 19 27 41 52 ^| 8
```

---

## Báo cáo có gì

File `bao-cao\thong-ke-vietlott.html`. Đây là **file tự chứa** — Sếp copy sang USB,
gửi Zalo, mở trên điện thoại đều được, không cần mạng.

Trong đó:

- **Vé của Sếp** — mỗi bộ số so với kỳ mới nhất; số nào trùng được tô xanh.
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

## Dữ liệu Sếp đang có

| Sản phẩm | Số kỳ | Từ ngày | Lịch quay |
|---|---:|---|---|
| Power 6/55 | 1.388 | 01/08/2017 | Thứ 3 – 5 – 7, 18h |
| Mega 6/45 | 1.553 | 20/07/2016 | Thứ 4 – 6 – CN, 18h |
| **Lotto 5/35** | 842 | 29/06/2025 | **hằng ngày 2 kỳ — 13h và 21h** |
| Keno | 81.861 | 04/12/2022 | Mỗi 10 phút, 6h – 21h55 |
| Bingo18 | 87.059 | 03/12/2024 | Mỗi 10 phút |
| Max 3D | 1.122 | 22/04/2019 | Thứ 2 – 4 – 6, 18h |
| Max 3D Pro | 769 | 14/09/2021 | Thứ 3 – 5 – 7, 18h |

Lịch trên **lấy từ chính dữ liệu**, không phải chép ở đâu: đếm thứ trong tuần và số kỳ
mỗi ngày của 120 ngày gần nhất.

> **Dữ liệu gốc của tác giả có lỗ, đã lấy bù xong.** Lotto 5/35 hụt 74 kỳ (vì repo gốc chỉ
> lấy 1 trang mỗi lần, mà sản phẩm này quay 2 kỳ/ngày), Mega 6/45 hụt 197 kỳ đầu, Max 3D
> hụt 4, Max 3D Pro hụt 4. Giờ cả 5 sản phẩm **liền mạch, không thiếu kỳ nào** — kiểm bằng
> cách soi mã kỳ có chạy liên tục không. Để không tái diễn, mỗi lần cập nhật giờ lấy 3 trang
> thay vì 1.

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
| Power 6/55 | 6 số từ 1–55 *(số đặc biệt do Vietlott quay, Sếp không chọn)* |
| Mega 6/45 | 6 số từ 1–45 |
| Lotto 5/35 | 5 số từ 1–35 **+ 1 số đặc biệt từ 1–12** |
| Keno | 10 số từ 1–80 *(Keno cho chọn 1–10 số, Sếp lấy bớt cũng được)* |

Tổng cộng **144 bộ** mỗi ngày (4 sản phẩm × 9 cách chọn × 4 bộ).

Bộ số **đổi theo ngày**: hôm nay chạy bao nhiêu lần cũng ra y nhau, sang ngày mai ra bộ khác.
Nhờ vậy Sếp không bị cám dỗ bấm đi bấm lại đến khi ra bộ "ưng mắt".

Trong báo cáo HTML, **bấm vào một bộ số là chép luôn** ở dạng dán được thẳng vào
`ve-cua-chi.txt`, ví dụ `power_655: 2 20 23 33 44 52`.

Muốn nhiều hay ít bộ hơn, hoặc chỉ một sản phẩm, thì mở cửa sổ lệnh rồi gõ:

```bash
.venv\Scripts\python.exe cua-chi\goi_so.py 5 power
```

> **Nói thẳng một lần cho rõ:** mấy bộ số này **không dễ trúng hơn** bộ Sếp tự nghĩ,
> cũng không dễ trúng hơn bộ bốc bừa. Mọi bộ 6 số đều có xác suất y hệt nhau —
> mục ngay dưới đây là bằng chứng. Đây là công cụ đỡ phải ngồi nghĩ số, thế thôi.

---

## Nhập vé ngay trên trang web

Trong mục **Sổ vé đã mua** trên trang có ô **"Ghi một tờ vé vào sổ"**. Nhập từ điện thoại
cũng được — vé đi thẳng vào sổ chính trên GitHub, máy tính và web đều thấy.

Bấm vào một bộ ở mục **Bộ số gợi ý** thì ô này **tự điền hộ**, Sếp chỉ việc bấm Ghi.

Mật khẩu chỉ phải gõ lần đầu trên mỗi thiết bị, sau đó trình duyệt nhớ.

### Cài đặt — làm một lần

Ô nhập chưa chạy được cho tới khi cài xong. Bấm thử bây giờ sẽ báo
*"Máy chủ chưa được cài đặt"* — đúng như vậy.

**Bước 1 — Tạo chìa khoá GitHub** (làm trên web, khoảng 1 phút)

1. Mở https://github.com/settings/personal-access-tokens/new
2. **Token name**: `vietlott-ghi-ve`
3. **Expiration**: `No expiration`
4. **Repository access** → **Only select repositories** → chọn `xo-so-vietlott`
5. **Permissions → Repository permissions**, đặt đúng 2 mục:
   - **Contents**: `Read and write`
   - **Actions**: `Read and write`
6. Bấm **Generate token**, rồi **copy** chuỗi hiện ra
   (bắt đầu bằng `github_pat_...`, chỉ hiện một lần — copy ngay)

**Bước 2 — Bấm `12-CAI-CUA-GHI-VE.bat`**

Nút này hỏi Sếp hai câu rồi tự lo hết phần còn lại:

1. *Chia khoa GitHub:* → bấm chuột phải vào cửa sổ đen để **dán** chuỗi vừa copy, Enter
2. *Mat khau chi tu nghi:* → gõ một mật khẩu dễ nhớ, Enter
   *(nên dùng chữ và số thôi, tránh ký tự lạ như `&` `|` `^` `!`)*

Rồi nó tự lưu lên Vercel, kiểm lại, đăng lại trang, và **thử gõ sai mật khẩu một lần**
để chứng minh cửa ghi đã sống. Dòng cuối cùng hiện ra sẽ nói cho Sếp biết:

| Dòng cuối hiện gì | Nghĩa là |
|---|---|
| `Mật khẩu không đúng` | ✅ **Cài xong.** Cửa ghi đang chạy, chỉ là vừa cố tình gõ sai |
| `Máy chủ chưa được cài đặt` | Chưa nhận biến. Đợi 1 phút rồi bấm `7-DUA-LEN-MANG.bat` |

Chìa khoá và mật khẩu đi thẳng từ cửa sổ đen lên Vercel, Vercel lưu ở dạng **Sensitive**
(ẩn, không xem lại được). Không lưu xuống file nào trên máy, không lọt vào trang web.

Muốn đổi mật khẩu sau này thì bấm lại nút 12, nhập lại cả hai giá trị.

### Xoá một tờ vé

Trong mục **Sổ vé đã mua**, mỗi dòng vé có nút **Xoá** ở cuối. Bấm → xác nhận → gõ mật khẩu
(nếu trình duyệt chưa nhớ). Khoảng 2 phút sau vé biến khỏi sổ, ở cả web lẫn máy.

Xoá theo **nguyên văn dòng vé** chứ không theo số thứ tự, nên không bao giờ xoá nhầm tờ khác.
Nếu trang đang cũ mà Sếp bấm xoá, nó báo *"Không tìm thấy vé này trong sổ"* thay vì xoá bừa.

**Xoá rồi không lấy lại được** — nhưng vé cũ vẫn còn trong lịch sử GitHub nếu thật sự cần tìm.

Muốn sửa hoặc xoá nhiều vé một lúc thì mở thẳng `cua-chi\so-ve.txt` bằng Notepad, sửa xong
bấm `10-DAY-LEN-GITHUB.bat`.

---

### Chạy như thế nào

1. Sếp bấm **Ghi vào sổ** trên trang
2. Máy chủ kiểm mật khẩu, ghi thêm một dòng vào `cua-chi/so-ve.txt` trên GitHub
3. Máy chủ kích workflow dựng lại trang — khoảng **2 phút** sau vé hiện ra, đã chấm sẵn
4. Lần sau Sếp bấm nút 0 hoặc nút 3 trên máy, nó tự kéo vé đó về

**Mật khẩu để làm gì:** trang công khai nên nếu không có mật khẩu thì ai cũng ghi vé vào
sổ Sếp được. Mật khẩu kiểm ở phía máy chủ, không nằm trong trang. Chìa khoá GitHub cũng
nằm ở phía máy chủ, người xem trang không thấy được.

**Nếu bấm Ghi mà báo lỗi:**

| Báo | Nghĩa là |
|---|---|
| *Máy chủ chưa được cài đặt* | Chưa làm Bước 1–2, hoặc chưa bấm nút 7 sau khi thêm biến |
| *Mật khẩu không đúng* | Gõ sai. Xoá ô mật khẩu rồi gõ lại |
| *Không đọc được sổ vé (mã 403/404)* | Chìa khoá thiếu quyền, hoặc chọn nhầm repo ở Bước 1 |
| *Không gọi được máy chủ* | Sếp đang mở file HTML từ máy. Ô nhập chỉ chạy trên trang web thật |

---

## Sổ vé đã mua (nút 11)

Khi Sếp **mua thật** một bộ số, ghi nó vào sổ để theo dõi kết quả và lãi/lỗ thật:

1. Trong báo cáo, bấm vào bộ số Sếp mua (nó tự chép, kèm luôn tên chiến lược và ngày)
2. Bấm **`11-GHI-VE-DA-MUA.bat`** — vé vào sổ với ngày hôm nay

Hoặc nhập thẳng trên trang web — xem mục ngay trên.

Từ đó, mỗi lần mở báo cáo (nút 0 / nút 3) sẽ có mục **"Sổ vé đã mua"**. Hai nút này giờ
**tự kéo về** những vé Sếp đã nhập trên web trước khi dựng báo cáo:

- Vé chưa tới kỳ quay: hiện *chờ quay*. Quay xong: tự chấm, tô xanh số trùng
- Trúng giải: ghi rõ hạng và tiền (Power 6/55: nhất 40tr / nhì 500k / ba 50k;
  Mega 6/45: nhất 10tr / nhì 300k / ba 30k; Jackpot ghi mức tối thiểu)
- Dòng tổng: **tiền mua vé − tiền trúng = lãi/lỗ thật của Sếp**

Mỗi vé gắn với đúng **một** kỳ: vé mua ngày nào dự kỳ quay đầu tiên từ ngày đó trở đi.
Lotto 5/35 quay 2 kỳ/ngày — mặc định chấm kỳ 13h; vé mua buổi chiều thì thêm `@<mã kỳ>`
vào dòng vé trong `cua-chi\so-ve.txt` (ví dụ `@843`).

Lotto 5/35 và Keno chỉ báo số trùng, **không tính tiền** — cơ cấu giải hai sản phẩm này
không có nguồn công khai đủ rõ, em không đoán bừa.

Sổ nằm ở `cua-chi\so-ve.txt` — file chữ thường, sửa tay bằng Notepad được.

**Sổ vé CÓ lên trang web** (Sếp chọn công khai 24/08/2026): sau khi ghi vé, nút 11 tự đẩy
lên mạng — khoảng 1 phút sau mục "Sổ vé đã mua" hiện trên vietlott-thongke.vercel.app,
xem được từ điện thoại, và bot tự chấm lại 3 lần mỗi ngày.

Muốn gỡ sổ vé khỏi trang web (giữ lại chỉ trên máy) thì bảo Claude — sửa một dòng là xong.

Bộ số **đang chơi** trong `ve-cua-chi.txt` thì vẫn chỉ nằm trên máy như cũ.

Sổ này cũng là bàn thí nghiệm tốt: sau vài chục vé, Sếp sẽ thấy lãi/lỗ thật của mình
bám đúng con số −70% mà bảng xác suất dự báo.

---

## Mục gợi ý trúng thật ra sao (nút 13)

Mỗi bộ số đề xuất đều được **cất lại** trong `cua-chi\kho-goi-so.jsonl`, neo vào đúng
mã kỳ mà nó biết lúc sinh ra. Kỳ nào quay xong thì bộ nhắm vào kỳ đó tự được chấm.

Nút 13 làm hai việc:

1. **Chấm những bộ đã đề xuất thật** — kho này lớn dần mỗi ngày, càng để lâu càng đáng tin
2. **Dựng lại quá khứ** — cho chương trình xem đúng phần lịch sử trước mỗi kỳ rồi hỏi nó
   gợi ý gì, y như nó đã chạy hôm ấy, rồi chấm với chính kỳ đó. Nhờ vậy có số **ngay**,
   khỏi đợi vài tháng

Phần dựng lại quá khứ **không cất vào kho** — nó tính lại được bất cứ lúc nào từ dữ liệu,
cất vào chỉ tổ phình repo và chạy hai lần là đếm trùng. Kho chỉ giữ đề xuất thật.

### Kết quả hiện tại (43.200 bộ dựng lại từ quá khứ)

| Cách chọn số | Trúng ≥3 số | Lý thuyết | Lệch |
|---|---:|---:|---:|
| Chuỗi Markov | 2,00% | 1,70% | +1,6 |
| Mẫu hình | 1,90% | 1,70% | +1,0 |
| Lâu chưa về | 1,88% | 1,70% | +0,9 |
| Không lặp lại | 1,83% | 1,70% | +0,7 |
| Số lạnh | 1,73% | 1,70% | +0,1 |
| Suy giảm mũ | 1,71% | 1,70% | +0,0 |
| Số nóng | 1,60% | 1,70% | −0,5 |
| Tần suất cặp | 1,54% | 1,70% | −0,8 |
| Ngẫu nhiên | 1,52% | 1,70% | −1,0 |

Gộp cả 43.200 bộ: trúng **1,75%**, lý thuyết nói **1,70%** — lệch +0,7 lần sai số chuẩn,
tức là nhiễu bình thường.

**Cách đọc:** cột *lệch* tính theo lần sai số chuẩn. Trong khoảng ±2 là dao động ngẫu nhiên,
không có ý nghĩa gì. Cả 9 cách đều nằm trong khoảng đó → **không cách nào giỏi hơn cách nào**,
đúng như lý thuyết xác suất nói.

### Ba bảng chi tiết, gấp lại được

Ngay dưới bảng gộp có ba khối bấm vào là mở ra:

| Khối | Có gì |
|---|---|
| **Chi tiết từng bộ đã đề xuất thật** | Mọi bộ trong kho: ngày, sản phẩm, cách chọn, bộ số, kỳ nó nhắm tới, trúng mấy con, được bao nhiêu. Chưa quay thì ghi *chưa quay* |
| **Những bộ đã trúng** | Chỉ những bộ trúng ≥3 số — số nào trúng in **xanh đậm**, kèm hạng giải và tiền |
| **Tách theo từng ngày và từng loại** | Mỗi dòng = một ngày quay của một sản phẩm: hôm đó gợi ý mấy bộ, trúng mấy bộ, được bao nhiêu |

Cả ba bảng đều **bấm tiêu đề cột để sắp xếp**. Muốn xem hôm nào trúng nhiều nhất thì bấm
cột "Trúng ≥3 số"; muốn xem cách chọn nào hay trúng thì bấm cột "Cách chọn".

Hai bảng lấy từ phần dựng lại quá khứ có cắt bớt (400 bộ trúng gần nhất trong 754, và
250 ngày gần nhất trong 1.000) — nếu để đủ thì trang nặng gần 1 MB, mở trên điện thoại
sẽ ì. Con số tổng ở bảng gộp vẫn tính trên **toàn bộ** 43.200 bộ.

**Đừng đọc cột ROI theo kiểu xếp hạng.** Trong lần chạy này, Chuỗi Markov ra ROI −10% trong
khi mọi cách khác quanh −93%. Nhìn cột *giải nhất+* là hiểu: Markov trúng **đúng một tờ**
giải nhất 40 triệu, còn lại đều 0 tờ. Một tờ đó kéo ROI của cả 4.800 tờ lên hơn 80 điểm
phần trăm. Đó là may, không phải tài.

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

**Trang của Sếp đã lên rồi:** https://vietlott-thongke.vercel.app

Mở bằng điện thoại, máy tính bảng, máy nào cũng được — không cần bật máy tính ở nhà.

`7-DUA-LEN-MANG.bat` làm 4 việc: kiểm tra đăng nhập → tải kỳ mới → dựng **bản công khai**
→ đăng đè lên trang cũ (giữ nguyên đường dẫn).

### Lần đầu phải đăng nhập một lần

Em đăng bản đầu tiên từ phiên làm việc của em. Nhưng cửa sổ lệnh trên máy Sếp thì
Vercel chưa nhận đăng nhập, nên **lần đầu Sếp phải bấm `8-DANG-NHAP-VERCEL.bat`**.
Nó mở trình duyệt cho Sếp bấm xác nhận, xong là thôi, không phải làm lại.

Nếu Sếp bấm nút 7 mà nó báo "chua dang nhap Vercel" thì đúng là chuyện này.

Bản công khai **không kèm vé của Sếp** — chỉ có thống kê và kết quả xổ số, là dữ liệu
ai cũng xem được. Bộ số riêng chỉ nằm trên máy Sếp.

Trang đặt cờ `noindex` nên Google không đưa vào kết quả tìm kiếm; ai có đường dẫn thì
vẫn mở được.

Muốn đăng lại sau khi có kỳ mới thì bấm lại nút 7 — vẫn giữ nguyên đường dẫn cũ.

---

## Ai xem được gì

Bộ công cụ có ba cánh cửa riêng biệt, đừng lẫn:

| Cửa | Ai vào được | Có gì bên trong |
|---|---|---|
| Máy của Sếp | Chỉ Sếp | Tất cả |
| Repo GitHub `Botraimua/xo-so-vietlott` | **Riêng tư — chỉ Sếp** | Mã nguồn, dữ liệu thô, `so-ve.txt`, `ve-cua-chi.txt` |
| Trang vietlott-thongke.vercel.app | **Công khai** — ai có link | Thống kê, biểu đồ, bộ số gợi ý, **Vé của Sếp**, **Sổ vé** |

Điều dễ hiểu nhầm: **repo riêng tư không làm trang web riêng tư.** Vercel đọc từ repo
riêng tư rồi dựng ra một trang công khai. Sếp đã chọn như vậy (24/08/2026) — biết và đồng ý.

Từ 24/08/2026 Sếp chọn công khai **cả hai** mục vé: "Vé của Sếp" (bộ số đang chơi)
và "Sổ vé đã mua". Cả hai đều hiện trên trang web.

Trang có đặt cờ `noindex` nên Google không đưa vào kết quả tìm kiếm; phải có đúng đường
dẫn mới vào được.

---

## Tự chạy mỗi ngày — GitHub Actions

Mặc định bộ công cụ **không tự chạy**: máy tắt là mọi thứ đứng yên, trang web giữ nguyên
số liệu của lần đăng cuối.

Muốn nó tự cập nhật kể cả khi máy Sếp tắt thì để GitHub chạy hộ — **và việc này đã bật rồi.**

### Đã xong hết — không còn việc gì phải làm

- ✅ Repo: **https://github.com/Botraimua/xo-so-vietlott** (**riêng tư** từ 24/08/2026).
  Actions vẫn chạy miễn phí: workflow tốn ~42 giây/lần, khoảng 62 phút/tháng trên
  hạn mức 2.000 phút. Vercel vẫn tự đăng trang bình thường.
  Bộ số đang chơi trong `ve-cua-chi.txt` **không** lên mạng — đã chặn và đã kiểm chứng.
- ✅ **GitHub Actions đã chạy thật** (00h20 ngày 24/08/2026): tự tải kỳ mới, dựng lại trang,
  ghi vào repo.
- ✅ **Vercel đã nối với repo** (Sếp nối đêm 23/08).
- ✅ **Root Directory** = `web`.
- ✅ Đã kiểm cả dây chuyền: đẩy lên GitHub → Vercel tự đăng lại trang trong vòng 1 phút.

> **Một lỗi đã xảy ra và đã chữa:** lúc đặt Root Directory bị gõ thành `wed`.
> Suốt 12 tiếng sau đó, mọi lần Vercel tự đăng đều thất bại — kể cả lần bot GitHub
> cập nhật dữ liệu — mà nhìn bên ngoài không biết, vì trang vẫn hiện bản cũ.
> Bài học: nếu thấy trang không đổi dù GitHub đã có bản mới, vào
> https://vercel.com/psd6/vietlott-thongke/deployments xem có dòng nào **Error** không.

---

## Nhập nhiều vé một lượt

Trong khối **Ghi một tờ vé vào sổ**, chọn xong bộ số thì có hai nút:

| Nút | Làm gì |
|---|---|
| **Thêm vé nữa** | Xếp vé đang chọn vào danh sách chờ, dọn ô để chọn bộ tiếp theo |
| **Ghi vào sổ** | Gửi tất cả — nhãn tự đổi thành "Ghi 3 vé vào sổ" |

Mỗi vé trong danh sách chờ có nút **Bỏ** riêng. Tối đa 20 vé một lượt.

Vì sao nên dùng: mỗi lần gửi là **một** commit và **một** lần bot chạy. Ngày
04/09/2026 nhập 5 vé liên tiếp theo kiểu cũ làm 5 lần chạy giẫm chân nhau, hai
lần hỏng ở bước đẩy lên và GitHub gửi mail báo hỏng — dù vé vẫn vào sổ đủ.

Đã chặn ở hai lớp: gom nhiều vé vào một lần gửi, và workflow đặt
`cancel-in-progress: true` kèm vòng thử-lại cho bước đẩy.

---

## Bot lấy dữ liệu ở đâu

Có **ba đường**, chạy lần lượt theo đúng thứ tự này:

| | Đường | Có gì | Độ trễ |
|---|---|---|---|
| 1 | **vietlott.vn** | đủ mọi sản phẩm, mã kỳ thật | mới nhất |
| 2 | **kqxs.vn** | chỉ Power 6/55 và Mega 6/45 | **trong ngày** |
| 3 | **ba kho trên GitHub** | đủ 5 sản phẩm, mã kỳ thật | chậm 1–2 ngày |

Đường 3 thử lần lượt **pqminh-4 → googlesky → vietvudanh**. Trước 02/09/2026 chỉ có một kho
(vietvudanh) và nó **ngừng cập nhật từ 29/08** — Lotto 5/35, Max 3D, Max 3D Pro mất sạch nguồn,
chuông báo phải kêu. Một kho là một điểm chết, nên giờ có ba.

Máy Sếp ở Việt Nam thì đường 1 luôn chạy, hai đường kia không cần tới.

**Máy chủ GitHub thì đường 1 luôn tắc.** Đo tận nơi ngày 30/08/2026: vietlott.vn nấp sau
dịch vụ chống bot, trả **403 ở mọi đường**. Không phải chặn theo nước — IP nhà dân Việt Nam
vẫn qua, còn máy chủ trung tâm dữ liệu thì bị chặn. Nhờ trung gian gọi hộ cũng tắc nốt.

Vì sao chuyện này quan trọng: bot từng chạy **8 ngày liền báo "thành công"** mà mỗi lần chỉ
đổi đúng một dòng đồng hồ trong trang — không có kỳ nào mới. Chỉ lộ ra khi Sếp hỏi "vé mua
không tự dò".

### Đường 2 có một chỗ phải cẩn thận

kqxs.vn **không in mã kỳ**, nên bot phải tự suy bằng *kỳ cuối cộng một*. Sai một cái là dò
vé sai mà nhìn vẫn như thật.

Nên mỗi kỳ lấy từ đó đều đóng dấu `"nguon": "kqxs"` trong file dữ liệu. Một hai ngày sau,
khi đường 3 bắt kịp, nó **đối chiếu lại**: lệch thì ghi đè bằng số của kho gốc và kêu lên.
Kỳ nào lệch mà *không* phải mã tự suy thì nó giữ nguyên bản của mình và cảnh báo to — vì
đó là chuyện không nên xảy ra.

### Ba sản phẩm vẫn chậm 1–2 ngày

**Lotto 5/35, Max 3D, Max 3D Pro** — không nguồn nào máy chủ GitHub gọi được có chúng.
kqxs.vn chỉ có 4 sản phẩm, minhngoc chỉ có 2. Muốn ba cái đó cũng có trong ngày thì bấm
`0-LAM-MOI-VA-XEM.bat` trên máy Sếp.

### Bản ghi hỏng còn nguy hơn không lấy được dữ liệu

Ngày 02/09/2026 phát hiện **kỳ 00944 của Power 6/55 sai suốt từ đầu**: ghi ngày 23/09/2022 với
6 số, đúng ra là 14/10/2023 với `08 23 30 34 38 47 | 10`. Sai từ repo gốc. Hai kho dự phòng cũng
sai y hệt vì đều là nhánh của nó — **chỉ lộ ra khi đối chiếu với một kho dựng độc lập**, rồi hỏi
thẳng vietlott.vn để xác nhận.

Kiểu hỏng này nguy hơn hỏng-không-lấy-được: nó làm **dò vé và thống kê sai mà nhìn vẫn như thật**.

Nên bước canh cuối giờ kiểm thêm ba thứ, hỏng là thoát mã lỗi và GitHub gửi mail:
- kỳ nào thiếu số (Power 6/55 phải đủ 7, Mega 6/45 đủ 6, Lotto 5/35 đủ 6)
- số nào ngoài dải cho phép
- mã kỳ tăng mà ngày lại giảm

### Nếu cả ba đường cùng tắc

Bước cuối của bot canh chừng: dữ liệu cũ quá trần ngày (Power/Mega 5 ngày, Lotto 3 ngày)
thì lần chạy bị **đánh dấu hỏng** và GitHub gửi mail cho Sếp. Lúc đó bấm
`0-LAM-MOI-VA-XEM.bat` là xong — máy Sếp vẫn gọi được vietlott.vn.

Trang vẫn được dựng bình thường kể cả khi bước canh này báo đỏ, nên không sợ mất trang.

### Muốn tự kiểm nguồn nào còn sống

Mỗi lần bot chạy, nó đo lại mọi nguồn và ghi kết quả vào `cua-chi/ket-qua-do-nguon.md`
ngay trong kho — mở file đó ra là thấy máy chủ GitHub gọi được cái gì, không gọi được cái
gì, kèm mã HTTP và ngày mới nhất từng nguồn. Chạy trên máy Sếp thì gõ:

```
.venv\Scripts\python.exe cua-chi\do_nguon.py
```

---

## Lịch tự chạy

Từ đó GitHub tự chạy **3 lần mỗi ngày**:

| Giờ Việt Nam | Sau khi quay |
|---|---|
| ~13h45 | Lotto 5/35 kỳ trưa |
| ~18h45 | Power 6/55, Mega 6/45, Max 3D, Max 3D Pro |
| ~21h45 | Lotto 5/35 kỳ tối |

Mỗi lần nó tải kỳ mới → chạy lại bàn kiểm thử → sinh bộ số mới cho ngày → dựng lại trang →
ghi vào repo. Vercel thấy repo đổi thì tự đăng lại trang. Máy Sếp không cần bật.

> GitHub hay chạy trễ 5–30 phút so với giờ hẹn, chuyện bình thường.
> Muốn chạy ngay không đợi: vào tab **Actions**, bấm **Run workflow**.

Sau khi bật cái này thì **nút 7 thành tuỳ chọn** — chỉ dùng khi Sếp muốn đẩy ngay lập tức
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
├── HUONG-DAN.md                 <- file Sếp đang đọc
├── cua-chi\                     <- phần em viết riêng cho Sếp
│   ├── ve-cua-chi.txt              bộ số của Sếp
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
├── .github\workflows\           <- lịch tự chạy 3 lần/ngày trên GitHub
├── data\*.jsonl                 <- dữ liệu thô
└── src\                         <- bộ crawler gốc (không cần đụng tới)
```

Phần `src\` là mã nguồn mở của dự án `vietvudanh/vietlott-data` (giấy phép MIT) —
em giữ nguyên để sau này còn kéo bản vá về được. Mọi thứ trong `cua-chi\` và các
file `.bat` là của riêng Sếp, em viết thêm.

Muốn kéo bản mới của tác giả gốc về: `git pull goc main`.

---

## Một điều cần nói thẳng

Bảng thống kê trong báo cáo là **nhìn lại quá khứ**, không phải dự đoán tương lai.

Mỗi kỳ quay hoàn toàn độc lập: quả cầu không nhớ kỳ trước. Con số "lâu chưa về"
không vì thế mà dễ về hơn ở kỳ sau — đó là cái bẫy suy nghĩ nổi tiếng, gọi là
*ngộ nhận của con bạc*. Số "về nhiều nhất" cũng không nóng hơn số khác.

Xác suất trúng Jackpot Power 6/55 là 1 trên 28.989.675. Bộ công cụ này để dò vé
cho nhanh và nhìn lịch sử cho vui. Sếp chơi trong khoản tiền sẵn sàng mất là được.
