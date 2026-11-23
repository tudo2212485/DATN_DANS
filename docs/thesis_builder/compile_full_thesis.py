# -*- coding: utf-8 -*-
"""
Trình biên dịch hoàn chỉnh Khóa luận Tốt nghiệp Kỹ sư Công nghệ Thông tin
Trường Đại học Đà Lạt - Khoa Công Nghệ Thông Tin
Tạo đồng thời:
1. Tập tin Word (.docx) chuẩn quy định (Times New Roman 13pt, 1.5 lines, A4, lề chuẩn, 75-100 trang nội dung chính)
2. Tập tin Markdown (.md) toàn văn
3. Cấu trúc thư mục nộp đĩa DVD (THESIS/, HUONG_DAN_SU_DUNG_DIA_DVD.txt)
"""
import os
import math
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

from build_thesis import (
    set_run_font,
    add_styled_paragraph,
    add_footer_page_number,
    add_formatted_table,
    build_enriched_chapters,
)
from part1_front_and_ch1 import FRONT_MATTER, ABBREVIATIONS, MO_DAU_SECTIONS
from part4_ch4_and_end import (
    KET_LUAN_PARAGRAPHS,
    HUONG_PHAT_TRIEN_PARAGRAPHS,
    REFERENCES_LIST,
)
from part8_code_and_security_walkthrough import APPENDIX_CONTENT
from part9_comprehensive_elaboration import (
    USE_CASE_DETAILED_SPECS,
    SCRAPER_AND_PIPELINE_MODULE_SPECS,
)
from part10_module_by_module_specs import BACKEND_AND_ML_MODULE_SPECS


def inject_all_elaborations(chapters):
    """Gắn kết toàn bộ các phần phân tích chuyên sâu vào 4 chương để đạt chuẩn 80-90 trang A4"""
    ch1, ch2, ch3, ch4 = chapters

    # Bổ sung phân tích chuyên sâu các mô-đun thu thập dữ liệu Việt Nam vào Chương 2.4
    for idx, (title, paras) in enumerate(SCRAPER_AND_PIPELINE_MODULE_SPECS, start=4):
        ch2["sections"][3]["subsections"].append(
            {"code": f"2.4.{idx}.", "title": title, "paragraphs": paras}
        )

    # Bổ sung đặc tả chi tiết từng Use Case (UC-01 -> UC-11) vào Chương 3.1
    for idx, (title, paras) in enumerate(USE_CASE_DETAILED_SPECS, start=4):
        ch3["sections"][0]["subsections"].append(
            {"code": f"3.1.{idx}.", "title": title, "paragraphs": paras}
        )

    # Bổ sung đặc tả chi tiết các mô-đun dịch vụ Backend vào Chương 3.2
    ch3["sections"][1]["subsections"].append(
        {
            "code": "3.2.7.",
            "title": BACKEND_AND_ML_MODULE_SPECS[0][0],
            "paragraphs": BACKEND_AND_ML_MODULE_SPECS[0][1],
        }
    )
    return chapters


