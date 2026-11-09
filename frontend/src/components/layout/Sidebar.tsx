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
  ChevronLeft, 
  ChevronRight,
  GitCompare,
  BarChart3,
} from 'lucide-react';
import { getUser, removeToken, User } from '@/lib/auth';

interface NavItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
}

const NAV_ITEMS: NavItem[] = [
  {
    name: 'Tổng quan thị trường',
    href: '/',
    icon: LayoutDashboard,
  },
  {
    name: 'Phân tích & Dự báo',
    href: '/forecast',
    icon: TrendingUp,
  },
  {
    name: 'Dữ liệu lịch sử',
    href: '/history',
    icon: BarChart3,
  },
  {
    name: 'So sánh nông sản',
    href: '/compare',
    icon: GitCompare,
  },
  {
    name: 'Cảnh báo giá',
    href: '/alerts',
    icon: Bell,
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
        isCollapsed ? 'w-16 px-2.5 py-4' : 'w-60 px-3.5 py-4'
      } h-screen sticky top-0 bg-[#FAFAFA] border-r border-zinc-200/80 hidden lg:flex flex-col justify-between select-none shrink-0 overflow-y-auto custom-scrollbar transition-all duration-200 ease-in-out z-20 font-sans`}
    >
      {/* Top section: Brand & Nav */}
      <div className="space-y-6">
        {/* Brand Header */}
        <div className={`flex items-center ${isCollapsed ? 'flex-col gap-2.5 justify-center' : 'justify-between px-1.5'} pb-3.5 border-b border-zinc-200/70`}>
          {!isCollapsed ? (
            <Link href="/" className="flex items-center gap-2.5 group min-w-0">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center overflow-hidden bg-white p-0.5 shrink-0 border border-zinc-200 shadow-2xs">
                <Image src="/logo.png" alt="AgroForecast" width={28} height={28} className="w-full h-full object-contain" />
              </div>
              <div className="truncate">
                <span className="text-[15px] font-bold text-zinc-900 tracking-tight block leading-none">
                  AgroForecast
                </span>
                <span className="text-[11px] font-medium text-zinc-500 block mt-1 truncate">
                  Dữ liệu Nông sản VN
                </span>
              </div>
            </Link>
          ) : (
            <Link href="/" title="AgroForecast">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center overflow-hidden bg-white p-0.5 border border-zinc-200 shadow-2xs">
                <Image src="/logo.png" alt="AgroForecast" width={28} height={28} className="w-full h-full object-contain" />
              </div>
            </Link>
          )}

          <button
            onClick={toggleCollapse}
            title={isCollapsed ? 'Mở rộng' : 'Thu gọn'}
            className="flex items-center justify-center w-6 h-6 rounded-md text-zinc-400 hover:text-zinc-700 hover:bg-zinc-200/60 transition-colors cursor-pointer"
          >
            {isCollapsed ? (
              <ChevronRight className="w-4 h-4" />
            ) : (
              <ChevronLeft className="w-4 h-4" />
            )}
          </button>
        </div>

        {/* Navigation Links */}
        <div className="space-y-1">
          {!isCollapsed && (
            <div className="px-2.5 pb-1.5">
              <span className="text-[11px] font-semibold text-zinc-400 uppercase tracking-wider">
                Phân tích
              </span>
            </div>
          )}

          <nav className="space-y-0.5">
            {NAV_ITEMS.map((item) => {
              const isActive = pathname === item.href;
              const Icon = item.icon;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  title={isCollapsed ? item.name : undefined}
                  className={`flex items-center ${
                    isCollapsed ? 'justify-center p-2.5' : 'px-2.5 py-2'
                  } rounded-lg text-[13.5px] transition-colors group relative ${
                    isActive
                      ? 'bg-zinc-900 text-white font-medium shadow-2xs'
                      : 'text-zinc-600 font-medium hover:text-zinc-900 hover:bg-zinc-200/50'
                  }`}
                >
                  <div className="flex items-center gap-2.5 min-w-0">
                    <Icon
                      className={`w-4 h-4 shrink-0 ${
                        isActive ? 'text-emerald-400' : 'text-zinc-400 group-hover:text-zinc-700'
                      }`}
                    />
                    {!isCollapsed && <span className="truncate">{item.name}</span>}
                  </div>
                </Link>
              );
            })}
            
            {(user?.role === 'admin' || user?.role === 'analyst') && (
              <>
                {!isCollapsed && (
                  <div className="px-2.5 pt-4 pb-1.5">
                    <span className="text-[11px] font-semibold text-zinc-400 uppercase tracking-wider">
                      Hệ thống
                    </span>
                  </div>
                )}
                <Link
                  href="/dashboard"
                  title={isCollapsed ? 'Quản trị dữ liệu' : undefined}
                  className={`flex items-center ${
                    isCollapsed ? 'justify-center p-2.5' : 'justify-between px-2.5 py-2'
                  } rounded-lg text-[13.5px] transition-colors group relative ${
                    pathname.startsWith('/dashboard') || pathname === '/admin'
                      ? 'bg-zinc-900 text-white font-medium shadow-2xs'
                      : 'text-zinc-600 font-medium hover:text-zinc-900 hover:bg-zinc-200/50'
                  }`}
                >
                  <div className="flex items-center gap-2.5 min-w-0">
                    <Database
                      className={`w-4 h-4 shrink-0 ${
                        pathname.startsWith('/dashboard') || pathname === '/admin' ? 'text-emerald-400' : 'text-zinc-400 group-hover:text-zinc-700'
                      }`}
                    />
                    {!isCollapsed && <span className="truncate">Quản trị dữ liệu</span>}
                  </div>
                </Link>
              </>
            )}
          </nav>
        </div>
      </div>

      {/* Bottom User Profile Section */}
      <div className={`pt-3 border-t border-zinc-200/70 flex items-center ${isCollapsed ? 'flex-col gap-2 justify-center' : 'justify-between px-1'}`}>
        <div className="flex items-center gap-2.5 min-w-0">
          <div className="w-7 h-7 rounded-full bg-zinc-200/80 text-zinc-700 flex items-center justify-center font-semibold text-xs shrink-0 uppercase border border-zinc-300/60">
            {user?.full_name?.substring(0, 2) || 'KH'}
          </div>
          {!isCollapsed && (
            <div className="flex flex-col truncate">
              <span className="text-[13px] font-semibold text-zinc-800 leading-tight truncate">
                {user?.full_name || 'Khách'}
              </span>
              <span className="text-[11px] text-zinc-500 truncate">
                {!user ? 'Chế độ xem' : user.role === 'admin' ? 'Quản trị viên' : user.role === 'analyst' ? 'Phân tích viên' : 'Thành viên'}
              </span>
            </div>
          )}
        </div>

        <button 
          onClick={handleLogout}
          title={user ? 'Đăng xuất' : 'Đăng nhập'}
          className="text-zinc-400 hover:text-zinc-800 hover:bg-zinc-200/60 p-1.5 rounded-md transition-colors cursor-pointer shrink-0"
        >
          <LogOut className="w-4 h-4" />
        </button>
      </div>
    </aside>
  );
};
export default Sidebar;
