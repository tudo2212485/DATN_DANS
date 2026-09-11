'use client';

import React from 'react';
import Link from 'next/link';
import { TrendingUp, TrendingDown, ArrowRight } from 'lucide-react';
import { CommoditySummary } from '@/types';

interface HotMoversBannerProps {
  commodities: CommoditySummary[];
}

export const HotMoversBanner: React.FC<HotMoversBannerProps> = ({ commodities }) => {
  // Sort by absolute changePct descending to pick top 3 hot movers
  const hotMovers = [...commodities]
    .sort((a, b) => Math.abs(b.changePct) - Math.abs(a.changePct))
    .slice(0, 3);

  if (hotMovers.length === 0) return null;

  return (
    <div className="p-4 sm:p-5 rounded-2xl bg-card border border-border-subtle shadow-xs space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-amber-500/10 text-amber-700 border border-amber-200">
            <TrendingUp className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-primary-text leading-tight flex items-center gap-1.5">
              Biến động nổi bật trong phiên
            </h3>
            <p className="text-[11px] text-secondary-text mt-0.5 font-medium">
              Các mặt hàng có biên độ dao động giá lớn nhất trong ngày giao dịch
            </p>
          </div>
        </div>

        <Link
          href="/compare"
          className="hidden sm:flex items-center gap-1 text-xs font-semibold text-brand hover:text-brand-hover transition"
        >
          <span>Chi tiết so sánh</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>

      {/* 3 Hot Movers Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {hotMovers.map((item) => {
          const isUp = item.changePct >= 0;
          return (
            <Link
              key={item.id}
              href={`/commodities/${item.id}`}
              className="p-3.5 rounded-xl bg-white border border-border-subtle hover:border-brand/40 hover:shadow-md transition-all group block"
            >
              <div className="flex items-start justify-between">
                <div>
                  <div className="text-xs font-bold text-primary-text group-hover:text-brand transition-colors">
                    {item.name}
                  </div>
                  <div className="text-[11px] text-secondary-text font-medium">{item.region}</div>
                </div>
                <span
                  className={`flex items-center gap-0.5 text-[11px] font-extrabold px-2 py-0.5 rounded-md ${
                    isUp ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'
                  }`}
                >
                  {isUp ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                  {isUp ? '+' : ''}
                  {item.changePct.toFixed(2)}%
                </span>
              </div>

              <div className="mt-2.5 flex items-baseline justify-between border-t border-border-subtle/60 pt-2">
                <span className="text-sm font-extrabold text-primary-text font-mono">
                  {item.formattedPrice}
                </span>
                <span className="text-[10px] text-brand font-semibold group-hover:translate-x-0.5 transition-transform flex items-center gap-0.5">
                  Xem chi tiết & AI →
                </span>
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
};

export default HotMoversBanner;
