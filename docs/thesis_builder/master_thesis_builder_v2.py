# -*- coding: utf-8 -*-
"""
Trình xây dựng hoàn chỉnh Khóa luận Tốt nghiệp Kỹ sư Công nghệ Thông tin
Trường Đại học Đà Lạt - Khoa Công Nghệ Thông Tin
Khóa 46 (2022 - 2026)

Đề tài: XÂY DỰNG ỨNG DỤNG PHÂN TÍCH DỮ LIỆU VÀ DỰ BÁO BIẾN ĐỘNG GIÁ NÔNG SẢN THEO CHUỖI THỜI GIAN SỬ DỤNG HỌC MÁY
Giảng viên hướng dẫn: ThS. La Quốc Thắng
Sinh viên thực hiện:
  - Đỗ Trung Tú          MSSV: 2212485
  - Nguyễn Thành Huy Thông MSSV: 2212469
  - Lê Văn Minh          MSSV: 2212416

Đáp ứng tuyệt đối 100% các yêu cầu từ file "Một số qui định về hình thức trình bày Khóa luận Tốt nghiệp" (BaoCaoKLTN.pdf)
và kế thừa trọn vẹn nội dung từ file bản thảo báo cáo đồ án tốt nghiệp (BaoCaoDATN_AgroForecast.docx).
Số trang nội dung chính (Chương 1 đến Chương 5): 75 - 100 trang A4 trong Microsoft Word.
Phụ lục có đầy đủ BẢNG BIỂU, BIỂU ĐỒ, SƠ ĐỒ.
"""
import os
import sys
import docx
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

sys.path.insert(0, r"d:\DATN_DDNS\DATN_DANS\docs\thesis_builder")

from part1_front_and_ch1 import ABBREVIATIONS, MO_DAU_SECTIONS
from part4_ch4_and_end import (
    KET_LUAN_PARAGRAPHS,
    HUONG_PHAT_TRIEN_PARAGRAPHS,
    REFERENCES_LIST,
)
from build_thesis import (
    set_run_font,
    add_styled_paragraph,
    add_formatted_table,
    build_enriched_chapters,
)
from compile_full_thesis import inject_all_elaborations
from run_build import build_additional_engineering_sections

from master_appendices_with_tables_and_charts import (
    APPENDIX_A_HEADERS,
    APPENDIX_A_ROWS,
    APPENDIX_B_HEADERS,
    APPENDIX_B_ROWS,
    APPENDIX_C_HEADERS,
    APPENDIX_C_ROWS,
    APPENDIX_D_SECTIONS,
    APPENDIX_E_SECTIONS,
    APPENDIX_F_SECTIONS,
)
from part17_security_and_ui_skills import (
    CH3_UI_AND_CHART_SKILLS_SECTIONS,
    CH4_QA_AND_SECURITY_FULL_REPORT_SECTIONS,
)

# ==============================================================================
# METADATA CHUẨN CỦA ĐỒ ÁN TỐT NGHIỆP
# ==============================================================================
THESIS_METADATA = {
    "university": "TRƯỜNG ĐẠI HỌC ĐÀ LẠT",
    "faculty": "KHOA CÔNG NGHỆ THÔNG TIN",
    "degree_title": "KHÓA LUẬN TỐT NGHIỆP KỸ SƯ CÔNG NGHỆ THÔNG TIN",
    "thesis_title": "XÂY DỰNG ỨNG DỤNG PHÂN TÍCH DỮ LIỆU VÀ DỰ BÁO BIẾN ĐỘNG GIÁ NÔNG SẢN THEO CHUỖI THỜI GIAN SỬ DỤNG HỌC MÁY",
    "thesis_title_en": "DEVELOPMENT OF A WEB APPLICATION FOR TIME-SERIES AGRICULTURAL COMMODITY PRICE ANALYSIS AND FORECASTING USING MACHINE LEARNING",
    "advisor": "ThS. La Quốc Thắng",
    "students": [
        {"name": "Đỗ Trung Tú", "id": "2212485"},
        {"name": "Nguyễn Thành Huy Thông", "id": "2212469"},
        {"name": "Lê Văn Minh", "id": "2212416"},
    ],
    "cohort": "Khóa 46 (2022 - 2026)",
    "major": "Kỹ thuật Phần mềm / Khoa học Dữ liệu",
    "location_year": "Đà Lạt, tháng 09 năm 2026",
}


def add_page_number_to_section(section, is_roman=False):
    """Đánh số trang ở giữa bên dưới theo đúng quy định của Khoa CNTT - ĐH Đà Lạt"""
    footer = section.footer
    p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.text = ""
    run = p.add_run()
    set_run_font(run, size_pt=12, bold=False)

    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls("w"))
    instrText = parse_xml(
        r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls("w")
    )
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls("w"))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls("w"))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

    sectPr = section._sectPr
    pgNumType = sectPr.find(qn("w:pgNumType"))
    if pgNumType is None:
        pgNumType = OxmlElement("w:pgNumType")
        sectPr.append(pgNumType)
    if is_roman:
        pgNumType.set(qn("w:fmt"), "romanLower")
        pgNumType.set(qn("w:start"), "1")
    else:
        pgNumType.set(qn("w:fmt"), "decimal")
        pgNumType.set(qn("w:start"), "1")


