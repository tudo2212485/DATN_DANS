'use client';

import React from 'react';
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
}

const METRIC_LABELS = {
  mae: 'Mean Absolute Error (MAE) - Càng thấp càng tốt',
  rmse: 'Root Mean Squared Error (RMSE) - Càng thấp càng tốt',
  mape: 'Mean Absolute Pct Error (MAPE) - Càng thấp càng tốt',
  r2: 'R-Squared (R²) - Càng cao càng tốt (Tối đa 1.0)',
};

export const ModelComparisonChart: React.FC<ModelComparisonChartProps> = ({
  data,
  metricToDisplay = 'mae',
}) => {
  // Find best model based on metric
  const sortedData = [...data].sort((a, b) => {
    if (metricToDisplay === 'r2') return b.r2 - a.r2; // Higher is better
    return a[metricToDisplay] - b[metricToDisplay]; // Lower is better
  });
  const bestModelName = sortedData.length > 0 ? sortedData[0].modelName : '';

  return (
    <div className="bg-card rounded-2xl border border-border-subtle p-6 shadow-card h-[400px] flex flex-col">
      <h3 className="text-lg font-bold text-primary-text mb-1">
        Model Comparison
      </h3>
      <p className="text-sm text-secondary-text mb-6">
        {METRIC_LABELS[metricToDisplay]}
      </p>

      <div className="flex-1 w-full min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 10, right: 10, left: 0, bottom: 20 }}
            barSize={40}
          >
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border-subtle)" />
            <XAxis 
              dataKey="modelName" 
              axisLine={false}
              tickLine={false}
              tick={{ fill: 'var(--secondary-text)', fontSize: 12, fontWeight: 500 }}
              dy={10}
            />
            <YAxis 
              axisLine={false}
              tickLine={false}
              tick={{ fill: 'var(--secondary-text)', fontSize: 12 }}
              dx={-10}
              domain={metricToDisplay === 'r2' ? [0, 1] : ['auto', 'auto']}
            />
            <Tooltip
              content={({ active, payload, label }) => {
                if (active && payload && payload.length) {
                  return (
                    <div className="bg-white/95 backdrop-blur-md border border-border-subtle p-3 rounded-xl shadow-lg text-xs">
                      <p className="font-bold text-primary-text mb-1">{label}</p>
                      <p className="text-secondary-text">
                        {METRIC_LABELS[metricToDisplay].split(' -')[0]}:{' '}
                        <span className="font-bold text-brand">
                          {Number(payload[0].value).toFixed(2)}
                        </span>
                      </p>
                      {label === bestModelName && (
                        <p className="text-[11px] text-brand font-extrabold mt-1">🏆 Mô hình tối ưu nhất</p>
                      )}
                    </div>
                  );
                }
                return null;
              }}
              cursor={{ fill: 'var(--border-subtle)', opacity: 0.2 }}
            />
            <Bar
              dataKey={metricToDisplay}
              radius={[4, 4, 0, 0]}
              animationDuration={1500}
            >
              {data.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={entry.modelName === bestModelName ? '#9C6644' : '#E8D8C8'}
                  stroke={entry.modelName === bestModelName ? '#9C6644' : 'transparent'}
                  strokeWidth={2}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default ModelComparisonChart;
