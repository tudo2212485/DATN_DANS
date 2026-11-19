# -*- coding: utf-8 -*-
"""
Trình biên dịch tự động Báo cáo Khóa luận Tốt nghiệp Kỹ sư Công nghệ Thông tin
Trường Đại học Đà Lạt - Khoa Công Nghệ Thông Tin
Đề tài: Nghiên cứu và xây dựng hệ thống dự đoán biến động giá nông sản Việt Nam bằng mô hình học máy (AgroForecast)
"""
import os
import math
import docx
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

from part1_front_and_ch1 import FRONT_MATTER, ABBREVIATIONS, MO_DAU_SECTIONS
from part1b_ch1 import CHUONG_1_DATA
from part2_ch2 import CHUONG_2_DATA
from part3_ch3 import CHUONG_3_DATA
from part4_ch4_and_end import (
    CHUONG_4_DATA,
    KET_LUAN_PARAGRAPHS,
    HUONG_PHAT_TRIEN_PARAGRAPHS,
    REFERENCES_LIST,
)
from part5_deep_dive import (
    CH1_EXTRA_SUBSECTIONS,
    CH2_EXTRA_SUBSECTIONS,
    CH3_EXTRA_SUBSECTIONS,
)
from part6_full_72_tests_and_screens import (
    CH4_EXTRA_FARM_GATE_SECTION,
    UI_IMPLEMENTATION_SECTION,
    FULL_72_TESTS_TABLE,
)
from part7_detailed_analysis_modules import COMMODITY_DEEP_ANALYSIS
from part8_code_and_security_walkthrough import (
    CH3_ALGORITHM_PSEUDOCODE_SECTIONS,
    CH4_SECURITY_CODE_ANALYSIS,
    APPENDIX_CONTENT,
)


def set_run_font(run, size_pt=13, bold=False, italic=False, color_rgb=None):
    run.font.name = "Times New Roman"
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    if color_rgb:
        run.font.color.rgb = RGBColor(*color_rgb)
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), "Times New Roman")
    rFonts.set(qn("w:hAnsi"), "Times New Roman")
    rFonts.set(qn("w:cs"), "Times New Roman")
    rFonts.set(qn("w:eastAsia"), "Times New Roman")


def add_styled_paragraph(
    doc,
    text,
    size_pt=13,
    bold=False,
    italic=False,
    align=WD_ALIGN_PARAGRAPH.JUSTIFY,
    first_line_indent_cm=1.0,
    space_before_pt=0,
    space_after_pt=1.5,
    line_spacing=1.5,
):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.line_spacing = line_spacing
    pf.space_before = Pt(space_before_pt)
    pf.space_after = Pt(space_after_pt)
    if first_line_indent_cm and align == WD_ALIGN_PARAGRAPH.JUSTIFY:
        pf.first_line_indent = Cm(first_line_indent_cm)
    run = p.add_run(text)
    set_run_font(run, size_pt=size_pt, bold=bold, italic=italic)
    return p


def add_footer_page_number(section):
    footer = section.footer
    p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    set_run_font(run, size_pt=12)
    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")
    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = "PAGE"
    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "separate")
    fldChar3 = OxmlElement("w:fldChar")
    fldChar3.set(qn("w:fldCharType"), "end")
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)


