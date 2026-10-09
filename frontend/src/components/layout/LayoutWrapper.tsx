'use client';

import React, { useEffect, useState } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import Sidebar from './Sidebar';
import { getToken } from '@/lib/auth';
import Link from 'next/link';
import {Bell, Database, LayoutDashboard, TrendingUp} from 'lucide-react';

export default function LayoutWrapper({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const isLoginPage = pathname === '/login';
  const isPublicPage = pathname === '/history' || pathname === '/forecast';
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      setIsAuthenticated(false);
      if (pathname !== '/login' && !isPublicPage) {
        router.replace('/login');
      }
    } else {
      setIsAuthenticated(true);
      if (pathname === '/login') {
        router.replace('/');
      }
    }
  }, [pathname, router, isPublicPage]);

  // Khi đang ở trang Login hoặc Admin Dashboard độc lập
  if (isLoginPage) {
    return (
      <main className="w-full min-h-screen bg-[#F9F6F2] overflow-y-auto flex items-center justify-center">
        {children}
      </main>
    );
  }

  // Khi đang ở Admin Dashboard Control Panel
  if (pathname.startsWith('/dashboard')) {
    return (
      <div className="w-full min-h-screen bg-canvas">
        {children}
      </div>
    );
  }

  // Khi chưa có Token và đang chuyển hướng
  if (isAuthenticated === false && !isPublicPage) {
    return (
      <div className="flex items-center justify-center min-h-screen w-full bg-[#F9F6F2]">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-3 border-[#527853] border-t-transparent rounded-full animate-spin" />
          <p className="text-xs font-bold text-[#3E2723]/60 tracking-wide uppercase">Đang chuyển hướng đăng nhập...</p>
        </div>
      </div>
    );
  }

  // Giao diện Người dùng Public (Nông dân & Thương lái)
  return (
    <div className="flex w-full min-h-screen">
      <Sidebar />
      <main className="flex-1 h-screen overflow-y-auto px-4 sm:px-6 lg:px-10 py-5 lg:py-7 pb-24 lg:pb-7 max-w-[1600px] transition-all custom-scrollbar">
        {children}
      </main>
      <nav aria-label="Điều hướng trên điện thoại" className="lg:hidden fixed inset-x-3 bottom-3 z-50 grid grid-cols-4 gap-1 rounded-2xl border border-border-subtle bg-white/95 p-2 shadow-xl backdrop-blur-md">
        {[
          {href:'/',label:'Tổng quan',icon:LayoutDashboard},
          {href:'/forecast',label:'Dự báo',icon:TrendingUp},
          {href:'/alerts',label:'Cảnh báo',icon:Bell},
          {href:'/history',label:'Lịch sử',icon:Database},
        ].map(item=>{const Icon=item.icon;const active=pathname===item.href;return <Link key={item.href} href={item.href} className={`flex min-w-0 flex-col items-center gap-1 rounded-xl px-1 py-2 text-[10px] font-bold transition-colors ${active?'bg-brand text-white':'text-secondary-text hover:bg-brand/5 hover:text-brand'}`}><Icon className="w-4 h-4"/><span className="truncate">{item.label}</span></Link>;})}
      </nav>
    </div>
  );
}

