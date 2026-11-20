'use client';

import React from 'react';

interface HeaderProps {
  title?: string;
  subtitle?: string;
  showLiveBadge?: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  title = 'Tổng quan thị trường',
  subtitle,
}) => {
  return (
    <header className="pb-3 border-b border-[#E5E7EB]">
      <h1 className="text-lg sm:text-xl font-bold text-[#1E293B] tracking-tight leading-snug">
        {title}
      </h1>
      {subtitle && (
        <p className="mt-0.5 text-xs text-[#64748B] font-normal">
          {subtitle}
        </p>
      )}
    </header>
  );
};

export default Header;
