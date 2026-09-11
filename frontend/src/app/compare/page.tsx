'use client';

import React, { useState, useEffect } from 'react';
import Header from '@/components/layout/Header';
import {
  fetchMarketComparison,
  fetchRegionalPricesApi,
} from '@/lib/api';
import { ComparisonDataPoint, RegionalPriceItem } from '@/types';
import { COMPARISON_SERIES } from '@/lib/mockData';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from 'recharts';
import {
  TrendingUp,
  MapPin,
  Filter,
  ArrowRight,
  Loader2,
} from 'lucide-react';
import Link from 'next/link';

export default function ComparePage() {
  const [comparisonData, setComparisonData] = useState<ComparisonDataPoint[]>(COMPARISON_SERIES);
  const [regionalPrices, setRegionalPrices] = useState<RegionalPriceItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Active series visibility toggles
  const [activeSeries, setActiveSeries] = useState<{ [key: string]: boolean }>({
    rice: true,
    coffee: true,
    pepper: true,
    sugar: true,
  });

  const [selectedRegionFilter, setSelectedRegionFilter] = useState<string>('ALL');

  useEffect(() => {
    async function loadData() {
      try {
        const [cmpData, rData] = await Promise.all([
          fetchMarketComparison(),
          fetchRegionalPricesApi(),
        ]);
        if (cmpData && cmpData.length > 0) setComparisonData(cmpData);
        if (rData && rData.length > 0) setRegionalPrices(rData);
      } catch (err) {
        console.error('Failed to load comparison data:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, []);

  const toggleSeries = (key: string) => {
    setActiveSeries((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const filteredRegionalPrices = regionalPrices.filter((p) => {
    if (selectedRegionFilter === 'ALL') return true;
    return p.region.toLowerCase().includes(selectedRegionFilter.toLowerCase());
  });

  const uniqueRegions = Array.from(new Set(regionalPrices.map((p) => p.region.split('(')[0].trim()))).filter(Boolean);

  return (
    <div className="space-y-6">
      <Header
        title="So Sánh Thị Trường & Giá Vùng Miền"
        subtitle="Đối sánh tương quan biến động giá và mức chênh lệch giữa các vùng trọng điểm"
        showLiveBadge={true}
      />

      {/* Series Toggle Selector Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { key: 'rice', label: 'Lúa gạo IR504', color: '#10B981', price: '7,850 đ/kg' },
          { key: 'coffee', label: 'Cà phê Robusta', color: '#527853', price: '62,300 đ/kg' },
          { key: 'pepper', label: 'Hồ tiêu đen', color: '#8B5CF6', price: '142,000 đ/kg' },
          { key: 'sugar', label: 'Mía đường', color: '#F59E0B', price: '1,150,000 đ/tấn' },
        ].map((item) => {
          const isActive = activeSeries[item.key];
          return (
            <button
              key={item.key}
              onClick={() => toggleSeries(item.key)}
              className={`p-3.5 rounded-2xl border text-left transition-all shadow-xs ${
                isActive
                  ? 'bg-white border-brand shadow-sm ring-1 ring-brand/20'
                  : 'bg-canvas border-border-subtle opacity-60'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-primary-text">{item.label}</span>
                <span
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: isActive ? item.color : '#A89F91' }}
                />
              </div>
              <div className="text-sm font-extrabold text-brand font-mono mt-1">{item.price}</div>
              <div className="text-[10px] text-secondary-text mt-0.5 font-medium">
                {isActive ? 'Đang hiển thị' : 'Đã ẩn khỏi biểu đồ'}
              </div>
            </button>
          );
        })}
      </div>

      {/* Main Chart Section: Multi-series Trend Comparison */}
      <div className="p-6 rounded-2xl bg-white border border-border-subtle shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-border-subtle">
          <div>
            <h3 className="text-base font-bold text-primary-text flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-brand" />
              Biểu Đồ Xu Hướng Giá Tương Quan (Normalized Growth Curve)
            </h3>
            <p className="text-xs text-secondary-text mt-0.5">
              Theo dõi tương quan nhịp độ tăng/giảm giá của các nhóm nông sản xuất khẩu
            </p>
          </div>
          {isLoading && (
            <div className="flex items-center gap-1.5 text-xs text-secondary-text font-medium">
              <Loader2 className="w-4 h-4 animate-spin text-brand" />
              Đang làm mới dữ liệu...
            </div>
          )}
        </div>

        <div className="h-[360px] w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={comparisonData} margin={{ top: 10, right: 15, left: 10, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#F0EBE5" vertical={false} />
              <XAxis
                dataKey="date"
                tickLine={false}
                axisLine={{ stroke: '#EAE5DF' }}
                tick={{ fill: '#7C6F62', fontSize: 11, fontWeight: 500 }}
              />
              <YAxis
                domain={['auto', 'auto']}
                tickLine={false}
                axisLine={false}
                tick={{ fill: '#7C6F62', fontSize: 11, fontWeight: 500 }}
                tickFormatter={(val) => `${(val / 1000).toFixed(0)}k`}
              />
              <Tooltip
                content={({ active, payload, label }) => {
                  if (active && payload && payload.length) {
                    return (
                      <div className="bg-white/95 backdrop-blur-md p-3.5 rounded-xl border border-border-subtle shadow-xl text-xs space-y-1.5 min-w-[180px]">
                        <div className="font-bold text-primary-text border-b border-border-subtle pb-1">
                          Thời điểm: {label}
                        </div>
                        {payload.map((entry) => (
                          <div
                            key={entry.dataKey as string}
                            className="font-semibold flex justify-between gap-3"
                            style={{ color: entry.color }}
                          >
                            <span>{entry.name}:</span>
                            <span>{Number(entry.value || 0).toLocaleString('vi-VN')} đ</span>
                          </div>
                        ))}
                      </div>
                    );
                  }
                  return null;
                }}
              />
              <Legend wrapperStyle={{ paddingTop: '10px', fontSize: '12px' }} />

              {activeSeries.rice && (
                <Line
                  type="monotone"
                  dataKey="rice"
                  name="Lúa gạo IR504"
                  stroke="#10B981"
                  strokeWidth={2.5}
                  dot={{ r: 3 }}
                />
              )}
              {activeSeries.coffee && (
                <Line
                  type="monotone"
                  dataKey="coffee"
                  name="Cà phê Robusta"
                  stroke="#527853"
                  strokeWidth={2.5}
                  dot={{ r: 3 }}
                />
              )}
              {activeSeries.pepper && (
                <Line
                  type="monotone"
                  dataKey="pepper"
                  name="Hồ tiêu đen"
                  stroke="#8B5CF6"
                  strokeWidth={2.5}
                  dot={{ r: 3 }}
                />
              )}
              {activeSeries.sugar && (
                <Line
                  type="monotone"
                  dataKey="sugar"
                  name="Mía đường"
                  stroke="#F59E0B"
                  strokeWidth={2.5}
                  dot={{ r: 3 }}
                />
              )}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Regional Comparison Table */}
      <div className="p-6 rounded-2xl bg-white border border-border-subtle shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-border-subtle">
          <div>
            <h3 className="text-base font-bold text-primary-text flex items-center gap-2">
              <MapPin className="w-5 h-5 text-brand" />
              Bảng Khảo Sát Giá Chênh Lệch Các Vùng Miền
            </h3>
            <p className="text-xs text-secondary-text mt-0.5">
              So sánh biên độ giá sàn/trần và khối lượng giao dịch tại từng địa phương
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <Filter className="w-3.5 h-3.5 text-secondary-text" />
            <select
              value={selectedRegionFilter}
              onChange={(e) => setSelectedRegionFilter(e.target.value)}
              className="bg-canvas border border-border-subtle text-primary-text px-3 py-1.5 rounded-xl font-semibold focus:outline-none"
            >
              <option value="ALL">Toàn bộ khu vực</option>
              {uniqueRegions.map((r) => (
                <option key={r} value={r}>
                  {r}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-primary-text">
            <thead className="bg-canvas text-secondary-text uppercase text-[11px] font-extrabold border-b border-border-subtle">
              <tr>
                <th className="py-3 px-4">Mặt Hàng Nông Sản</th>
                <th className="py-3 px-4">Khu Vực / Tỉnh Thành</th>
                <th className="py-3 px-4">Giá Hiện Tại</th>
                <th className="py-3 px-4">Biên Độ Sàn / Trần</th>
                <th className="py-3 px-4">Biến Động</th>
                <th className="py-3 px-4">Nguồn Báo Giá</th>
                <th className="py-3 px-4 text-right">Chi Tiết</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle/60">
              {filteredRegionalPrices.map((item) => (
                <tr key={item.id} className="hover:bg-canvas/60 transition">
                  <td className="py-3.5 px-4 font-bold text-primary-text">{item.commodityName}</td>
                  <td className="py-3.5 px-4 text-secondary-text font-medium">{item.region}</td>
                  <td className="py-3.5 px-4 font-extrabold text-brand font-mono">{item.price}</td>
                  <td className="py-3.5 px-4 font-mono text-secondary-text">{item.minMax}</td>
                  <td className="py-3.5 px-4">
                    <span
                      className={`px-2 py-0.5 rounded-md font-bold text-[11px] ${
                        item.changePct >= 0
                          ? 'bg-emerald-50 text-emerald-700'
                          : 'bg-rose-50 text-rose-700'
                      }`}
                    >
                      {item.changePct >= 0 ? '+' : ''}
                      {item.changePct.toFixed(2)}%
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-[11px] text-secondary-text">{item.source}</td>
                  <td className="py-3.5 px-4 text-right">
                    <Link
                      href={`/commodities/${item.id}`}
                      className="text-brand font-bold hover:underline flex items-center justify-end gap-1"
                    >
                      <span>Xem AI</span>
                      <ArrowRight className="w-3 h-3" />
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
