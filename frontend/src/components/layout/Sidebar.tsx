'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { usePathname, useRouter } from 'next/navigation';
import { LayoutDashboard, TrendingUp, Bell, Sprout, Sparkles, CheckCircle, ShieldCheck, Database, LogOut } from 'lucide-react';
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
  
  useEffect(() => {
    setUser(getUser());
  }, []);

  const handleLogout = () => {
    removeToken();
    router.push('/login');
  };

  return (
    <aside className="w-64 h-screen sticky top-0 bg-sidebar border-r border-border-subtle flex flex-col justify-between p-5 select-none shrink-0 overflow-y-auto custom-scrollbar">
      {/* Top section: Brand Logo & Navigation */}
      <div className="space-y-6">
        {/* Brand Header */}
        <div className="flex items-center justify-between pb-4 border-b border-border-subtle/80">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-2xl flex items-center justify-center shadow-md shadow-brand/20 group-hover:scale-105 transition-transform overflow-hidden bg-white p-1">
              <Image src="/logo.png" alt="AgroForecast Logo" width={40} height={40} className="w-full h-full object-contain" />
            </div>
            <div>
              <h1 className="text-base font-bold text-primary-text leading-tight tracking-tight group-hover:text-brand transition-colors">
                AgroForecast
              </h1>
              <div className="flex items-center gap-1.5 mt-0.5">
                <span className="text-[11px] font-semibold text-secondary-text tracking-wide">
                  v2.4.1
                </span>
                <span className="w-1 h-1 rounded-full bg-brand" />
                <span className="text-[10px] font-bold text-brand uppercase tracking-wider">
                  Pro
                </span>
              </div>
            </div>
          </Link>
        </div>

        {/* Section: Navigation Links */}
        <div>
          <div className="mb-2.5 px-2">
            <span className="text-[10px] font-bold text-secondary-text/70 uppercase tracking-widest">
              ĐIỀU HƯỚNG
            </span>
          </div>

          <nav className="space-y-1.5">
            {NAV_ITEMS.map((item) => {
              const isActive = pathname === item.href;
              const Icon = item.icon;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-bold transition-all duration-200 group ${
                    isActive
                      ? 'bg-brand-light text-brand shadow-sm border border-brand/20'
                      : 'text-secondary-text hover:text-primary-text hover:bg-black/[0.03]'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <Icon
                      className={`w-4 h-4 transition-transform group-hover:scale-110 ${
                        isActive ? 'text-brand stroke-[2.4]' : 'text-secondary-text stroke-[1.8]'
                      }`}
                    />
                    <span className="tracking-tight">{item.name}</span>
                  </div>

                  {item.badge && (
                    <span
                      className={`text-[10px] font-extrabold px-2 py-0.5 rounded-md ${
                        isActive
                          ? 'bg-brand text-white shadow-xs'
                          : 'bg-canvas border border-border-subtle text-secondary-text'
                      }`}
                    >
                      {item.badge}
                    </span>
                  )}
                </Link>
              );
            })}
            
            {user?.role === 'admin' && (
              <Link
                href="/admin"
                className={`flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-bold transition-all duration-200 group ${
                  pathname === '/admin'
                    ? 'bg-brand-light text-brand shadow-sm border border-brand/20'
                    : 'text-secondary-text hover:text-primary-text hover:bg-black/[0.03]'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Database
                    className={`w-4 h-4 transition-transform group-hover:scale-110 ${
                      pathname === '/admin' ? 'text-brand stroke-[2.4]' : 'text-secondary-text stroke-[1.8]'
                    }`}
                  />
                  <span className="tracking-tight">Quản trị dữ liệu</span>
                </div>
              </Link>
            )}
          </nav>
        </div>


      </div>

      {/* Bottom User Profile Section */}
      <div className="pt-3.5 border-t border-border-subtle flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-9 h-9 rounded-xl bg-[#EAE5DF] text-primary-text flex items-center justify-center font-extrabold text-xs shadow-inner uppercase">
              {user?.full_name?.substring(0, 2) || 'U'}
            </div>
            <span className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full bg-brand border-2 border-sidebar" />
          </div>
          <div className="flex flex-col">
            <span className="text-xs font-bold text-primary-text leading-tight flex items-center gap-1 truncate max-w-[100px]">
              {user?.full_name || 'Đang tải...'}
            </span>
            <span className="text-[11px] text-secondary-text font-medium">
              {user?.role === 'admin' ? 'Quản trị viên' : 'Nhà phân tích'}
            </span>
          </div>
        </div>

        <div className="flex items-center gap-1">
          <div title="Tài khoản đã xác thực" className="text-brand p-1">
            <ShieldCheck className="w-4 h-4" />
          </div>
          <button 
            onClick={handleLogout}
            title="Đăng xuất"
            className="text-secondary-text hover:text-red-500 hover:bg-red-50 p-1.5 rounded-lg transition-colors"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
  );
};
export default Sidebar;
