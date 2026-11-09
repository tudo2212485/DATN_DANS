'use client';

import React from 'react';

interface HeaderProps {
  title?: string;
  subtitle?: string;
  showLiveBadge?: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  title = 'Tổng quan thị trường',
  subtitle = 'Dữ liệu giá thu mua nội địa cập nhật từ các vùng chuyên canh',
  showLiveBadge = true,
}) => {
  return (
    <header className="flex flex-col sm:flex-row sm:items-end justify-between gap-3 pb-4 border-b border-zinc-200/80">
      <div>
        <h1 className="text-xl sm:text-[22px] font-bold text-zinc-900 tracking-tight leading-snug">
          {title}
        </h1>
        {subtitle && (
          <p className="mt-0.5 text-[13px] text-zinc-500 font-normal">
            {subtitle}
          </p>
        )}
      </div>

      {showLiveBadge && (
        <div className="flex items-center gap-2 text-[12px] text-zinc-500 font-medium shrink-0">
          <span className="inline-block w-1.5 h-1.5 rounded-full bg-emerald-600" />
          <span>Thị trường nội địa Việt Nam</span>
        </div>
      )}
    </header>
  );
};

export default Header;
