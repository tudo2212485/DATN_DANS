'use client';

import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  GridComponent,
  ColumnsDirective,
  ColumnDirective,
  Inject,
  Page,
  Sort,
  Filter,
  Toolbar,
  Search,
  ExcelExport,
  ExcelQueryCellInfoEventArgs,
  PageSettingsModel,
  FilterSettingsModel,
} from '@syncfusion/ej2-react-grids';
import { ClickEventArgs } from '@syncfusion/ej2-navigations';
import { initSyncfusion } from '@/lib/syncfusion';
import { formatDateTimeVN, formatDateVN, formatNumberVN, formatPct } from '@/lib/formatters';

// Đảm bảo Syncfusion license & Việt hóa L10n luôn sẵn sàng trước khi mount GridComponent
initSyncfusion();

export type AgroColumnKind = 'text' | 'date' | 'datetime' | 'number' | 'money' | 'pct' | 'decimal';

export interface AgroColumn {
  field: string;
  headerText: string;
  kind?: AgroColumnKind;
  width?: number | string;
  align?: 'Left' | 'Right' | 'Center';
  unit?: string;
  unitField?: string;
  digits?: number;
  template?: (row: Record<string, unknown>) => React.ReactNode;
  allowSorting?: boolean;
  allowFiltering?: boolean;
  allowSearching?: boolean;
  exportable?: boolean;
}

interface AgroGridProps {
  data: object[];
  columns: AgroColumn[];
  pageSize?: number;
  height?: number | string;
  fileName?: string;
  toolbar?: ('Search' | 'ExcelExport' | 'CsvExport')[];
  emptyText?: string;
}

function formatCellValue(col: AgroColumn, row: Record<string, unknown>): string {
  const kind = col.kind ?? 'text';
  const value = row?.[col.field];
  if (value === null || value === undefined || value === '') return '—';
  switch (kind) {
    case 'date':
      return formatDateVN(String(value));
    case 'datetime':
      return formatDateTimeVN(String(value));
    case 'number':
      return formatNumberVN(Number(value), 0);
    case 'decimal':
      return formatNumberVN(Number(value), col.digits ?? 2);
    case 'pct':
      return formatPct(Number(value), col.digits ?? 2);
    case 'money': {
      const unit = col.unitField ? String(row?.[col.unitField] ?? '') : col.unit;
      return `${formatNumberVN(Number(value), 0)} ${unit ?? ''}`.trim();
    }
    default:
      return String(value);
  }
}

function defaultAlign(kind?: AgroColumnKind): 'Left' | 'Right' {
  return kind === 'number' || kind === 'money' || kind === 'pct' || kind === 'decimal' ? 'Right' : 'Left';
}

function sanitizeExportValue(raw: string): string {
  const str = String(raw ?? '').trim();
  if (/^[=+\-@\t\r]/.test(str) && !/^[+-]?[\d.,]+%?/.test(str)) {
    return `'${str}`;
  }
  return str;
}

