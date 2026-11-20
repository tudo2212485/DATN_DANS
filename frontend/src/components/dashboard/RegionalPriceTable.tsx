'use client';

import React, { useState, useEffect } from 'react';
import { ArrowRight } from 'lucide-react';
import { RegionalPriceItem } from '@/types';
import { fetchRegionalPrices } from '@/lib/api';
import { formatPct, getCommodityUnit } from '@/lib/formatters';
import { useLocation } from '@/contexts/LocationContext';
import Link from 'next/link';

const FALLBACK_REGIONAL_PRICES: RegionalPriceItem[] = [
  {
    id: 1,
    commodityName: 'Lúa gạo IR50404',
    code: 'RICE',
    region: 'Huyện Châu Phú, An Giang (Tại ruộng)',
    price: '8.065',
    unit: 'VNĐ/kg',
    minMax: '7.944 - 8.186',
    volume: '28.500 tấn',
    changePct: 1.2,
    source: 'Khảo sát giá bán tại ruộng Châu Phú',
    updatedAt: 'Hôm nay',
  },
  {
    id: 2,
    commodityName: 'Cà phê Robusta',
    code: 'COFFEE',
    region: 'Huyện Cư M\'gar, Đắk Lắk (Tại vườn)',
    price: '117.500',
    unit: 'VNĐ/kg',
    minMax: '116.700 - 117.700',
    volume: '12.400 tấn',
    changePct: 2.5,
    source: 'Khảo sát giá bán tại vườn Cư M\'gar',
    updatedAt: 'Hôm nay',
  },
  {
    id: 3,
    commodityName: 'Hồ tiêu đen',
    code: 'PEPPER',
    region: 'Huyện Chư Sê, Gia Lai (Tại vườn)',
    price: '143.360',
    unit: 'VNĐ/kg',
    minMax: '142.800 - 144.800',
    volume: '4.800 tấn',
    changePct: -0.8,
    source: 'Khảo sát giá bán tại vườn Chư Sê',
    updatedAt: 'Hôm nay',
  },
  {
    id: 4,
    commodityName: 'Mía đường',
    code: 'SUGAR',
    region: 'Huyện Tây Hòa, Phú Yên (Tại ruộng)',
    price: '1.246.588',
    unit: 'VNĐ/tấn',
    minMax: '1.236.000 - 1.250.000',
    volume: '35.000 tấn',
    changePct: 0.5,
    source: 'Khảo sát giá bán tại ruộng Tây Hòa',
    updatedAt: 'Hôm nay',
  },
];

export const RegionalPriceTable: React.FC = () => {
  const { provinceCode } = useLocation();
  const [data, setData] = useState<RegionalPriceItem[]>(FALLBACK_REGIONAL_PRICES);
  const [selectedRegion, setSelectedRegion] = useState<string>('ALL');

  useEffect(() => {
    let active = true;
    async function loadData() {
      try {
        const res = await fetchRegionalPrices(provinceCode);
        if (active && res && res.length > 0) {
          setData(res);
          setSelectedRegion('ALL');
        }
      } catch (err) {
        console.error('Error fetching regional prices:', err);
      }
    }
    void loadData();
    return () => {
      active = false;
    };
  }, [provinceCode]);

  const regions = Array.from(
    new Set(data.map((item) => item.region.split('(')[0].trim()))
  ).filter(Boolean);

  const filteredData = data.filter((item) => {
    if (selectedRegion === 'ALL') return true;
    return item.region.toLowerCase().includes(selectedRegion.toLowerCase());
  });

  return (
    <div className="bg-white rounded-xl border border-[#E5E7EB] p-5 shadow-card flex flex-col justify-between h-full font-sans">
      <div>
        <div className="flex items-center justify-between gap-2.5 pb-3 border-b border-[#E5E7EB]">
          <h2 className="text-[15px] font-bold text-[#1E293B]">
            Giá nông sản hiện tại
          </h2>

          <select
            aria-label="Chọn địa phương"
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
            className="bg-[#F8FAF9] border border-[#E5E7EB] text-[#1E293B] px-2.5 py-1.5 rounded-lg text-xs font-medium focus:outline-none cursor-pointer w-fit"
          >
            <option value="ALL">Tất cả địa phương ({data.length})</option>
            {regions.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>
        </div>

        <div className="divide-y divide-[#E5E7EB] overflow-y-auto max-h-[380px] custom-scrollbar">
          {filteredData.map((item) => {
            const isPos = item.changePct >= 0;
            const unit = getCommodityUnit(item.commodityName, item.unit);
            const shortRegion = item.region.split('(')[0].trim();

            return (
              <div
                key={item.id}
                title={`Nguồn: ${item.source} · Biên độ: ${item.minMax} ${unit}`}
                className="py-3 first:pt-3.5 last:pb-1 space-y-1 group"
              >
                {/* Line 1: Commodity Name + Bold Price with clear unit */}
                <div className="flex items-baseline justify-between gap-3">
                  <span className="font-semibold text-[14px] text-[#1E293B] truncate">
                    {item.commodityName}
                  </span>
                  <div className="text-[14.5px] font-bold text-[#1E293B] tabular-nums shrink-0">
                    {item.price}{' '}
                    <span className="text-[11.5px] font-normal text-[#64748B]">
                      {unit}
                    </span>
                  </div>
                </div>

                {/* Line 2: Short Region + % Change + Forecast link */}
                <div className="flex items-center justify-between gap-2 text-xs">
                  <span className="text-[#64748B] truncate">{shortRegion}</span>
                  <div className="flex items-center gap-3 shrink-0">
                    <span
                      className={`font-semibold tabular-nums ${
                        isPos ? 'text-[#15803D]' : 'text-[#DC2626]'
                      }`}
                    >
                      {formatPct(item.changePct, 1)}
                    </span>
                    <Link
                      href={`/forecast?commodity_id=${item.id}`}
                      className="text-xs font-semibold text-[#2F6F4E] hover:underline inline-flex items-center gap-0.5"
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
