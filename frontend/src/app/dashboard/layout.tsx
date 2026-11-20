'use client';

import { fetchCurrentUserApi } from '@/lib/api';
import React, { useState, useEffect } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import { logout } from '@/lib/auth';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    fetchCurrentUserApi()
      .then((user) => {
        if (cancelled) return;
        if (user.role !== 'admin') {
          router.replace('/');
          return;
        }
        localStorage.setItem('agro_user', JSON.stringify(user));
        setLoading(false);
      })
      .catch(() => {
        if (!cancelled) {
          logout();
          router.replace('/login?redirect=' + encodeURIComponent(pathname));
        }
      });
    return () => {
      cancelled = true;
    };
  }, [router, pathname]);

  if (loading) {
    return (
      <div className="py-20 flex flex-col items-center justify-center text-[#0F172A]">
        <div className="w-7 h-7 border-2 border-[#166534] border-t-transparent rounded-full animate-spin mb-3" />
        <p className="text-xs font-medium text-[#475569]">Đang xác thực quyền truy cập quản trị...</p>
      </div>
    );
  }

  return <div className="space-y-5">{children}</div>;
}
