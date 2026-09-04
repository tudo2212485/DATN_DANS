'use client';

import React, { useState, useEffect } from 'react';
import Header from '@/components/layout/Header';
import CommodityCard from '@/components/dashboard/CommodityCard';
import MarketComparisonChart from '@/components/dashboard/MarketComparisonChart';
import CommoditySpotlight from '@/components/dashboard/CommoditySpotlight';
import RegionalPriceTable from '@/components/dashboard/RegionalPriceTable';
import { CommoditySummary, ComparisonDataPoint, SpotlightSummary } from '@/types';
import {
  fetchCommoditiesOverview,
  fetchMarketComparison,
  fetchCommoditySpotlight,
} from '@/lib/api';
import { COMMODITIES_DATA, COMPARISON_SERIES, SPOTLIGHT_SUGAR } from '@/lib/mockData';

export default function OverviewPage() {
  const [commodities, setCommodities] = useState<CommoditySummary[]>(COMMODITIES_DATA);
  const [comparison, setComparison] = useState<ComparisonDataPoint[]>(COMPARISON_SERIES);
  const [spotlight, setSpotlight] = useState<SpotlightSummary>(SPOTLIGHT_SUGAR);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [cData, cmpData, spotData] = await Promise.all([
          fetchCommoditiesOverview(),
          fetchMarketComparison(),
          fetchCommoditySpotlight('SUGAR'),
        ]);
        if (cData && cData.length > 0) setCommodities(cData);
        if (cmpData && cmpData.length > 0) setComparison(cmpData);
        if (spotData) setSpotlight(spotData);
      } catch (err) {
        console.error('Failed to load overview data:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <Header
        title="Tổng quan thị trường"
        subtitle={
          isLoading
            ? 'Đang đồng bộ dữ liệu từ PostgreSQL...'
            : `Dữ liệu giao dịch thực tế đồng bộ từ CSDL PostgreSQL & giacaphe.com`
        }
        showLiveBadge={true}
      />

      {/* 4 Commodity Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {commodities.map((commodity) => (
          <CommodityCard key={commodity.id} commodity={commodity} />
        ))}
      </div>

      {/* Main Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Left: Market Comparison Chart (~65%) */}
        <div className="lg:col-span-8">
          <MarketComparisonChart data={comparison} />
        </div>

        {/* Right: Commodity Spotlight Detail (~35%) */}
        <div className="lg:col-span-4">
          <CommoditySpotlight spotlight={spotlight} />
        </div>
      </div>

      {/* Regional Price Table (Bảng cập nhật giá theo vùng) */}
      <div className="pt-2">
        <RegionalPriceTable />
      </div>
    </div>
  );
}