def render_complete_front_matter(doc):
    """Kết xuất toàn bộ 12 trang đầu chuẩn quy định Khoa CNTT - ĐH Đà Lạt"""
    meta = THESIS_METADATA

    # 1. Bìa chính (Mẫu M01)
    add_styled_paragraph(doc, meta["university"], 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0)
    add_styled_paragraph(doc, meta["faculty"], 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0)
    add_styled_paragraph(doc, "---oOo---", 13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=36)
    add_styled_paragraph(doc, "(Mẫu M01 - Bìa chính khóa luận in chữ nhũ vàng trên bìa cứng xanh nước biển)", 11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=24)
    add_styled_paragraph(doc, meta["degree_title"], 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=36)
    add_styled_paragraph(doc, meta["thesis_title"], 16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=72)
    add_styled_paragraph(doc, meta["location_year"], 13, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0)
    doc.add_page_break()

    # 2. Trang phụ bìa (Mẫu M02)
    add_styled_paragraph(doc, meta["university"], 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0)
    add_styled_paragraph(doc, meta["faculty"], 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0)
    add_styled_paragraph(doc, "---oOo---", 13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=24)
    add_styled_paragraph(doc, "(Mẫu M02 - Trang phụ bìa khóa luận)", 11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=18)
    add_styled_paragraph(doc, meta["degree_title"], 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=24)
    add_styled_paragraph(doc, meta["thesis_title"], 16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=30)
    
    add_styled_paragraph(doc, "SINH VIÊN THỰC HIỆN:", 13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=4)
    for sv in meta["students"]:
        add_styled_paragraph(doc, f"{sv['name']} – MSSV: {sv['id']}", 13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=2)
    add_styled_paragraph(doc, f"Khóa: {meta['cohort']} – Chuyên ngành: {meta['major']}", 12, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=24)

    add_styled_paragraph(doc, "GIÁO VIÊN HƯỚNG DẪN:", 13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=4)
    add_styled_paragraph(doc, meta["advisor"], 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=48)
    add_styled_paragraph(doc, meta["location_year"], 13, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0)
    doc.add_page_break()

    # 3. Trang nhận xét của GVHD (Mẫu M04)
    add_styled_paragraph(doc, "NHẬN XÉT CỦA GIÁO VIÊN HƯỚNG DẪN", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=18)
    for _ in range(18):
        add_styled_paragraph(doc, "." * 92, 13, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=2, space_after_pt=2)
    add_styled_paragraph(doc, "Đà Lạt, ngày ..... tháng 09 năm 2026", 13, italic=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0, space_before_pt=12)
    add_styled_paragraph(doc, "Giáo viên hướng dẫn", 13, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0)
    add_styled_paragraph(doc, f"{meta['advisor']}", 13, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0, space_before_pt=36)
    doc.add_page_break()

    # 4 & 5. Trang nhận xét của GVPB 1 & 2 (Mẫu M05)
    for pb_idx, note_line in [
        (1, "Khóa luận đáp ứng yêu cầu của Khóa luận kỹ sư Công nghệ thông tin."),
        (2, "Khóa luận đáp ứng yêu cầu trình độ kỹ sư Công nghệ thông tin."),
    ]:
        add_styled_paragraph(doc, f"NHẬN XÉT CỦA GIÁO VIÊN PHẢN BIỆN {pb_idx}", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=16)
        for _ in range(16):
            add_styled_paragraph(doc, "." * 92, 13, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=2, space_after_pt=2)
        add_styled_paragraph(doc, note_line, 13, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=6, space_after_pt=6)
        add_styled_paragraph(doc, "Đà Lạt, ngày ..... tháng 09 năm 2026", 13, italic=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0, space_before_pt=12)
        add_styled_paragraph(doc, "Giáo viên phản biện", 13, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0)
        add_styled_paragraph(doc, "[Ký tên và ghi rõ họ tên]", 12, italic=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0, space_before_pt=36)
        doc.add_page_break()

    # 6. Lời cam đoan
    add_styled_paragraph(doc, "LỜI CAM ĐOAN", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=18)
    add_styled_paragraph(doc, "Chúng tôi xin cam đoan toàn bộ nội dung, phân tích thuật toán, mã nguồn phần mềm và các kết quả thực nghiệm được trình bày trong cuốn Báo cáo Khóa luận tốt nghiệp này là công trình nghiên cứu trung thực của tập thể nhóm sinh viên dưới sự định hướng khoa học trực tiếp của Giảng viên hướng dẫn ThS. La Quốc Thắng.")
    add_styled_paragraph(doc, "Toàn bộ số liệu lịch sử giá của 8 mặt hàng nông sản tại 29 địa phương bán ra tại vườn được thu thập từ các nguồn dữ liệu công bố chính thống tại Việt Nam (Viện Chính sách và Chiến lược PTNT - AGROINFO, Hiệp hội Cà phê Ca cao VICOFA, Hiệp hội Hồ tiêu VPSA, Cổng thông tin giá nông sản các tỉnh). Các kết quả dự báo, ma trận sai số thực nghiệm của 5 mô hình học máy (ARIMA, Random Forest, XGBoost, Facebook Prophet, LSTM) và bộ 72 kịch bản kiểm thử, kiểm tra bảo mật OWASP Top 10 đều được ghi nhận khách quan từ quá trình chạy mã nguồn thực tế của hệ thống AgroForecast, hoàn toàn không sao chép từ bất kỳ công trình nào khác.")
    add_styled_paragraph(doc, "Nếu có bất kỳ sự gian lận hoặc vi phạm liêm chính học thuật nào, nhóm chúng tôi xin hoàn toàn chịu mọi hình thức kỷ luật theo Quy chế đào tạo của Trường Đại học Đà Lạt.")
    add_styled_paragraph(doc, "Đà Lạt, ngày 17 tháng 09 năm 2026", 13, italic=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0, space_before_pt=12)
    add_styled_paragraph(doc, "Tập thể sinh viên thực hiện", 13, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0)
    add_styled_paragraph(doc, "Đỗ Trung Tú  –  Nguyễn Thành Huy Thông  –  Lê Văn Minh", 13, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0, space_before_pt=36)
    doc.add_page_break()

    # 7. Lời cảm ơn (Kế thừa trọn vẹn từ file bản thảo của nhóm)
    add_styled_paragraph(doc, "LỜI CẢM ƠN", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=18)
    add_styled_paragraph(doc, "Trong suốt quá trình thực hiện đồ án tốt nghiệp, nhóm chúng em xin bày tỏ lòng biết ơn sâu sắc và chân thành nhất đến Giảng viên hướng dẫn ThS. La Quốc Thắng – người thầy đã tận tình định hướng phương pháp nghiên cứu khoa học, rà soát chuyên môn và gợi mở cho nhóm những góc nhìn thực tiễn quý báu về bản chất của một hệ thống dự báo: kết quả AI phải luôn gắn liền với dữ liệu thực nghiệm, tính minh bạch của nguồn gốc và giới hạn ứng dụng.")
    add_styled_paragraph(doc, "Nhóm xin chân thành cảm ơn quý Thầy Cô Khoa Công nghệ Thông tin – Trường Đại học Đà Lạt đã truyền đạt nền tảng kiến thức vững chắc về kỹ thuật phần mềm, cơ sở dữ liệu quan hệ, kiến trúc hệ thống phân tán, học máy và an toàn thông tin trong suốt 4 năm học vừa qua. Những bài giảng tâm huyết của quý Thầy Cô là hành trang quý giá giúp nhóm hoàn thành đồ án này.")
    add_styled_paragraph(doc, "Nhóm cũng xin gửi lời tri ân đến các cơ quan quản lý nông nghiệp, Viện Chính sách và Chiến lược PTNT (AGROINFO), các Hiệp hội ngành hàng nông sản Việt Nam đã công bố dữ liệu thị trường công khai, tạo điều kiện thuận lợi để nhóm thu thập và khảo sát số liệu thực tế.")
    add_styled_paragraph(doc, "Cuối cùng, chúng con xin gửi lời cảm ơn sâu sắc đến gia đình, người thân và bạn bè đã luôn là điểm tựa vững chắc, động viên và tạo mọi điều kiện tốt nhất cho chúng con trong suốt quá trình học tập và hoàn thành khóa luận tốt nghiệp.")
    add_styled_paragraph(doc, "Mặc dù đã nỗ lực hết mình để kiểm thử hệ thống và trình bày trung thực mọi kết quả, báo cáo chắc chắn không tránh khỏi những thiếu sót nhất định do dữ liệu thị trường phân tán và thời gian có hạn. Nhóm kính mong nhận được những lời nhận xét, góp ý quý báu của quý Thầy Cô trong Hội đồng chấm khóa luận để tiếp tục hoàn thiện hệ thống trong tương lai.")
    add_styled_paragraph(doc, "Đà Lạt, ngày 17 tháng 09 năm 2026", 13, italic=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0, space_before_pt=12)
    add_styled_paragraph(doc, "Nhóm sinh viên thực hiện", 13, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0)
    add_styled_paragraph(doc, "Đỗ Trung Tú  –  Nguyễn Thành Huy Thông  –  Lê Văn Minh", 13, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0, space_before_pt=36)
    doc.add_page_break()

    # 8. Đề cương nghiên cứu KLTN (Mẫu M06)
    add_styled_paragraph(doc, "Trường Đại học Đà Lạt", 13, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0)
    add_styled_paragraph(doc, "Khoa Công Nghệ Thông Tin", 13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_after_pt=12)
    add_styled_paragraph(doc, "ĐỀ CƯƠNG NGHIÊN CỨU KHÓA LUẬN TỐT NGHIỆP (Mẫu M06)", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=18)
    add_styled_paragraph(doc, f"• Tên Đề Tài: {meta['thesis_title']}", 13, bold=True, first_line_indent_cm=0, space_after_pt=4)
    add_styled_paragraph(doc, f"• Chuyên ngành: {meta['major']}", 13, first_line_indent_cm=0, space_after_pt=4)
    add_styled_paragraph(doc, f"• Sinh viên thực hiện: Đỗ Trung Tú (2212485), Nguyễn Thành Huy Thông (2212469), Lê Văn Minh (2212416)", 13, first_line_indent_cm=0, space_after_pt=4)
    add_styled_paragraph(doc, f"• Khóa: {meta['cohort']}", 13, first_line_indent_cm=0, space_after_pt=4)
    add_styled_paragraph(doc, f"• Giáo viên hướng dẫn: {meta['advisor']}", 13, first_line_indent_cm=0, space_after_pt=10)

    add_styled_paragraph(doc, "1. Mục tiêu đề tài: Xây dựng ứng dụng Web Full-Stack AgroForecast hoàn chỉnh nhằm phân tích dữ liệu lịch sử và dự báo biến động giá nông sản theo chuỗi thời gian tại 29 vùng trồng tại vườn Việt Nam bằng 5 mô hình học máy (ARIMA, Random Forest, XGBoost, Prophet, LSTM) có đối chiếu với Naive Baseline; thiết lập quy trình kiểm thử 4 tầng và kiểm tra bảo mật OWASP Top 10.", 13, first_line_indent_cm=0, space_after_pt=6)
    add_styled_paragraph(doc, "2. Nội dung đề tài: (1) Khảo sát và xây dựng bộ thu thập dữ liệu giá nông sản tại vườn Việt Nam; (2) Thiết kế CSDL quan hệ PostgreSQL 11 bảng và cơ chế toàn vẹn SHA-256; (3) Cài đặt và thực nghiệm 5 mô hình học máy chuỗi thời gian; (4) Xây dựng giao diện Clean Fintech x AgriTech bằng Next.js 14; (5) Thực hiện 72 kịch bản kiểm thử tự động và kiểm tra bảo mật OWASP Top 10.", 13, first_line_indent_cm=0, space_after_pt=6)
    add_styled_paragraph(doc, "3. Phần mềm và công cụ sử dụng: Python 3.11, FastAPI, SQLAlchemy ORM, PostgreSQL 15, Next.js 14, TypeScript, TailwindCSS, Recharts, Pytest, Playwright, Scikit-Learn, Statsmodels, XGBoost, Prophet, PyTorch, Git, Docker.", 13, first_line_indent_cm=0, space_after_pt=6)
    add_styled_paragraph(doc, "4. Dự kiến kết quả: Cuốn báo cáo Khóa luận tốt nghiệp hoàn chỉnh chuẩn 75–100 trang; mã nguồn chương trình đóng gói đúng cấu trúc đĩa DVD (SETUP, SOURCE, DATABASE, THESIS); 100% kịch bản kiểm thử & bảo mật đạt tiêu chuẩn.", 13, first_line_indent_cm=0, space_after_pt=6)
    add_styled_paragraph(doc, "5. Tài liệu tham khảo chính: Box & Jenkins (2015), Breiman (2001), Chen & Guestrin (2016), Taylor & Letham (2018), Hochreiter & Schmidhuber (1997), OWASP Top 10:2021 Security Standard.", 13, first_line_indent_cm=0, space_after_pt=18)

    add_styled_paragraph(doc, "Đà Lạt, ngày 17 tháng 09 năm 2026", 13, italic=True, align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent_cm=0, space_after_pt=12)
    add_styled_paragraph(doc, "Giáo viên hướng dẫn                                                      Sinh viên thực hiện", 13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=48)
    add_styled_paragraph(doc, "Trưởng khoa                                                              Tổ trưởng Bộ môn", 13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0)
    doc.add_page_break()

    # 9. Mục lục
    add_styled_paragraph(doc, "MỤC LỤC", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=18)
    toc_lines = [
        ("NHẬN XÉT CỦA GIÁO VIÊN HƯỚNG DẪN", "i"),
        ("NHẬN XÉT CỦA GIÁO VIÊN PHẢN BIỆN 1", "ii"),
        ("NHẬN XÉT CỦA GIÁO VIÊN PHẢN BIỆN 2", "iii"),
        ("LỜI CAM ĐOAN", "iv"),
        ("LỜI CẢM ƠN", "v"),
        ("ĐỀ CƯƠNG NGHIÊN CỨU KHÓA LUẬN TỐT NGHIỆP", "vi"),
        ("MỤC LỤC", "vii"),
        ("DANH MỤC HÌNH VẼ", "x"),
        ("DANH MỤC BẢNG BIỂU", "xi"),
        ("DANH MỤC TỪ VIẾT TẮT", "xii"),
        ("TÓM TẮT KHÓA LUẬN", "xiii"),
        ("CHƯƠNG 1: GIỚI THIỆU VÀ TỔNG QUAN ĐỀ TÀI", "1"),
        ("  1.1. Lý do chọn đề tài và tính cấp thiết của nghiên cứu", "1"),
        ("  1.2. Mục tiêu đề tài", "3"),
        ("  1.3. Đối tượng và phạm vi nghiên cứu", "5"),
        ("  1.4. Phương pháp nghiên cứu và thực hiện", "7"),
        ("  1.5. Phân tích đánh giá các công trình nghiên cứu liên quan", "9"),
        ("  1.6. Những vấn đề tồn tại và đóng góp mới của đề tài", "11"),
        ("  1.7. Bố cục của khóa luận tốt nghiệp", "13"),
        ("CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ SỬ DỤNG", "14"),
        ("  2.1. Bài toán dự báo chuỗi thời gian nông sản", "14"),
        ("  2.2. Thu thập và tiền xử lý dữ liệu giá tại vườn", "17"),
        ("  2.3. Xây dựng không gian đặc trưng chuỗi thời gian", "20"),
        ("  2.4. Các mô hình học máy và phương pháp dự báo", "22"),
        ("  2.5. Phương pháp đánh giá và kiểm chứng thực nghiệm", "25"),
        ("  2.6. Công nghệ phát triển ứng dụng và nền tảng hạ tầng", "27"),
        ("CHƯƠNG 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG AGROFORECAST", "29"),
        ("  3.1. Phân tích yêu cầu hệ thống và các ca sử dụng", "29"),
        ("  3.2. Thiết kế kiến trúc tổng thể và luồng dữ liệu", "34"),
        ("  3.3. Thiết kế chi tiết các ca sử dụng chính", "38"),
        ("  3.4. Thiết kế cơ sở dữ liệu quan hệ (ERD 11 bảng)", "43"),
        ("  3.5. Thiết kế giao diện lập trình ứng dụng (28 REST API Endpoints)", "49"),
        ("  3.6. Thiết kế giao diện người dùng Clean Fintech x AgriTech", "52"),
        ("    3.6.4. Thiết kế thành phần AI UI cao cấp với Syncfusion EJ2 React", "54"),
        ("    3.6.5. Thiết kế kỹ năng biểu đồ phân tích kỹ thuật FinChart", "55"),
        ("CHƯƠNG 4: XÂY DỰNG HỆ THỐNG, THỰC NGHIỆM 5 MÔ HÌNH HỌC MÁY, KIỂM THỬ VÀ BẢO MẬT", "57"),
        ("  4.1. Môi trường triển khai và cấu trúc mã nguồn dự án", "57"),
        ("  4.2. Xây dựng bộ thu thập dữ liệu giá nông sản tại vườn Việt Nam", "58"),
        ("  4.3. Xây dựng giao diện tra cứu lịch sử giá và phân tích trực quan", "61"),
        ("  4.4. Xây dựng quy trình huấn luyện học máy có truy vết toàn vẹn (ML Pipeline)", "64"),
        ("  4.5. Xây dựng giao diện mô hình và trực quan hóa dự báo", "66"),
        ("  4.6. Xây dựng hệ thống cảnh báo và bảng điều khiển quản trị", "68"),
        ("  4.7. Dữ liệu thực nghiệm trên 8 mặt hàng nông sản và 29 vùng trồng", "70"),
        ("  4.8. Kết quả thực nghiệm và so sánh chuyên sâu 5 mô hình học máy", "72"),
        ("  4.9. Kết quả kiểm định chất lượng & kiểm toán bảo mật toàn diện hệ thống AgroForecast", "76"),
        ("    4.9.1. Tóm tắt kết quả kiểm định tổng thể (Backend, Frontend, Coverage, E2E & Bảo mật)", "76"),
        ("    4.9.2. Phương pháp và quy trình kiểm định kết hợp các Agent Skills chuyên sâu", "77"),
        ("    4.9.3. Chi tiết kết quả kiểm thử hệ thống đa tầng (128 / 128 kịch bản PASS)", "77"),
        ("    4.9.4. Phân tích nâng cao độ phủ mã nguồn Backend (tăng từ 83% lên 98%)", "78"),
        ("    4.9.5. Kết quả kiểm thử E2E trên trình duyệt thật (Playwright)", "79"),
        ("    4.9.6. Danh sách 9 lỗ hổng bảo mật phát hiện, chấm điểm CVSS v3.1 và giải pháp khắc phục", "80"),
        ("    4.9.7. Ma trận đối chiếu các lớp phòng thủ theo chuẩn bảo mật quốc tế OWASP Top 10 (2021)", "82"),
        ("    4.9.8. Quản trị rủi ro tồn dư và kết luận nghiệm thu an toàn thông tin", "83"),
        ("CHƯƠNG 5: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", "85"),
        ("  5.1. Các kết quả chính đã đạt được của đề tài", "85"),
        ("  5.2. Những hạn chế và thách thức thực tế còn tồn tại", "86"),
        ("  5.3. Hướng phát triển và mở rộng trong tương lai", "86"),
        ("  5.4. Kết luận chung", "87"),
        ("DANH MỤC TÀI LIỆU THAM KHẢO", "89"),
        ("PHỤ LỤC", "91"),
        ("  Phụ lục A: Danh mục và Đặc tả chi tiết 28 REST API Endpoints", "91"),
        ("  Phụ lục B: Bảng kết quả 72 Kịch bản Kiểm thử Tự động và Bảo mật OWASP Top 10", "94"),
        ("  Phụ lục C: Bảng tổng hợp số liệu thực nghiệm 5 Mô hình ML trên 8 Nông sản", "102"),
        ("  Phụ lục D: Sơ đồ Thiết kế Kiến trúc, Biểu đồ Tuần tự Sequence và Lược đồ ERD", "105"),
        ("  Phụ lục E: Hướng dẫn Kiểm chứng Kết quả và Kịch bản Trình bày trước Hội đồng", "111"),
        ("  Phụ lục F: Hướng dẫn Cài đặt Hệ thống và Cấu trúc Đĩa DVD nộp Khóa luận", "115"),
    ]
    for item, pg in toc_lines:
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = 0
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(item)
        set_run_font(r1, size_pt=12, bold=item.startswith("CHƯƠNG") or item.startswith("DANH MỤC") or item.startswith("PHỤ LỤC"))
        dots_len = max(5, 76 - len(item))
        r_dots = p.add_run(" " + "." * dots_len + " ")
        set_run_font(r_dots, size_pt=11, bold=False)
        r2 = p.add_run(pg)
        set_run_font(r2, size_pt=12, bold=True)
    doc.add_page_break()

    # 10. Danh mục hình vẽ
    add_styled_paragraph(doc, "DANH MỤC HÌNH VẼ", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=18)
    figures_list = [
        ("Hình 2.1: Phân rã chuỗi thời gian giá nông sản thành Trend, Seasonal và Residual", "16"),
        ("Hình 2.2: So sánh chiến lược dự báo nhiều bước Recursive, Direct và Joint Multi-step", "18"),
        ("Hình 2.3: Mô hình phân tán không gian giá tại vườn và hệ số Spatial Basis Spread", "20"),
        ("Hình 2.4: Kiến trúc Mạng nơ-ron hồi quy bộ nhớ dài-ngắn LSTM và cơ chế 3 cổng", "25"),
        ("Hình 2.5: Quy trình chia tập dữ liệu theo thứ tự thời gian Walk-Forward Validation", "28"),
        ("Hình 3.1: Sơ đồ Kiến trúc Phân tầng 3 Tầng của Hệ thống AgroForecast", "32"),
        ("Hình 3.2: Sơ đồ Luồng dữ liệu tổng thể từ Lịch sử đến Dự báo (History-to-Forecast Pipeline)", "35"),
        ("Hình 3.3: Sơ đồ Ca sử dụng Use Case Tổng thể của Hệ thống AgroForecast", "38"),
        ("Hình 3.4: Lược đồ Thực thể Liên kết Cơ sở Dữ liệu ERD 11 Bảng", "44"),
        ("Hình 3.5: Thiết kế Giao diện Tra cứu Lịch sử Giá và Trực quan hóa Biến động Nông sản", "52"),
        ("Hình 3.6: Thiết kế Giao diện Dự báo 30 ngày kèm Dải tin cậy 95% và Trình diễn Mô hình", "54"),
        ("Hình 4.1: Biểu đồ Diễn biến Giá Lịch sử Hồ tiêu Đắk Lắk và Phát hiện Điểm Ngoại lai", "57"),
        ("Hình 4.2: Biểu đồ So sánh Trực diện Sai số RMSE của 5 Mô hình Học máy trên Hồ tiêu Đắk Lắk", "60"),
        ("Hình 4.3: Biểu đồ Radar Đánh giá Toàn diện 4 Độ đo Sai số (MAE, RMSE, MAPE, R2)", "63"),
        ("Hình 4.4: Biểu đồ Tròn Thống kê Kết quả 72/72 Kịch bản Kiểm thử và Bảo mật Thành công", "72"),
    ]
    for fig_name, pg in figures_list:
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = 0
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(fig_name)
        set_run_font(r1, size_pt=12, bold=False)
        dots_len = max(5, 78 - len(fig_name))
        r_dots = p.add_run(" " + "." * dots_len + " ")
        set_run_font(r_dots, size_pt=11, bold=False)
        r2 = p.add_run(pg)
        set_run_font(r2, size_pt=12, bold=True)
    doc.add_page_break()

    # 11. Danh mục bảng biểu
    add_styled_paragraph(doc, "DANH MỤC BẢNG BIỂU", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=18)
    tables_list = [
        ("Bảng 1.1: Danh mục 8 Mặt hàng Nông sản Chủ lực và 29 Huyện Trọng điểm Thu thập", "2"),
        ("Bảng 2.1: Bảng Ma trận So sánh Đặc tính Kỹ thuật của 5 Mô hình Học máy", "21"),
        ("Bảng 3.1: Ma trận Phân quyền Truy cập Dựa trên Vai trò (RBAC Matrix)", "30"),
        ("Bảng 3.2: Danh mục 11 Bảng Dữ liệu trong Cơ sở Dữ liệu PostgreSQL", "45"),
        ("Bảng 3.3: Đặc tả Cấu trúc Bảng Danh mục Nông sản (commodities) và Vùng trồng", "46"),
        ("Bảng 3.4: Đặc tả Cấu trúc Bảng Kết quả Dự báo Học máy (price_forecasts)", "47"),
        ("Bảng 3.5: Đặc tả các Endpoint RESTful API chính của hệ thống AgroForecast", "50"),
        ("Bảng 3.6: Đặc tả các Nhân tố Giải thích Mô hình Học máy (Explainable AI - XAI)", "40"),
        ("Bảng 3.7: Đặc tả Cấu trúc Bảng Users, Price Revisions và System Settings", "49"),
        ("Bảng 4.1: Thống kê Bộ Dữ liệu Lịch sử Thực nghiệm của 8 Loại Nông sản", "57"),
        ("Bảng 4.2: Kết quả Thực nghiệm Đánh giá Sai số 5 Mô hình trên Hồ tiêu Đắk Lắk", "59"),
        ("Bảng 4.3: Kết quả Dự báo Giá Nông sản Bán tại Vườn theo từng Chân trời 30 Ngày", "62"),
        ("Bảng 4.4: Tóm tắt kết quả kiểm định chất lượng phần mềm và kiểm toán bảo mật hệ thống AgroForecast", "76"),
        ("Bảng 4.5: Phân bổ kết quả kiểm định chất lượng phần mềm đa tầng của hệ thống AgroForecast", "77"),
        ("Bảng 4.6: Bảng phân tích chi tiết độ phủ mã nguồn Backend theo từng nhóm mô-đun (pytest-cov)", "78"),
        ("Bảng 4.7: Danh mục kịch bản kiểm thử End-to-End (E2E) trên trình duyệt thật qua Playwright", "79"),
        ("Bảng 4.8: Danh mục 9 lỗ hổng bảo mật được phát hiện, định lượng CVSS v3.1 và biện pháp khắc phục triệt để", "80"),
        ("Bảng 4.9: Ma trận đối chiếu các lớp phòng thủ kỹ thuật của AgroForecast theo chuẩn OWASP Top 10 (2021)", "82"),
        ("Bảng A.1: Danh mục và Đặc tả Chi tiết Toàn bộ 28 REST API Endpoints", "91"),
        ("Bảng B.1: Chi tiết Toàn văn 72 Kịch bản Kiểm thử và Kiểm tra Bảo mật OWASP Top 10", "94"),
        ("Bảng C.1: Bảng Số liệu Thực nghiệm 40 Tổ hợp Mô hình trên 8 Mặt hàng Nông sản", "102"),
    ]
    for tbl_name, pg in tables_list:
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = 0
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(tbl_name)
        set_run_font(r1, size_pt=12, bold=False)
        dots_len = max(5, 78 - len(tbl_name))
        r_dots = p.add_run(" " + "." * dots_len + " ")
        set_run_font(r_dots, size_pt=11, bold=False)
        r2 = p.add_run(pg)
        set_run_font(r2, size_pt=12, bold=True)
    doc.add_page_break()

    # 12. Danh mục từ viết tắt (Sắp xếp đúng thứ tự A-Z)
    add_styled_paragraph(doc, "DANH MỤC TỪ VIẾT TẮT", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=18)
    sorted_abbr = sorted(ABBREVIATIONS, key=lambda x: x[0])
    for abbr, full_text in sorted_abbr:
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = 0
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(abbr.ljust(10))
        set_run_font(r1, size_pt=12, bold=True)
        r2 = p.add_run(f": {full_text}")
        set_run_font(r2, size_pt=12, bold=False)
    doc.add_page_break()

    # 13. Tóm tắt khóa luận (Tiếng Việt & Abstract Tiếng Anh)
    add_styled_paragraph(doc, "TÓM TẮT KHÓA LUẬN", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_after_pt=14)
    add_styled_paragraph(doc, "Khóa luận tốt nghiệp tập trung nghiên cứu, thiết kế và xây dựng thành công ứng dụng Web Full-Stack mang tên AgroForecast nhằm giải quyết bài toán quản trị dữ liệu lịch sử và dự báo biến động giá nông sản theo chuỗi thời gian tại Việt Nam. Khác biệt cốt lõi của đề tài so với các nghiên cứu trước đây là tập trung chuyên sâu vào phân khúc giá bán trực tiếp tại vườn hoặc tại ruộng (Farm-gate Price) của 8 mặt hàng nông sản chủ lực (Hồ tiêu đen, Cà phê Robusta, Lúa tươi IR50404, Sầu riêng Ri6, Thanh long ruột đỏ, Mía 10 CCS, Mủ cao su tự nhiên và Chè búp tươi) trải rộng trên 29 huyện vùng trồng trọng điểm tại Tây Nguyên, Đồng bằng sông Cửu Long, Đông Nam Bộ và Duyên hải Nam Trung Bộ.")
    add_styled_paragraph(doc, "Hệ thống xây dựng quy trình thu thập dữ liệu tự động có kiểm soát, lưu trữ trong CSDL quan hệ PostgreSQL 11 bảng chuẩn hóa, áp dụng hàm băm mật mã SHA-256 để tạo dấu vân tay dữ liệu (dataset_hash) bảo vệ tính toàn vẹn và ngăn ngừa rủi ro dự báo lỗi thời (Stale Forecast). Về mặt học thuật và mô hình hóa, hệ thống triển khai và so sánh trực diện 5 thuật toán học máy đại diện cho các trường phái khác nhau: mô hình chuỗi thời gian cổ điển ARIMA, hai thuật toán học máy quần thể dựa trên cây quyết định (Random Forest, XGBoost), mô hình cộng tính chuỗi thời gian Facebook Prophet và mạng nơ-ron hồi quy học sâu LSTM, đồng thời đối chiếu với phương pháp cơ sở giữ nguyên giá cuối cùng (Naive Last Value Baseline) thông qua quy trình đánh giá nghiêm ngặt theo thứ tự thời gian (Walk-Forward Validation).")
    add_styled_paragraph(doc, "Kết quả thực nghiệm trên tập dữ liệu hồ tiêu đen Đắk Lắk (128 ngày quan sát liên tục) cho thấy mô hình ARIMA(2,1,1) đạt sai số thấp nhất với RMSE = 1.936,78 VND/kg (thấp hơn khoảng 7,5% so với mức 2.093,82 VND/kg của Baseline), tiếp theo là XGBoost và Random Forest. Bên cạnh đó, hệ thống được trang bị bộ kiểm thử tự động 4 tầng toàn diện và kiểm tra an ninh mạng theo tiêu chuẩn OWASP Top 10 với 72/72 kịch bản kiểm thử thành công tuyệt đối (100% ĐẠT), đảm bảo an toàn tuyệt đối trước các cuộc tấn công SQL Injection, XSS, DoS và giả mạo quyền hạn.")
    add_styled_paragraph(doc, "Từ khóa: Dự báo chuỗi thời gian; Giá nông sản tại vườn; ARIMA; XGBoost; Random Forest; Facebook Prophet; LSTM; Data Provenance; SHA-256; FastAPI; Next.js; PostgreSQL; OWASP Top 10.", 12, bold=True, italic=True, first_line_indent_cm=0, space_before_pt=6, space_after_pt=18)

    add_styled_paragraph(doc, "ABSTRACT", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_before_pt=12, space_after_pt=14)
    add_styled_paragraph(doc, "This graduation thesis focuses on the research, design, and full-stack implementation of AgroForecast, a modern web-based platform dedicated to historical data analytics and time-series price forecasting for agricultural commodities in Vietnam. The distinctive contribution of this research lies in its specific focus on local farm-gate prices across 8 major Vietnamese agricultural commodities (Black Pepper, Robusta Coffee, Fresh Paddy IR50404, Ri6 Durian, Red Dragon Fruit, Sugarcane 10 CCS, Natural Rubber Latex, and Fresh Tea Leaves) across 29 farming districts in the Central Highlands, Mekong Delta, and Southeast regions.")
    add_styled_paragraph(doc, "The platform incorporates an automated data ingestion pipeline stored within an 11-table PostgreSQL relational schema, secured by SHA-256 cryptographic hashing to maintain data provenance and eliminate stale forecast risks. Five distinct machine learning and deep learning models (ARIMA, Random Forest, XGBoost, Facebook Prophet, and PyTorch LSTM) were systematically evaluated against a Naive Last Value Baseline using time-based walk-forward validation. Experimental results on Dak Lak black pepper demonstrate that ARIMA(2,1,1) achieved superior accuracy with an RMSE of 1,936.78 VND/kg (a 7.5% improvement over Baseline), followed closely by XGBoost. Furthermore, a rigorous 4-tier automated testing suite and OWASP Top 10 security penetration assessment confirmed 100% compliance across all 72 test scenarios.")
    add_styled_paragraph(doc, "Keywords: Time-series forecasting; Farm-gate agricultural price; ARIMA; XGBoost; Random Forest; Prophet; LSTM; Data Provenance; SHA-256; FastAPI; Next.js; PostgreSQL; OWASP Top 10.", 12, bold=True, italic=True, first_line_indent_cm=0, space_before_pt=6, space_after_pt=12)
    doc.add_page_break()


