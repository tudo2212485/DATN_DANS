'use client';

import React from 'react';
import { MapPin, TrendingUp, TrendingDown, Building2 } from 'lucide-react';

interface RegionalPriceItem {
  id: number;
  commodityName: string;
  code: string;
  region: string;
  price: string;
  unit: string;
  minMax: string;
  volume: string;
  changePct: number;
  source: string;
  updatedAt: string;
}

const REGIONAL_PRICES: RegionalPriceItem[] = [
  {
    id: 1,
    commodityName: 'Lúa gạo IR50404',
    code: 'RICE',
    region: 'An Giang & Tiền Giang (ĐBSCL)',
    price: '8.450',
    unit: 'đ/kg',
    minMax: '8.300 - 8.650',
    volume: '1.450 tấn',
    changePct: 2.4,
    source: 'Sở NN&PTNT An Giang',
    updatedAt: 'Hôm nay 14:15',
  },
  {
    id: 2,
    commodityName: 'Cà phê Robusta nhân xô',
    code: 'COFFEE',
    region: 'Đắk Lắk & Lâm Đồng (Tây Nguyên)',
    price: '62.300',
    unit: 'đ/kg',
    minMax: '61.500 - 63.200',
    volume: '580 tấn',
    changePct: -1.1,
    source: 'Hiệp hội VICOFA',
    updatedAt: 'Hôm nay 14:20',
  },
  {
    id: 3,
    commodityName: 'Hồ tiêu đen xô',
    code: 'PEPPER',
    region: 'Chư Sê (Gia Lai) & Đắk Song (Đắk Nông)',
    price: '145.000',
    unit: 'đ/kg',
    minMax: '143.800 - 146.500',
    volume: '390 tấn',
    changePct: 0.7,
    source: 'Hiệp hội Hồ tiêu Chư Sê',
    updatedAt: 'Hôm nay 13:50',
  },
  {
    id: 4,
    commodityName: 'Mía đường nguyên liệu 10 CCS',
    code: 'SUGAR',
    region: 'Phú Yên & Hậu Giang (Miền Trung & Tây Nam Bộ)',
    price: '1.200',
    unit: 'đ/kg',
    minMax: '1.185 - 1.205',
    volume: '2.800 tấn',
    changePct: 3.8,
    source: 'Hiệp hội VSSA',
    updatedAt: 'Hôm nay 11:30',
  },
];

export const RegionalPriceTable: React.FC = () => {
  return (
    <div className="bg-card rounded-2xl border border-border-subtle p-6 shadow-card">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-base font-bold text-primary-text tracking-tight">
            Bảng cập nhật giá nông sản theo vùng trọng điểm
          </h2>
          <p className="text-xs text-secondary-text mt-0.5 font-medium">
            Giá giao dịch bình quân tại ruộng và kho thu mua lớn trên toàn quốc
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
            {REGIONAL_PRICES.map((item) => {
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
