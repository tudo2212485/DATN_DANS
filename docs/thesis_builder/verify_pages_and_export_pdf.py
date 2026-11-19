# -*- coding: utf-8 -*-
import os
import sys
import win32com.client

def main():
    target_docx = r"d:\DATN_DDNS\DATN_DANS\docs\KHOA_LUAN_TOT_NGHIEP_AGROFORECAST_DLU_HOAN_THIEN.docx"
    target_pdf = r"d:\DATN_DDNS\DATN_DANS\docs\KHOA_LUAN_TOT_NGHIEP_AGROFORECAST_DLU_HOAN_THIEN.pdf"
    thesis_pdf = r"d:\DATN_DDNS\DATN_DANS\THESIS\KHOA_LUAN_TOT_NGHIEP_AGROFORECAST_DLU.pdf"

    print("Opening Word Application...")
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0

    try:
        print(f"Opening document: {target_docx}")
        doc = word.Documents.Open(target_docx, ReadOnly=True, Visible=False)
        
        # Lấy số trang
        total_pages = doc.ComputeStatistics(2) # 2 = wdStatisticPages
        print(f"Total pages in entire document: {total_pages}")
        
        num_sections = doc.Sections.Count
        print(f"Total sections: {num_sections}")
        for i in range(1, num_sections + 1):
            sec = doc.Sections(i)
            sec_pages = sec.Range.ComputeStatistics(2)
            print(f"  Section {i} pages: {sec_pages}")

        print("Exporting to PDF...")
        doc.ExportAsFixedFormat(target_pdf, 17) # 17 = wdExportFormatPDF
        doc.ExportAsFixedFormat(thesis_pdf, 17)
        print("Exported to PDF successfully!")
        print(f"  -> {target_pdf}")
        print(f"  -> {thesis_pdf}")

        doc.Close(False)
    finally:
        word.Quit()
        print("Word Application closed.")

if __name__ == "__main__":
    main()
