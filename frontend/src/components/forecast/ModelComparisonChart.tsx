'use client';

import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import { ModelComparisonMetrics } from '@/types';

interface ModelComparisonChartProps {
  data: ModelComparisonMetrics[];
  metricToDisplay?: 'mae' | 'rmse' | 'mape' | 'r2';
}

const METRIC_LABELS = {
  mae: 'Mean Absolute Error (MAE) - Lower is better',
  rmse: 'Root Mean Squared Error (RMSE) - Lower is better',
  mape: 'Mean Absolute Pct Error (MAPE) - Lower is better',
  r2: 'R-Squared (R²) - Higher is better',
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
  
  const bestModelName = sortedData.length > 0 ? sortedData[0].model_name : '';

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-card border border-border-subtle p-3 rounded-lg shadow-lg">
          <p className="font-bold text-primary-text mb-1">{label}</p>
          <p className="text-sm text-secondary-text">
            {METRIC_LABELS[metricToDisplay].split(' -')[0]}:{' '}
            <span className="font-semibold text-brand">
              {Number(payload[0].value).toFixed(2)}
            </span>
          </p>
          {label === bestModelName && (
            <p className="text-xs text-brand font-semibold mt-1">🏆 Best Performing</p>
          )}
        </div>
      );
    }
    return null;
  };

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
              dataKey="model_name" 
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
            <Tooltip content={<CustomTooltip />} cursor={{ fill: 'var(--border-subtle)', opacity: 0.2 }} />
            <Bar
              dataKey={metricToDisplay}
              radius={[4, 4, 0, 0]}
              animationDuration={1500}
            >
              {data.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={entry.model_name === bestModelName ? 'var(--brand)' : 'var(--brand-badge)'}
                  stroke={entry.model_name === bestModelName ? 'var(--brand)' : 'transparent'}
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