def add_formatted_table(doc, caption, headers, rows):
    add_styled_paragraph(
        doc,
        caption,
        size_pt=13,
        bold=True,
        italic=True,
        align=WD_ALIGN_PARAGRAPH.LEFT,
        first_line_indent_cm=0,
        space_before_pt=8,
        space_after_pt=4,
    )
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.autofit = False

    # Tính toán độ rộng cột thông minh theo tỷ lệ nội dung (tổng chiều rộng chuẩn A4 = 15.5 cm)
    weights = []
    for col_idx, h_text in enumerate(headers):
        h_low = str(h_text).strip().lower()
        max_len = max([len(str(h_text))] + [len(str(r[col_idx])) for r in rows if col_idx < len(r)])
        if h_low in ("stt", "id"):
            w = 0.85
        elif h_low in ("đơn vị", "kết quả", "mã http", "phương thức"):
            w = 1.35
        elif any(k in h_low for k in ("mae", "rmse", "mape", "hệ số r2", "số bản ghi", "chênh lệch", "độ lệch", "+7 ngày", "+10 ngày", "+14 ngày", "+30 ngày", "hiện tại")):
            w = 1.55
        elif "mã nông sản" in h_low or "tên bảng" in h_low or "lớp orm" in h_low or "tệp kiểm thử" in h_low:
            w = 2.45
        elif max_len > 80:
            w = 4.5
        elif max_len > 45:
            w = 3.4
        elif max_len > 25:
            w = 2.6
        else:
            w = 2.0
        weights.append(w)

    total_w = sum(weights)
    col_widths = [Cm(15.5 * (w / total_w)) for w in weights]
    col_dxa = [int(round(8787 * (w / total_w))) for w in weights]

    tblPr = table._tbl.tblPr
    tblPr.append(parse_xml(f'<w:tblW {nsdecls("w")} w:w="8787" w:type="dxa"/>'))
    tblPr.append(parse_xml(f'<w:tblLayout {nsdecls("w")} w:type="fixed"/>'))

    for idx, cw in enumerate(col_widths):
        table.columns[idx].width = cw

    hdr_cells = table.rows[0].cells
    for idx, h_text in enumerate(headers):
        hdr_cells[idx].width = col_widths[idx]
        tcPr = hdr_cells[idx]._tc.get_or_add_tcPr()
        for old_tcW in tcPr.findall(qn("w:tcW")):
            tcPr.remove(old_tcW)
        tcPr.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{col_dxa[idx]}" w:type="dxa"/>'))
        hdr_cells[idx].text = ""
        p = hdr_cells[idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.08
        p.paragraph_format.space_before = Pt(1.0)
        p.paragraph_format.space_after = Pt(1.0)
        run = p.add_run(str(h_text))
        set_run_font(run, size_pt=10.5, bold=True)
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="E8EEF5"/>')
        tcPr.append(shading)

    for r_data in rows:
        row_cells = table.add_row().cells
        for idx, val in enumerate(r_data):
            row_cells[idx].width = col_widths[idx]
            tcPr = row_cells[idx]._tc.get_or_add_tcPr()
            for old_tcW in tcPr.findall(qn("w:tcW")):
                tcPr.remove(old_tcW)
            tcPr.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{col_dxa[idx]}" w:type="dxa"/>'))
            row_cells[idx].text = ""
            p = row_cells[idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.08
            p.paragraph_format.space_before = Pt(0.8)
            p.paragraph_format.space_after = Pt(0.8)
            run = p.add_run(str(val))
            set_run_font(run, size_pt=10.5, bold=False)

    add_styled_paragraph(
        doc, "", size_pt=6, first_line_indent_cm=0, space_before_pt=0, space_after_pt=2
    )


def build_enriched_chapters():
    """
    Hợp nhất toàn bộ dữ liệu các chương và bổ sung phân tích chuyên sâu từng mô-đun
    để đảm bảo phần Nội dung chính của Khóa luận đạt chuẩn 75 - 100 trang A4.
    """
    # Enrich Chapter 1
    ch1 = CHUONG_1_DATA
    ch1["sections"][0]["subsections"].extend(CH1_EXTRA_SUBSECTIONS)

    # Add deep commodity analysis to Chapter 1 Section 1.1
    for idx, (c_title, c_paras) in enumerate(COMMODITY_DEEP_ANALYSIS, start=5):
        ch1["sections"][0]["subsections"].append(
            {
                "code": f"1.1.{idx}.",
                "title": c_title,
                "paragraphs": c_paras,
            }
        )

    # Enrich Chapter 2
    ch2 = CHUONG_2_DATA
    ch2["sections"][0]["subsections"].append(CH2_EXTRA_SUBSECTIONS[0])
    ch2["sections"][1]["subsections"].append(CH2_EXTRA_SUBSECTIONS[1])

    # Add deep mathematical derivation & walk-forward methodology to Chapter 2
    ch2["sections"][2]["subsections"].append(
        {
            "code": "2.3.4.",
            "title": "Phân tích toán học về tính ổn định của dự báo đệ quy đa bước (Multi-step Recursive Stability)",
            "paragraphs": [
                "Trong bài toán dự báo giá nông sản với kỳ hạn H bước tương lai (H = 7, 10, 14, 30 ngày), việc sử dụng chiến lược dự báo đệ quy (Recursive Strategy) đồng nghĩa với việc đầu ra dự báo hat{y}_{t+1} ở bước 1 lại trở thành biến đầu vào trễ lag_1 cho bước dự báo t+2. Nếu một mô hình học máy có hệ số khuếch đại sai số lớn hơn 1 (tức |d hat{y}_{t+1} / d y_t| > 1), sai số nhỏ ở bước đầu sẽ tích lũy theo cấp số nhân và gây ra hiện tượng trôi dạt dự báo (Forecast Drift) ở ngày thứ 14 đến ngày thứ 30.",
                "Để kiểm soát chặt chẽ hiện tượng này trong hệ thống AgroForecast, ba kỹ thuật ổn định hóa toán học đã được áp dụng đồng thời trong mô-đun app/services/training_service.py: (1) Đối với mô hình ARIMA(2,1,1), nghiệm của đa thức đặc trưng tự hồi quy 1 - phi_1*z - phi_2*z^2 = 0 luôn nằm ngoài vòng tròn đơn vị (|z| > 1), đảm bảo dự báo xa hội tụ mượt mà về đường xu thế cân bằng; (2) Đối với Random Forest và XGBoost, độ sâu tối đa của cây được giới hạn ở mức max_depth = 4..6 kết hợp cập nhật trung bình trượt động (rolling_mean_7d, rolling_mean_14d) tại mỗi bước lặp đệ quy h = 1..H, giúp kéo quỹ đạo dự báo bám sát dải trung bình động lịch sử; và (3) Đối với mạng học sâu LSTM, việc chuẩn hóa chuỗi vào đoạn [-1, 1] và sử dụng hàm kích hoạt bão hòa hai đầu tanh() giúp chặn trên và chặn dưới biên độ dự báo một cách tự nhiên.",
                "Bên cạnh đó, để người dùng đánh giá minh bạch giá trị gia tăng của từng mô hình học máy, mọi phiên huấn luyện đều tính toán song song sai số của mô hình Ngây thơ (Naive Persistence Baseline: hat{y}_{t+h} = y_t). Tỷ số cải thiện kỹ năng dự báo (Forecast Skill Score) được xác định bởi công thức: Skill = 1 - (RMSE_model / RMSE_naive). Khi Skill > 0, mô hình học máy chứng minh được năng lực dự báo vượt trội hơn việc giả định giá không đổi.",
            ],
        }
    )

    # Enrich Chapter 3
    ch3 = CHUONG_3_DATA
    ch3["sections"][1]["subsections"].extend(CH3_EXTRA_SUBSECTIONS[:1])
    ch3["sections"][1]["subsections"].extend(CH3_ALGORITHM_PSEUDOCODE_SECTIONS)
    ch3["sections"][2]["subsections"].extend(CH3_EXTRA_SUBSECTIONS[1:])

    # Add detailed Frontend Component & State Architecture to Chapter 3.4
    ch3["sections"][3]["subsections"].append(
        {
            "code": "3.4.3.",
            "title": "Thiết kế kiến trúc thành phần giao diện (Component Hierarchy) và đồng bộ trạng thái bất đồng bộ",
            "paragraphs": [
                "Phân hệ Frontend Next.js 14 được tổ chức theo kiến trúc mô-đun hóa cao tại thư mục frontend/src/, phân tách rõ ràng giữa 4 tầng mã nguồn: (1) Tầng Định nghĩa Kiểu tĩnh (src/types/index.ts) khai báo 18 giao diện TypeScript chuẩn hóa (CommoditySummary, ForecastPoint, ModelMetrics, RegionInfo, TrainingMetadata, AlertRuleItem, RegionalPriceItem...); (2) Tầng Dịch vụ Giao tiếp API (src/lib/api.ts và src/lib/auth.ts) quản lý tập trung mọi lời gọi fetch bất đồng bộ, tự động đính kèm tiêu đề Authorization: Bearer <token> và xử lý lỗi mạng; (3) Tầng Thành phần Giao diện Tái sử dụng (src/components/layout/ và src/components/dashboard/) gồm Sidebar, Header, CommodityCard, MarketComparisonChart, RegionalPriceTable, XAIFeatureDrivers, ModelComparisonChart, TrainingSummary, JobStatus; và (4) Tầng Trang Ứng dụng (src/app/) định tuyến cho 8 màn hình nghiệp vụ.",
                "Trên trang Phân tích & Dự báo AI (src/app/forecast/page.tsx), luồng đồng bộ trạng thái bất đồng bộ được điều khiển bởi cặp React Hooks useEffect và useMemo theo 4 biến phụ thuộc: [selectedCommodityId, selectedModel, forecastDays, selectedRegion]. Khi người dùng chuyển đổi sang một mặt hàng nông sản mới, hệ thống tự động đặt lại selectedRegion = '' để nạp địa phương bán tại vườn chuẩn của mặt hàng đó; khi người dùng nhấp chọn một huyện cụ thể trên thanh Spatio-Temporal Selector, yêu cầu GET /api/v1/forecast?commodity_id=...&model_name=...&days=...&region=... được gửi đi tức thời và toàn bộ dải 4 chỉ số tổng hợp, đường biểu đồ lịch sử - dự báo, dải tin cậy CI 95% cùng bảng lịch trình CSV được tính toán lại trong thời gian dưới 50 mili-giây.",
            ],
        }
    )

    # Enrich Chapter 4
    ch4 = CHUONG_4_DATA
    ch4["sections"][1]["subsections"].append(CH4_EXTRA_FARM_GATE_SECTION)
    # Insert UI Implementation section as 4.3, and shift Testing & Security to 4.4
    testing_sec = ch4["sections"][2]
    testing_sec["code"] = "4.4."
    for idx, sub in enumerate(testing_sec["subsections"], start=1):
        sub["code"] = f"4.4.{idx}."
    testing_sec["subsections"].extend(CH4_SECURITY_CODE_ANALYSIS)
    testing_sec["subsections"][-1]["code"] = "4.4.4."
    testing_sec["subsections"][2]["tables"].append(FULL_72_TESTS_TABLE)

    ch4["sections"] = [
        ch4["sections"][0],
        ch4["sections"][1],
        UI_IMPLEMENTATION_SECTION,
        testing_sec,
    ]

    return [ch1, ch2, ch3, ch4]
