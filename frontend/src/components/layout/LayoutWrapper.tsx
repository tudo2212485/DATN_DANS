'use client';

import React, { useEffect, useState } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import Sidebar from './Sidebar';
import { getToken } from '@/lib/auth';

export default function LayoutWrapper({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const isLoginPage = pathname === '/login';
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const token = getToken();
    if (!token && pathname !== '/login') {
      router.push('/login');
    } else if (token && pathname === '/login') {
      router.push('/');
    }
  }, [pathname, router]);

  if (!mounted) return null; // Prevent hydration mismatch

  if (isLoginPage) {
    return <main className="flex-1 h-screen w-full">{children}</main>;
  }

  return (
    <>
      <Sidebar />
      <main className="flex-1 h-screen overflow-y-auto px-7 lg:px-10 py-7 max-w-[1600px] transition-all">
        {children}
      </main>
    </>
  );
}
