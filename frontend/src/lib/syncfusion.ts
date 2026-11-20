'use client';

import { registerLicense, L10n } from '@syncfusion/ej2-base';

let initialized = false;

export function initSyncfusion(): void {
  if (initialized) return;
  initialized = true;

  const key = (process.env.NEXT_PUBLIC_SYNCFUSION_LICENSE_KEY || '').trim();
  if (key && !key.startsWith('[')) {
    registerLicense(key);
  }

  // Việt hóa đầy đủ giao diện DataGrid, Phân trang, Tìm kiếm, Bộ lọc & Xuất file
  L10n.load({
    'en-US': {
      grid: {
        EmptyRecord: 'Không có bản ghi để hiển thị',
        Search: 'Tìm kiếm...',
        Excelexport: 'Xuất Excel',
        Csvexport: 'Xuất CSV',
        Pdfexport: 'Xuất PDF',
        Print: 'In bảng',
        FilterButton: 'Lọc',
        ClearButton: 'Xóa lọc',
        SelectAll: 'Chọn tất cả',
        Blanks: 'Trống',
        SearchColumns: 'Tìm cột',
        Matchs: 'Không tìm thấy kết quả phù hợp',
        Item: 'bản ghi',
        Items: 'bản ghi',
        FilterMenu: 'Bộ lọc',
        OKButton: 'Áp dụng',
        CancelButton: 'Hủy',
        EnterValue: 'Nhập giá trị',
        Equal: 'Bằng',
        NotEqual: 'Khác',
        StartsWith: 'Bắt đầu với',
        EndsWith: 'Kết thúc với',
        Contains: 'Chứa',
        GreaterThan: 'Lớn hơn',
        GreaterThanOrEqual: 'Lớn hơn hoặc bằng',
        LessThan: 'Nhỏ hơn',
        LessThanOrEqual: 'Nhỏ hơn hoặc bằng',
        CustomFilter: 'Bộ lọc tùy chỉnh',
        CustomFilterPlaceHolder: 'Nhập giá trị cần lọc',
        CustomFilterDatePlaceHolder: 'Chọn ngày',
        AND: 'VÀ',
        OR: 'HOẶC',
        ShowRowsWhere: 'Hiển thị các dòng khi:',
      },
      pager: {
        currentPageInfo: 'Trang {0} / {1}',
        totalItemsInfo: '({0} bản ghi)',
        totalItemInfo: '({0} bản ghi)',
        firstPageTooltip: 'Trang đầu',
        lastPageTooltip: 'Trang cuối',
        nextPageTooltip: 'Trang sau',
        previousPageTooltip: 'Trang trước',
        nextPagerTooltip: 'Nhóm trang sau',
        previousPagerTooltip: 'Nhóm trang trước',
        pagerDropDown: 'Số dòng / trang',
        pagerAllDropDown: 'Bản ghi',
        All: 'Tất cả',
        of: 'trên',
      },
    },
  });
}

// Khởi tạo ngay ở top-level module scope trước khi bất kỳ Grid/Chart nào render
initSyncfusion();

