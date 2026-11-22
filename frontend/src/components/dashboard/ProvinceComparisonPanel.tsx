'use client';

import React, { useEffect, useState } from 'react';
import { CommodityProvinceComparison } from '@/types';
import { fetchCommodityProvinceComparisonApi } from '@/lib/api';
import { formatDateVN, formatNumberVN } from '@/lib/formatters';
import { MapPin, ExternalLink } from 'lucide-react';

const COMMODITY_TABS = [
  { code: 'COFFEE_ROBUSTA', label: 'Cà phê Robusta' },
  { code: 'PEPPER_BLACK', label: 'Hồ tiêu đen' },
  { code: 'RICE_IR504', label: 'Lúa gạo IR50404' },
  { code: 'SUGARCANE', label: 'Mía đường' },
  { code: 'STRAWBERRY', label: 'Dâu tây Đà Lạt' },
  { code: 'POTATO', label: 'Khoai tây Đà Lạt' },
  { code: 'SWEET_POTATO', label: 'Khoai lang tím' },
  { code: 'CASHEW_NUT', label: 'Hạt điều' },
];

interface ProvinceComparisonPanelProps {
  activeProvinceCode: string;
  onSelectProvince?: (code: string) => void;
}

export default function ProvinceComparisonPanel({
  activeProvinceCode,
  onSelectProvince,
}: ProvinceComparisonPanelProps) {
  const [selectedCode, setSelectedCode] = useState<string>('COFFEE_ROBUSTA');
  const [data, setData] = useState<CommodityProvinceComparison | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    let active = true;
    setLoading(true);
    fetchCommodityProvinceComparisonApi(selectedCode, activeProvinceCode)
      .then((res) => {
        if (active) setData(res);
      })
      .catch(() => {
        if (active) setData(null);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [selectedCode, activeProvinceCode]);

  return (
    <section className="bg-white rounded-xl border border-[#E5E7EB] shadow-card overflow-hidden font-sans">
      <div className="px-4 py-3 bg-[#F8FAF9] border-b border-[#E5E7EB] flex flex-wrap items-center justify-between gap-2.5">
        <div className="flex items-center gap-2">
          <MapPin className="w-4 h-4 text-[#2F6F4E] shrink-0" />
          <div>
            <h3 className="text-[14px] font-bold text-[#1E293B]">
              Chênh lệch giá theo tỉnh hôm nay
            </h3>
            {data && (
              <p className="text-[11.5px] text-[#64748B] tabular-nums">
                Giá chuẩn vùng trọng điểm:{' '}
                <strong className="text-[#1E293B]">
                  {data.formatted_national_price} {data.commodity.unit}
                </strong>
                {data.latest_date ? ` · Cập nhật ${formatDateVN(data.latest_date)}` : ''}
              </p>
            )}
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-1 bg-white p-0.5 rounded-lg border border-[#E5E7EB]">
          {COMMODITY_TABS.map((tab) => (
            <button
              key={tab.code}
              type="button"
              onClick={() => setSelectedCode(tab.code)}
              className={`px-2.5 py-1 rounded-md text-xs font-semibold transition-colors cursor-pointer ${
                selectedCode === tab.code
                  ? 'bg-[#2F6F4E] text-white'
                  : 'text-[#334155] hover:text-[#1E293B]'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      <div className="overflow-x-auto">
        {loading ? (
          <div className="py-8 text-center text-xs text-[#64748B]">
            Đang tải bảng giá các tỉnh/thành phố...
          </div>
        ) : !data || data.provinces.length === 0 ? (
          <div className="py-8 text-center text-xs text-[#64748B]">
            Chưa có dữ liệu so sánh theo tỉnh cho mặt hàng này.
          </div>
        ) : (
          <table className="w-full text-left text-xs border-collapse">
            <thead className="bg-[#F8FAF9] text-[#64748B] uppercase text-[11px] font-semibold border-b border-[#E5E7EB]">
              <tr>
                <th className="py-2.5 px-3.5">Tỉnh / Thành phố</th>
                <th className="py-2.5 px-3.5">Vùng</th>
                <th className="py-2.5 px-3.5 text-right">Giá niêm yết</th>
                <th className="py-2.5 px-3.5 text-right">Chênh lệch chuẩn</th>
                <th className="py-2.5 px-3.5">Phân loại nguồn giá</th>
                <th className="py-2.5 px-3.5">Nguồn / Ngày</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E5E7EB] text-[12.5px]">
              {data.provinces.map((row) => {
                const isDirect = row.pricing_mode === 'direct';
                const isFocused = row.province_code === activeProvinceCode;
                const diffSign = row.diff_vs_national > 0 ? '+' : '';
                return (
                  <tr
                    key={row.province_code}
                    className={`transition-colors ${
                      isFocused ? 'bg-[#F0F7F4]/70' : 'hover:bg-[#F8FAF9]'
                    }`}
                  >
                    <td className="py-2.5 px-3.5 font-semibold text-[#1E293B]">
                      {onSelectProvince ? (
                        <button
                          type="button"
                          onClick={() => onSelectProvince(row.province_code)}
                          className="hover:text-[#2F6F4E] hover:underline cursor-pointer text-left"
                        >
                          {row.province_name}
                        </button>
                      ) : (
                        row.province_name
                      )}
                      {isFocused && (
                        <span className="ml-1.5 text-[10px] font-semibold px-1.5 py-0.5 rounded bg-[#2F6F4E] text-white">
                          Đang chọn
                        </span>
                      )}
                    </td>
                    <td className="py-2.5 px-3.5 text-[#64748B]">{row.region_name}</td>
                    <td className="py-2.5 px-3.5 text-right tabular-nums font-bold text-[#1E293B]">
                      {row.formatted_price}{' '}
                      <span className="text-[11px] font-normal text-[#64748B]">{row.unit}</span>
                    </td>
                    <td
                      className={`py-2.5 px-3.5 text-right tabular-nums font-semibold ${
                        row.diff_vs_national > 0
                          ? 'text-[#15803D]'
                          : row.diff_vs_national < 0
                            ? 'text-[#DC2626]'
                            : 'text-[#64748B]'
                      }`}
                    >
                      {row.diff_vs_national === 0
                        ? '0'
                        : `${diffSign}${formatNumberVN(Math.round(row.diff_vs_national))}`}
                    </td>
                    <td className="py-2.5 px-3.5">
                      {isDirect ? (
                        <span className="inline-flex items-center px-2 py-0.5 rounded-md bg-[#F0F7F4] text-[#15803D] border border-[#15803D]/20 text-[11px] font-semibold">
                          Khảo sát trực tiếp
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 border border-slate-200 text-[11px] font-medium">
                          Tham chiếu {row.reference_province} (~{Math.round(row.distance_km)} km)
                        </span>
                      )}
                    </td>
                    <td className="py-2.5 px-3.5 text-[11.5px] text-[#64748B]">
                      <div className="flex items-center gap-1.5">
                        <span className="truncate max-w-[240px]" title={row.source}>
                          {row.source}
                          {row.recorded_date ? ` (${formatDateVN(row.recorded_date)})` : ''}
                        </span>
                        {row.source_url && /^https?:\/\//i.test(row.source_url) && (
                          <a
                            href={row.source_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            aria-label={`Mở nguồn ${row.source}`}
                            className="text-[#2F6F4E] hover:text-[#15803D] shrink-0"
                          >
                            <ExternalLink className="w-3 h-3" />
                          </a>
                        )}
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </section>
  );
}