export default function AgroGrid({
  data,
  columns,
  pageSize = 15,
  height = 400,
  fileName = 'agroforecast',
  toolbar = ['Search', 'ExcelExport', 'CsvExport'],
}: AgroGridProps) {
  const gridRef = useRef<GridComponent | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    initSyncfusion();
    setMounted(true);
  }, []);

  const colMap = useMemo(() => {
    const map = new Map<string, AgroColumn>();
    columns.forEach((c) => map.set(c.field, c));
    return map;
  }, [columns]);

  const pageSettings: PageSettingsModel = useMemo(
    () => ({
      pageSize,
      pageSizes: [10, 15, 25, 50],
      pageCount: 5,
    }),
    [pageSize]
  );

  const filterSettings: FilterSettingsModel = useMemo(
    () => ({
      type: 'Excel',
    }),
    []
  );

  const hiddenExportFieldsRef = useRef<string[]>([]);

  const columnsKey = useMemo(
    () => columns.map((c) => `${c.field}:${c.headerText}`).join('|'),
    [columns]
  );

  const handleToolbarClick = (args: ClickEventArgs) => {
    const grid = gridRef.current;
    if (!grid || !args?.item?.id) return;
    const itemId = args.item.id.toLowerCase();

    const isExcel = itemId.includes('_excelexport');
    const isCsv = itemId.includes('_csvexport');
    if (!isExcel && !isCsv) return;

    const nonExportFields = columns
      .filter((c) => c.exportable === false || c.field === 'actions')
      .map((c) => c.field);

    hiddenExportFieldsRef.current = nonExportFields;
    nonExportFields.forEach((field) => {
      const colObj = grid.getColumnByField(field);
      if (colObj) colObj.visible = false;
    });

    if (isExcel) {
      grid.excelExport({ fileName: `${fileName}.xlsx` });
    } else if (isCsv) {
      grid.csvExport({ fileName: `${fileName}.csv` });
    }
  };

  const handleExcelExportComplete = () => {
    const grid = gridRef.current;
    if (!grid || hiddenExportFieldsRef.current.length === 0) return;
    hiddenExportFieldsRef.current.forEach((field) => {
      const colObj = grid.getColumnByField(field);
      if (colObj) colObj.visible = true;
    });
    hiddenExportFieldsRef.current = [];
  };

  const handleExcelQueryCellInfo = (args: ExcelQueryCellInfoEventArgs) => {
    const field = args.column?.field;
    if (!field) return;
    const col = colMap.get(field);
    if (!col) return;
    const row = (args.data ?? {}) as Record<string, unknown>;
    const formatted = formatCellValue(col, row);
    args.value = sanitizeExportValue(formatted);
  };

  if (!mounted) {
    return (
      <div
        style={{ minHeight: typeof height === 'number' ? `${Math.min(height, 360)}px` : height }}
        className="rounded-xl border border-[#E5E7EB] bg-white p-4 flex items-center justify-center text-xs text-[#64748B]"
      >
        Đang khởi tạo bảng dữ liệu Syncfusion...
      </div>
    );
  }

  return (
    <div className="agro-syncfusion-grid w-full">
      <GridComponent
        key={columnsKey}
        ref={gridRef}
        dataSource={data}
        allowPaging={true}
        allowSorting={true}
        allowFiltering={true}
        allowExcelExport={true}
        allowTextWrap={false}
        enableHover={true}
        gridLines="Horizontal"
        rowHeight={42}
        height={height}
        pageSettings={pageSettings}
        filterSettings={filterSettings}
        toolbar={toolbar}
        toolbarClick={handleToolbarClick}
        excelQueryCellInfo={handleExcelQueryCellInfo}
        excelExportComplete={handleExcelExportComplete}
      >
        <ColumnsDirective>
          {columns.map((col) => {
            const align = col.align ?? defaultAlign(col.kind);
            const isNumeric =
              col.kind === 'number' ||
              col.kind === 'money' ||
              col.kind === 'pct' ||
              col.kind === 'decimal';
            const isActionCol = col.field === 'actions';

            const accessor =
              !col.template && col.kind && col.kind !== 'text'
                ? (_field: string, rowData: object) =>
                    formatCellValue(col, rowData as Record<string, unknown>)
                : undefined;

            return (
              <ColumnDirective
                key={col.field + col.headerText}
                field={col.field}
                headerText={col.headerText}
                width={col.width ?? 150}
                textAlign={align}
                headerTextAlign={align}
                allowSorting={col.allowSorting ?? !isActionCol}
                allowFiltering={col.allowFiltering ?? !isActionCol}
                allowSearching={col.allowSearching ?? !isActionCol}
                valueAccessor={accessor}
                template={
                  col.template
                    ? (rowData: Record<string, unknown>) => col.template!(rowData)
                    : undefined
                }
                customAttributes={
                  isNumeric
                    ? { class: 'agro-num-cell' }
                    : col.kind === 'date' || col.kind === 'datetime'
                      ? { class: 'agro-date-cell' }
                      : undefined
                }
              />
            );
          })}
        </ColumnsDirective>
        <Inject services={[Page, Sort, Filter, Toolbar, Search, ExcelExport]} />
      </GridComponent>
    </div>
  );
}
