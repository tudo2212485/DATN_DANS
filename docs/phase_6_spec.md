# Phase 6 Specification: Public User UI (Giao Diện Nông Dân & Thương Lái)

## 1. Mục Tiêu (Objective)
Xây dựng giao diện công khai (Public Interface) tại trang chủ `/` giúp người nông dân, thương lái và người tiêu dùng tra cứu giá nông sản/hàng hóa nhanh chóng, trực quan, không phức tạp, tối ưu hóa cho thiết bị di động (Mobile Responsive).

## 2. Kiến Trúc Trang Public UI (`src/app/(public)`)

```text
src/app/(public)/
├── page.tsx                  # Trang chủ (Bảng giá nhanh, Tìm kiếm, Banner biến động)
├── commodities/
│   └── [id]/page.tsx        # Trang chi tiết 1 loại hàng hóa (Biểu đồ lịch sử + Dự báo AI)
└── compare/page.tsx          # Trang so sánh giá giữa các vùng miền / nông sản
```

## 3. Đặc Tả Chi Tiết Giao Diện Người Dùng

### 3.1 Trang Chủ Tra Cứu (`/`)
- **Thanh Tìm Kiếm Nhanh (Quick Search):** Cho phép gõ tên nông sản (VD: "Gạo ST25", "Cà phê", "Thịt heo") hoặc chọn theo tỉnh thành/vùng miền.
- **Bảng Giá Vùng Miền (`RegionalPriceTable.tsx`):**
  - Hiển thị danh sách giá hiện tại, mức tăng/giảm so với hôm qua (màu xanh/đỏ trực quan).
  - Phân loại rõ ràng: Nông sản, Năng lượng, Kim loại, Gia súc.
- **Highlight Card (Mặt Hàng Biến Động Nóng):** Hiển thị 3 mặt hàng có sự thay đổi giá lớn nhất trong ngày để nông dân kịp thời nắm bắt.

### 3.2 Trang Chi Tiết Hàng Hóa & Dự Báo AI (`/commodities/[id]`)
- **Biểu Đồ Xu Hướng Giá (Interactive Chart):**
  - Đường màu xanh: Giá lịch sử thực tế trong quá khứ.
  - Đường nét đứt màu cam: Dự báo giá của AI trong 7 - 30 ngày tới.
  - Khoảng mờ (Upper/Lower Bound): Khoảng dao động giá dự kiến.
- **Khuyến Nghị Thông Minh (AI Insight Summary):**
  - Hiển thị dòng tóm tắt dễ hiểu cho nông dân, ví dụ: *"Dự báo: Giá lúa ST25 có xu hướng tăng nhẹ 2% trong 5 ngày tới do nhu cầu xuất khẩu tăng."*

### 3.3 Thiết Kế Trải Nghiệm Người Dùng (UX for Farmers)
- **Mobile First Design:** Nông dân thường xem giá trên điện thoại ngay tại đồng ruộng -> Giao diện phải gọn nhẹ, chữ to, dễ thao tác bằng 1 tay.
- **Tốc độ tải trang nhanh:** Tối ưu hình ảnh và cache dữ liệu API để trang nạp dưới 1.5 giây.

## 4. Kiểm Thử & Nghiệm Thu
- [ ] Kiểm thử hiển thị hoàn hảo trên các thiết bị: iPhone, Android Phone, Tablet, Laptop.
- [ ] Kiểm thử tính năng tìm kiếm và lọc dữ liệu giá không bị giật lag.
- [ ] Đo đạc hiệu năng Lighthouse trên Mobile đạt tối thiểu 90 điểm.
