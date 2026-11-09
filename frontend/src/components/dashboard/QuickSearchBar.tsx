'use client';

import React from 'react';
import { Search, X } from 'lucide-react';

interface QuickSearchBarProps {
  searchTerm: string;
  onSearchChange: (value: string) => void;
  selectedRegion: string;
  onRegionChange: (region: string) => void;
  selectedCategory: string;
  onCategoryChange: (category: string) => void;
  regions: string[];
  categories: string[];
}

export const QuickSearchBar: React.FC<QuickSearchBarProps> = ({
  searchTerm,
  onSearchChange,
  selectedRegion,
  onRegionChange,
  selectedCategory,
  onCategoryChange,
  regions,
  categories,
}) => {
  const hasFilter = searchTerm || selectedRegion !== 'ALL' || selectedCategory !== 'ALL';

  const clearAllFilters = () => {
    onSearchChange('');
    onRegionChange('ALL');
    onCategoryChange('ALL');
  };

  return (
    <div className="p-3.5 rounded-xl bg-white border border-zinc-200/90 shadow-[0_1px_2px_rgba(0,0,0,0.02)] font-sans">
      <div className="flex flex-col md:flex-row items-stretch md:items-center gap-2.5">
        {/* Search Input */}
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Tìm mặt hàng hoặc vùng trồng (VD: Cà phê, Hồ tiêu, Lúa IR504...)"
            className="w-full pl-9 pr-8 py-2 rounded-lg bg-zinc-50/80 border border-zinc-200 text-[13.5px] text-zinc-900 placeholder:text-zinc-400 focus:bg-white focus:outline-none focus:border-zinc-400 transition"
          />
          {searchTerm && (
            <button
              onClick={() => onSearchChange('')}
              className="absolute right-2.5 top-1/2 -translate-y-1/2 p-1 text-zinc-400 hover:text-zinc-700"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-2 shrink-0">
          <select
            value={selectedRegion}
            onChange={(e) => onRegionChange(e.target.value)}
            className="px-3 py-2 rounded-lg bg-zinc-50/80 hover:bg-zinc-100/80 border border-zinc-200 text-[13px] font-medium text-zinc-700 focus:outline-none focus:border-zinc-400 cursor-pointer"
          >
            <option value="ALL">Tất cả khu vực</option>
            {regions.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>

          <select
            value={selectedCategory}
            onChange={(e) => onCategoryChange(e.target.value)}
            className="px-3 py-2 rounded-lg bg-zinc-50/80 hover:bg-zinc-100/80 border border-zinc-200 text-[13px] font-medium text-zinc-700 focus:outline-none focus:border-zinc-400 cursor-pointer"
          >
            <option value="ALL">Tất cả nhóm hàng</option>
            {categories.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>

          {hasFilter && (
            <button
              onClick={clearAllFilters}
              className="px-3 py-2 rounded-lg bg-zinc-100 hover:bg-zinc-200 text-zinc-700 text-[12.5px] font-medium transition cursor-pointer"
            >
              Đặt lại
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default QuickSearchBar;
