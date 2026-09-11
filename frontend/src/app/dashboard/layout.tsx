'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { getUser, User, logout } from '@/lib/auth';
import {
  LayoutDashboard,
  Database,
  Cpu,
  Users,
  LogOut,
  TrendingUp,
  Activity,
  ArrowLeft,
  Menu,
  X
} from 'lucide-react';


export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const user = getUser();
    if (!user) {
      router.push('/login?redirect=/dashboard');
      return;
    }
    if (user.role !== 'admin' && user.role !== 'analyst') {
      router.push('/');
      return;
    }
    setCurrentUser(user);
    setLoading(false);
  }, [router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-canvas flex flex-col items-center justify-center text-primary-text">
        <div className="w-10 h-10 border-4 border-brand border-t-transparent rounded-full animate-spin mb-4" />
        <p className="text-sm font-medium text-secondary-text">Đang xác thực quyền Quản trị viên...</p>
      </div>
    );
  }

  const navItems = [
    {
      label: 'Tổng Quan Hệ Thống',
      href: '/dashboard/overview',
      icon: LayoutDashboard,
      desc: 'Chỉ số vĩ mô & Bảng giá thị trường'
    },
    {
      label: 'Quản Lý Dữ Liệu',
      href: '/dashboard/data-control',
      icon: Database,
      desc: 'Bot Scraper, Crawler Logs & CSV'
    },
    {
      label: 'Mô Hình Machine Learning',
      href: '/dashboard/ml-models',
      icon: Cpu,
      desc: 'Đánh giá sai số, Retrain & Model Switcher'
    },
    {
      label: 'Quản Lý Người Dùng',
      href: '/dashboard/users',
      icon: Users,
      desc: 'Phân quyền Admin/Analyst & Tài khoản'
    },
  ];

  return (
    <div className="min-h-screen bg-canvas text-primary-text flex flex-col">
      {/* Top Header Bar */}
      <header className="h-16 border-b border-border-subtle bg-card/90 backdrop-blur-md sticky top-0 z-40 px-4 sm:px-6 flex items-center justify-between shadow-xs">
        <div className="flex items-center gap-3">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-xl bg-canvas text-secondary-text hover:text-primary-text border border-border-subtle"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
          
          <Link href="/" className="flex items-center gap-2 group">
            <div className="w-9 h-9 rounded-xl bg-brand flex items-center justify-center shadow-xs">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="font-bold text-base text-primary-text">
                AgroForecast Admin
              </span>
              <span className="hidden sm:inline-block ml-2 text-[11px] font-medium text-brand px-2 py-0.5 rounded-md bg-brand-light border border-brand/20">
                Control Panel
              </span>
            </div>
          </Link>
        </div>

        <div className="flex items-center gap-4">
          <Link
            href="/"
            className="hidden sm:flex items-center gap-1.5 text-xs text-secondary-text hover:text-primary-text px-3 py-1.5 rounded-lg bg-canvas border border-border-subtle hover:bg-[#F2ECE4] transition font-medium"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            Về Trang Chủ Public
          </Link>

          <div className="flex items-center gap-3 pl-3 border-l border-border-subtle">
            <div className="text-right hidden sm:block">
              <div className="text-xs font-semibold text-primary-text">{currentUser?.full_name}</div>
              <div className="text-[11px] text-brand capitalize font-mono font-medium">Role: {currentUser?.role}</div>
            </div>
            <button
              onClick={() => {
                logout();
                router.push('/login');
              }}
              className="p-2 rounded-lg text-secondary-text hover:text-rose-600 hover:bg-rose-50 transition"
              title="Đăng xuất"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </header>

      {/* Main Layout Body */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar for Desktop */}
        <aside className="w-64 border-r border-border-subtle bg-card hidden md:flex flex-col justify-between p-4 shrink-0">
          <div className="space-y-1.5">
            <div className="px-3 py-2 text-[11px] font-bold tracking-wider text-secondary-text uppercase">
              Menu Điều Khiển
            </div>
            {navItems.map((item) => {
              const isActive = pathname.startsWith(item.href);
              const Icon = item.icon;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-start gap-3 px-3 py-2.5 rounded-xl transition ${
                    isActive
                      ? 'bg-brand text-white font-medium shadow-xs'
                      : 'text-secondary-text hover:text-primary-text hover:bg-canvas'
                  }`}
                >
                  <Icon className={`w-5 h-5 mt-0.5 shrink-0 ${isActive ? 'text-white' : 'text-secondary-text'}`} />
                  <div>
                    <div className="text-sm font-semibold">{item.label}</div>
                    <div className={`text-[11px] font-normal leading-tight mt-0.5 ${isActive ? 'text-white/80' : 'text-secondary-text'}`}>
                      {item.desc}
                    </div>
                  </div>
                </Link>
              );
            })}
          </div>

          <div className="p-3.5 rounded-xl bg-canvas border border-border-subtle text-xs text-secondary-text space-y-1.5">
            <div className="flex items-center gap-2 text-brand font-semibold">
              <Activity className="w-3.5 h-3.5 animate-pulse" />
              <span>Hệ Thống Trực Tuyến</span>
            </div>
            <p className="text-[11px] text-secondary-text leading-relaxed">
              PostgreSQL DB & FastAPI ML Engine đang hoạt động ổn định.
            </p>
          </div>
        </aside>

        {/* Mobile Navigation Drawer */}
        {mobileMenuOpen && (
          <div className="fixed inset-0 z-50 bg-primary-text/40 backdrop-blur-sm md:hidden p-6 flex flex-col justify-between">
            <div className="bg-card rounded-2xl p-5 border border-border-subtle shadow-xl space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
                <span className="font-bold text-primary-text">Điều hướng Quản trị</span>
                <button onClick={() => setMobileMenuOpen(false)} className="p-2 text-secondary-text">
                  <X className="w-5 h-5" />
                </button>
              </div>
              <div className="space-y-2">
                {navItems.map((item) => {
                  const Icon = item.icon;
                  const isActive = pathname.startsWith(item.href);
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={() => setMobileMenuOpen(false)}
                      className={`flex items-center gap-3 p-3 rounded-xl border transition ${
                        isActive 
                          ? 'bg-brand text-white border-brand font-medium' 
                          : 'bg-canvas border-border-subtle text-primary-text'
                      }`}
                    >
                      <Icon className="w-5 h-5" />
                      <span>{item.label}</span>
                    </Link>
                  );
                })}
              </div>
            </div>
            <button
              onClick={() => {
                logout();
                router.push('/login');
              }}
              className="w-full py-3 rounded-xl bg-rose-50 text-rose-700 border border-rose-200 flex items-center justify-center gap-2 font-medium"
            >
              <LogOut className="w-4 h-4" />
              Đăng Xuất
            </button>
          </div>
        )}

        {/* Main Content Viewport */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 bg-canvas">
          <div className="max-w-7xl mx-auto space-y-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
