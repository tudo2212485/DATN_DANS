'use client';

import React, { useState, useEffect, useMemo } from 'react';
import Header from '@/components/layout/Header';
import CommodityCard from '@/components/dashboard/CommodityCard';
import MarketComparisonChart from '@/components/dashboard/MarketComparisonChart';
import RegionalPriceTable from '@/components/dashboard/RegionalPriceTable';
import ProvinceComparisonPanel from '@/components/dashboard/ProvinceComparisonPanel';
import QuickSearchBar from '@/components/dashboard/QuickSearchBar';
import { CommoditySummary, ComparisonDataPoint } from '@/types';
import {
  fetchCommoditiesOverview,
  fetchMarketComparison,
} from '@/lib/api';
import { COMMODITIES_DATA, COMPARISON_SERIES } from '@/lib/mockData';
import { useLocation } from '@/contexts/LocationContext';
import { MapPin, ChevronDown, ChevronUp } from 'lucide-react';
import Link from 'next/link';

export default function OverviewPage() {
  const { provinceCode, provinceName, setProvinceCode } = useLocation();
  const [commodities, setCommodities] = useState<CommoditySummary[]>(COMMODITIES_DATA);
  const [comparison, setComparison] = useState<ComparisonDataPoint[]>(COMPARISON_SERIES);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [showProvinceCompare, setShowProvinceCompare] = useState<boolean>(false);

  const [searchTerm, setSearchTerm] = useState<string>('');
  const [selectedRegion, setSelectedRegion] = useState<string>('ALL');
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');

  useEffect(() => {
    let active = true;
    async function loadData() {
      setIsLoading(true);
      try {
        const [cData, cmpData] = await Promise.all([
          fetchCommoditiesOverview(provinceCode),
          fetchMarketComparison(provinceCode),
        ]);
        if (active && cData && cData.length > 0) setCommodities(cData);
        if (active && cmpData && cmpData.length > 0) setComparison(cmpData);
      } catch (err) {
        console.error('Failed to load overview data:', err);
      } finally {
        if (active) setIsLoading(false);
      }
    }
    void loadData();
    return () => {
      active = false;
    };
  }, [provinceCode]);

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
    <div className="space-y-5 max-w-[1440px] mx-auto pb-12 font-sans">
      <Header
        title="Tổng quan giá nông sản"
        subtitle={isLoading ? 'Đang đồng bộ dữ liệu thị trường...' : undefined}
      />

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
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="flex flex-wrap items-center gap-2">
            <h2 className="text-[15px] font-bold text-[#1E293B]">
              Bảng giá niêm yết ({filteredCommodities.length} mặt hàng)
            </h2>
            {provinceCode !== 'all' && (
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-[#F0F7F4] text-[#2F6F4E] border border-[#2F6F4E]/20 text-xs font-semibold">
                <MapPin className="w-3 h-3" />
                {provinceName}
              </span>
            )}
          </div>

          <button
            type="button"
            onClick={() => setShowProvinceCompare((prev) => !prev)}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-[#E5E7EB] bg-white hover:bg-[#F8FAF9] text-xs font-semibold text-[#1E293B] transition-colors cursor-pointer"
          >
            <MapPin className="w-3.5 h-3.5 text-[#2F6F4E]" />
            <span>Chênh lệch giá theo tỉnh hôm nay</span>
            {showProvinceCompare ? (
              <ChevronUp className="w-3.5 h-3.5 text-[#64748B]" />
            ) : (
              <ChevronDown className="w-3.5 h-3.5 text-[#64748B]" />
            )}
          </button>
        </div>

        {showProvinceCompare && (
          <ProvinceComparisonPanel
            activeProvinceCode={provinceCode}
            onSelectProvince={setProvinceCode}
          />
        )}

        {filteredCommodities.length === 0 ? (
          <div className="p-10 rounded-xl bg-white border border-[#E5E7EB] text-center text-[#64748B] text-[13.5px]">
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
