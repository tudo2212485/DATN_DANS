'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  fetchAdminStats,
  fetchAdminCommodities,
  fetchRecentPricesApi,
} from '@/lib/api';
import {
  AdminStats,
  AdminPriceItem,
} from '@/types';
import {
  formatDateVN,
  formatNumberVN,
  getCommodityUnit,
} from '@/lib/formatters';
import {
  ArrowRight,
  RefreshCw,
} from 'lucide-react';

interface CommodityItem {
  id: number;
  code: string;
  name: string;
  category: string;
  unit: string;
  region: string;
}

export default function DashboardOverviewPage() {
  const [error, setError] = useState('');
  const [stats, setStats] = useState<AdminStats>({
    totalCommodities: 0,
    totalPriceRecords: 0,
    totalForecastRecords: 0,
    totalAlertRules: 0,
    latestPriceDate: null,
    systemStatus: 'ĐANG KIỂM TRA',
  });
  const [recentPrices, setRecentPrices] = useState<AdminPriceItem[]>([]);
  const [commodities, setCommodities] = useState<CommodityItem[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    setLoading(true);
    setError('');
    try {
      const [sData, pData, cData] = await Promise.all([
        fetchAdminStats(),
        fetchRecentPricesApi(undefined, undefined, undefined, 0, 10),
        fetchAdminCommodities(),
      ]);
      setStats(sData);
      setRecentPrices(pData.slice(0, 10));
      setCommodities(cData);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Không tải được dữ liệu hệ thống');
      setStats((prev) => ({ ...prev, systemStatus: 'KHÔNG KẾT NỐI' }));
      setRecentPrices([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadData();
  }, []);

  return (
    <div className="space-y-5 font-sans">
      {error && (
        <p role="alert" className="p-3.5 bg-red-50 text-[#DC2626] border border-red-200 rounded-lg text-xs font-medium">
          {error}
        </p>
      )}

      {/* Compact 1-Line Page Header */}
      <div className="flex items-center justify-between gap-3 pb-3 border-b border-[#E5E7EB]">
        <h1 className="text-lg sm:text-xl font-bold text-[#1E293B] tracking-tight">
          Tổng quan hệ thống
        </h1>

        <button
          type="button"
          onClick={() => void loadData()}
          disabled={loading}
          className="px-3 py-1.5 rounded-lg bg-white hover:bg-[#F8FAF9] text-[#334155] hover:text-[#1E293B] border border-[#E5E7EB] text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Làm mới</span>
        </button>
      </div>

      {/* Tier 1: 4 Compact KPI Cards */}
      <section
        aria-label="Chỉ số hệ thống"
        className="bg-white rounded-xl border border-[#E5E7EB] grid grid-cols-2 lg:grid-cols-4 divide-y sm:divide-y-0 sm:divide-x divide-[#E5E7EB]"
      >
        <div className="p-4">
          <p className="text-xs font-medium text-[#64748B]">Mặt hàng theo dõi</p>
          <div className="mt-1.5 flex items-baseline gap-1.5">
            <span className="text-2xl font-bold text-[#1E293B] tabular-nums">
              {stats.totalCommodities}
            </span>
            <span className="text-xs text-[#64748B]">mặt hàng</span>
          </div>
        </div>

        <div className="p-4">
          <p className="text-xs font-medium text-[#64748B]">Bản ghi giá</p>
          <div className="mt-1.5 flex items-baseline gap-1.5">
            <span className="text-2xl font-bold text-[#1E293B] tabular-nums">
              {formatNumberVN(stats.totalPriceRecords)}
            </span>
            <span className="text-xs text-[#64748B]">bản ghi</span>
          </div>
          <p className="mt-1 text-[11px] text-[#64748B] tabular-nums">
            Mới nhất: {formatDateVN(stats.latestPriceDate)}
          </p>
        </div>

        <div className="p-4">
          <p className="text-xs font-medium text-[#64748B]">Điểm dự báo</p>
          <div className="mt-1.5 flex items-baseline gap-1.5">
            <span className="text-2xl font-bold text-[#1E293B] tabular-nums">
              {formatNumberVN(stats.totalForecastRecords)}
            </span>
            <span className="text-xs text-[#64748B]">điểm</span>
          </div>
          <p className="mt-1 text-[11px] text-[#64748B]">5 mô hình dự báo</p>
        </div>

        <div className="p-4">
          <p className="text-xs font-medium text-[#64748B]">Trạng thái</p>
          <div className="mt-2 flex items-center gap-2">
            <span
              className={`w-2.5 h-2.5 rounded-full ${
                stats.systemStatus === 'ONLINE' ? 'bg-[#15803D]' : 'bg-amber-500'
              }`}
            />
            <span className="text-base font-bold text-[#15803D]">
              {stats.systemStatus === 'ONLINE' ? 'Hoạt động' : stats.systemStatus}
            </span>
          </div>
          <p className="mt-1 text-[11px] text-[#64748B] tabular-nums">
            {stats.totalAlertRules} quy tắc cảnh báo
          </p>
        </div>
      </section>

      {/* Tier 2: 2 Side-by-Side Tables */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
        {/* Left: Commodity Catalog & Units */}
        <section className="lg:col-span-7 bg-white rounded-xl border border-[#E5E7EB] overflow-hidden">
          <div className="px-4 py-3 bg-[#F8FAF9] border-b border-[#E5E7EB] flex items-center justify-between">
            <h2 className="text-[14px] font-bold text-[#1E293B]">
              Danh mục mặt hàng & Đơn vị chuẩn
            </h2>
            <span className="text-xs tabular-nums font-semibold text-[#64748B]">
              {commodities.length} mặt hàng
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead className="bg-[#F8FAF9] text-[#64748B] uppercase text-[11px] font-semibold tracking-wider border-b border-[#E5E7EB]">
                <tr>
                  <th className="py-2.5 px-3.5">Mã</th>
                  <th className="py-2.5 px-3.5">Tên mặt hàng</th>
                  <th className="py-2.5 px-3.5">Nhóm</th>
                  <th className="py-2.5 px-3.5">Vùng khảo sát</th>
                  <th className="py-2.5 px-3.5 text-right">Đơn vị chuẩn</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E5E7EB] text-[13px]">
                {commodities.map((c) => {
                  const unit = getCommodityUnit(c.name, c.unit);
                  return (
                    <tr key={c.id} className="hover:bg-[#F8FAF9] transition-colors">
                      <td className="py-2.5 px-3.5 tabular-nums font-semibold text-[#2F6F4E]">
                        {c.code}
                      </td>
                      <td className="py-2.5 px-3.5 font-semibold text-[#1E293B]">{c.name}</td>
                      <td className="py-2.5 px-3.5 text-[#475569]">{c.category}</td>
                      <td className="py-2.5 px-3.5 text-[#475569]">{c.region}</td>
                      <td className="py-2.5 px-3.5 text-right tabular-nums font-semibold text-[#1E293B]">
                        {unit}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>

        {/* Right: Recent Prices */}
        <section className="lg:col-span-5 bg-white rounded-xl border border-[#E5E7EB] overflow-hidden">
          <div className="px-4 py-3 bg-[#F8FAF9] border-b border-[#E5E7EB] flex items-center justify-between">
            <h2 className="text-[14px] font-bold text-[#1E293B]">
              Giá cập nhật gần nhất
            </h2>
            <Link
              href="/dashboard/data-control"
              className="text-xs font-semibold text-[#2F6F4E] hover:underline inline-flex items-center gap-1 whitespace-nowrap shrink-0"
            >
              <span>Toàn bộ</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead className="bg-[#F8FAF9] text-[#64748B] uppercase text-[11px] font-semibold tracking-wider border-b border-[#E5E7EB]">
                <tr>
                  <th className="py-2.5 px-3.5">Mặt hàng</th>
                  <th className="py-2.5 px-3.5">Ngày</th>
                  <th className="py-2.5 px-3.5 text-right">Mức giá</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E5E7EB] text-[13px]">
                {recentPrices.map((p) => {
                  const unit = getCommodityUnit(p.commodityName);
                  return (
                    <tr key={p.id} className="hover:bg-[#F8FAF9] transition-colors">
                      <td className="py-2.5 px-3.5">
                        <div className="font-semibold text-[#1E293B]">{p.commodityName}</div>
                        <div className="text-[11px] text-[#64748B] truncate max-w-[165px]">
                          {p.source || 'Sở NN&PTNT'}
                        </div>
                      </td>
                      <td className="py-2.5 px-3.5 tabular-nums text-[#475569]">
                        {formatDateVN(p.recordDate)}
                      </td>
                      <td className="py-2.5 px-3.5 text-right tabular-nums font-bold text-[#1E293B] whitespace-nowrap">
                        {formatNumberVN(p.price)}{' '}
                        <span className="text-[11px] font-normal text-[#64748B]">{unit}</span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
}
