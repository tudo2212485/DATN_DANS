# -*- coding: utf-8 -*-
import os
import sys
import win32com.client

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    target_docx = os.path.join(repo_root, "THESIS", "KHOA_LUAN_TOT_NGHIEP_AGROFORECAST_DLU.docx")
    thesis_pdf = os.path.join(repo_root, "THESIS", "KHOA_LUAN_TOT_NGHIEP_AGROFORECAST_DLU.pdf")

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

        print("Exporting official PDF to THESIS/...")
        doc.ExportAsFixedFormat(thesis_pdf, 17) # 17 = wdExportFormatPDF
        print(f"Exported to PDF successfully: {thesis_pdf}")

        doc.Close(False)
    finally:
        word.Quit()
        print("Word Application closed.")

if __name__ == "__main__":
    main()
