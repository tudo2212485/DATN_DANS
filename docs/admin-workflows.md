# Các chức năng quản trị

## Khởi chạy

Tại thư mục `backend`, dùng `venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000`.
Tại thư mục gốc dự án, dùng `npm run dev`. Giao diện: http://localhost:3000/dashboard/overview.

Backend tự bổ sung cột `users.is_active` còn thiếu trên CSDL cũ và tạo bảng cấu hình/tác vụ. Không chạy lại `database/init.sql` để nâng cấp: file đó dùng cho khởi tạo và có lệnh xóa bảng.

## Tổng quan và tài khoản

- Tổng quan đọc số bản ghi trực tiếp từ PostgreSQL. Khi API lỗi, giao diện hiển thị lỗi.
- Đăng nhập được kiểm tra lại qua `/auth/me`. Admin quản lý tài khoản; analyst được xem tổng quan, dữ liệu và mô hình.
- Khóa tài khoản thay đổi `is_active`, đồng thời chặn cả token đang có. Mở khóa giữ vai trò cũ.
- Admin không thể tự khóa hoặc tự hạ quyền. Đăng ký công khai chỉ tạo vai trò `user`.
- Đường dẫn cũ `/admin` chuyển tới dashboard.

## Dữ liệu giá

- Lọc theo nông sản, ngày bắt đầu và ngày kết thúc; phân trang 30 bản ghi.
- Thêm/cập nhật giá theo cặp nông sản–ngày; sửa giá trên hàng được chọn giữ nguyên cặp định danh này.
- CSV dùng UTF-8; cột bắt buộc: `commodity_id` hoặc `commodity_code`, `record_date` (YYYY-MM-DD), `price`.
- Cột tùy chọn: `price_min`, `price_max`, `volume`, `source`. Giá dùng đúng đơn vị trong danh mục nông sản.
- Giá trị âm, không hữu hạn, ngày tương lai và cận giá sai bị từ chối. Mỗi dòng CSV lỗi được báo riêng; các dòng hợp lệ vẫn được lưu. Ngày trùng được cập nhật.
- Export gửi token đăng nhập và áp dụng cùng bộ lọc ngày/nông sản.

## Thu thập lịch sử

Chi tiết luồng mới: [history-to-forecast.md](history-to-forecast.md). Trang xem lịch sử công khai: `/history`.

Nguồn đã tích hợp: giá cà phê trung bình công bố tại
`https://giacaphe.com/gia-ca-phe-noi-dia-ngay-YYYY-MM-DD/`.

- Phạm vi 7/30/90/365 ngày tính tới ngày chạy. Scraper kiểm tra ngày trên trang, đơn vị VNĐ/kg và giá trung bình.
- Giữ nguyên bản ghi có nguồn đã thu thập/xác nhận. Với bản ghi cũ chưa xác minh, lưu bản gốc vào `price_revisions` trước khi cập nhật từ nguồn. Không tự sinh giá khi thiếu nguồn.
- Lưu URL nguồn theo từng bản ghi. Nguồn bị lỗi được báo `FAILED` hoặc `PARTIAL`, không thay bằng dữ liệu mẫu.
- Lúa gạo, hồ tiêu và mía đường hiện nhập lịch sử qua CSV; chưa có nguồn thu thập tự động được xác minh cho ba loại này.
- Các bản ghi có sẵn trước đợt sửa có thể là dữ liệu mẫu/mô phỏng. Việc kết nối PostgreSQL không xác nhận tính thực tế của dữ liệu cũ; cần kiểm tra nguồn trước khi dùng cho báo cáo nghiên cứu.

## Mô hình và tác vụ

- Huấn luyện lại chạy năm mô hình: Random Forest, XGBoost, Prophet, ARIMA, LSTM, cho nông sản được chọn.
- Cần ít nhất 60 ngày có quan sát đã thu thập/được admin xác nhận; khoảng trống tối đa 7 ngày. Ngày thiếu được điền bằng giá đã biết gần nhất và không tính vào điểm kiểm thử.
- Lưu 30 điểm dự báo mỗi mô hình thành công. Ngày đầu dự báo là ngày sau mốc lịch sử cuối.
- Năm mô hình đánh giá trên cùng đoạn kiểm thử cuối theo phương pháp nhiều bước; có mốc đối chiếu giữ nguyên giá cuối cùng. Chỉ so sánh cùng lần huấn luyện và dữ liệu đầu vào, giữ R² âm. Nhãn RMSE thấp nhất chỉ chọn một hàng.
- Chọn mô hình mặc định được lưu trong PostgreSQL và áp dụng cho `/api/v1/forecast` khi không truyền `model_name`. Lựa chọn mô hình tường minh của người xem có ưu tiên hơn mặc định.
- Trạng thái và tiến độ từng bước của tác vụ lưu trong `background_jobs`; giao diện kiểm tra lại định kỳ. Chỉ chạy một tác vụ thu thập/huấn luyện tại một thời điểm.
- Khi khởi động lại máy chủ, tác vụ chưa hoàn tất được đánh dấu gián đoạn. Cấu hình local dùng một tiến trình Uvicorn.
- Dải dự báo hiện là ước lượng của mô hình; các dải dựa trên RMSE chưa được kiểm chứng độ bao phủ 95% trên dữ liệu thực tế.

## Kiểm thử

Tại thư mục `backend`, chạy `venv\Scripts\python.exe -m pytest -q`.
Test dùng SQLite trong bộ nhớ và thư mục mô hình tạm, không huấn luyện vào tệp mô hình thật hoặc ghi vào PostgreSQL.
Frontend: `npm run build` tại thư mục gốc dự án.
