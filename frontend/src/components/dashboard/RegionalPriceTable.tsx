'use client';

import React, { useState, useEffect } from 'react';
import { ArrowRight } from 'lucide-react';
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
    price: '117.500',
    unit: 'VNĐ/kg',
    minMax: '116.700 - 117.700',
    volume: '12.400 tấn',
    changePct: 2.5,
    source: 'Vinanet & VICOFA',
    updatedAt: 'Hôm nay',
  },
  {
    id: 3,
    commodityName: 'Hồ tiêu đen',
    code: 'PEPPER',
    region: 'Tây Nguyên & Đông Nam Bộ',
    price: '143.360',
    unit: 'VNĐ/kg',
    minMax: '142.800 - 144.800',
    volume: '4.800 tấn',
    changePct: -0.8,
    source: 'VPSA Hiệp hội Hồ tiêu',
    updatedAt: 'Hôm nay',
  },
  {
    id: 4,
    commodityName: 'Mía đường 10 CCS',
    code: 'SUGAR',
    region: 'Miền Trung & Tây Nam Bộ',
    price: '1.246.588',
    unit: 'VNĐ/tấn',
    minMax: '1.236.000 - 1.250.000',
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
    <div className="bg-white rounded-xl border border-zinc-200/90 p-5 shadow-[0_1px_2px_rgba(0,0,0,0.02)] flex flex-col justify-between h-full font-sans">
      <div>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 pb-3.5 border-b border-zinc-100">
          <div>
            <h2 className="text-[15px] font-semibold text-zinc-900">
              Giá giao dịch theo vùng
            </h2>
            <p className="text-[12.5px] text-zinc-500 mt-0.5">
              Khảo sát tại kho thu mua và vùng chuyên canh
            </p>
          </div>

          <select
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
            className="bg-zinc-50 border border-zinc-200 text-zinc-800 px-2.5 py-1.5 rounded-lg text-[12.5px] font-medium focus:outline-none cursor-pointer w-fit"
          >
            <option value="ALL">Tất cả vùng ({data.length})</option>
            {regions.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>
        </div>

        <div className="divide-y divide-zinc-100 overflow-y-auto max-h-[380px] custom-scrollbar">
          {filteredData.map((item) => {
            const isPos = item.changePct >= 0;
            return (
              <div
                key={item.id}
                className="py-3.5 first:pt-4 last:pb-1 flex items-center justify-between gap-3 group"
              >
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-[14px] text-zinc-900 truncate">
                      {item.commodityName}
                    </span>
                  </div>
                  <p className="text-[12px] text-zinc-500 truncate mt-0.5">
                    {item.region}
                  </p>
                  <p className="text-[11px] text-zinc-400 truncate mt-0.5" title={item.source}>
                    Nguồn: {item.source}
                  </p>
                </div>

                <div className="text-right shrink-0">
                  <div className="text-[14.5px] font-bold text-zinc-900 font-mono">
                    {item.price}{' '}
                    <span className="text-[11.5px] font-normal text-zinc-500 font-sans">
                      {item.unit}
                    </span>
                  </div>
                  <div className="mt-1 flex items-center justify-end gap-2.5">
                    <span
                      className={`text-[11.5px] font-semibold font-mono ${
                        isPos ? 'text-emerald-700' : 'text-rose-600'
                      }`}
                    >
                      {isPos ? '+' : ''}
                      {item.changePct}%
                    </span>
                    <Link
                      href={`/forecast?commodity_id=${item.id}`}
                      className="text-[12px] font-medium text-zinc-500 hover:text-zinc-900 inline-flex items-center gap-0.5"
                    >
                      <span>Dự báo</span>
                      <ArrowRight className="w-3 h-3" />
                    </Link>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default RegionalPriceTable;
