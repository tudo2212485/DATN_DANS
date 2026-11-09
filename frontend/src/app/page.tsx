'use client';

import React, { useState, useEffect, useMemo } from 'react';
import Header from '@/components/layout/Header';
import CommodityCard from '@/components/dashboard/CommodityCard';
import MarketComparisonChart from '@/components/dashboard/MarketComparisonChart';
import RegionalPriceTable from '@/components/dashboard/RegionalPriceTable';
import QuickSearchBar from '@/components/dashboard/QuickSearchBar';
import { CommoditySummary, ComparisonDataPoint } from '@/types';
import {
  fetchCommoditiesOverview,
  fetchMarketComparison,
} from '@/lib/api';
import { COMMODITIES_DATA, COMPARISON_SERIES } from '@/lib/mockData';
import Link from 'next/link';
import { ArrowRight } from 'lucide-react';

export default function OverviewPage() {
  const [commodities, setCommodities] = useState<CommoditySummary[]>(COMMODITIES_DATA);
  const [comparison, setComparison] = useState<ComparisonDataPoint[]>(COMPARISON_SERIES);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const [searchTerm, setSearchTerm] = useState<string>('');
  const [selectedRegion, setSelectedRegion] = useState<string>('ALL');
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');

  useEffect(() => {
    async function loadData() {
      try {
        const [cData, cmpData] = await Promise.all([
          fetchCommoditiesOverview(),
          fetchMarketComparison(),
        ]);
        if (cData && cData.length > 0) setCommodities(cData);
        if (cmpData && cmpData.length > 0) setComparison(cmpData);
      } catch (err) {
        console.error('Failed to load overview data:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, []);

  const uniqueRegions = useMemo(() => {
    return Array.from(new Set(commodities.map((c) => c.region.split('(')[0].trim()))).filter(Boolean);
  }, [commodities]);

  const uniqueCategories = useMemo(() => {
    return Array.from(new Set(commodities.map((c) => c.category))).filter(Boolean);
  }, [commodities]);

  const filteredCommodities = useMemo(() => {
    return commodities.filter((item) => {
      const matchSearch =
        searchTerm === '' ||
        item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.region.toLowerCase().includes(searchTerm.toLowerCase());

      const matchRegion =
        selectedRegion === 'ALL' || item.region.toLowerCase().includes(selectedRegion.toLowerCase());

      const matchCategory =
        selectedCategory === 'ALL' || item.category.toLowerCase() === selectedCategory.toLowerCase();

      return matchSearch && matchRegion && matchCategory;
    });
  }, [commodities, searchTerm, selectedRegion, selectedCategory]);

  const marketStats = useMemo(() => {
    const rising = commodities.filter((item) => item.changePct > 0).length;
    const falling = commodities.filter((item) => item.changePct < 0).length;
    const unchanged = commodities.filter((item) => item.changePct === 0).length;
    const sorted = [...commodities].sort((a, b) => b.changePct - a.changePct);
    const topGainer = sorted[0];
    const topLoser = sorted[sorted.length - 1];
    const avgChange = commodities.length
      ? Number((commodities.reduce((acc, c) => acc + c.changePct, 0) / commodities.length).toFixed(2))
      : 0;
    return { rising, falling, unchanged, topGainer, topLoser, avgChange };
  }, [commodities]);

  return (
    <div className="space-y-5 max-w-[1440px] mx-auto pb-12 font-sans">
      <Header
        title="Tổng quan thị trường nông sản"
        subtitle={
          isLoading
            ? 'Đang đồng bộ dữ liệu giao dịch...'
            : 'Tổng hợp giá thu mua nội địa từ Sở NN&PTNT các tỉnh và Hiệp hội ngành hàng (VPSA, VINACAS, Vinanet)'
        }
        showLiveBadge={true}
      />

      {/* Unified Market Summary Strip */}
      <section
        aria-label="Tóm tắt thị trường"
        className="bg-white rounded-xl border border-zinc-200/90 shadow-[0_1px_2px_rgba(0,0,0,0.02)] grid grid-cols-2 lg:grid-cols-4 divide-y sm:divide-y-0 sm:divide-x divide-zinc-200/70"
      >
        <div className="p-4 sm:p-5">
          <p className="text-[12.5px] font-medium text-zinc-500">Danh mục theo dõi</p>
          <div className="mt-1.5 flex items-baseline gap-1.5">
            <span className="text-2xl font-bold text-zinc-900 font-mono">{commodities.length}</span>
            <span className="text-[12.5px] text-zinc-500">nông sản chủ lực</span>
          </div>
          <p className="mt-1 text-[12px] text-zinc-500 truncate">
            Tây Nguyên, ĐBSCL & Đông Nam Bộ
          </p>
        </div>

        <div className="p-4 sm:p-5">
          <p className="text-[12.5px] font-medium text-zinc-500">Độ rộng thị trường</p>
          <div className="mt-1.5 flex items-baseline gap-3 font-mono">
            <span className="text-[15px] font-semibold text-emerald-700">
              {marketStats.rising} tăng
            </span>
            <span className="text-zinc-300">·</span>
            <span className="text-[15px] font-semibold text-rose-600">
              {marketStats.falling} giảm
            </span>
            {marketStats.unchanged > 0 && (
              <>
                <span className="text-zinc-300">·</span>
                <span className="text-[15px] font-semibold text-zinc-600">
                  {marketStats.unchanged} đi ngang
                </span>
              </>
            )}
          </div>
          <p className="mt-1 text-[12px] text-zinc-500">
            Biến động bình quân:{' '}
            <span className="font-mono font-medium text-zinc-800">
              {marketStats.avgChange >= 0 ? `+${marketStats.avgChange}%` : `${marketStats.avgChange}%`}
            </span>
          </p>
        </div>

        <div className="p-4 sm:p-5">
          <p className="text-[12.5px] font-medium text-zinc-500">Tăng trưởng mạnh nhất</p>
          <div className="mt-1.5 flex items-baseline justify-between gap-2">
            <span className="text-[15px] font-semibold text-zinc-900 truncate">
              {marketStats.topGainer?.name || '—'}
            </span>
            <span className="text-[13px] font-semibold font-mono text-emerald-700 shrink-0">
              {marketStats.topGainer ? `+${marketStats.topGainer.changePct}%` : '—'}
            </span>
          </div>
          <p className="mt-1 text-[12px] text-zinc-500 font-mono truncate">
            {marketStats.topGainer?.formattedPrice} {marketStats.topGainer?.unit}
          </p>
        </div>

        <div className="p-4 sm:p-5 flex flex-col justify-between">
          <div>
            <p className="text-[12.5px] font-medium text-zinc-500">Phân tích & Dự báo</p>
            <p className="mt-1 text-[12.5px] text-zinc-600">
              Tra cứu dự báo ngắn hạn 7–30 ngày theo từng vùng thu mua
            </p>
          </div>
          <div className="mt-2 flex items-center gap-4 text-[12.5px] font-semibold">
            <Link
              href="/forecast"
              className="inline-flex items-center gap-1 text-emerald-700 hover:text-emerald-800"
            >
              <span>Mở trang dự báo</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
            <Link href="/history" className="text-zinc-600 hover:text-zinc-900">
              Dữ liệu lịch sử
            </Link>
          </div>
        </div>
      </section>

      {/* Search & Filters */}
      <QuickSearchBar
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        selectedRegion={selectedRegion}
        onRegionChange={setSelectedRegion}
        selectedCategory={selectedCategory}
        onCategoryChange={setSelectedCategory}
        regions={uniqueRegions}
        categories={uniqueCategories}
      />

      {/* Commodity Price Grid */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-[15.5px] font-semibold text-zinc-900">
            Bảng giá niêm yết ({filteredCommodities.length} mặt hàng)
          </h2>
          <span className="text-[12px] text-zinc-500">
            Nhấp vào mặt hàng để xem chi tiết
          </span>
        </div>

        {filteredCommodities.length === 0 ? (
          <div className="p-10 rounded-xl bg-white border border-zinc-200/90 text-center text-zinc-500 text-[13.5px]">
            Không tìm thấy mặt hàng phù hợp với bộ lọc hiện tại.
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {filteredCommodities.map((commodity) => (
              <Link
                key={commodity.id}
                href={`/forecast?commodity_id=${commodity.id}`}
                className="block focus:outline-none"
              >
                <CommodityCard commodity={commodity} />
              </Link>
            ))}
          </div>
        )}
      </div>

      {/* Bottom Row: Market Comparison & Regional Price Table */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-stretch pt-1">
        <div className="lg:col-span-7">
          <MarketComparisonChart data={comparison} />
        </div>
        <div className="lg:col-span-5">
          <RegionalPriceTable />
        </div>
      </div>
    </div>
  );
}
