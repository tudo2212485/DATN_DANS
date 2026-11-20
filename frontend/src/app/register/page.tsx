'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Sprout, ArrowRight, Loader2, CheckCircle2 } from 'lucide-react';

export default function RegisterPage() {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const router = useRouter();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
      const response = await fetch(`${API_BASE}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          full_name: fullName,
          email,
          password,
        }),
      });

      if (!response.ok) {
        const errBody = await response.json().catch(() => ({}));
        throw new Error(typeof errBody.detail === 'string' ? errBody.detail : 'Không thể đăng ký tài khoản');
      }

      setSuccess(true);
      setTimeout(() => {
        router.push('/login');
      }, 1500);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Đã có lỗi xảy ra khi đăng ký');
    } finally {
      setIsLoading(false);
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
            Đăng ký tài khoản AgroForecast
          </h1>
          <p className="text-xs sm:text-sm text-[#64748B] mt-1 text-center">
            Tạo tài khoản theo dõi giá và thiết lập cảnh báo thị trường nông sản
          </p>
        </div>

        {error && (
          <div role="alert" className="mb-5 p-3 bg-red-50 border border-red-200 rounded-lg text-[#DC2626] text-xs font-medium text-center">
            {error}
          </div>
        )}

        {success && (
          <div role="status" className="mb-5 p-3 bg-[#F0F7F4] border border-[#2F6F4E]/30 rounded-lg text-[#2F6F4E] text-xs font-semibold flex items-center justify-center gap-2">
            <CheckCircle2 className="w-4 h-4" />
            <span>Đăng ký thành công! Đang chuyển hướng tới trang đăng nhập...</span>
          </div>
        )}

        <form onSubmit={handleRegister} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-[#334155] mb-1.5">
              Họ và tên
            </label>
            <input
              type="text"
              minLength={2}
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
              className="w-full px-3.5 py-2.5 rounded-lg bg-white border border-[#E5E7EB] focus:border-[#2F6F4E] focus:outline-none text-sm text-[#1E293B]"
              placeholder="VD: Nguyễn Văn An"
            />
          </div>

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
              Mật khẩu (tối thiểu 6 ký tự)
            </label>
            <input
              type="password"
              minLength={6}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-3.5 py-2.5 rounded-lg bg-white border border-[#E5E7EB] focus:border-[#2F6F4E] focus:outline-none text-sm text-[#1E293B]"
              placeholder="Tối thiểu 6 ký tự"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading || success}
            className="w-full bg-[#2F6F4E] hover:bg-[#24583D] text-white font-semibold py-2.5 px-4 rounded-lg text-sm transition-colors flex items-center justify-center gap-2 disabled:opacity-60 cursor-pointer"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <>
                <span>Tạo tài khoản</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        <p className="text-center text-xs text-[#64748B] mt-6 pt-4 border-t border-[#E5E7EB]">
          Đã có tài khoản?{' '}
          <Link href="/login" className="text-[#2F6F4E] font-semibold hover:underline">
            Đăng nhập ngay
          </Link>
        </p>
      </div>
    </div>
  );
}
