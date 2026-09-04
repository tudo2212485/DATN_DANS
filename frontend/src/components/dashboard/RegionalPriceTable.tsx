'use client';

import React, { useState, useEffect } from 'react';
import { MapPin, TrendingUp, TrendingDown, Building2 } from 'lucide-react';
import { RegionalPriceItem } from '@/types';
import { fetchRegionalPrices } from '@/lib/api';

const FALLBACK_REGIONAL_PRICES: RegionalPriceItem[] = [
  {
    id: 1,
    commodityName: 'Lúa gạo IR50404',
    code: 'RICE',
    region: 'Đồng bằng Sông Cửu Long',
    price: '8.065',
    unit: 'VNĐ/kg',
    minMax: '7.944 - 8.186',
    volume: '28.500 tấn',
    changePct: 1.2,
    source: 'Hiệp hội Lương thực VN (VFA)',
    updatedAt: 'Hôm nay',
  },
  {
    id: 2,
    commodityName: 'Cà phê Robusta nhân xô',
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
    source: 'Hiệp hội Hồ tiêu VN (VPA)',
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
    source: 'Hiệp hội Mía đường VN (VSSA)',
    updatedAt: 'Hôm nay',
  },
];

export const RegionalPriceTable: React.FC = () => {
  const [data, setData] = useState<RegionalPriceItem[]>(FALLBACK_REGIONAL_PRICES);

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

  return (
    <div className="bg-card rounded-2xl border border-border-subtle p-6 shadow-card">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-base font-bold text-primary-text tracking-tight">
            Bảng cập nhật giá nông sản theo vùng trọng điểm (Đồng bộ PostgreSQL)
          </h2>
          <p className="text-xs text-secondary-text mt-0.5 font-medium">
            Giá giao dịch thực tế bình quân tại ruộng và kho thu mua lớn trên toàn quốc
          </p>
        </div>
        <div className="flex items-center gap-1 text-xs font-semibold text-secondary-text bg-canvas px-3 py-1.5 rounded-xl border border-border-subtle">
          <Building2 className="w-3.5 h-3.5 text-brand" />
          <span>4 Vùng trọng điểm</span>
        </div>
      </div>

      <div className="overflow-x-auto pb-2 custom-scrollbar">
        <table className="w-full text-left text-xs whitespace-nowrap">
          <thead>
            <tr className="border-b border-border-subtle text-secondary-text font-bold uppercase tracking-wider pb-2">
              <th className="py-3 px-3 sticky left-0 bg-card z-10 shadow-[2px_0_5px_-2px_rgba(0,0,0,0.05)]">Nông sản</th>
              <th className="py-3 px-3">Khu vực / Vùng trọng điểm</th>
              <th className="py-3 px-3">Giá bình quân</th>
              <th className="py-3 px-3">Biên độ ngày (Min - Max)</th>
              <th className="py-3 px-3">Khối lượng GD</th>
              <th className="py-3 px-3">Biến động</th>
              <th className="py-3 px-3">Nguồn thu thập</th>
              <th className="py-3 px-3 text-right">Cập nhật</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border-subtle">
            {data.map((item) => {
              const isPos = item.changePct >= 0;
              return (
                <tr key={item.id} className="hover:bg-canvas/50 transition-colors group">
                  <td className="py-3.5 px-3 sticky left-0 bg-card group-hover:bg-canvas/90 z-10 shadow-[2px_0_5px_-2px_rgba(0,0,0,0.05)] transition-colors">
                    <div className="font-bold text-primary-text">{item.commodityName}</div>
                    <span className="text-[10px] font-semibold text-secondary-text uppercase tracking-wider">
                      {item.code}
                    </span>
                  </td>
                  <td className="py-3.5 px-3">
                    <div className="flex items-center gap-1.5 text-primary-text font-medium">
                      <MapPin className="w-3.5 h-3.5 text-brand shrink-0" />
                      <span>{item.region}</span>
                    </div>
                  </td>
                  <td className="py-3.5 px-3 font-extrabold text-primary-text text-sm">
                    {item.price} <span className="text-xs font-semibold text-secondary-text">{item.unit}</span>
                  </td>
                  <td className="py-3.5 px-3 text-secondary-text font-medium">
                    {item.minMax} {item.unit}
                  </td>
                  <td className="py-3.5 px-3 text-primary-text font-bold">
                    {item.volume}
                  </td>
                  <td className="py-3.5 px-3">
                    <span
                      className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-bold ${
                        isPos
                          ? 'bg-brand-badge text-brand border border-brand/15'
                          : 'bg-accent-coralLight text-accent-coral border border-accent-coral/20'
                      }`}
                    >
                      {isPos ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                      {isPos ? `+${item.changePct}%` : `${item.changePct}%`}
                    </span>
                  </td>
                  <td className="py-3.5 px-3 text-secondary-text">
                    {item.source}
                  </td>
                  <td className="py-3.5 px-3 text-right text-secondary-text font-medium">
                    {item.updatedAt}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
export default RegionalPriceTable;

