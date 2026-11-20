'use client';

import React, { useEffect, useState } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import Sidebar from './Sidebar';
import LocationSelector from './LocationSelector';
import { getToken, getUser, removeToken, User } from '@/lib/auth';
import { fetchCommoditiesOverview } from '@/lib/api';
import { formatDateVN } from '@/lib/formatters';
import Link from 'next/link';
import {
  Bell,
  Database,
  LayoutDashboard,
  TrendingUp,
  ChevronRight,
  Clock,
  LogOut,
  Shield,
} from 'lucide-react';

function getBreadcrumb(pathname: string): { section: string; page: string } {
  if (pathname === '/') return { section: 'Thị trường', page: 'Tổng quan giá nông sản' };
  if (pathname.startsWith('/forecast')) return { section: 'Thị trường', page: 'Phân tích & Dự báo' };
  if (pathname.startsWith('/history')) return { section: 'Thị trường', page: 'Dữ liệu lịch sử' };
  if (pathname.startsWith('/compare')) return { section: 'Thị trường', page: 'So sánh nông sản' };
  if (pathname.startsWith('/alerts')) return { section: 'Thị trường', page: 'Cảnh báo giá' };
  if (pathname.startsWith('/commodities/')) return { section: 'Thị trường', page: 'Chi tiết mặt hàng' };
  if (pathname.startsWith('/dashboard/overview')) return { section: 'Quản trị', page: 'Tổng quan hệ thống' };
  if (pathname.startsWith('/dashboard/data-control')) return { section: 'Quản trị', page: 'Quản lý dữ liệu & Scraper' };
  if (pathname.startsWith('/dashboard/ml-models')) return { section: 'Quản trị', page: 'Quản lý Mô hình ML' };
  if (pathname.startsWith('/dashboard/users')) return { section: 'Quản trị', page: 'Quản lý Tài khoản' };
  if (pathname.startsWith('/dashboard')) return { section: 'Quản trị', page: 'Tổng quan hệ thống' };
  return { section: 'Hệ thống', page: 'AgroForecast' };
}

