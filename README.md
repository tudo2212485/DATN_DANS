# DA_TN - Nhật ký Cập nhật

Dưới đây là tổng hợp các thay đổi và công việc đã thực hiện trong dự án:

## 1. Cấu trúc thư mục & Tài nguyên tĩnh
- Đã tạo thư mục `frontend/public` (do Next.js yêu cầu để chứa tài nguyên tĩnh).
- Đã thêm tệp ảnh logo (`logo.png`) vào thư mục `public` để sử dụng cho toàn dự án.

## 2. Cập nhật Giao diện (UI)
- **Tệp chỉnh sửa**: `frontend/src/components/layout/Sidebar.tsx`
- **Chi tiết thay đổi**:
  - Tích hợp component `<Image>` của Next.js để tối ưu hóa việc tải ảnh logo.
  - Thay thế biểu tượng mặc định (`Sprout` của thư viện `lucide-react`) bằng ảnh logo mới (`logo.png`).
  - Tinh chỉnh các CSS class: thêm nền trắng (`bg-white`), padding (`p-1`), và đặt `object-contain` để logo hiển thị gọn gàng, đẹp mắt trên thanh Sidebar.

## 3. Khởi động môi trường phát triển (Local)
- Đã sửa lỗi không tìm thấy `package.json` khi chạy `npm run dev` bằng cách di chuyển đúng vào thư mục `frontend` để khởi động server.
- Server hiện đang được chạy thành công trên máy ở chế độ nền.
