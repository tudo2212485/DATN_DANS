'use client';

import React from 'react';
import { Calendar, Clock } from 'lucide-react';

interface HeaderProps {
  title?: string;
  subtitle?: string;
  showLiveBadge?: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  title = 'Tổng quan thị trường',
  subtitle = 'Cập nhật lần cuối: 28/08/2026 · 14:30',
  showLiveBadge = true,
}) => {
  return (
    <header className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-7 pb-2">
      <div>
        <h1 className="text-2xl font-extrabold text-primary-text tracking-tight">
          {title}
        </h1>
        <div className="flex items-center gap-2 mt-1 text-xs text-secondary-text font-medium">
          <Clock className="w-3.5 h-3.5 text-secondary-text/80" />
          <span>{subtitle}</span>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-canvas border border-border-subtle text-xs font-semibold text-secondary-text">
          <Calendar className="w-3.5 h-3.5 text-brand" />
          <span>Q3/2026</span>
        </div>

        {showLiveBadge && (
          <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-brand-badge text-brand text-xs font-bold border border-brand/20 shadow-xs">
            <span className="w-2 h-2 rounded-full bg-brand animate-pulse-live" />
            <span className="tracking-wide font-extrabold">LIVE</span>
          </div>
        )}
      </div>
    </header>
  );
};
export default Header;
