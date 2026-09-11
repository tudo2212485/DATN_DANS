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
            4 Nông Sản Trọng Điểm ({filteredCommodities.length})
          </h2>
          <span className="text-[11px] text-secondary-text font-medium">
            Nhấp vào từng thẻ để xem biểu đồ dự báo AI và phân tích chuyên sâu
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
