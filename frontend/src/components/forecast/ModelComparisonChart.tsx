'use client';

import React, { useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import { ModelComparisonMetrics } from '@/types';

interface ModelComparisonChartProps {
  data: ModelComparisonMetrics[];
  metricToDisplay?: 'mae' | 'rmse' | 'mape' | 'r2';
  onMetricChange?: (m: 'mae' | 'rmse' | 'mape' | 'r2') => void;
}

const METRIC_CONFIG = {
  mae: {
    title: 'Sai số tuyệt đối trung bình (MAE)',
    desc: 'Giá trị càng thấp càng chính xác',
    unit: 'đ',
  },
  rmse: {
    title: 'Căn bậc hai sai số toàn phương (RMSE)',
    desc: 'Phản ánh độ lệch chuẩn sai số dự báo',
    unit: 'đ',
  },
  mape: {
    title: 'Tỷ lệ phần trăm sai số (MAPE)',
    desc: 'Sai số tương đối trên tập kiểm thử',
    unit: '%',
  },
  r2: {
    title: 'Hệ số xác định (R²)',
    desc: 'Mức độ khớp xu hướng (tối đa 1.0)',
    unit: '',
  },
};

export const ModelComparisonChart: React.FC<ModelComparisonChartProps> = ({
  data,
  metricToDisplay: initialMetric = 'mae',
  onMetricChange,
}) => {
  const [activeMetric, setActiveMetric] = useState<'mae' | 'rmse' | 'mape' | 'r2'>(initialMetric);

  const handleSelectMetric = (m: 'mae' | 'rmse' | 'mape' | 'r2') => {
    setActiveMetric(m);
    if (onMetricChange) onMetricChange(m);
  };

  const sortedData = [...data].sort((a, b) => {
    if (activeMetric === 'r2') return (b.r2 || 0) - (a.r2 || 0);
    return (a[activeMetric] || 0) - (b[activeMetric] || 0);
  });
  const bestModelName = sortedData.length > 0 ? sortedData[0].modelName : 'LSTM';

  return (
    <div className="bg-white rounded-xl border border-zinc-200/90 p-5 space-y-4 font-sans">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3.5 border-b border-zinc-100">
        <div>
          <h3 className="text-[15px] font-semibold text-zinc-900">
            So sánh sai số giữa các mô hình
          </h3>
          <p className="text-[12.5px] text-zinc-500 mt-0.5">
            {METRIC_CONFIG[activeMetric].title} · {METRIC_CONFIG[activeMetric].desc}
          </p>
        </div>

        <div className="flex items-center gap-0.5 bg-zinc-100 p-0.5 rounded-lg border border-zinc-200/60 shrink-0 w-fit">
          {(['mae', 'rmse', 'mape', 'r2'] as const).map((metric) => (
            <button
              key={metric}
              onClick={() => handleSelectMetric(metric)}
              className={`px-2.5 py-1 rounded-md text-[12px] font-medium transition-all cursor-pointer ${
                activeMetric === metric
                  ? 'bg-white text-zinc-900 shadow-2xs font-semibold'
                  : 'text-zinc-500 hover:text-zinc-800'
              }`}
            >
              {metric.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      <div className="h-[240px] w-full pt-1">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 8, right: 12, left: -12, bottom: 8 }}
            barSize={34}
          >
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F4F4F5" />
            <XAxis
              dataKey="modelName"
              axisLine={{ stroke: '#E4E4E7' }}
              tickLine={false}
              tick={{ fill: '#52525B', fontSize: 12, fontWeight: 500 }}
              dy={6}
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#71717A', fontSize: 11, fontWeight: 400 }}
              domain={activeMetric === 'r2' ? [0, 1] : ['auto', 'auto']}
              tickFormatter={(v) => {
                if (activeMetric === 'r2') return Number(v).toFixed(2);
                if (activeMetric === 'mape') return `${Number(v).toFixed(1)}%`;
                if (Number(v) >= 1000) return `${(Number(v) / 1000).toFixed(1)}k`;
                return Number(v).toLocaleString('vi-VN');
              }}
            />
            <Tooltip
              content={({ active, payload, label }) => {
                if (active && payload && payload.length) {
                  const val = Number(payload[0].value || 0);
                  const isBest = label === bestModelName;
                  return (
                    <div className="bg-zinc-900 text-white px-3 py-2.5 rounded-lg shadow-lg text-xs space-y-1 min-w-[165px]">
                      <div className="font-medium border-b border-zinc-800 pb-1 flex items-center justify-between gap-3">
                        <span className="text-zinc-200">{label}</span>
                        {isBest && (
                          <span className="text-[10px] font-medium px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400">
                            Sai số thấp nhất
                          </span>
                        )}
                      </div>
                      <div className="flex justify-between items-center pt-0.5">
                        <span className="text-zinc-400">{activeMetric.toUpperCase()}:</span>
                        <span className="font-semibold text-white font-mono">
                          {activeMetric === 'r2' ? val.toFixed(3) : Math.round(val).toLocaleString('vi-VN')} {METRIC_CONFIG[activeMetric].unit}
                        </span>
                      </div>
                    </div>
                  );
                }
                return null;
              }}
              cursor={{ fill: '#F4F4F5', opacity: 0.6 }}
            />
            <Bar
              dataKey={activeMetric}
              radius={[4, 4, 0, 0]}
              animationDuration={500}
            >
              {data.map((entry, index) => {
                const isBest = entry.modelName === bestModelName;
                return (
                  <Cell
                    key={`cell-${index}`}
                    fill={isBest ? '#18181B' : '#D4D4D8'}
                  />
                );
              })}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default ModelComparisonChart;
