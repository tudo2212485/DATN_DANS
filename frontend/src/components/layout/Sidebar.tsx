'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  TrendingUp,
  Bell,
  Database,
  ChevronLeft,
  ChevronRight,
  GitCompare,
  BarChart3,
  Cpu,
  Users,
  Activity,
} from 'lucide-react';
import { getUser, User } from '@/lib/auth';

interface NavItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  adminOnly?: boolean;
}

const MARKET_ITEMS: NavItem[] = [
  { name: 'Tổng quan', href: '/', icon: LayoutDashboard },
  { name: 'Phân tích & Dự báo', href: '/forecast', icon: TrendingUp },
  { name: 'Dữ liệu lịch sử', href: '/history', icon: BarChart3 },
  { name: 'So sánh nông sản', href: '/compare', icon: GitCompare },
  { name: 'Cảnh báo giá', href: '/alerts', icon: Bell },
];

const ADMIN_ITEMS: NavItem[] = [
  { name: 'Tổng quan hệ thống', href: '/dashboard/overview', icon: Activity },
  { name: 'Quản lý dữ liệu & Scraper', href: '/dashboard/data-control', icon: Database },
  { name: 'Quản lý Mô hình ML', href: '/dashboard/ml-models', icon: Cpu },
  { name: 'Quản lý Tài khoản', href: '/dashboard/users', icon: Users, adminOnly: true },
];

export const Sidebar: React.FC = () => {
  const pathname = usePathname();
  const [user, setUser] = useState<User | null>(null);
  const [isCollapsed, setIsCollapsed] = useState<boolean>(false);

  useEffect(() => {
    setUser(getUser());
    const saved = localStorage.getItem('agro_sidebar_collapsed');
    if (saved !== null) {
      setIsCollapsed(saved === 'true');
    }
  }, [pathname]);

  const toggleCollapse = () => {
    const nextState = !isCollapsed;
    setIsCollapsed(nextState);
    localStorage.setItem('agro_sidebar_collapsed', String(nextState));
  };

  const showAdminSection = user?.role === 'admin';
  const visibleAdminItems = ADMIN_ITEMS;

  return (
    <aside
      className={`${
        isCollapsed ? 'w-16 px-2 py-3.5' : 'w-[240px] px-3 py-3.5'
      } h-screen sticky top-0 bg-white border-r border-[#E5E7EB] hidden lg:flex flex-col justify-between select-none shrink-0 overflow-y-auto custom-scrollbar transition-all duration-150 ease-in-out z-30 font-sans`}
    >
      {/* Top section: Brand & Navigation */}
      <div className="space-y-5">
        {/* Brand Header */}
        <div
          className={`flex items-center ${
            isCollapsed ? 'flex-col gap-2 justify-center' : 'justify-between px-1.5'
          } pb-3 border-b border-[#E5E7EB]`}
        >
          {!isCollapsed ? (
            <Link href="/" className="flex items-center gap-2.5 group">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center overflow-hidden bg-white p-0.5 shrink-0 border border-[#E5E7EB]">
                <Image
                  src="/logo.png"
                  alt="AgroForecast"
                  width={26}
                  height={26}
                  className="w-full h-full object-contain"
                />
              </div>
              <div>
                <span className="text-[15px] font-bold text-[#1E293B] tracking-tight block leading-tight">
                  AgroForecast
                </span>
                <span className="text-[11px] font-medium text-[#64748B] block leading-tight">
                  Dự báo Giá Nông sản
                </span>
              </div>
            </Link>
          ) : (
            <Link href="/" title="AgroForecast">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center overflow-hidden bg-white p-0.5 border border-[#E5E7EB]">
                <Image
                  src="/logo.png"
                  alt="AgroForecast"
                  width={26}
                  height={26}
                  className="w-full h-full object-contain"
                />
              </div>
            </Link>
          )}

          <button
            type="button"
            onClick={toggleCollapse}
            title={isCollapsed ? 'Mở rộng thanh điều hướng' : 'Thu gọn thanh điều hướng'}
            className="flex items-center justify-center w-6 h-6 rounded-md text-[#64748B] hover:text-[#0F172A] hover:bg-[#F8FAFC] transition-colors cursor-pointer"
          >
            {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
          </button>
        </div>

        {/* Group 1: Thị trường */}
        <div className="space-y-1">
          {!isCollapsed && (
            <div className="px-2.5 pb-1">
              <span className="text-[10.5px] font-bold text-[#64748B] uppercase tracking-wider">
                Thị trường
              </span>
            </div>
          )}

          <nav aria-label="Điều hướng thị trường" className="space-y-0.5">
            {MARKET_ITEMS.map((item) => {
              const isActive =
                item.href === '/'
                  ? pathname === '/' || pathname.startsWith('/commodities/')
                  : pathname.startsWith(item.href);
              const Icon = item.icon;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  title={isCollapsed ? item.name : undefined}
                  className={`flex items-center ${
                    isCollapsed ? 'justify-center p-2' : 'px-2.5 py-2'
                  } rounded-lg text-[13px] transition-colors group ${
                    isActive
                      ? 'bg-[#2F6F4E] text-white font-semibold'
                      : 'text-[#334155] font-medium hover:text-[#1E293B] hover:bg-[#F8FAF9]'
                  }`}
                >
                  <div className="flex items-center gap-2.5 min-w-0">
                    <Icon
                      className={`w-4 h-4 shrink-0 ${
                        isActive ? 'text-white' : 'text-[#64748B] group-hover:text-[#0F172A]'
                      }`}
                    />
                    {!isCollapsed && <span className="truncate">{item.name}</span>}
                  </div>
                </Link>
              );
            })}
          </nav>
        </div>

        {/* Group 2: Quản trị */}
        {showAdminSection && (
          <div className="space-y-1 pt-2 border-t border-[#E2E8F0]">
            {!isCollapsed && (
              <div className="px-2.5 pb-1 pt-1">
                <span className="text-[10.5px] font-bold text-[#64748B] uppercase tracking-wider">
                  Quản trị
                </span>
              </div>
            )}

            <nav aria-label="Điều hướng quản trị" className="space-y-0.5">
              {visibleAdminItems.map((item) => {
                const isActive = pathname.startsWith(item.href);
                const Icon = item.icon;

                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    title={isCollapsed ? item.name : undefined}
                    className={`flex items-center ${
                      isCollapsed ? 'justify-center p-2' : 'px-2.5 py-2'
                    } rounded-lg text-[13px] transition-colors group ${
                      isActive
                        ? 'bg-[#2F6F4E] text-white font-semibold'
                        : 'text-[#334155] font-medium hover:text-[#1E293B] hover:bg-[#F8FAF9]'
                    }`}
                  >
                    <div className="flex items-center gap-2.5 min-w-0">
                      <Icon
                        className={`w-4 h-4 shrink-0 ${
                          isActive ? 'text-white' : 'text-[#64748B] group-hover:text-[#0F172A]'
                        }`}
                      />
                      {!isCollapsed && <span className="truncate">{item.name}</span>}
                    </div>
                  </Link>
                );
              })}
            </nav>
          </div>
        )}
      </div>

      {/* Compact Footer Version Note (Tài khoản & Đăng xuất hiển thị duy nhất ở góc phải Topbar) */}
      {!isCollapsed && (
        <div className="pt-3 border-t border-[#E5E7EB] px-2 text-[11px] text-[#64748B] flex items-center justify-between">
          <span>AgroForecast</span>
          <span className="tabular-nums font-medium">v2.0</span>
        </div>
      )}
    </aside>
  );
};

export default Sidebar;