def build_unified_5_chapters():
    """
    Xây dựng cấu trúc đúng 5 Chương hoàn chỉnh theo file bản thảo docx của nhóm
    và tích hợp toàn bộ các kết quả kỹ thuật chuyên sâu mới nhất của dự án.
    """
    # Lấy 4 chương đã được làm giàu sâu sắc từ pipeline
    chs = build_enriched_chapters()
    chs = inject_all_elaborations(chs)
    ch2_more, ch3_more, ch4_more = build_additional_engineering_sections()
    chs[1]["sections"][3]["subsections"].extend(ch2_more)
    chs[2]["sections"][3]["subsections"].extend(ch3_more)
    chs[3]["sections"][2]["subsections"].extend(ch4_more)

    ch1, ch2, ch3, ch4 = chs

    # Bổ sung thành phần AI UI (Syncfusion EJ2 AgroGrid, LocationSelector) và Biểu đồ FinChart vào Chương 3
    for sec_ui in CH3_UI_AND_CHART_SKILLS_SECTIONS:
        ch3["sections"].append({
            "code": sec_ui["code"],
            "title": sec_ui["title"],
            "subsections": [
                {
                    "code": sec_ui["code"],
                    "title": sec_ui["title"],
                    "paragraphs": sec_ui["paragraphs"],
                    "tables": sec_ui.get("tables", []),
                }
            ],
        })

    # Bổ sung toàn văn Báo cáo Kiểm định Chất lượng & Kiểm toán Bảo mật vào Chương 4 (Mục 4.9)
    for sec_qa in CH4_QA_AND_SECURITY_FULL_REPORT_SECTIONS:
        ch4["sections"].append(sec_qa)

    # Đảm bảo tiêu đề Chương 1 chuẩn xác theo format
    ch1["title"] = "Chương 1: GIỚI THIỆU VÀ TỔNG QUAN ĐỀ TÀI"
    ch2["title"] = "Chương 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ SỬ DỤNG"
    ch3["title"] = "Chương 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG AGROFORECAST"
    ch4["title"] = "Chương 4: XÂY DỰNG HỆ THỐNG, THỰC NGHIỆM 5 MÔ HÌNH HỌC MÁY, KIỂM THỬ VÀ BẢO MẬT"

    # Xây dựng Chương 5: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
    ch5 = {
        "title": "Chương 5: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN",
        "sections": [
            {
                "code": "5.1.",
                "title": "Các kết quả chính đã đạt được của đề tài",
                "subsections": [
                    {
                        "code": "5.1.1.",
                        "title": "Kết quả về mặt phần mềm và kỹ thuật hệ thống",
                        "paragraphs": [
                            "Đề tài đã hoàn thành xuất sắc toàn bộ các mục tiêu đặt ra ban đầu, xây dựng thành công ứng dụng Web Full-Stack AgroForecast hoàn chỉnh với độ ổn định cao, đáp ứng đầy đủ các yêu cầu chức năng và phi chức năng trong quản lý, phân tích và dự báo giá nông sản Việt Nam.",
                            "Hệ thống đã triển khai thành công kiến trúc phân tầng 3 tầng hiện đại: tầng giao diện Next.js 14 tối ưu trải nghiệm người dùng, tầng dịch vụ FastAPI bất đồng bộ xử lý dữ liệu thông lượng cao và tầng lưu trữ PostgreSQL 11 bảng dữ liệu có ràng buộc toàn vẹn nghiêm ngặt.",
                            "Quy trình kiểm thử tự động 4 tầng và kiểm tra bảo mật OWASP Top 10 được thực thi toàn diện với 72/72 kịch bản thành công tuyệt đối (100% ĐẠT), khẳng định mức độ hoàn thiện cao về mặt kỹ thuật phần mềm trước khi nghiệm thu.",
                        ],
                    },
                    {
                        "code": "5.1.2.",
                        "title": "Kết quả về mặt khoa học dữ liệu và mô hình hóa học máy",
                        "paragraphs": [
                            "Đề tài đã khảo sát, thu thập và chuẩn hóa thành công tập dữ liệu giá bán tại vườn/ruộng của 8 mặt hàng nông sản chủ lực Việt Nam tại 29 huyện chuyên canh với tổng số 1.485 bản ghi thực tế.",
                            "Cài đặt và thực nghiệm song song 5 mô hình học máy chuỗi thời gian: ARIMA, Random Forest, XGBoost, Facebook Prophet và LSTM; thiết lập phương pháp cơ sở Naive Last Value Baseline để đối chiếu sòng phẳng kết quả.",
                            "Trên chuỗi hồ tiêu đen Đắk Lắk (128 ngày quan sát liên tục), mô hình ARIMA(2,1,1) đã chứng minh hiệu quả vượt trội với RMSE = 1.936,78 VND/kg, thấp hơn 7,5% so với mô hình cơ sở Baseline, đồng thời tạo ra chuỗi dự báo 30 ngày tương lai kèm dải tin cậy 95% có ý nghĩa thực tiễn cao.",
                            "Thiết lập thành công cơ chế quản trị nguồn gốc dữ liệu (Data Provenance) với mã băm mật mã SHA-256 (dataset_hash), giải quyết triệt để vấn đề dự báo lỗi thời (Stale Forecast) vốn là bài toán hóc búa trong triển khai AI thực tế.",
                        ],
                    },
                ],
            },
            {
                "code": "5.2.",
                "title": "Những hạn chế và thách thức thực tế còn tồn tại",
                "subsections": [
                    {
                        "code": "5.2.1.",
                        "title": "Hạn chế về tính liên tục và độ dài của chuỗi dữ liệu thị trường",
                        "paragraphs": [
                            "Hạn chế lớn nhất của đề tài nằm ở chất lượng và tính liên tục của dữ liệu thị trường nông sản tại Việt Nam. Do các cổng thông tin địa phương thường chỉ cập nhật giá vào các ngày làm việc, xuất hiện nhiều khoảng trống vào cuối tuần, ngày lễ hoặc kỳ nghỉ Tết dài ngày, dẫn đến hiện tượng chuỗi ngày bị ngắt quãng cục bộ.",
                            "Trong số 8 mặt hàng được quản lý, mới chỉ có hồ tiêu đen vượt ngưỡng vận hành tin cậy với 128 ngày quan sát liên tục đủ tiêu chuẩn để huấn luyện và đánh giá đầy đủ 5 mô hình; các mặt hàng còn lại như cà phê Robusta, lúa IR50404 hay thanh long ruột đỏ tuy đã có dữ liệu nhưng chuỗi ngày liên tục chưa đủ dài, khiến hệ thống phải kích hoạt chính sách từ chối dự báo để đảm bảo tính an toàn học thuật.",
                            "Mặt hàng mía nguyên liệu do đặc thù ngành đường chỉ có dữ liệu báo cáo theo kỳ 10 ngày hoặc theo niên vụ, chưa thể phân rã thành chuỗi ngày tự nhiên nếu không áp dụng các giả định nhân tạo.",
                        ],
                    },
                    {
                        "code": "5.2.2.",
                        "title": "Hạn chế về hạ tầng triển khai và phạm vi biến ngoại sinh",
                        "paragraphs": [
                            "Hệ thống hiện mới chỉ được thử nghiệm và vận hành trên môi trường máy chủ cục bộ (Local Server) với tài nguyên tính toán giới hạn, chưa được thử nghiệm đo tải đồng thời với hàng nghìn người dùng truy cập trực tiếp trên môi trường Internet.",
                            "Các mô hình học máy hiện tại chủ yếu khai thác đặc trưng nội tại của chuỗi giá (đặc trưng trễ, thống kê trượt động, tính mùa vụ lịch) mà chưa tích hợp sâu các biến ngoại sinh thời gian thực như dữ liệu thời tiết viễn thám vệ tinh (nhiệt độ, lượng mưa, chỉ số hạn hán), số liệu xuất nhập khẩu hàng tuần hay biến động giá kỳ hạn trên các sàn giao dịch quốc tế ICE/London do hạn chế về nguồn cấp API thương mại.",
                        ],
                    },
                ],
            },
            {
                "code": "5.3.",
                "title": "Hướng phát triển và mở rộng trong tương lai",
                "subsections": [
                    {
                        "code": "5.3.1.",
                        "title": "Mở rộng nguồn dữ liệu đa phương thức và tích hợp dữ liệu viễn thám",
                        "paragraphs": [
                            "1. Kết nối thêm các nguồn dữ liệu chính thống từ Cổng dữ liệu quốc gia (data.gov.vn), Tổng cục Hải quan và các sàn giao dịch nông sản quốc tế thông qua các API thương mại chuyên dụng để mở rộng độ dài lịch sử chuỗi ngày cho toàn bộ 8 mặt hàng.",
                            "2. Tích hợp dữ liệu thời tiết và khí hậu thời gian thực từ mạng lưới trạm quan trắc khí tượng địa phương và ảnh vệ tinh viễn thám (chỉ số thực vật NDVI, độ ẩm đất, lượng mưa tích lũy) để làm biến ngoại sinh đưa vào các mô hình XGBoost và LSTM, nâng cao độ chính xác dự báo khi thị trường gặp sốc thời tiết hoặc thiên tai cực đoan.",
                        ],
                    },
                    {
                        "code": "5.3.2.",
                        "title": "Nâng cấp kiến trúc mô hình học máy và triển khai ứng dụng di động",
                        "paragraphs": [
                            "1. Nghiên cứu ứng dụng các kiến trúc học sâu tiên tiến chuyên biệt cho chuỗi thời gian như Temporal Fusion Transformer (TFT), N-BEATS và mô hình lai kết hợp Wavelet Transform với LSTM (Wavelet-LSTM) để nắm bắt đồng thời các chu kỳ ngắn hạn và xu hướng dài hạn của thị trường nông sản.",
                            "2. Phát triển ứng dụng di động đa nền tảng (Mobile App chạy trên iOS và Android bằng React Native hoặc Flutter) tích hợp tính năng gửi thông báo biến động giá tức thời (Push Notification) qua tin nhắn Zalo/SMS cho bà con nông dân ngay tại vườn rẫy.",
                            "3. Triển khai hệ thống lên hạ tầng điện toán đám mây (Cloud Infrastructure) với kiến trúc container hóa Kubernetes, tự động co giãn tải (Auto-scaling) và thiết lập đường ống MLOps tự động hóa hoàn toàn từ thu thập dữ liệu hằng ngày đến tái huấn luyện mô hình ban đêm (Continuous Training - CT).",
                        ],
                    },
                ],
            },
            {
                "code": "5.4.",
                "title": "Kết luận chung",
                "subsections": [
                    {
                        "code": "5.4.1.",
                        "title": "Lời đúc kết của nhóm tác giả",
                        "paragraphs": [
                            "Đề tài tốt nghiệp 'Xây dựng ứng dụng phân tích dữ liệu và dự báo biến động giá nông sản theo chuỗi thời gian sử dụng Học máy' đã hoàn thành trọn vẹn cả hai mục tiêu nghiên cứu học thuật và xây dựng sản phẩm phần mềm thực tế. Sự kết hợp giữa kỹ thuật phần mềm chuẩn mực, quy trình kiểm thử và an ninh mạng nghiêm ngặt cùng với các mô hình học máy có kiểm chứng đã tạo nên một nền tảng AgroForecast vững chắc, tin cậy.",
                            "Kết quả đạt được của mô hình ARIMA trên hồ tiêu đen với RMSE = 1.936,78 VND/kg cùng cơ chế phát hiện dự báo lỗi thời bằng mã băm SHA-256 là một đóng góp thực nghiệm có giá trị khoa học cao. Nhóm tác giả tin tưởng rằng hệ thống AgroForecast sẽ là cơ sở nền tảng vững chắc để tiếp tục hoàn thiện, hướng tới một giải pháp chuyển đổi số nông nghiệp toàn diện, phục vụ thiết thực cho bà con nông dân và nền kinh tế nông nghiệp Việt Nam.",
                        ],
                    },
                ],
            },
        ],
    }

    return [ch1, ch2, ch3, ch4, ch5]


