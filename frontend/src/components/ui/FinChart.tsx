'use client';

import React, { useEffect, useMemo, useState } from 'react';
import {
  ChartComponent,
  SeriesCollectionDirective,
  SeriesDirective,
  Inject,
  ColumnSeries,
  LineSeries,
  SplineSeries,
  AreaSeries,
  SplineAreaSeries,
  RangeAreaSeries,
  Category,
  DateTime,
  Legend,
  Tooltip,
  DataLabel,
  Crosshair,
  IAxisLabelRenderEventArgs,
  ITooltipRenderEventArgs,
  ISharedTooltipRenderEventArgs,
  IPointRenderEventArgs,
  AxisModel,
  TooltipSettingsModel,
  CrosshairSettingsModel,
  LegendSettingsModel,
  MarginModel,
  ChartAreaModel,
} from '@syncfusion/ej2-react-charts';
import { initSyncfusion } from '@/lib/syncfusion';

// Đảm bảo Syncfusion license sẵn sàng trước khi mount ChartComponent
initSyncfusion();

export interface FinSeries {
  type: 'Line' | 'Spline' | 'Area' | 'SplineArea' | 'RangeArea' | 'Column';
  name: string;
  yName?: string;
  high?: string;
  low?: string;
  color: string;
  dashArray?: string;
  width?: number;
  opacity?: number;
  tipField?: string;
  labels?: boolean;
  labelField?: string;
  hidden?: boolean;
  showMarkers?: boolean;
}

interface FinChartProps {
  id: string;
  data: Record<string, unknown>[];
  xName?: string;
  xValueType?: 'Category' | 'DateTime';
  xLabelFormat?: string;
  series: FinSeries[];
  height?: number;
  yFormat: (value: number) => string;
  tooltipFormat?: (value: number) => string;
  yMinimum?: number;
  yMaximum?: number;
  yInterval?: number;
  showLegend?: boolean;
  xLabelRotation?: number;
  sharedTooltip?: boolean;
  showCrosshair?: boolean;
  zeroReferenceLine?: boolean;
}

