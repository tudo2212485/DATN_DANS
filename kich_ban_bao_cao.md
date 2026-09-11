# Kịch bản Báo cáo Đồ án Tốt nghiệp: Hệ thống AgroForecast

**Thời gian dự kiến:** 5 - 10 phút
**Người trình bày:** [Tên của bạn]

---

## 1. Lời chào & Đặt vấn đề (1 phút)
- **Kính chào:** "Kính chào quý thầy cô trong hội đồng bảo vệ đồ án. Em là [Tên], sau đây em xin phép trình bày về đồ án tốt nghiệp với đề tài: **Xây dựng hệ thống dự báo giá nông sản AgroForecast ứng dụng học máy**."
- **Vấn đề:** "Hiện nay, giá cả nông sản (như lúa gạo, cà phê, tiêu) thường biến động thất thường, gây khó khăn cho người nông dân và doanh nghiệp trong việc lên kế hoạch sản xuất kinh doanh."
- **Giải pháp:** "Do đó, em đã xây dựng hệ thống **AgroForecast**. Hệ thống giúp thu thập dữ liệu giá tự động, phân tích xu hướng và sử dụng AI (Mô hình LSTM) để dự báo giá trong tương lai, đồng thời gửi cảnh báo khi giá chạm ngưỡng."

## 2. Kiến trúc & Công nghệ (1 phút)
- **Frontend:** Next.js (React), TailwindCSS, Recharts (giao diện Minimalist Warm Light thân thiện, dễ nhìn).
- **Backend:** FastAPI (Python), PostgreSQL, SQLAlchemy.
- **AI/ML:** PyTorch (mô hình LSTM đa biến) để huấn luyện và dự báo.
- **Data Pipeline:** Selenium/BeautifulSoup để cào dữ liệu tự động hằng ngày.

## 3. Demo Các tính năng chính (3-5 phút)
*(Vừa nói vừa thao tác trực tiếp trên web)*

- **Trang Tổng quan (Dashboard):** 
  "Đây là màn hình chính. Nó cung cấp ngay bức tranh toàn cảnh về thị trường với các chỉ số quan trọng, giá hiện tại và biểu đồ xu hướng 30 ngày gần nhất."
- **Trang Dự báo & Mô hình:** 
  "Tiếp theo là phần cốt lõi của hệ thống. Tại đây hiển thị kết quả dự báo của mô hình AI cho 7-30 ngày tới. Mọi người có thể thấy đường giá thực tế (màu sậm) và đường dự báo (màu đứt nét), kèm theo các chỉ số sai số (RMSE, MAPE) thể hiện độ chính xác."
- **Hệ thống Cảnh báo (Alerts):** 
  "Người dùng có thể cài đặt ngưỡng giá. Khi hệ thống thu thập dữ liệu mới, nếu giá thị trường vượt ngưỡng, hệ thống sẽ tự động gửi email cảnh báo."
- **Trang Quản trị (Dành cho Admin):** 
  "Về phần quản trị, do định hướng của em trong đồ án này là tập trung nghiên cứu **quy trình thu thập (cào) dữ liệu thực tế từ trên mạng** và làm sạch dữ liệu, nên vai trò của Admin hiện tại được thiết kế chủ yếu để giám sát Data Pipeline. Cụ thể, Admin có thể theo dõi tiến trình cào dữ liệu (Crawler Logs), quản lý các tập dữ liệu thô và kích hoạt huấn luyện lại mô hình (Retrain) khi có dữ liệu mới, thay vì đi sâu vào các tính năng quản trị người dùng phức tạp."

## 4. Kết luận & Hướng phát triển (1 phút)
- **Kết quả đạt được:** "Hệ thống đã hoạt động ổn định, dự báo bám sát được chu kỳ giá cơ bản của nông sản, giao diện trực quan, tính ứng dụng cao."
- **Hạn chế & Hướng phát triển:** "Trong tương lai, em dự kiến tích hợp thêm các yếu tố bên ngoài (như thời tiết, giá xăng dầu, tỷ giá) vào mô hình để tăng độ chính xác, và mở rộng thêm các loại nông sản khác."

## 5. Lời cảm ơn
- "Em xin chân thành cảm ơn thầy/cô [Tên GVHD] đã tận tình hướng dẫn em hoàn thành đồ án này. Cảm ơn quý thầy cô trong hội đồng đã lắng nghe. Em xin phép mời quý thầy cô đặt câu hỏi ạ."
