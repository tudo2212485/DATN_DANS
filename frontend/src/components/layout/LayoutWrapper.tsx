'use client';

import React, { useEffect, useState } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import Sidebar from './Sidebar';
import { getToken } from '@/lib/auth';

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
      <main className="flex-1 h-screen overflow-y-auto px-7 lg:px-10 py-7 max-w-[1600px] transition-all custom-scrollbar">
        {children}
      </main>
    </div>
  );
}

