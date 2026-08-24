// Cửa ghi vé: nhận vé từ trang web, ghi (hoặc xoá) trong cua-chi/so-ve.txt trên GitHub,
// rồi kích workflow dựng lại trang. Chạy trên máy chủ Vercel, không lộ ra trình duyệt.
//
// Cần 2 biến môi trường đặt trong Vercel (Settings -> Environment Variables):
//   MAT_KHAU      mật khẩu chị tự nghĩ, để người lạ không ghi vé vào sổ được
//   GITHUB_TOKEN  token GitHub có quyền Contents:write + Actions:write trên repo này

const CHU_REPO = "Botraimua";
const TEN_REPO = "xo-so-vietlott";
const DUONG_DAN_SO = "cua-chi/so-ve.txt";
const TEN_WORKFLOW = "cap-nhat-vietlott.yml";
const NHANH = "main";

// Dòng vé hợp lệ, ví dụ:  2026-08-24 | power: 3 12 19 27 41 52 | 8   # ghi chú
const MAU_DONG = /^\d{4}-\d{2}-\d{2}\s*\|\s*[A-Za-z_0-9/]{2,12}\s*:\s*[\d\s,;|@]{1,80}(#.{0,80})?$/;

function ghApi(duong) {
  return `https://api.github.com/repos/${CHU_REPO}/${TEN_REPO}${duong}`;
}

function dauGh(token) {
  return {
    Authorization: `Bearer ${token}`,
    Accept: "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "vietlott-thongke",
    "Content-Type": "application/json",
  };
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ loi: "Chỉ nhận POST" });
  }

  const matKhauThat = process.env.MAT_KHAU;
  const token = process.env.GITHUB_TOKEN;
  if (!matKhauThat || !token) {
    return res.status(500).json({
      loi: "Máy chủ chưa được cài đặt. Thiếu MAT_KHAU hoặc GITHUB_TOKEN trong Vercel.",
    });
  }

  let than = req.body;
  if (typeof than === "string") {
    try { than = JSON.parse(than); } catch { than = {}; }
  }
  const { matKhau, dong, viec } = than || {};
  const laXoa = viec === "xoa";

  if (typeof matKhau !== "string" || matKhau !== matKhauThat) {
    return res.status(401).json({ loi: "Mật khẩu không đúng." });
  }

  if (typeof dong !== "string" || !dong.trim()) {
    return res.status(400).json({ loi: "Thiếu dòng vé." });
  }
  const dongSach = dong.trim();
  // Khi ghi thêm thì phải đúng khuôn. Khi xoá thì chỉ cần khớp nguyên văn dòng đã có.
  if (!laXoa && !MAU_DONG.test(dongSach)) {
    return res.status(400).json({
      loi: "Dòng vé không đúng khuôn. Mẫu: 2026-08-24 | power: 3 12 19 27 41 52",
    });
  }

  try {
    // 1. Đọc sổ hiện tại (cần sha để ghi đè đúng bản)
    const doc = await fetch(ghApi(`/contents/${DUONG_DAN_SO}?ref=${NHANH}`), {
      headers: dauGh(token),
      cache: "no-store",
    });
    if (!doc.ok) {
      const t = await doc.text();
      return res.status(502).json({
        loi: `Không đọc được sổ vé trên GitHub (mã ${doc.status}). Token có quyền Contents chưa?`,
        chi_tiet: t.slice(0, 200),
      });
    }
    const jsDoc = await doc.json();
    const noiDungCu = Buffer.from(jsDoc.content, "base64").toString("utf-8");

    let noiDungMoi;
    if (laXoa) {
      // Xoá đúng MỘT dòng khớp nguyên văn (nếu có dòng trùng nhau thì bỏ dòng đầu tiên)
      const cacDong = noiDungCu.split(/\r?\n/);
      const vt = cacDong.findIndex((d) => d.trim() === dongSach);
      if (vt < 0) {
        return res.status(404).json({
          loi: "Không tìm thấy vé này trong sổ. Trang có thể đang cũ — tải lại rồi thử lại.",
        });
      }
      cacDong.splice(vt, 1);
      noiDungMoi = cacDong.join("\n");
      if (!noiDungMoi.endsWith("\n")) noiDungMoi += "\n";
    } else {
      // Đã có dòng y hệt thì thôi, khỏi ghi trùng
      if (noiDungCu.split(/\r?\n/).some((d) => d.trim() === dongSach)) {
        return res.status(200).json({
          ok: true, trung: true, thong_bao: "Vé này đã có trong sổ rồi.",
        });
      }
      noiDungMoi =
        (noiDungCu.endsWith("\n") || noiDungCu === "" ? noiDungCu : noiDungCu + "\n") +
        dongSach + "\n";
    }

    // 2. Ghi vào sổ
    const ghi = await fetch(ghApi(`/contents/${DUONG_DAN_SO}`), {
      method: "PUT",
      headers: dauGh(token),
      body: JSON.stringify({
        message: laXoa ? "Xoa ve tu trang web" : "Ghi ve tu trang web",
        content: Buffer.from(noiDungMoi, "utf-8").toString("base64"),
        sha: jsDoc.sha,
        branch: NHANH,
      }),
    });
    if (!ghi.ok) {
      const t = await ghi.text();
      return res.status(502).json({
        loi: `Không ${laXoa ? "xoá" : "ghi"} được (mã ${ghi.status}).`,
        chi_tiet: t.slice(0, 200),
      });
    }

    // 3. Kích workflow dựng lại trang. Bước này hỏng thì vé VẪN đã vào sổ,
    //    chỉ là trang chờ tới lượt chạy theo lịch mới hiện.
    let daKich = false;
    try {
      const kich = await fetch(
        ghApi(`/actions/workflows/${TEN_WORKFLOW}/dispatches`),
        { method: "POST", headers: dauGh(token), body: JSON.stringify({ ref: NHANH }) }
      );
      daKich = kich.ok;
    } catch { /* bỏ qua */ }

    return res.status(200).json({
      ok: true,
      da_kich_workflow: daKich,
      thong_bao: laXoa
        ? (daKich
            ? "Đã xoá khỏi sổ. Khoảng 2 phút nữa trang cập nhật."
            : "Đã xoá khỏi sổ. Trang sẽ cập nhật ở lần chạy tự động kế tiếp.")
        : (daKich
            ? "Đã ghi vào sổ. Khoảng 2 phút nữa trang sẽ hiện vé này."
            : "Đã ghi vào sổ. Trang sẽ hiện vé ở lần cập nhật tự động kế tiếp."),
    });
  } catch (e) {
    return res.status(500).json({ loi: "Lỗi máy chủ: " + String(e).slice(0, 200) });
  }
}
