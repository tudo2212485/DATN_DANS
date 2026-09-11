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
import { Award, BarChart3 } from 'lucide-react';

interface ModelComparisonChartProps {
  data: ModelComparisonMetrics[];
  metricToDisplay?: 'mae' | 'rmse' | 'mape' | 'r2';
  onMetricChange?: (m: 'mae' | 'rmse' | 'mape' | 'r2') => void;
}

const METRIC_CONFIG = {
  mae: {
    title: 'MAE (Mean Absolute Error)',
    desc: 'Sai số tuyệt đối trung bình (Càng thấp càng tốt)',
    unit: 'VNĐ',
  },
  rmse: {
    title: 'RMSE (Root Mean Squared Error)',
    desc: 'Căn bậc hai sai số toàn phương (Càng thấp càng tốt)',
    unit: 'VNĐ',
  },
  mape: {
    title: 'MAPE (% Sai số trung bình)',
    desc: 'Tỷ lệ phần trăm sai số dự báo (Càng thấp càng chuẩn xác)',
    unit: '%',
  },
  r2: {
    title: 'R² (R-Squared Score)',
    desc: 'Hệ số xác định độ phù hợp xu hướng (Càng cao càng tốt, tối đa 1.0)',
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

  // Find best model based on metric
  const sortedData = [...data].sort((a, b) => {
    if (activeMetric === 'r2') return (b.r2 || 0) - (a.r2 || 0); // Higher is better
    return (a[activeMetric] || 0) - (b[activeMetric] || 0); // Lower is better
  });
  const bestModelName = sortedData.length > 0 ? sortedData[0].modelName : 'LSTM';

  return (
    <div className="bg-card rounded-2xl border border-border-subtle p-5 sm:p-6 shadow-card space-y-4">
      {/* Top Header & Horizontal Segmented Tabs */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-border-subtle">
        <div>
          <h3 className="text-base font-bold text-primary-text flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-brand" />
            <span>Đối Sánh Hiệu Năng 5 Thuật Toán Machine Learning</span>
          </h3>
          <p className="text-xs text-secondary-text mt-0.5">
            {METRIC_CONFIG[activeMetric].title} · {METRIC_CONFIG[activeMetric].desc}
          </p>
        </div>

        {/* Horizontal Segmented Tabs */}
        <div className="flex items-center gap-1 bg-canvas p-1 rounded-xl border border-border-subtle shrink-0">
          {(['mae', 'rmse', 'mape', 'r2'] as const).map((metric) => (
            <button
              key={metric}
              onClick={() => handleSelectMetric(metric)}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                activeMetric === metric
                  ? 'bg-brand text-white shadow-xs'
                  : 'text-secondary-text hover:text-primary-text hover:bg-black/[0.03]'
              }`}
            >
              {metric.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {/* Chart Canvas */}
      <div className="h-[280px] w-full pt-2">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 10, right: 15, left: -10, bottom: 25 }}
            barSize={44}
          >
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F0ECE4" />
            <XAxis
              dataKey="modelName"
              axisLine={{ stroke: '#EFECE6' }}
              tickLine={false}
              tick={{ fill: '#4A3E3D', fontSize: 11, fontWeight: 700 }}
              dy={8}
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#8D7B68', fontSize: 11, fontWeight: 500 }}
              domain={activeMetric === 'r2' ? [0, 1] : ['auto', 'auto']}
              tickFormatter={(v) => {
                if (activeMetric === 'r2') return Number(v).toFixed(2);
                if (activeMetric === 'mape') return `${Number(v).toFixed(1)}%`;
                return Number(v).toLocaleString('vi-VN');
              }}
            />
            <Tooltip
              content={({ active, payload, label }) => {
                if (active && payload && payload.length) {
                  const val = Number(payload[0].value || 0);
                  const isBest = label === bestModelName;
                  return (
                    <div className="bg-white/95 backdrop-blur-md border border-border-subtle p-3 rounded-xl shadow-xl text-xs space-y-1 min-w-[170px]">
                      <div className="font-bold text-primary-text border-b border-border-subtle pb-1 flex items-center justify-between">
                        <span>{label}</span>
                        {isBest && (
                          <span className="text-[10px] font-extrabold px-1.5 py-0.5 rounded bg-brand/10 text-brand flex items-center gap-1">
                            <Award className="w-3 h-3 text-brand" />
                            Tối ưu
                          </span>
                        )}
                      </div>
                      <div className="flex justify-between items-center text-secondary-text pt-1">
                        <span>Chỉ số {activeMetric.toUpperCase()}:</span>
                        <span className="font-extrabold text-brand font-mono text-sm">
                          {activeMetric === 'r2' ? val.toFixed(3) : val.toLocaleString('vi-VN')} {METRIC_CONFIG[activeMetric].unit}
                        </span>
                      </div>
                    </div>
                  );
                }
                return null;
              }}
              cursor={{ fill: '#F5EFE6', opacity: 0.5 }}
            />
            <Bar
              dataKey={activeMetric}
              radius={[6, 6, 0, 0]}
              animationDuration={800}
            >
              {data.map((entry, index) => {
                const isBest = entry.modelName === bestModelName;
                return (
                  <Cell
                    key={`cell-${index}`}
                    fill={isBest ? '#527853' : '#D4CEBE'}
                    className="hover:opacity-90 transition-opacity"
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
