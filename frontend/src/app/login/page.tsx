'use client';

import React, { useState } from 'react';
import Link from 'next/link';
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
      const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errBody = await response.json().catch(() => ({}));
        throw new Error(typeof errBody.detail === 'string' ? errBody.detail : 'Không thể đăng nhập');
      }

      const data = await response.json();
      setToken(data.access_token, data.user);
      const target = new URLSearchParams(window.location.search).get('redirect');
      router.push(target?.startsWith('/') && !target.startsWith('//') ? target : '/');
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Đã có lỗi xảy ra khi đăng nhập');
    } finally {
      setIsLoading(false);
    }
  };

  const setDemoAccount = (role: 'analyst' | 'admin') => {
    if (role === 'analyst') {
      setEmail('anhnguyen@agroforecast.vn');
      setPassword('123456');
    } else {
      setEmail('admin@agroforecast.vn');
      setPassword('admin123');
    }
  };

  return (
    <div className="w-full flex items-center justify-center p-4 bg-[#F8FAF9]">
      <div className="w-full max-w-md bg-white rounded-xl border border-[#E5E7EB] p-7 sm:p-8 shadow-card">
        <div className="flex flex-col items-center mb-6">
          <div className="w-12 h-12 rounded-xl bg-[#2F6F4E] flex items-center justify-center mb-3">
            <Sprout className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-xl sm:text-2xl font-bold text-[#1E293B] tracking-tight">
            Đăng nhập AgroForecast
          </h1>
          <p className="text-xs sm:text-sm text-[#64748B] mt-1 text-center">
            Hệ thống Phân tích & Dự báo Giá Nông sản Việt Nam
          </p>
        </div>

        {error && (
          <div role="alert" className="mb-5 p-3 bg-red-50 border border-red-200 rounded-lg text-[#DC2626] text-xs font-medium text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-[#334155] mb-1.5">
              Email đăng nhập
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-3.5 py-2.5 rounded-lg bg-white border border-[#E5E7EB] focus:border-[#2F6F4E] focus:outline-none text-sm text-[#1E293B]"
              placeholder="nhap.email@agroforecast.vn"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-[#334155] mb-1.5">
              Mật khẩu
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-3.5 py-2.5 rounded-lg bg-white border border-[#E5E7EB] focus:border-[#2F6F4E] focus:outline-none text-sm text-[#1E293B]"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-[#2F6F4E] hover:bg-[#24583D] text-white font-semibold py-2.5 px-4 rounded-lg text-sm transition-colors flex items-center justify-center gap-2 disabled:opacity-60 cursor-pointer"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <>
                <span>Đăng nhập</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        <div className="mt-6 pt-5 border-t border-[#E5E7EB] space-y-3">
          <p className="text-[11px] font-semibold text-[#64748B] uppercase tracking-wider text-center">
            Tài khoản kiểm thử nhanh
          </p>
          <div className="grid grid-cols-2 gap-2.5">
            <button
              type="button"
              onClick={() => setDemoAccount('analyst')}
              className="flex items-center justify-center gap-1.5 py-2 px-3 rounded-lg border border-[#E5E7EB] bg-[#F8FAF9] hover:bg-[#F0F7F4] text-[#2F6F4E] font-semibold text-xs transition-colors cursor-pointer"
            >
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Chuyên viên (Analyst)</span>
            </button>
            <button
              type="button"
              onClick={() => setDemoAccount('admin')}
              className="flex items-center justify-center gap-1.5 py-2 px-3 rounded-lg border border-[#E5E7EB] bg-[#F8FAF9] hover:bg-[#F0F7F4] text-[#1E293B] font-semibold text-xs transition-colors cursor-pointer"
            >
              <ShieldCheck className="w-3.5 h-3.5 text-[#2F6F4E]" />
              <span>Quản trị viên (Admin)</span>
            </button>
          </div>
          <p className="text-center text-xs text-[#64748B] pt-1">
            Chưa có tài khoản?{' '}
            <Link href="/register" className="text-[#2F6F4E] font-semibold hover:underline">
              Đăng ký tài khoản mới
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
