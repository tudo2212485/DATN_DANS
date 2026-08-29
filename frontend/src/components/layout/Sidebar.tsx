'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { usePathname, useRouter } from 'next/navigation';
import { 
  LayoutDashboard, 
  TrendingUp, 
  Bell, 
  Database, 
  LogOut, 
  ShieldCheck, 
  ChevronLeft, 
  ChevronRight
} from 'lucide-react';
import { getUser, removeToken, User } from '@/lib/auth';

interface NavItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: string;
}

const NAV_ITEMS: NavItem[] = [
  {
    name: 'Tổng quan',
    href: '/',
    icon: LayoutDashboard,
  },
  {
    name: 'Mô hình & Dự báo',
    href: '/forecast',
    icon: TrendingUp,
    badge: 'AI 96.5%',
  },
  {
    name: 'Quản lý Cảnh báo',
    href: '/alerts',
    icon: Bell,
    badge: '4 Rules',
  },
];

export const Sidebar: React.FC = () => {
  const pathname = usePathname();
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [isCollapsed, setIsCollapsed] = useState<boolean>(false);
  
  useEffect(() => {
    setUser(getUser());
    const saved = localStorage.getItem('agro_sidebar_collapsed');
    if (saved !== null) {
      setIsCollapsed(saved === 'true');
    }
  }, []);

  const toggleCollapse = () => {
    const nextState = !isCollapsed;
    setIsCollapsed(nextState);
    localStorage.setItem('agro_sidebar_collapsed', String(nextState));
  };

  const handleLogout = () => {
    removeToken();
    router.push('/login');
  };

  return (
    <aside 
      className={`${
        isCollapsed ? 'w-[72px] px-2.5 py-4' : 'w-64 p-5'
      } h-screen sticky top-0 bg-sidebar border-r border-border-subtle flex flex-col justify-between select-none shrink-0 overflow-y-auto custom-scrollbar transition-all duration-300 ease-in-out z-20`}
    >
      {/* Top section: Brand Logo & Navigation */}
      <div className="space-y-6">
        {/* Brand Header */}
        <div className={`flex items-center ${isCollapsed ? 'flex-col gap-3 justify-center' : 'justify-between'} pb-4 border-b border-border-subtle/80 relative`}>
          {!isCollapsed ? (
            <Link href="/" className="flex items-center gap-3 group overflow-hidden">
              <div className="w-10 h-10 rounded-2xl flex items-center justify-center shadow-md shadow-brand/20 group-hover:scale-105 transition-transform overflow-hidden bg-white p-1 shrink-0 border border-border-subtle">
                <Image src="/logo.png" alt="AgroForecast Logo" width={40} height={40} className="w-full h-full object-contain" />
              </div>
              <div className="truncate">
                <h1 className="text-base font-bold text-primary-text leading-tight tracking-tight group-hover:text-brand transition-colors truncate flex items-center gap-1.5">
                  AgroForecast
                </h1>
                <div className="flex items-center gap-1.5 mt-0.5">
                  <span className="text-[11px] font-semibold text-secondary-text tracking-wide">
                    v2.4.1
                  </span>
                  <span className="w-1 h-1 rounded-full bg-brand" />
                  <span className="text-[10px] font-bold text-brand uppercase tracking-wider">
                    PRO
                  </span>
                </div>
              </div>
            </Link>
          ) : (
            <Link href="/" title="AgroForecast" className="group">
              <div className="w-10 h-10 rounded-2xl flex items-center justify-center shadow-md shadow-brand/20 group-hover:scale-105 transition-transform overflow-hidden bg-white p-1 border border-border-subtle">
                <Image src="/logo.png" alt="AgroForecast Logo" width={40} height={40} className="w-full h-full object-contain" />
              </div>
            </Link>
          )}

          {/* Collapse / Expand Toggle Button with clear Arrow */}
          <button
            onClick={toggleCollapse}
            title={isCollapsed ? 'Mở rộng thanh điều hướng' : 'Thu gọn thanh điều hướng'}
            className="flex items-center justify-center w-7 h-7 rounded-lg border border-border-subtle bg-white text-secondary-text hover:text-brand hover:border-brand/40 hover:bg-brand-badge shadow-xs transition-all cursor-pointer group"
          >
            {isCollapsed ? (
              <ChevronRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform text-primary-text hover:text-brand" />
            ) : (
              <ChevronLeft className="w-4 h-4 group-hover:-translate-x-0.5 transition-transform text-primary-text hover:text-brand" />
            )}
          </button>
        </div>

        {/* Section: Navigation Links */}
        <div>
          {!isCollapsed && (
            <div className="mb-2.5 px-2">
              <span className="text-[10px] font-extrabold text-secondary-text/70 uppercase tracking-widest">
                ĐIỀU HƯỚNG
              </span>
            </div>
          )}

          <nav className="space-y-1.5">
            {NAV_ITEMS.map((item) => {
              const isActive = pathname === item.href;
              const Icon = item.icon;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  title={isCollapsed ? item.name : undefined}
                  className={`flex items-center ${
                    isCollapsed ? 'justify-center px-0 py-3' : 'justify-between px-3.5 py-2.5'
                  } rounded-xl text-xs font-bold transition-all duration-200 group relative ${
                    isActive
                      ? 'bg-brand-light text-brand shadow-xs border border-brand/25'
                      : 'text-secondary-text hover:text-primary-text hover:bg-black/[0.03]'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <Icon
                      className={`w-4 h-4 transition-transform group-hover:scale-110 shrink-0 ${
                        isActive ? 'text-brand stroke-[2.4]' : 'text-secondary-text stroke-[1.8]'
                      }`}
                    />
                    {!isCollapsed && <span className="tracking-tight truncate">{item.name}</span>}
                  </div>

                  {!isCollapsed && item.badge && (
                    <span
                      className={`text-[10px] font-extrabold px-2 py-0.5 rounded-md shrink-0 ${
                        isActive
                          ? 'bg-brand text-white shadow-xs'
                          : 'bg-canvas border border-border-subtle text-secondary-text'
                      }`}
                    >
                      {item.badge}
                    </span>
                  )}

                  {/* Active dot indicator when collapsed */}
                  {isCollapsed && isActive && (
                    <span className="absolute right-1.5 top-1/2 -translate-y-1/2 w-1.5 h-1.5 rounded-full bg-brand" />
                  )}
                </Link>
              );
            })}
            
            {user?.role === 'admin' && (
              <Link
                href="/admin"
                title={isCollapsed ? 'Quản trị dữ liệu' : undefined}
                className={`flex items-center ${
                  isCollapsed ? 'justify-center px-0 py-3' : 'justify-between px-3.5 py-2.5'
                } rounded-xl text-xs font-bold transition-all duration-200 group relative ${
                  pathname === '/admin'
                    ? 'bg-brand-light text-brand shadow-xs border border-brand/25'
                    : 'text-secondary-text hover:text-primary-text hover:bg-black/[0.03]'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Database
                    className={`w-4 h-4 transition-transform group-hover:scale-110 shrink-0 ${
                      pathname === '/admin' ? 'text-brand stroke-[2.4]' : 'text-secondary-text stroke-[1.8]'
                    }`}
                  />
                  {!isCollapsed && <span className="tracking-tight truncate">Quản trị dữ liệu</span>}
                </div>
                {isCollapsed && pathname === '/admin' && (
                  <span className="absolute right-1.5 top-1/2 -translate-y-1/2 w-1.5 h-1.5 rounded-full bg-brand" />
                )}
              </Link>
            )}
          </nav>
        </div>
      </div>

      {/* Bottom User Profile Section */}
      <div className={`pt-3.5 border-t border-border-subtle flex items-center ${isCollapsed ? 'flex-col gap-2.5 justify-center' : 'justify-between'}`}>
        <div className="flex items-center gap-3">
          <div className="relative shrink-0">
            <div className="w-9 h-9 rounded-xl bg-[#EAE5DF] text-primary-text flex items-center justify-center font-extrabold text-xs shadow-inner uppercase border border-border-subtle">
              {user?.full_name?.substring(0, 2) || 'U'}
            </div>
            <span className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full bg-brand border-2 border-sidebar" />
          </div>
          {!isCollapsed && (
            <div className="flex flex-col truncate">
              <span className="text-xs font-bold text-primary-text leading-tight flex items-center gap-1 truncate max-w-[105px]">
                {user?.full_name || 'Đang tải...'}
              </span>
              <span className="text-[11px] text-secondary-text font-medium truncate">
                {user?.role === 'admin' ? 'Quản trị viên' : 'Nhà phân tích'}
              </span>
            </div>
          )}
        </div>

        <div className={`flex items-center ${isCollapsed ? 'flex-col gap-1' : 'gap-1'}`}>
          {!isCollapsed && (
            <div title="Tài khoản đã xác thực" className="text-brand p-1">
              <ShieldCheck className="w-4 h-4" />
            </div>
          )}
          <button 
            onClick={handleLogout}
            title="Đăng xuất"
            className="text-secondary-text hover:text-red-500 hover:bg-red-50 p-1.5 rounded-lg transition-colors cursor-pointer"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
  );
};
export default Sidebar;