export default function FinChart({
  id,
  data,
  xName = 'x',
  xValueType = 'Category',
  xLabelFormat,
  series,
  height = 300,
  yFormat,
  tooltipFormat,
  yMinimum,
  yMaximum,
  yInterval,
  showLegend = false,
  xLabelRotation,
  sharedTooltip,
  showCrosshair,
}: FinChartProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    initSyncfusion();
    setMounted(true);
  }, []);

  const visibleSeries = useMemo(() => series.filter((s) => !s.hidden), [series]);
  const isColumnChart = visibleSeries.some((s) => s.type === 'Column');
  const hasTopLabels = visibleSeries.some((s) => s.type === 'Column' && s.labels);
  const enableCrosshair = showCrosshair ?? !isColumnChart;
  const enableSharedTooltip = sharedTooltip ?? !isColumnChart;

  // ID cố định, duy nhất và luôn đồng bộ 1:1 với React key để tránh lệch #id_Secondary_Element khi hover tooltip
  const chartDomId = useMemo(() => {
    const base = id.replace(/[^a-zA-Z0-9_-]/g, '-');
    const seriesTag = visibleSeries
      .map((s) => `${s.type}-${(s.yName || s.name).replace(/[^a-zA-Z0-9]/g, '')}`)
      .join('_');
    return seriesTag ? `${base}--${seriesTag}` : base;
  }, [id, visibleSeries]);

  const chartArea: ChartAreaModel = useMemo(() => ({ border: { width: 0 } }), []);

  const margin: MarginModel = useMemo(
    () => ({ top: hasTopLabels ? 20 : 12, right: 16, left: 6, bottom: 8 }),
    [hasTopLabels]
  );

  const legendSettings: LegendSettingsModel = useMemo(
    () => ({
      visible: showLegend,
      position: 'Top',
      textStyle: {
        color: '#334155',
        fontFamily: 'Be Vietnam Pro, sans-serif',
        size: '12px',
        fontWeight: '600',
      },
    }),
    [showLegend]
  );

  const tooltipSettings: TooltipSettingsModel = useMemo(
    () => ({
      enable: true,
      shared: enableSharedTooltip,
      enableAnimation: false,
      fadeOutDuration: 0,
      fill: '#FFFFFF',
      border: { width: 1, color: '#E5E7EB' },
      textStyle: {
        color: '#1E293B',
        fontFamily: 'Be Vietnam Pro, sans-serif',
        size: '12px',
      },
      header: '<b>${point.x}</b>',
    }),
    [enableSharedTooltip]
  );

  const crosshairSettings: CrosshairSettingsModel = useMemo(
    () =>
      enableCrosshair
        ? {
            enable: true,
            lineType: 'Vertical',
            line: { color: '#94A3B8', width: 1, dashArray: '4,3' },
          }
        : { enable: false },
    [enableCrosshair]
  );

  const primaryXAxis: AxisModel = useMemo(
    () => ({
      valueType: xValueType,
      ...(xValueType === 'DateTime' ? { labelFormat: xLabelFormat || 'dd/MM/yy' } : {}),
      majorGridLines: { width: 0 },
      majorTickLines: { width: 0 },
      lineStyle: { color: '#E5E7EB', width: 1 },
      labelStyle: {
        color: isColumnChart ? '#1E293B' : '#64748B',
        fontFamily: 'Be Vietnam Pro, sans-serif',
        size: isColumnChart ? '12px' : '11.5px',
        fontWeight: isColumnChart ? '600' : '500',
      },
      labelIntersectAction: xLabelRotation ? 'Rotate45' : 'Hide',
      labelRotation: xLabelRotation ?? 0,
      edgeLabelPlacement: 'Shift',
    }),
    [isColumnChart, xLabelRotation, xValueType, xLabelFormat]
  );

  const primaryYAxis: AxisModel = useMemo(
    () => ({
      minimum: yMinimum,
      maximum: yMaximum,
      interval: yInterval,
      rangePadding:
        yMinimum !== undefined
          ? yMaximum !== undefined
            ? 'None'
            : 'Normal'
          : hasTopLabels
            ? 'Additional'
            : 'Auto',
      lineStyle: { width: 0 },
      majorTickLines: { width: 0 },
      majorGridLines: { color: '#E5E7EB', width: 1, dashArray: '3,3' },
      labelStyle: {
        color: '#64748B',
        fontFamily: 'Be Vietnam Pro, sans-serif',
        size: '11.5px',
        fontWeight: '500',
      },
    }),
    [yMinimum, yMaximum, yInterval, hasTopLabels]
  );

  const handleAxisLabelRender = (args: IAxisLabelRenderEventArgs) => {
    if (args.axis.name === 'primaryYAxis') {
      args.text = yFormat(Number(args.value));
    }
  };

  const valueFormatter = tooltipFormat ?? yFormat;

  const findRowForPoint = (pt: { index?: number; x?: unknown } | undefined) => {
    const idx = Number(pt?.index ?? -1);
    if (idx >= 0 && idx < data.length) return data[idx];
    if (pt?.x instanceof Date) {
      const targetMs = pt.x.getTime();
      return data.find((r) => {
        const xv = r[xName];
        return xv instanceof Date && xv.getTime() === targetMs;
      });
    }
    return undefined;
  };

  const handleTooltipRender = (args: ITooltipRenderEventArgs) => {
    const row = findRowForPoint(args.point);
    const seriesName = String(args.series?.name ?? '');
    const matched = visibleSeries.find((s) => s.name === seriesName);

    if (row && row.fullDate) {
      args.headerText = `<b>${String(row.fullDate)}</b>`;
    }

    if (matched?.tipField && row && row[matched.tipField] !== undefined) {
      args.text = `${seriesName}: <b>${String(row[matched.tipField])}</b>`;
    } else if (args.point?.y !== undefined && args.point?.y !== null) {
      args.text = `${seriesName}: <b>${valueFormatter(Number(args.point.y))}</b>`;
    }
  };

  const handleSharedTooltipRender = (args: ISharedTooltipRenderEventArgs) => {
    if (!args.point || !args.series || !args.text) return;
    const firstRow = findRowForPoint(args.point[0]);
    if (firstRow && firstRow.fullDate) {
      args.headerText = `<b>${String(firstRow.fullDate)}</b>`;
    }

    args.text = args.point.map((pt, i) => {
      const sObj = args.series[i];
      const sName = String(sObj?.name ?? '');
      const matched = visibleSeries.find((s) => s.name === sName);
      const row = findRowForPoint(pt);
      if (matched?.tipField && row && row[matched.tipField] !== undefined) {
        return `${sName}: <b>${String(row[matched.tipField])}</b>`;
      }
      if (pt?.y !== undefined && pt?.y !== null) {
        return `${sName}: <b>${valueFormatter(Number(pt.y))}</b>`;
      }
      return args.text?.[i] ?? '';
    });
  };

  const handlePointRender = (args: IPointRenderEventArgs) => {
    if (!isColumnChart) return;
    const idx = Number(args.point?.index ?? -1);
    const row = idx >= 0 && idx < data.length ? data[idx] : undefined;
    if (row && typeof row.isBest === 'boolean') {
      args.fill = row.isBest ? '#2F6F4E' : '#94A3B8';
    }
  };

  if (!mounted) {
    return (
      <div
        style={{ height: `${height}px` }}
        className="w-full rounded-lg bg-[#F8FAF9]/60 flex items-center justify-center text-xs text-[#64748B]"
      >
        Đang khởi tạo biểu đồ...
      </div>
    );
  }

  if (data.length === 0 || visibleSeries.length === 0) {
    return (
      <div
        style={{ height: `${height}px` }}
        className="w-full rounded-lg bg-[#F8FAF9]/60 flex items-center justify-center text-xs text-[#64748B]"
      >
        {data.length === 0 ? 'Chưa có dữ liệu biểu đồ.' : 'Chọn ít nhất 1 mặt hàng để hiển thị biểu đồ.'}
      </div>
    );
  }

  return (
    <div style={{ height: `${height}px` }} className="w-full">
      <ChartComponent
        key={chartDomId}
        id={chartDomId}
        height={`${height}px`}
        width="100%"
        background="transparent"
        chartArea={chartArea}
        margin={margin}
        primaryXAxis={primaryXAxis}
        primaryYAxis={primaryYAxis}
        legendSettings={legendSettings}
        tooltip={tooltipSettings}
        crosshair={crosshairSettings}
        axisLabelRender={handleAxisLabelRender}
        tooltipRender={handleTooltipRender}
        sharedTooltipRender={handleSharedTooltipRender}
        pointRender={handlePointRender}
      >
        <Inject
          services={[
            ColumnSeries,
            LineSeries,
            SplineSeries,
            AreaSeries,
            SplineAreaSeries,
            RangeAreaSeries,
            Category,
            DateTime,
            Legend,
            Tooltip,
            DataLabel,
            Crosshair,
          ]}
        />
        <SeriesCollectionDirective>
          {visibleSeries.map((s) => {
            const isArea = s.type === 'Area' || s.type === 'SplineArea';
            const isColumn = s.type === 'Column';

            return (
              <SeriesDirective
                key={s.name + (s.yName ?? '')}
                dataSource={data}
                xName={xName}
                yName={s.yName}
                high={s.high}
                low={s.low}
                name={s.name}
                type={s.type}
                fill={s.color}
                width={s.width ?? 2.25}
                dashArray={s.dashArray}
                opacity={isArea ? (s.opacity ?? 0.16) : (s.opacity ?? 1)}
                border={
                  isArea
                    ? { width: s.width ?? 2.25, color: s.color }
                    : undefined
                }
                columnWidth={isColumn ? 0.52 : undefined}
                cornerRadius={isColumn ? { topLeft: 6, topRight: 6 } : undefined}
                animation={{ enable: false }}
                marker={{
                  visible: s.showMarkers ?? (!isColumn && data.length <= 45),
                  width: 6,
                  height: 6,
                  fill: s.color,
                  border: { width: 1.5, color: '#FFFFFF' },
                  dataLabel: s.labels
                    ? {
                        visible: true,
                        name: s.labelField || s.yName,
                        position: 'Outer',
                        font: {
                          color: '#1E293B',
                          fontWeight: '700',
                          size: '11.5px',
                          fontFamily: 'Be Vietnam Pro, sans-serif',
                        },
                      }
                    : { visible: false },
                }}
              />
            );
          })}
        </SeriesCollectionDirective>
      </ChartComponent>
    </div>
  );
}