def render_front_matter(doc):
    # 1. Bìa chính (Mẫu M01)
    add_styled_paragraph(doc, FRONT_MATTER["university"], 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0)
    add_styled_paragraph(doc, FRONT_MATTER["faculty"], 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0)
    add_styled_paragraph(doc, "---oOo---", 13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=36)
    add_styled_paragraph(doc, "(Mẫu M01 - Bìa chính khóa luận in chữ nhũ vàng trên bìa xanh nước biển)", 11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=24)
    add_styled_paragraph(doc, FRONT_MATTER["student_name"], 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=48)
    add_styled_paragraph(doc, FRONT_MATTER["thesis_title"], 16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=60)
    add_styled_paragraph(doc, FRONT_MATTER["degree_title"], 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=90)
    add_styled_paragraph(doc, FRONT_MATTER["location_year"], 13, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0)
    doc.add_page_break()

    # 2. Trang phụ bìa (Mẫu M02)
    add_styled_paragraph(doc, FRONT_MATTER["university"], 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0)
    add_styled_paragraph(doc, FRONT_MATTER["faculty"], 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0)
    add_styled_paragraph(doc, "---oOo---", 13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=30)
    add_styled_paragraph(doc, "(Mẫu M02 - Trang phụ bìa khóa luận)", 11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=24)
    add_styled_paragraph(doc, f"{FRONT_MATTER['student_name']} – {FRONT_MATTER['student_id']}", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=36)
    add_styled_paragraph(doc, FRONT_MATTER["thesis_title"], 16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=42)
    add_styled_paragraph(doc, FRONT_MATTER["degree_title"], 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=42)
    add_styled_paragraph(doc, "GIÁO VIÊN HƯỚNG DẪN", 13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=6)
    add_styled_paragraph(doc, FRONT_MATTER["advisor"], 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=60)
    add_styled_paragraph(doc, FRONT_MATTER["location_year"], 13, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0)
    doc.add_page_break()

    # 3. Trang nhận xét của GVHD (Mẫu M04)
    add_styled_paragraph(doc, "NHẬN XÉT CỦA GIÁO VIÊN HƯỚNG DẪN", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=18)
    for _ in range(18):
        add_styled_paragraph(doc, "." * 92, 13, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=2, space_after_pt=2)
    add_styled_paragraph(doc, "Đà Lạt, ngày ..... tháng ...... năm 2026", 13, italic=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0, space_before_pt=12)
    add_styled_paragraph(doc, "Giáo viên hướng dẫn", 13, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0)
    add_styled_paragraph(doc, "[Ký tên và ghi rõ họ tên]", 12, italic=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0)
    doc.add_page_break()

    # 4 & 5. Trang nhận xét của GVPB 1 & 2 (Mẫu M05)
    for pb_idx, note_line in [
        (1, "Khóa luận đáp ứng yêu cầu của Khóa luận kỹ sư Công nghệ thông tin."),
        (2, "Khóa luận đáp ứng yêu cầu trình độ kỹ sư Công nghệ thông tin."),
    ]:
        add_styled_paragraph(doc, f"NHẬN XÉT CỦA GIÁO VIÊN PHẢN BIỆN {pb_idx}", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=18)
        for _ in range(16):
            add_styled_paragraph(doc, "." * 92, 13, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=2, space_after_pt=2)
        add_styled_paragraph(doc, note_line, 13, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=8)
        add_styled_paragraph(doc, "Đà Lạt, ngày ..... tháng ...... năm 2026", 13, italic=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0, space_before_pt=8)
        add_styled_paragraph(doc, "Giáo viên phản biện", 13, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0)
        add_styled_paragraph(doc, "[Ký tên và ghi rõ họ tên]", 12, italic=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0)
        doc.add_page_break()

    # 6. Trang cam đoan
    add_styled_paragraph(doc, "LỜI CAM ĐOAN", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=18)
    add_styled_paragraph(doc, "Tôi xin cam đoan toàn bộ nội dung trình bày trong cuốn Khóa luận tốt nghiệp 'Nghiên cứu và xây dựng hệ thống dự đoán biến động giá nông sản Việt Nam bằng mô hình học máy' (AgroForecast) là công trình nghiên cứu và thực nghiệm của cá nhân tôi dưới sự hướng dẫn khoa học của Giáo viên hướng dẫn.")
    add_styled_paragraph(doc, "Toàn bộ số liệu lịch sử giá của 8 mặt hàng nông sản tại 29 địa phương bán tại vườn/ruộng, kết quả thực nghiệm huấn luyện và đánh giá sai số của 5 mô hình học máy (LSTM, Prophet, ARIMA, XGBoost, Random Forest) cùng kết quả thực thi 72 kịch bản kiểm thử tự động và kiểm tra bảo mật OWASP Top 10 được nêu trong khóa luận là hoàn toàn trung thực, khách quan, xuất phát trực tiếp từ mã nguồn và cơ sở dữ liệu thực tế của dự án.")
    add_styled_paragraph(doc, "Các tài liệu tham khảo, công trình nghiên cứu và nguồn dữ liệu trích dẫn trong khóa luận đều được ghi rõ nguồn gốc theo đúng quy định của Khoa Công nghệ Thông tin – Trường Đại học Đà Lạt. Tôi xin chịu hoàn toàn trách nhiệm trước Khoa và Nhà trường về lời cam đoan này.")
    add_styled_paragraph(doc, "Đà Lạt, ngày ..... tháng ...... năm 2026", 13, italic=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0, space_before_pt=24)
    add_styled_paragraph(doc, "Sinh viên thực hiện", 13, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0)
    add_styled_paragraph(doc, FRONT_MATTER["student_name"], 13, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0)
    doc.add_page_break()

    # 7. Lời cám ơn
    add_styled_paragraph(doc, "LỜI CÁM ƠN", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=18)
    add_styled_paragraph(doc, "Trước hết, em xin bày tỏ lòng biết ơn sâu sắc và chân thành nhất đến Ban Giám hiệu Trường Đại học Đà Lạt cùng toàn thể quý Thầy, Cô giáo trong Khoa Công nghệ Thông tin đã tận tình giảng dạy, truyền đạt cho em những kiến thức nền tảng và chuyên sâu quý báu về Kỹ thuật Phần mềm, Khoa học Dữ liệu, Trí tuệ Nhân tạo và An toàn Thông tin trong suốt những năm học tập dưới mái trường Đại học Đà Lạt.")
    add_styled_paragraph(doc, "Đặc biệt, em xin gửi lời tri ân sâu sắc nhất đến Giáo viên hướng dẫn – người đã luôn tận tâm định hướng phương pháp nghiên cứu khoa học, đóng góp những ý kiến chuyên môn vô cùng sắc bén về mô hình hóa giá nông sản bán tại vườn/ruộng theo địa phương cũng như yêu cầu nghiêm ngặt về quy trình kiểm thử phần mềm và kiểm tra bảo mật hệ thống để em hoàn thiện khóa luận này.")
    add_styled_paragraph(doc, "Cuối cùng, con xin cảm ơn gia đình, người thân và bạn bè đã luôn động viên, tạo mọi điều kiện thuận lợi nhất để con hoàn thành tốt Khóa luận tốt nghiệp Kỹ sư Công nghệ Thông tin.")
    doc.add_page_break()

    # 8. Đề cương nghiên cứu KLTN (Mẫu M06)
    add_styled_paragraph(doc, "Trường Đại học Đà Lạt", 13, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_after_pt=0)
    add_styled_paragraph(doc, "Khoa Công Nghệ Thông Tin", 13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_after_pt=12)
    add_styled_paragraph(doc, "ĐỀ CƯƠNG NGHIÊN CỨU KHÓA LUẬN TỐT NGHIỆP (Mẫu M06)", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=12)
    add_styled_paragraph(doc, f"• Tên Đề Tài: {FRONT_MATTER['thesis_title']}", 13, bold=True, first_line_indent_cm=0)
    add_styled_paragraph(doc, f"• Chuyên ngành: {FRONT_MATTER['major']}", 13, first_line_indent_cm=0)
    add_styled_paragraph(doc, f"• Sinh viên thực hiện: {FRONT_MATTER['student_name']} – MSSV: {FRONT_MATTER['student_id']}", 13, first_line_indent_cm=0)
    add_styled_paragraph(doc, f"• Khóa: {FRONT_MATTER['cohort']}", 13, first_line_indent_cm=0)
    add_styled_paragraph(doc, f"• Giáo viên hướng dẫn: {FRONT_MATTER['advisor']}", 13, first_line_indent_cm=0)
    add_styled_paragraph(doc, "1. Mục tiêu đề tài: Nghiên cứu và xây dựng hệ thống Web Full-Stack ứng dụng 5 mô hình học máy chuỗi thời gian để dự báo biến động giá nông sản Việt Nam bán ra tại vườn/ruộng ở 29 địa phương chuyên canh, kèm dải tin cậy 95%, giải thích AI (XAI), kiểm thử tự động và bảo mật OWASP Top 10.", 13, first_line_indent_cm=0)
    add_styled_paragraph(doc, "2. Nội dung đề tài: (1) Thu thập và xác minh nguồn gốc dữ liệu lịch sử của 8 loại nông sản chủ lực; (2) Tiền xử lý chuỗi thời gian (lọc ngoại lai IQR, kiểm định tính dừng ADF, tạo biến trễ Lag & Rolling); (3) Huấn luyện và đối sánh 5 mô hình (LSTM, Prophet, ARIMA, XGBoost, Random Forest) qua các độ đo MAE, RMSE, MAPE, R2; (4) Mô hình hóa độ lệch giá bán tại vườn theo huyện (Basis Spread); (5) Phát triển giao diện Web và thực thi 72 kịch bản kiểm thử phần mềm & kiểm tra bảo mật.", 13, first_line_indent_cm=0)
    add_styled_paragraph(doc, "3. Phần mềm và công cụ sử dụng: Python 3.11, FastAPI, SQLAlchemy ORM, PostgreSQL 15, PyTorch (LSTM), Facebook Prophet, Statsmodels (ARIMA), XGBoost, Scikit-learn, Next.js 14, React 18, TypeScript, TailwindCSS, Recharts, Pytest.", 13, first_line_indent_cm=0)
    add_styled_paragraph(doc, "4. Dự kiến kết quả: Cuốn báo cáo Khóa luận tốt nghiệp hoàn chỉnh (75–100 trang A4 nội dung chính) và phần mềm Web AgroForecast vận hành ổn định, đạt 100% kịch bản kiểm thử tự động (72/72 PASSED) và sai số dự báo của mô hình tối ưu đạt MAPE < 6% trên toàn bộ 8 nông sản.", 13, first_line_indent_cm=0)
    add_styled_paragraph(doc, "5. Tài liệu tham khảo chính: Box & Jenkins (2015), Breiman (2001), Chen & Guestrin (2016), Hochreiter & Schmidhuber (1997), Taylor & Letham (2018), OWASP Top 10 (2021).", 13, first_line_indent_cm=0)
    add_styled_paragraph(doc, "Đà Lạt, ngày ..... tháng ...... năm 2026", 13, italic=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0, space_before_pt=12)
    add_styled_paragraph(doc, "Giáo viên hướng dẫn                                                  SV Thực hiện", 13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=36)
    add_styled_paragraph(doc, "Trưởng khoa                                                          Tổ trưởng Bộ môn", 13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0)
    doc.add_page_break()

    # 9. Mục lục
    add_styled_paragraph(doc, "MỤC LỤC", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=14)
    toc_items = [
        "MỞ ĐẦU ................................................................................................................... Trang 1",
        "  1. Lý do chọn đề tài .................................................................................................. Trang 1",
        "  2. Mục đích nghiên cứu ............................................................................................. Trang 2",
        "  3. Đối tượng nghiên cứu ............................................................................................ Trang 3",
        "  4. Phương pháp nghiên cứu ....................................................................................... Trang 4",
        "  5. Phạm vi nghiên cứu và Bố cục của khóa luận ....................................................... Trang 5",
        "Chương 1: TỔNG QUAN VỀ ĐỀ TÀI NGHIÊN CỨU .......................................... Trang 6",
        "  1.1. Tổng quan về thị trường nông sản Việt Nam và giá bán tại vườn/ruộng .......... Trang 6",
        "  1.2. Phân tích, đánh giá các hướng nghiên cứu trong và ngoài nước ..................... Trang 18",
        "  1.3. Những vấn đề còn tồn tại của các nghiên cứu và hệ thống hiện có ................ Trang 22",
        "  1.4. Các vấn đề trọng tâm mà đề tài tập trung nghiên cứu giải quyết .................... Trang 23",
        "Chương 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ SỬ DỤNG .......................... Trang 25",
        "  2.1. Lý thuyết về chuỗi thời gian (Time Series) và tiền xử lý dữ liệu nông sản .... Trang 25",
        "  2.2. Cơ sở toán học và cơ chế hoạt động của 5 mô hình học máy dự báo giá ....... Trang 28",
        "  2.3. Các độ đo đánh giá chất lượng mô hình và ước lượng khoảng tin cậy ............ Trang 34",
        "  2.4. Cơ sở công nghệ phát triển hệ thống và tiêu chuẩn bảo mật OWASP Top 10 . Trang 38",
        "Chương 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG AGROFORECAST ............ Trang 45",
        "  3.1. Phân tích yêu cầu hệ thống (Actors, RBAC & Đặc tả Use Cases UC-01..11) . Trang 45",
        "  3.2. Thiết kế kiến trúc tổng thể và luồng xử lý dữ liệu học máy ............................ Trang 54",
        "  3.3. Thiết kế Cơ sở dữ liệu quan hệ (PostgreSQL Schema & ERD 11 bảng) ........ Trang 61",
        "  3.4. Thiết kế hệ thống RESTful API (28 Endpoints) và Giao diện (UI/UX) ......... Trang 67",
        "Chương 4: CÀI ĐẶT, THỰC NGHIỆM 5 MÔ HÌNH, KIỂM THỬ & BẢO MẬT Trang 74",
        "  4.1. Môi trường cài đặt và bộ dữ liệu thực nghiệm của hệ thống (4.899 bản ghi) . Trang 74",
        "  4.2. Kết quả thực nghiệm huấn luyện và đánh giá sai số của 5 mô hình học máy .. Trang 75",
        "  4.3. Kết quả cài đặt các phân hệ chức năng trên giao diện Web AgroForecast ...... Trang 83",
        "  4.4. Kiểm thử phần mềm và Kiểm tra bảo mật OWASP Top 10 (132/132 PASSED) Trang 86",
        "KẾT LUẬN ............................................................................................................ Trang 95",
        "HƯỚNG PHÁT TRIỂN ......................................................................................... Trang 97",
        "DANH MỤC TÀI LIỆU THAM KHẢO .............................................................. Trang 98",
        "PHỤ LỤC ............................................................................................................. Trang 100",
    ]
    for item in toc_items:
        is_top = not item.startswith("  ")
        add_styled_paragraph(doc, item, 13, bold=is_top, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=2, space_after_pt=2)
    doc.add_page_break()

    # 10. Bảng các chữ viết tắt (Xếp theo thứ tự bảng chữ cái A-Z)
    add_formatted_table(
        doc,
        "BẢNG CÁC KÝ HIỆU VÀ CHỮ VIẾT TẮT (Xếp theo thứ tự bảng chữ cái A – Z)",
        ["Chữ viết tắt", "Giải thích thuật ngữ tiếng Anh và nghĩa tiếng Việt"],
        ABBREVIATIONS,
    )
    doc.add_page_break()

    # 11. Tóm tắt khóa luận
    add_styled_paragraph(doc, "TÓM TẮT KHÓA LUẬN", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=14)
    add_styled_paragraph(doc, "Khóa luận trình bày quá trình nghiên cứu, phân tích, thiết kế và xây dựng hệ thống dự đoán biến động giá nông sản Việt Nam bằng mô hình học máy (AgroForecast). Hệ thống giải quyết bài toán thực tiễn về sự bất cân xứng thông tin giá cả tại hộ nông dân thông qua việc thu thập dữ liệu có kiểm chứng nguồn gốc (Data Provenance) của 8 mặt hàng nông sản chủ lực (Lúa gạo IR50404, Cà phê Robusta, Hồ tiêu đen, Mía đường 10 CCS, Dâu tây Đà Lạt, Khoai lang tím Vĩnh Long, Khoai tây Đà Lạt và Hạt điều thô) gắn liền với mô hình hóa giá bán trực tiếp tại vườn và tại ruộng (Farm-gate Price) ở 29 địa phương cấp huyện, thị xã, phường.")
    add_styled_paragraph(doc, "Về mặt phương pháp học máy, đề tài triển khai đường ống tiền xử lý tự động tích hợp 2 biến ngoại sinh vĩ mô nhân quả (USD/VND và Dầu thô WTI), sau đó huấn luyện và kiểm định chéo theo thời gian (Walk-Forward 7 ngày Zero-Leakage) đồng thời 5 mô hình: PyTorch Stacked LSTM, Facebook Prophet, ARIMA, XGBoost và Random Forest kèm khoảng tin cậy Conformal 95%. Kết quả thực nghiệm chốt tại mốc 23/11/2026 cho thấy mô hình tối ưu nhất đạt MAPE từ 0,74% đến 2,62% trên cả 8 mặt hàng (nổi bật là PyTorch Stacked LSTM hạng 1 trên Cà phê Robusta với R² = 0,8972). Toàn bộ hệ thống Web Full-Stack (FastAPI + Next.js 14 + Syncfusion EJ2 + PostgreSQL + Docker Compose) đã vượt qua 132/132 kịch bản kiểm thử tự động (125 Pytest Backend, 3 Frontend Unit, 4 Playwright E2E) và kiểm toán bảo mật chuẩn OWASP Top 10 (Bandit 0 lỗi Medium/High).")
