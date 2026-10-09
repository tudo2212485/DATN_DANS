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
import { ArrowRight, BarChart3, Database, History, TrendingDown, TrendingUp } from 'lucide-react';

export default function OverviewPage() {
  const [commodities, setCommodities] = useState<CommoditySummary[]>(COMMODITIES_DATA);
  const [comparison, setComparison] = useState<ComparisonDataPoint[]>(COMPARISON_SERIES);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Search & Filter state
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

  // Filtered lists for QuickSearchBar
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
    const strongest = [...commodities].sort((a, b) => Math.abs(b.changePct) - Math.abs(a.changePct))[0];
    return { rising, falling, strongest };
  }, [commodities]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <Header
        title="Tổng quan thị trường nông sản"
        subtitle={
          isLoading
            ? 'Đang đồng bộ dữ liệu giao dịch từ CSDL PostgreSQL...'
            : 'Dữ liệu giao dịch thực tế đồng bộ từ CSDL PostgreSQL & Sở NN&PTNT các tỉnh'
        }
        showLiveBadge={true}
      />

      <section className="grid grid-cols-2 xl:grid-cols-4 gap-3" aria-label="Tóm tắt thị trường">
        <div className="rounded-2xl border border-border-subtle bg-white p-4 shadow-card">
          <div className="flex items-center justify-between"><p className="text-xs font-bold uppercase tracking-wider text-secondary-text">Đang theo dõi</p><Database className="w-4 h-4 text-brand" /></div>
          <p className="mt-2 text-2xl font-extrabold text-primary-text">{commodities.length} <span className="text-xs font-semibold text-secondary-text">nông sản</span></p>
        </div>
        <div className="rounded-2xl border border-emerald-200 bg-emerald-50/60 p-4 shadow-card">
          <div className="flex items-center justify-between"><p className="text-xs font-bold uppercase tracking-wider text-emerald-800">Đang tăng</p><TrendingUp className="w-4 h-4 text-emerald-700" /></div>
          <p className="mt-2 text-2xl font-extrabold text-emerald-800">{marketStats.rising} <span className="text-xs font-semibold">mặt hàng</span></p>
        </div>
        <div className="rounded-2xl border border-rose-200 bg-rose-50/60 p-4 shadow-card">
          <div className="flex items-center justify-between"><p className="text-xs font-bold uppercase tracking-wider text-rose-800">Đang giảm</p><TrendingDown className="w-4 h-4 text-rose-700" /></div>
          <p className="mt-2 text-2xl font-extrabold text-rose-800">{marketStats.falling} <span className="text-xs font-semibold">mặt hàng</span></p>
        </div>
        <div className="rounded-2xl border border-border-subtle bg-brand/10 p-4 shadow-card">
          <div className="flex items-center justify-between"><p className="text-xs font-bold uppercase tracking-wider text-brand">Biến động mạnh nhất</p><BarChart3 className="w-4 h-4 text-brand" /></div>
          <p className="mt-2 text-base font-extrabold text-primary-text truncate">{marketStats.strongest?.name || '—'}</p>
          <p className="text-xs font-bold text-brand">{marketStats.strongest ? `${marketStats.strongest.changePct > 0 ? '+' : ''}${marketStats.strongest.changePct}%` : '—'}</p>
        </div>
      </section>

      <div className="flex flex-wrap items-center gap-2 rounded-2xl border border-border-subtle bg-white px-4 py-3 shadow-card">
        <span className="text-xs font-bold text-secondary-text mr-auto">Truy cập nhanh</span>
        <Link href="/history" className="inline-flex items-center gap-2 rounded-xl border border-border-subtle px-3 py-2 text-xs font-bold text-primary-text hover:border-brand/30 hover:bg-brand/5 transition-colors"><History className="w-4 h-4 text-brand" />Xem lịch sử giá</Link>
        <Link href="/forecast" className="inline-flex items-center gap-2 rounded-xl bg-brand px-3 py-2 text-xs font-bold text-white hover:bg-brand/90 transition-colors">Mở dự báo AI<ArrowRight className="w-4 h-4" /></Link>
      </div>

      {/* Quick Search & Category/Region Filter Bar */}
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

      {/* Grid 4 Card Giá Nông Sản Chính (Lúa gạo IR504, Cà phê Robusta, Hồ tiêu đen, Mía đường) */}
      <div className="space-y-2.5">
        <div className="flex items-center justify-between px-1">
          <h2 className="text-sm font-bold text-primary-text">
            Giá nông sản mới nhất ({filteredCommodities.length})
          </h2>
          <span className="text-[11px] text-secondary-text font-medium">
            Chọn một thẻ để xem lịch sử và dự báo chi tiết
          </span>
        </div>

        {filteredCommodities.length === 0 ? (
          <div className="p-8 rounded-2xl bg-white border border-border-subtle text-center text-secondary-text text-xs space-y-2">
            <p className="font-semibold text-primary-text">Không tìm thấy nông sản phù hợp với bộ lọc</p>
            <p>Vui lòng thử tìm kiếm với từ khóa khác hoặc xóa bộ lọc vùng miền.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {filteredCommodities.map((commodity) => (
              <Link
                key={commodity.id}
                href={`/commodities/${commodity.id}`}
                className="block group"
              >
                <CommodityCard commodity={commodity} />
              </Link>
            ))}
          </div>
        )}
      </div>

      {/* Main Row: Left (60%) Comparison Chart + Right (40%) Regional Price Table */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-stretch">
        {/* Left Column (60%): Market Comparison Growth Chart */}
        <div className="lg:col-span-7">
          <MarketComparisonChart data={comparison} />
        </div>

        {/* Right Column (40%): Regional Price Table */}
        <div className="lg:col-span-5">
          <RegionalPriceTable />
        </div>
      </div>
    </div>
  );
}
