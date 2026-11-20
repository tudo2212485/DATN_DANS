'use client';

import React, { useState, useMemo } from 'react';
import { ModelComparisonMetrics } from '@/types';
import { formatNumberVN } from '@/lib/formatters';
import FinChart from '@/components/ui/FinChart';

interface ModelComparisonChartProps {
  data: ModelComparisonMetrics[];
  metricToDisplay?: 'mae' | 'rmse' | 'mape' | 'r2';
  onMetricChange?: (m: 'mae' | 'rmse' | 'mape' | 'r2') => void;
  unit?: string;
}

const METRIC_LABELS: Record<'mae' | 'rmse' | 'mape' | 'r2', { label: string; title: string; desc: string }> = {
  mae: {
    label: 'MAE',
    title: 'Sai số tuyệt đối trung bình (MAE)',
    desc: 'Giá trị càng thấp càng chính xác',
  },
  rmse: {
    label: 'RMSE',
    title: 'Căn bậc hai sai số toàn phương (RMSE)',
    desc: 'Phản ánh độ lệch chuẩn sai số dự báo',
  },
  mape: {
    label: 'MAPE',
    title: 'Tỷ lệ phần trăm sai số tuyệt đối (MAPE)',
    desc: 'Sai số tương đối (%) trên tập kiểm thử',
  },
  r2: {
    label: 'R²',
    title: 'Hệ số xác định (R²)',
    desc: 'Mức độ khớp phương sai xu hướng',
  },
};

export const ModelComparisonChart: React.FC<ModelComparisonChartProps> = ({
  data,
  metricToDisplay: initialMetric = 'mae',
  onMetricChange,
  unit = 'VNĐ/kg',
}) => {
  const [activeMetric, setActiveMetric] = useState<'mae' | 'rmse' | 'mape' | 'r2'>(initialMetric);

  const handleSelectMetric = (m: 'mae' | 'rmse' | 'mape' | 'r2') => {
    setActiveMetric(m);
    if (onMetricChange) onMetricChange(m);
  };

  const sortedData = useMemo(() => {
    return [...data].sort((a, b) => {
      if (activeMetric === 'r2') return (b.r2 || 0) - (a.r2 || 0);
      return (a[activeMetric] || 0) - (b[activeMetric] || 0);
    });
  }, [data, activeMetric]);
  const bestModelName = sortedData.length > 0 ? sortedData[0].modelName : 'LSTM';

  const chartRows = useMemo(() => {
    return data.map((item) => {
      const val = Number(item[activeMetric] ?? 0);
      let formattedLabel = '';
      if (activeMetric === 'r2') {
        formattedLabel = val.toFixed(3);
      } else if (activeMetric === 'mape') {
        formattedLabel = `${val.toFixed(2)}%`;
      } else {
        formattedLabel = `${formatNumberVN(Math.round(val))} ${unit}`;
      }
      return {
        x: item.modelName,
        value: val,
        isBest: item.modelName === bestModelName,
        labelText: activeMetric === 'r2' ? val.toFixed(2) : activeMetric === 'mape' ? `${val.toFixed(1)}%` : formatNumberVN(Math.round(val)),
        tipText: formattedLabel,
      };
    });
  }, [data, activeMetric, unit, bestModelName]);

  return (
    <div className="bg-white rounded-xl border border-[#E5E7EB] p-4 sm:p-5 space-y-3 font-sans">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-2.5 border-b border-[#E5E7EB]">
        <div>
          <h3 className="text-[14px] font-bold text-[#1E293B]">
            So sánh hiệu năng 5 mô hình
          </h3>
          <p className="text-[12px] text-[#64748B] mt-0.5">
            {METRIC_LABELS[activeMetric].title}
          </p>
        </div>

        {/* Segmented Control: MAE | RMSE | MAPE | R² */}
        <div className="flex items-center gap-0.5 bg-[#F8FAF9] p-0.5 rounded-lg border border-[#E5E7EB] shrink-0 w-fit">
          {(['mae', 'rmse', 'mape', 'r2'] as const).map((metric) => (
            <button
              key={metric}
              type="button"
              onClick={() => handleSelectMetric(metric)}
              className={`px-2.5 py-1 rounded-md text-xs font-semibold transition-colors cursor-pointer ${
                activeMetric === metric
                  ? 'bg-[#2F6F4E] text-white'
                  : 'text-[#334155] hover:text-[#1E293B]'
              }`}
            >
              {METRIC_LABELS[metric].label}
            </button>
          ))}
        </div>
      </div>

      <div className="w-full pt-1">
        {chartRows.length > 0 ? (
          (() => {
            const vals = chartRows.map((r) => r.value);
            const maxVal = Math.max(...vals, 0);
            const minVal = Math.min(...vals, 0);
            const isNonNegMetric = activeMetric !== 'r2' || minVal >= 0;
            const yMin = isNonNegMetric ? 0 : undefined;
            const yMax =
              activeMetric === 'r2'
                ? isNonNegMetric
                  ? Math.max(1.15, Math.ceil(maxVal * 12) / 10)
                  : undefined
                : activeMetric === 'mape'
                  ? Math.max(1, Math.ceil(maxVal * 1.25 * 2) / 2)
                  : maxVal > 0
                    ? Math.ceil((maxVal * 1.22) / 100) * 100
                    : undefined;

            return (
              <FinChart
                id={`agro-model-cmp-${activeMetric}`}
                data={chartRows}
                xName="x"
                height={250}
                showLegend={false}
                yMinimum={yMin}
                yMaximum={yMax}
                yFormat={(v) => {
                  if (activeMetric === 'r2') return Number(v).toFixed(2);
                  if (activeMetric === 'mape') return `${Number(v).toFixed(1)}%`;
                  if (Math.abs(v) >= 1000) return `${(v / 1000).toFixed(1)}k`;
                  return formatNumberVN(v);
                }}
                series={[
                  {
                    type: 'Column',
                    name: METRIC_LABELS[activeMetric].label,
                    yName: 'value',
                    color: '#2F6F4E',
                    tipField: 'tipText',
                    labels: true,
                    labelField: 'labelText',
                  },
                ]}
              />
            );
          })()
        ) : (
          <div className="h-[250px] flex items-center justify-center text-xs text-[#64748B]">
            Chưa có dữ liệu so sánh mô hình.
          </div>
        )}
      </div>
    </div>
  );
};

export default ModelComparisonChart;
