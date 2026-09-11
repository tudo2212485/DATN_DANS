'use client';

import React from 'react';
import { Search, MapPin, Tag, X } from 'lucide-react';

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
    <div className="p-4 rounded-2xl bg-white border border-border-subtle shadow-sm space-y-3">
      <div className="flex flex-col md:flex-row items-stretch md:items-center gap-3">
        {/* Search Input */}
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-secondary-text absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Tìm nhanh nông sản (VD: Cà phê, Gạo IR504, Hồ tiêu, Mía đường...)"
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-canvas border border-border-subtle text-sm text-primary-text placeholder:text-secondary-text/60 focus:outline-none focus:border-brand focus:ring-2 focus:ring-brand/10 transition"
          />
          {searchTerm && (
            <button
              onClick={() => onSearchChange('')}
              className="absolute right-3 top-1/2 -translate-y-1/2 p-1 text-secondary-text hover:text-primary-text"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>

        {/* Region Filter */}
        <div className="flex items-center gap-2 shrink-0">
          <div className="relative">
            <MapPin className="w-3.5 h-3.5 text-brand absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            <select
              value={selectedRegion}
              onChange={(e) => onRegionChange(e.target.value)}
              className="pl-8 pr-8 py-2.5 rounded-xl bg-canvas border border-border-subtle text-xs font-semibold text-primary-text focus:outline-none focus:border-brand appearance-none cursor-pointer"
            >
              <option value="ALL">Toàn bộ vùng miền</option>
              {regions.map((r) => (
                <option key={r} value={r}>
                  {r}
                </option>
              ))}
            </select>
          </div>

          {/* Category Filter */}
          <div className="relative">
            <Tag className="w-3.5 h-3.5 text-secondary-text absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            <select
              value={selectedCategory}
              onChange={(e) => onCategoryChange(e.target.value)}
              className="pl-8 pr-8 py-2.5 rounded-xl bg-canvas border border-border-subtle text-xs font-semibold text-primary-text focus:outline-none focus:border-brand appearance-none cursor-pointer"
            >
              <option value="ALL">Tất cả ngành hàng</option>
              {categories.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>

          {hasFilter && (
            <button
              onClick={clearAllFilters}
              className="px-3 py-2.5 rounded-xl bg-rose-50 text-rose-700 hover:bg-rose-100 text-xs font-semibold transition"
            >
              Xóa lọc
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default QuickSearchBar;
