'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Sprout, ShieldCheck, ArrowRight, Loader2 } from 'lucide-react';
import { setToken } from '@/lib/auth';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleLogin = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error('Email hoặc mật khẩu không chính xác');
      }

      const data = await response.json();
      setToken(data.access_token, data.user);
      router.push('/');
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message || 'Đã có lỗi xảy ra khi đăng nhập');
      } else {
        setError('Đã có lỗi xảy ra khi đăng nhập');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const setDummyData = (role: 'analyst' | 'admin') => {
    if (role === 'analyst') {
      setEmail('anhnguyen@agroforecast.vn');
      setPassword('123456');
    } else {
      setEmail('admin@agroforecast.vn');
      setPassword('admin123');
    }
  };

  return (
    <div className="min-h-screen bg-[#F9F6F2] flex items-center justify-center p-4 selection:bg-[#527853]/20">
      <div className="w-full max-w-md bg-white rounded-3xl shadow-xl shadow-black/[0.03] border border-black/[0.05] p-8 md:p-10 relative overflow-hidden">
        {/* Decorative elements */}
        <div className="absolute top-0 right-0 -mr-16 -mt-16 w-32 h-32 rounded-full bg-[#527853]/5 blur-2xl pointer-events-none" />
        <div className="absolute bottom-0 left-0 -ml-16 -mb-16 w-40 h-40 rounded-full bg-[#3E2723]/5 blur-3xl pointer-events-none" />

        <div className="relative z-10 flex flex-col items-center mb-8">
          <div className="w-14 h-14 rounded-2xl bg-[#527853] flex items-center justify-center shadow-lg shadow-[#527853]/20 mb-4">
            <Sprout className="w-8 h-8 text-white stroke-[2]" />
          </div>
          <h1 className="text-2xl md:text-3xl font-bold text-[#3E2723] tracking-tight">AgroForecast</h1>
          <p className="text-sm font-medium text-black/50 mt-1.5 text-center">
            Hệ thống Dự báo Giá & Cảnh báo Nông sản
          </p>
        </div>

        {error && (
          <div className="mb-6 p-3.5 bg-red-50 border border-red-100 rounded-xl text-red-600 text-sm font-medium text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4 relative z-10">
          <div>
            <label className="block text-[13px] font-bold text-[#3E2723] mb-1.5 uppercase tracking-wide">
              Email đăng nhập
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-3 rounded-xl bg-[#F9F6F2]/50 border border-black/10 focus:border-[#527853] focus:ring-2 focus:ring-[#527853]/20 focus:bg-white transition-all outline-none text-[#3E2723] font-medium"
              placeholder="nhap.email@agroforecast.vn"
            />
          </div>

          <div>
            <label className="block text-[13px] font-bold text-[#3E2723] mb-1.5 uppercase tracking-wide">
              Mật khẩu
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-3 rounded-xl bg-[#F9F6F2]/50 border border-black/10 focus:border-[#527853] focus:ring-2 focus:ring-[#527853]/20 focus:bg-white transition-all outline-none text-[#3E2723] font-medium"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full mt-2 bg-[#527853] hover:bg-[#436544] text-white font-bold py-3.5 px-4 rounded-xl shadow-md shadow-[#527853]/20 transition-all flex items-center justify-center gap-2 group disabled:opacity-70 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <>
                <span>Đăng nhập</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </>
            )}
          </button>
        </form>

        <div className="mt-8 relative z-10">
          <div className="flex items-center gap-3 mb-4">
            <div className="flex-1 h-px bg-black/5" />
            <span className="text-[11px] font-bold text-black/40 uppercase tracking-widest">Hoặc demo nhanh</span>
            <div className="flex-1 h-px bg-black/5" />
          </div>

          <div className="flex flex-col sm:flex-row gap-2.5">
            <button
              type="button"
              onClick={() => setDummyData('analyst')}
              className="flex-1 flex items-center justify-center gap-1.5 py-2.5 px-3 rounded-lg border border-[#527853]/20 bg-[#527853]/5 hover:bg-[#527853]/10 text-[#527853] font-bold text-xs transition-colors"
            >
              <ShieldCheck className="w-3.5 h-3.5" />
              Dùng thử Analyst
            </button>
            <button
              type="button"
              onClick={() => setDummyData('admin')}
              className="flex-1 flex items-center justify-center gap-1.5 py-2.5 px-3 rounded-lg border border-[#3E2723]/20 bg-[#3E2723]/5 hover:bg-[#3E2723]/10 text-[#3E2723] font-bold text-xs transition-colors"
            >
              <ShieldCheck className="w-3.5 h-3.5" />
              Dùng thử Admin
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