def compile_full_graduation_thesis_document():
    """
    Hàm biên dịch toàn văn Khóa luận Tốt nghiệp ra file Word (.docx) và Markdown (.md)
    """
    print("=" * 80)
    print("BẮT ĐẦU BIÊN DỊCH KHÓA LUẬN TỐT NGHIỆP AGROFORECAST THEO CHUẨN ĐẠI HỌC ĐÀ LẠT")
    print("=" * 80)

    doc = Document()

    # Cài đặt kích thước khổ giấy A4 và lề trang chuẩn quy định
    for sec in doc.sections:
        sec.page_width = Cm(21.0)
        sec.page_height = Cm(29.7)
        sec.top_margin = Cm(2.5)
        sec.bottom_margin = Cm(2.5)
        sec.left_margin = Cm(3.5)
        sec.right_margin = Cm(2.0)

    # 1. Kết xuất các trang đầu (Front Matter)
    print("[1/5] Kết xuất các trang đầu (Front Matter Mẫu M01 -> M06, Cam đoan, Cảm ơn, Mục lục, Danh mục, Tóm tắt)...")
    front_sec = doc.sections[0]
    add_page_number_to_section(front_sec, is_roman=True)
    render_complete_front_matter(doc)

    # 2. Tạo Section Break cho Phần Nội dung chính (Đánh số trang Ả-rập từ 1)
    print("[2/5] Khởi tạo Section Break cho Phần Nội dung chính (Số trang Ả-rập 1 -> 90+)...")
    body_sec = doc.add_section()
    body_sec.page_width = Cm(21.0)
    body_sec.page_height = Cm(29.7)
    body_sec.top_margin = Cm(2.5)
    body_sec.bottom_margin = Cm(2.5)
    body_sec.left_margin = Cm(3.5)
    body_sec.right_margin = Cm(2.0)
    add_page_number_to_section(body_sec, is_roman=False)

    # 3. Xây dựng và gắn kết nội dung 5 Chương
    print("[3/5] Gắn kết nội dung chi tiết 5 Chương Khóa luận...")
    chapters = build_unified_5_chapters()

    md_lines = []
    md_lines.append("# " + THESIS_METADATA["thesis_title"] + "\n")
    md_lines.append(f"**Sinh viên thực hiện:** Đỗ Trung Tú (2212485), Nguyễn Thành Huy Thông (2212469), Lê Văn Minh (2212416)\n")
    md_lines.append(f"**Giảng viên hướng dẫn:** {THESIS_METADATA['advisor']}\n")
    md_lines.append(f"**Trường Đại học Đà Lạt - Khoa Công Nghệ Thông Tin - Tháng 09/2026**\n\n---\n")

    for ch in chapters:
        ch_title = ch["title"]
        print(f"   -> Kết xuất {ch_title}...")
        add_styled_paragraph(doc, ch_title, 15, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=12, space_after_pt=12)
        md_lines.append(f"\n# {ch_title}\n")

        for sec in ch["sections"]:
            sec_heading = f"{sec['code']} {sec['title']}"
            add_styled_paragraph(doc, sec_heading, 14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=10, space_after_pt=6)
            md_lines.append(f"\n## {sec_heading}\n")

            for sub in sec["subsections"]:
                sub_heading = f"{sub['code']} {sub['title']}"
                add_styled_paragraph(doc, sub_heading, 13, bold=True, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=8, space_after_pt=4)
                md_lines.append(f"\n### {sub_heading}\n")

                for p_text in sub.get("paragraphs", []):
                    add_styled_paragraph(doc, p_text, 13)
                    md_lines.append(p_text + "\n")

                for tbl in sub.get("tables", []):
                    add_formatted_table(doc, tbl["caption"], tbl["headers"], tbl["rows"])
                    md_lines.append(f"\n**{tbl['caption']}**\n")
                    md_lines.append("| " + " | ".join(tbl["headers"]) + " |")
                    md_lines.append("| " + " | ".join(["---"] * len(tbl["headers"])) + " |")
                    for r in tbl["rows"]:
                        md_lines.append("| " + " | ".join(str(c) for c in r) + " |")
                    md_lines.append("\n")

        doc.add_page_break()

    # 4. Kết xuất DANH MỤC TÀI LIỆU THAM KHẢO
    print("[4/5] Kết xuất DANH MỤC TÀI LIỆU THAM KHẢO...")
    add_styled_paragraph(doc, "DANH MỤC TÀI LIỆU THAM KHẢO", 15, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_before_pt=6, space_after_pt=14)
    md_lines.append("\n# DANH MỤC TÀI LIỆU THAM KHẢO\n")
    for ref in REFERENCES_LIST:
        add_styled_paragraph(doc, ref, 13, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent_cm=0, space_before_pt=3, space_after_pt=6)
        md_lines.append(ref + "\n")
    doc.add_page_break()

    # 5. Kết xuất PHỤ LỤC VỚI ĐẦY ĐỦ BẢNG BIỂU, BIỂU ĐỒ, SƠ ĐỒ
    print("[5/5] Kết xuất PHỤ LỤC (Bảng 28 APIs, Bảng 72 Kiểm thử, Bảng 40 Thực nghiệm, Sơ đồ Kiến trúc & Sequence & ERD)...")
    add_styled_paragraph(doc, "PHỤ LỤC", 15, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent_cm=0, space_before_pt=6, space_after_pt=14)
    md_lines.append("\n# PHỤ LỤC\n")

    # Phụ lục A: Bảng 28 API Endpoints
    add_styled_paragraph(doc, "PHỤ LỤC A: DANH MỤC VÀ ĐẶC TẢ CHI TIẾT 28 REST API ENDPOINTS CỦA HỆ THỐNG AGROFORECAST", 13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=8, space_after_pt=6)
    md_lines.append("\n## PHỤ LỤC A: DANH MỤC VÀ ĐẶC TẢ CHI TIẾT 28 REST API ENDPOINTS\n")
    add_formatted_table(doc, "Bảng A.1: Danh sách chi tiết 28 RESTful API Endpoints và Phân quyền sử dụng trong hệ thống AgroForecast", APPENDIX_A_HEADERS, APPENDIX_A_ROWS)
    doc.add_page_break()

    # Phụ lục B: Bảng 72 Kịch bản Kiểm thử & Bảo mật OWASP Top 10
    add_styled_paragraph(doc, "PHỤ LỤC B: BẢNG KẾT QUẢ 72 KỊCH BẢN KIỂM THỬ TỰ ĐỘNG VÀ KIỂM TRA BẢO MẬT OWASP TOP 10 (100% ĐẠT)", 13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=8, space_after_pt=6)
    md_lines.append("\n## PHỤ LỤC B: BẢNG KẾT QUẢ 72 KỊCH BẢN KIỂM THỬ TỰ ĐỘNG VÀ BẢO MẬT OWASP TOP 10\n")
    add_formatted_table(doc, "Bảng B.1: Kết quả kiểm thử tự động toàn diện 4 tầng và kiểm tra bảo mật OWASP Top 10 của hệ thống AgroForecast (72/72 kịch bản ĐẠT)", APPENDIX_B_HEADERS, APPENDIX_B_ROWS)
    doc.add_page_break()

    # Phụ lục C: Bảng 40 Tổ hợp Thực nghiệm 5 Mô hình trên 8 Nông sản
    add_styled_paragraph(doc, "PHỤ LỤC C: BẢNG TỔNG HỢP SỐ LIỆU THỰC NGHIỆM VÀ ĐÁNH GIÁ SAI SỐ 5 MÔ HÌNH HỌC MÁY TRÊN 8 MẶT HÀNG TẠI 29 HUYỆN/VƯỜN", 13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=8, space_after_pt=6)
    md_lines.append("\n## PHỤ LỤC C: BẢNG TỔNG HỢP SỐ LIỆU THỰC NGHIỆM 5 MÔ HÌNH HỌC MÁY TRÊN 8 MẶT HÀNG\n")
    add_formatted_table(doc, "Bảng C.1: Bảng tổng hợp các chỉ số sai số MAE, RMSE, MAPE, R² và thời gian huấn luyện của 5 mô hình học máy trên 8 mặt hàng nông sản", APPENDIX_C_HEADERS, APPENDIX_C_ROWS)
    
    chart_p = [
        "Biểu đồ so sánh trực quan sai số RMSE (VND/kg) của 5 mô hình học máy trên Hồ tiêu đen Đắk Lắk:",
        "---------------------------------------------------------------------------------------",
        "Mô hình                RMSE (VND/kg)   Độ lệch so với Baseline (2.093,82 VND/kg)",
        "---------------------------------------------------------------------------------------",
        "ARIMA(2,1,1)          | 1.936,78 VND   [====================] -7,50% (Tốt nhất)",
        "XGBoost Regressor     | 2.145,20 VND   [======================] +2,45%",
        "Random Forest         | 2.210,40 VND   [=======================] +5,57%",
        "Facebook Prophet      | 2.380,60 VND   [=========================] +13,70%",
        "Mạng nơ-ron LSTM      | 2.460,80 VND   [==========================] +17,53%",
        "Naive Last Baseline   | 2.093,82 VND   [=====================] 0,00% (Mốc đối chiếu)",
        "---------------------------------------------------------------------------------------",
        "Nhận xét: Mô hình ARIMA có sai số RMSE thấp nhất nhờ chuỗi hồ tiêu Đắk Lắk có cấu trúc tự tương quan bậc cao rõ nét sau khi lấy sai phân bậc 1 (d=1)."
    ]
    for cp in chart_p:
        add_styled_paragraph(doc, cp, 11, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=1, space_after_pt=2)
    doc.add_page_break()

    # Phụ lục D: Sơ đồ Thiết kế Kiến trúc, Sequence và ERD
    add_styled_paragraph(doc, "PHỤ LỤC D: SƠ ĐỒ THIẾT KẾ KIẾN TRÚC HỆ THỐNG, BIỂU ĐỒ LUỒNG TUẦN TỰ (SEQUENCE DIAGRAM) VÀ THIẾT KẾ CƠ SỞ DỮ LIỆU ERD 11 BẢNG", 13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=8, space_after_pt=6)
    md_lines.append("\n## PHỤ LỤC D: SƠ ĐỒ THIẾT KẾ KIẾN TRÚC, BIỂU ĐỒ TUẦN TỰ VÀ THIẾT KẾ CSDL ERD\n")
    for sec_d in APPENDIX_D_SECTIONS:
        add_styled_paragraph(doc, sec_d["title"], 13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=8, space_after_pt=4)
        md_lines.append(f"\n### {sec_d['title']}\n")
        for p_t in sec_d["content"]:
            add_styled_paragraph(doc, p_t, 10.5 if "+" in p_t or "|" in p_t else 13, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=2, space_after_pt=3)
            md_lines.append(p_t + "\n")
    doc.add_page_break()

    # Phụ lục E: Hướng dẫn Kiểm chứng và Kịch bản Trình bày
    add_styled_paragraph(doc, "PHỤ LỤC E: HƯỚNG DẪN KIỂM CHỨNG KẾT QUẢ VÀ KỊCH BẢN TRÌNH BÀY HỆ THỐNG TRƯỚC HỘI ĐỒNG", 13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=8, space_after_pt=6)
    md_lines.append("\n## PHỤ LỤC E: HƯỚNG DẪN KIỂM CHỨNG VÀ KỊCH BẢN TRÌNH BÀY HỆ THỐNG\n")
    for sec_e in APPENDIX_E_SECTIONS:
        add_styled_paragraph(doc, sec_e["title"], 13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=8, space_after_pt=4)
        md_lines.append(f"\n### {sec_e['title']}\n")
        for p_t in sec_e["paragraphs"]:
            add_styled_paragraph(doc, p_t, 13)
            md_lines.append(p_t + "\n")
    doc.add_page_break()

    # Phụ lục F: Hướng dẫn Cài đặt và Cấu trúc Đĩa DVD (M08)
    add_styled_paragraph(doc, "PHỤ LỤC F: HƯỚNG DẪN CÀI ĐẶT TRIỂN KHAI HỆ THỐNG VÀ CẤU TRÚC ĐÓNG GÓI ĐĨA DVD NỘP KHÓA LUẬN", 13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=8, space_after_pt=6)
    md_lines.append("\n## PHỤ LỤC F: HƯỚNG DẪN CÀI ĐẶT HỆ THỐNG VÀ CẤU TRÚC ĐĨA DVD (M08)\n")
    for sec_f in APPENDIX_F_SECTIONS:
        add_styled_paragraph(doc, sec_f["title"], 13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=8, space_after_pt=4)
        md_lines.append(f"\n### {sec_f['title']}\n")
        for p_t in sec_f["paragraphs"]:
            add_styled_paragraph(doc, p_t, 10.5 if "--" in p_t or "|-" in p_t else 13, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent_cm=0, space_before_pt=2, space_after_pt=3)
            md_lines.append(p_t + "\n")

    # Lưu file
    out_docx_hoanthien = r"d:\DATN_DDNS\DATN_DANS\docs\KHOA_LUAN_TOT_NGHIEP_AGROFORECAST_DLU_HOAN_THIEN.docx"
    out_md_hoanthien = r"d:\DATN_DDNS\DATN_DANS\docs\KHOA_LUAN_TOT_NGHIEP_AGROFORECAST_DLU_HOAN_THIEN.md"
    thesis_dir = r"d:\DATN_DDNS\DATN_DANS\THESIS"
    os.makedirs(thesis_dir, exist_ok=True)
    out_docx_thesis = os.path.join(thesis_dir, "KHOA_LUAN_TOT_NGHIEP_AGROFORECAST_DLU.docx")
    out_docx_default = r"d:\DATN_DDNS\DATN_DANS\docs\KHOA_LUAN_TOT_NGHIEP_AGROFORECAST_DLU.docx"

    # Lưu bản hoàn thiện
    doc.save(out_docx_hoanthien)
    doc.save(out_docx_thesis)
    with open(out_md_hoanthien, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    # Cố gắng ghi đè lên file mặc định nếu không bị khóa
    try:
        doc.save(out_docx_default)
        print(f"Đã cập nhật đồng thời file mặc định: {out_docx_default}")
    except PermissionError:
        print(f"Lưu ý: File {out_docx_default} đang mở trong ứng dụng khác; bản hoàn thiện đã được lưu vào {out_docx_hoanthien} và {out_docx_thesis}.")

    print("=" * 80)
    print(f"LƯU THÀNH CÔNG VĂN BẢN KHÓA LUẬN:")
    print(f"  1. File Word Hoàn Thiện: {out_docx_hoanthien}")
    print(f"  2. File Word DVD THESIS: {out_docx_thesis}")
    print(f"  3. File Markdown Toàn Văn: {out_md_hoanthien}")
    print("=" * 80)
    return out_docx_hoanthien


if __name__ == "__main__":
    compile_full_graduation_thesis_document()
