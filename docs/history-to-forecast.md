# Luồng lịch sử → dự báo

## Sử dụng

1. Mở `/history` từ menu **Lịch sử giá**. Chọn nông sản, ngày bắt đầu/kết thúc.
2. Admin bấm **Thu thập khoảng đã chọn**. Tác vụ lưu tiến độ và lỗi vào PostgreSQL. Người xem không cần đăng nhập để tra cứu lịch sử.
3. Xem bảng, biểu đồ, nguồn, ngày thiếu và trạng thái dữ liệu. Mặc định không hiển thị dữ liệu chưa xác minh; có thể bật để đối chiếu.
4. Khi đủ điều kiện, bấm **Huấn luyện từ toàn bộ lịch sử đủ điều kiện**. Khoảng đang lọc chỉ giới hạn phần xem/thu thập, không cắt dữ liệu huấn luyện.
5. Bấm **Xem dự báo**: chọn mô hình và 7/14/30 ngày sau ngày lịch sử cuối. Phần giải thích nêu khoảng đầu vào, thời điểm huấn luyện, tập kiểm thử, RMSE của mô hình đối chiếu và độ cũ của dữ liệu.

## Nguồn Việt Nam được tích hợp

| Nông sản | Nguồn khảo sát | Khả năng sử dụng |
|---|---|---|
| Cà phê | [Giacaphe, bảng giá theo ngày](https://giacaphe.com/gia-ca-phe-noi-dia-ngay-2026-09-11/) | Giá Robusta nội địa theo ngày. Nguồn giới hạn lịch sử xa nếu không đăng nhập nên tác vụ có thể hoàn thành một phần. |
| Hồ tiêu | [AGROINFO – CSDL giá nông sản](https://agro.gov.vn/vn/nguonwmy.aspx) | Thu đúng `Hạt tiêu đen trong nước`, thị trường `Đắk Lắk`, loại giá `Bán buôn`, đơn vị `VND/kg`. |
| Lúa IR50404 | [AGROINFO – CSDL giá nông sản](https://agro.gov.vn/vn/nguonwmy.aspx) | Thu đúng `Lúa IR 50404 - lúa tươi`, thị trường `An Giang`, loại giá `Bán tại hộ`, đơn vị `VND/kg`. Nguồn không công bố đủ mọi ngày. |
| Mía đường | [Bộ Công Thương – giá nông sản Phú Yên](https://thuongmaibiengioimiennui.gov.vn/gia-hang-hoa/2024/2/tham-khao-gia-ca-thi-truong-nong-san-tai-phu-yen) | Báo cáo theo kỳ cho `Mía (từ 7 – 10 chữ đường)` tại Tây Hòa, Phú Yên, đơn vị đồng/tấn. Hệ thống lưu riêng giá mua và giá bán, giữ nguyên kỳ báo cáo. |

AGROINFO là nguồn ASP.NET phân trang; bộ thu thập gửi đúng bộ lọc ngày, sản phẩm, thị trường và loại giá, sau đó kiểm tra lại từng dòng trước khi lưu. Nếu nguồn đổi nhãn, cột, đơn vị hoặc trả trùng ngày với giá khác nhau, tác vụ dừng thay vì đoán dữ liệu. Chọn 365 ngày không có nghĩa sẽ có đủ 365 quan sát vì nguồn có thể không công bố giá mỗi ngày.

Mía hiện chỉ có báo cáo giá theo kỳ. Các bản ghi này nằm ở `periodic_prices` và xuất CSV theo kỳ; hệ thống không sao chép một báo cáo thành nhiều ngày và chưa cho huấn luyện dự báo ngày từ chuỗi này. Muốn dự báo mía theo ngày cần thêm nguồn Việt Nam công bố nhất quán ít nhất 60 quan sát ngày.

## Nguồn gốc dữ liệu

- `price_history.provenance`: `collected` (đọc đúng ngày và đơn vị từ nguồn), `reviewed` (admin đã đối chiếu), `unverified` (mặc định cho dữ liệu cũ).
- Chỉ `collected` và `reviewed` được dùng huấn luyện. Tất cả dữ liệu cũ giữ trạng thái chưa xác minh khi nâng cấp, kể cả dòng có tên nguồn giống nguồn chính thức.
- Khi scraper gặp ngày đã có `unverified`, lưu bản gốc vào `price_revisions` rồi thay bằng quan sát đọc được. Nếu có dữ liệu đã thu thập/xác nhận thì giữ nguyên, không tạo trùng ngày.
- Nhập CSV: `commodity_code` hoặc `commodity_id`, `record_date`, `price`, `source`; thêm `reviewed=true` chỉ sau khi admin đã đối chiếu nguồn. Không có cột này thì mặc định chưa xác minh. CSV có giá giả không trở thành dữ liệu thực tế chỉ vì được nhập vào CSDL.
- Form sửa giá có ô xác nhận. Sửa dữ liệu chưa xác nhận lại sẽ đưa bản ghi về `unverified`; bản trước sửa được lưu để đối chiếu.
- Mỗi lần huấn luyện lưu bản chụp đầu vào và mã SHA-256 ở `training_runs`. API `/api/v1/history/training-runs/{id}` trả bản chụp này.
- Cập nhật định kỳ lúc 18:00 giờ Việt Nam, kiểm tra lại 7 ngày gần nhất khi backend đang chạy. Không cần trình duyệt mở; backend phải hoạt động.

## Đánh giá và tạo dự báo

- Dùng đoạn công bố mới nhất sau khoảng gián đoạn dài trên 30 ngày; các điểm cũ vẫn được giữ để tra cứu nhưng không nối qua khoảng trống lớn. Đoạn huấn luyện cần tối thiểu 60 quan sát và không có khoảng thiếu liên tiếp quá 14 ngày (đủ bao quát kỳ nghỉ dài như Tết). Đây là ngưỡng vận hành tối thiểu, không khẳng định độ chính xác cao.
- Sắp theo ngày, giữ một quan sát/ngày, điền khoảng thiếu bằng giá gần nhất đã biết. Không điền ngược từ tương lai.
- Giữ lại 15% ngày quan sát cuối, tối thiểu 7 và tối đa 30 ngày quan sát. Năm mô hình cùng được đánh giá nhiều bước từ cùng một mốc; không đọc giá thực tế của đoạn kiểm thử khi dự báo.
- RMSE/MAE/MAPE/R² chỉ tính trên ngày có quan sát, không chấm điểm trên giá điền. Giữ nguyên R² âm.
- Mốc đối chiếu là giá cuối tập huấn luyện được giữ nguyên cho toàn bộ đoạn kiểm thử, tương ứng dự báo nhiều bước. Chỉ so sánh các mô hình thuộc cùng lần huấn luyện và cùng đầu vào.
- Sau đánh giá, huấn luyện lại trên toàn bộ lịch sử đủ điều kiện rồi lưu 30 giá dự báo. Đầu ra này được lưu trong CSDL; luồng mới không phụ thuộc các tệp mô hình cũ.
- Dải ±1,96 RMSE chỉ là ước lượng, chưa kiểm chứng độ bao phủ 95% và không phải cam kết giá.
- Nếu dữ liệu có nguồn thay đổi, dự báo trước đó trả HTTP 409 yêu cầu huấn luyện lại. Dự báo cũ không có bản chụp đầu vào cũng không được phục vụ như kết quả hợp lệ.

## Kiểm chứng

Tại thư mục `backend`, chạy `venv/Scripts/python.exe -m pytest -q`.
Kiểm thử dùng CSDL SQLite và dữ liệu fixture, bao gồm chạy thực tế cả năm thuật toán, tách tập theo thời gian, chống dùng dữ liệu chưa xác minh, nguồn yêu cầu đăng nhập và vô hiệu hóa dự báo khi lịch sử thay đổi.

Frontend kiểm tra bằng `npm run build`. Bản chạy local kết nối PostgreSQL. Để nghiệm thu dự báo từ giá thị trường thực tế, phải thu thập hoặc nhập đủ lịch sử có nguồn; không dùng bộ dữ liệu fixture hay dữ liệu seed để thay thế phần này.

Kiểm chứng thực tế ngày 16/09/2026:

- Cà phê: nguồn cho đọc 14 ngày quan sát từ 31/08 đến 15/09 rồi chặn lịch sử xa; `ready=false` (14/60), dự báo cũ trả HTTP 409.
- Lúa IR50404: thu 112 quan sát AGROINFO nhưng các đợt công bố rời rạc; đoạn mới nhất sau khoảng gián đoạn dài chỉ có 2 quan sát nên khóa huấn luyện.
- Hồ tiêu: thu 132 quan sát AGROINFO. Đoạn liên tục mới nhất giữ 128 quan sát từ 20/11/2025 đến 14/09/2026 và loại 4 điểm trước khoảng ngừng công bố 311 ngày khỏi đầu vào. Đã huấn luyện năm mô hình và lưu 150 điểm dự báo (30 ngày/mô hình).
- Mía: lưu đúng hai kỳ báo cáo năm 2024 trong `periodic_prices`; chưa dự báo ngày do không có đủ chuỗi ngày nhất quán từ nguồn Việt Nam.
