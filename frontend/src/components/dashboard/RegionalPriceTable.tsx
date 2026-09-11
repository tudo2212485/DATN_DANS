'use client';

import React, { useState, useEffect } from 'react';
import { MapPin, TrendingUp, TrendingDown, ArrowRight, Building2, Filter } from 'lucide-react';
import { RegionalPriceItem } from '@/types';
import { fetchRegionalPrices } from '@/lib/api';
import Link from 'next/link';

const FALLBACK_REGIONAL_PRICES: RegionalPriceItem[] = [
  {
    id: 1,
    commodityName: 'Lúa gạo IR504',
    code: 'RICE',
    region: 'Đồng bằng Sông Cửu Long',
    price: '8.065',
    unit: 'VNĐ/kg',
    minMax: '7.944 - 8.186',
    volume: '28.500 tấn',
    changePct: 1.2,
    source: 'VFA Hiệp hội Lương thực',
    updatedAt: 'Hôm nay',
  },
  {
    id: 2,
    commodityName: 'Cà phê Robusta',
    code: 'COFFEE',
    region: 'Tây Nguyên (Đắk Lắk, Lâm Đồng)',
    price: '93.800',
    unit: 'VNĐ/kg',
    minMax: '92.393 - 95.207',
    volume: '12.400 tấn',
    changePct: 2.5,
    source: 'giacaphe.com & VICOFA',
    updatedAt: 'Hôm nay',
  },
  {
    id: 3,
    commodityName: 'Hồ tiêu đen',
    code: 'PEPPER',
    region: 'Tây Nguyên & Đông Nam Bộ',
    price: '137.158',
    unit: 'VNĐ/kg',
    minMax: '135.101 - 139.216',
    volume: '4.800 tấn',
    changePct: -0.8,
    source: 'VPA Hiệp hội Hồ tiêu',
    updatedAt: 'Hôm nay',
  },
  {
    id: 4,
    commodityName: 'Mía đường 10 CCS',
    code: 'SUGAR',
    region: 'Miền Trung & Tây Nam Bộ',
    price: '1.279.516',
    unit: 'VNĐ/tấn',
    minMax: '1.260.323 - 1.298.708',
    volume: '35.000 tấn',
    changePct: 0.5,
    source: 'VSSA Hiệp hội Mía đường',
    updatedAt: 'Hôm nay',
  },
];

export const RegionalPriceTable: React.FC = () => {
  const [data, setData] = useState<RegionalPriceItem[]>(FALLBACK_REGIONAL_PRICES);
  const [selectedRegion, setSelectedRegion] = useState<string>('ALL');

  useEffect(() => {
    async function loadData() {
      try {
        const res = await fetchRegionalPrices();
        if (res && res.length > 0) {
          setData(res);
        }
      } catch (err) {
        console.error('Error fetching regional prices:', err);
      }
    }
    loadData();
  }, []);

  const regions = Array.from(
    new Set(data.map((item) => item.region.split('(')[0].trim()))
  ).filter(Boolean);

  const filteredData = data.filter((item) => {
    if (selectedRegion === 'ALL') return true;
    return item.region.toLowerCase().includes(selectedRegion.toLowerCase());
  });

  return (
    <div className="bg-card rounded-2xl border border-border-subtle p-5 sm:p-6 shadow-card flex flex-col justify-between h-full space-y-4">
      {/* Header & Filter */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-border-subtle">
        <div>
          <h2 className="text-base font-bold text-primary-text tracking-tight flex items-center gap-2">
            <Building2 className="w-5 h-5 text-brand" />
            <span>Giá Niêm Yết Vùng Trọng Điểm</span>
          </h2>
          <p className="text-xs text-secondary-text mt-0.5 font-medium">
            Khảo sát giao dịch thực tế tại kho thu mua lớn
          </p>
        </div>

        {/* Region Filter */}
        <div className="flex items-center gap-1.5 text-xs">
          <Filter className="w-3.5 h-3.5 text-secondary-text" />
          <select
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
            className="bg-canvas border border-border-subtle text-primary-text px-2.5 py-1 rounded-lg text-xs font-semibold focus:outline-none cursor-pointer"
          >
            <option value="ALL">Tất cả vùng ({data.length})</option>
            {regions.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Items List */}
      <div className="space-y-2.5 overflow-y-auto max-h-[300px] custom-scrollbar pr-1">
        {filteredData.map((item) => {
          const isPos = item.changePct >= 0;
          return (
            <div
              key={item.id}
              className="p-3.5 rounded-xl bg-canvas border border-border-subtle hover:border-brand/30 hover:bg-white transition-all shadow-2xs group flex items-center justify-between gap-3"
            >
              <div className="space-y-1 min-w-0 flex-1">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-xs text-primary-text truncate">
                    {item.commodityName}
                  </span>
                  <span className="text-[10px] font-bold px-1.5 py-0.2 rounded bg-border-subtle/80 text-secondary-text uppercase">
                    {item.code}
                  </span>
                </div>
                <div className="flex items-center gap-1 text-[11px] text-secondary-text font-medium truncate">
                  <MapPin className="w-3 h-3 text-brand shrink-0" />
                  <span className="truncate">{item.region}</span>
                </div>
              </div>

              <div className="text-right shrink-0 space-y-1">
                <div className="text-sm font-extrabold text-primary-text font-mono">
                  {item.price}{' '}
                  <span className="text-[10px] font-semibold text-secondary-text">{item.unit}</span>
                </div>
                <div className="flex items-center justify-end gap-1.5">
                  <span
                    className={`inline-flex items-center gap-0.5 text-[10px] font-extrabold px-1.5 py-0.2 rounded-md ${
                      isPos ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'
                    }`}
                  >
                    {isPos ? <TrendingUp className="w-2.5 h-2.5" /> : <TrendingDown className="w-2.5 h-2.5" />}
                    {isPos ? '+' : ''}
                    {item.changePct}%
                  </span>
                  <Link
                    href={`/commodities/${item.id}`}
                    className="text-[11px] font-bold text-brand hover:underline flex items-center gap-0.5 ml-1"
                    title="Xem biểu đồ dự báo AI"
                  >
                    <span>Xem AI</span>
                    <ArrowRight className="w-3 h-3 group-hover:translate-x-0.5 transition-transform" />
                  </Link>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default RegionalPriceTable;