export default function LayoutWrapper({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const isLoginPage = pathname === '/login' || pathname === '/register';
  const isPublicPage = pathname === '/history' || pathname === '/forecast';
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [latestUpdateLabel, setLatestUpdateLabel] = useState<string>('20/11/2026');

  useEffect(() => {
    const token = getToken();
    setUser(getUser());
    if (!token) {
      setIsAuthenticated(false);
      if (pathname !== '/login' && pathname !== '/register' && !isPublicPage) {
        router.replace('/login');
      }
    } else {
      setIsAuthenticated(true);
      if (pathname === '/login' || pathname === '/register') {
        router.replace('/');
      }
    }
  }, [pathname, router, isPublicPage]);

  useEffect(() => {
    if (isLoginPage) return;
    let active = true;
    fetchCommoditiesOverview()
      .then((list) => {
        if (!active || !list || list.length === 0) return;
        const firstSpark = list[0]?.sparkline;
        if (firstSpark && firstSpark.length > 0) {
          const lastPoint = firstSpark[firstSpark.length - 1].date;
          setLatestUpdateLabel(lastPoint.includes('/') && lastPoint.length === 5 ? `${lastPoint}/2026` : formatDateVN(lastPoint));
        }
      })
      .catch(() => {});
    return () => {
      active = false;
    };
  }, [isLoginPage]);

  if (isLoginPage) {
    return (
      <main className="w-full min-h-screen bg-[#F8FAFC] overflow-y-auto flex items-center justify-center">
        {children}
      </main>
    );
  }

  if (isAuthenticated === false && !isPublicPage) {
    return (
      <div className="flex items-center justify-center min-h-screen w-full bg-[#F8FAFC]">
        <div className="flex flex-col items-center gap-2.5">
          <div className="w-7 h-7 border-2 border-[#166534] border-t-transparent rounded-full animate-spin" />
          <p className="text-xs font-semibold text-[#475569] tracking-wide uppercase">
            Đang chuyển hướng đăng nhập...
          </p>
        </div>
      </div>
    );
  }

  const crumb = getBreadcrumb(pathname);

  return (
    <div className="flex w-full min-h-screen bg-[#F8FAF9] text-[#1E293B]">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0 h-screen overflow-hidden">
        {/* Top Header Bar (h-14, border-b) */}
        <header className="h-14 shrink-0 border-b border-[#E5E7EB] bg-white px-4 sm:px-6 lg:px-8 flex items-center justify-between gap-4 z-20">
          {/* Breadcrumb */}
          <nav aria-label="Breadcrumb" className="flex items-center gap-1.5 text-xs min-w-0">
            <span className="font-medium text-[#64748B] truncate">{crumb.section}</span>
            <ChevronRight className="w-3.5 h-3.5 text-[#64748B] shrink-0" />
            <span className="font-semibold text-[#1E293B] truncate">{crumb.page}</span>
          </nav>

          {/* Right: Location Picker, Latest DB Update & Account Info */}
          <div className="flex items-center gap-2.5 sm:gap-3 shrink-0">
            <LocationSelector />

            <div className="hidden md:flex items-center gap-1.5 text-xs text-[#334155] bg-[#F8FAF9] px-2.5 py-1 rounded-lg border border-[#E5E7EB]">
              <Clock className="w-3.5 h-3.5 text-[#2F6F4E]" />
              <span>Kỳ dữ liệu mới nhất:</span>
              <strong className="font-mono tabular-nums font-semibold text-[#1E293B]">
                {latestUpdateLabel}
              </strong>
            </div>

            {user?.role === 'admin' && !pathname.startsWith('/dashboard') && (
              <Link
                href="/dashboard/overview"
                className="hidden md:inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg border border-[#E5E7EB] bg-white hover:bg-[#F8FAF9] text-xs font-semibold text-[#1E293B] transition-colors"
              >
                <Shield className="w-3.5 h-3.5 text-[#2F6F4E]" />
                <span>Quản trị</span>
              </Link>
            )}

            <div className="flex items-center gap-2.5 pl-3 border-l border-[#E2E8F0]">
              <div className="text-right hidden sm:block">
                <div className="text-xs font-semibold text-[#0F172A] leading-tight">
                  {user?.full_name || 'Khách truy cập'}
                </div>
                <div className="text-[11px] text-[#64748B] leading-tight">
                  {user?.role === 'admin'
                    ? 'Quản trị viên'
                    : user?.role === 'analyst'
                      ? 'Chuyên viên phân tích'
                      : 'Chế độ xem'}
                </div>
              </div>
              <button
                type="button"
                onClick={() => {
                  removeToken();
                  router.push('/login');
                }}
                title="Đăng xuất"
                className="p-1.5 rounded-md text-[#64748B] hover:text-[#DC2626] hover:bg-[#F8FAFC] border border-transparent hover:border-[#E2E8F0] transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          </div>
        </header>

        {/* Scrollable Content Viewport */}
        <main className="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 py-5 pb-24 lg:pb-8 max-w-[1600px] w-full mx-auto custom-scrollbar">
          {children}
        </main>
      </div>

      {/* Mobile Bottom Nav */}
      <nav
        aria-label="Điều hướng trên điện thoại"
        className="lg:hidden fixed inset-x-3 bottom-3 z-50 grid grid-cols-4 gap-1 rounded-lg border border-[#E2E8F0] bg-white p-1.5 shadow-md"
      >
        {[
          { href: '/', label: 'Tổng quan', icon: LayoutDashboard },
          { href: '/forecast', label: 'Dự báo', icon: TrendingUp },
          { href: '/alerts', label: 'Cảnh báo', icon: Bell },
          { href: '/history', label: 'Lịch sử', icon: Database },
        ].map((item) => {
          const Icon = item.icon;
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex min-w-0 flex-col items-center gap-1 rounded-md px-1 py-1.5 text-[10px] font-semibold transition-colors ${
                active
                  ? 'bg-[#166534] text-white'
                  : 'text-[#475569] hover:bg-[#F8FAFC] hover:text-[#0F172A]'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span className="truncate">{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
