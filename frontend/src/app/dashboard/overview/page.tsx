'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  fetchAdminStats,
  fetchAdminCommodities,
  fetchRecentPricesApi,
} from '@/lib/api';
import {
  AdminStats,
  AdminPriceItem,
} from '@/types';
import {
  Database,
  TrendingUp,
  Cpu,
  Layers,
  ArrowUpRight,
  Activity,
  RefreshCw,
  Clock,
  Sparkles,
  Server,
} from 'lucide-react';

interface CommodityItem {
  id: number;
  code: string;
  name: string;
  category: string;
  unit: string;
  region: string;
}

export default function DashboardOverviewPage() {
  const [stats, setStats] = useState<AdminStats>({
    totalCommodities: 4,
    totalPriceRecords: 6420,
    totalForecastRecords: 120,
    totalAlertRules: 4,
    latestPriceDate: '2026-09-05',
    systemStatus: 'ONLINE',
  });
  const [recentPrices, setRecentPrices] = useState<AdminPriceItem[]>([]);
  const [commodities, setCommodities] = useState<CommodityItem[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    setLoading(true);
    try {
      const [sData, pData, cData] = await Promise.all([
        fetchAdminStats(),
        fetchRecentPricesApi(),
        fetchAdminCommodities(),
      ]);
      setStats(sData);
      setRecentPrices(pData.slice(0, 8));
      setCommodities(cData);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      {/* Page Title & Quick Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-border-subtle">
        <div>
          <h1 className="text-2xl font-bold text-primary-text flex items-center gap-2.5">
            <Activity className="w-6 h-6 text-brand" />
            Tổng Quan Hệ Thống (System Overview)
          </h1>
          <p className="text-sm text-secondary-text mt-1">
            Giám sát thời gian thực số lượng dữ liệu, mô hình dự báo và tình trạng máy chủ
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={loadData}
            disabled={loading}
            className="px-3.5 py-2 rounded-xl bg-card hover:bg-canvas text-secondary-text border border-border-subtle text-xs font-semibold flex items-center gap-2 transition shadow-xs"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            Làm mới dữ liệu
          </button>
          <Link
            href="/dashboard/data-control"
            className="px-3.5 py-2 rounded-xl bg-brand hover:bg-brand-hover text-white text-xs font-semibold flex items-center gap-1.5 shadow-xs transition"
          >
            <Database className="w-3.5 h-3.5" />
            Điều khiển Bot cào
          </Link>
        </div>
      </div>

      {/* 4 Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Hàng hóa */}
        <div className="p-5 rounded-2xl bg-card border border-border-subtle shadow-xs relative overflow-hidden group hover:border-brand/40 transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-secondary-text">Nông Sản Theo Dõi</span>
            <div className="p-2.5 rounded-xl bg-brand-light text-brand border border-brand/20">
              <Layers className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-3xl font-bold text-primary-text">{stats.totalCommodities}</div>
            <div className="text-xs text-brand flex items-center gap-1 mt-1 font-medium">
              <span>Đang hoạt động trên sàn</span>
            </div>
          </div>
        </div>

        {/* Card 2: Tổng bản ghi */}
        <div className="p-5 rounded-2xl bg-card border border-border-subtle shadow-xs relative overflow-hidden group hover:border-brand/40 transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-secondary-text">Lịch Sử Giá Đã Lưu</span>
            <div className="p-2.5 rounded-xl bg-amber-50 text-amber-700 border border-amber-200">
              <Database className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-3xl font-bold text-primary-text">{stats.totalPriceRecords.toLocaleString('vi-VN')}</div>
            <div className="text-xs text-secondary-text flex items-center gap-1 mt-1">
              <span>Cập nhật ngày: {stats.latestPriceDate || '2026-09-05'}</span>
            </div>
          </div>
        </div>

        {/* Card 3: Dự báo AI */}
        <div className="p-5 rounded-2xl bg-card border border-border-subtle shadow-xs relative overflow-hidden group hover:border-purple-300 transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-secondary-text">Điểm Dự Báo AI</span>
            <div className="p-2.5 rounded-xl bg-purple-50 text-purple-700 border border-purple-200">
              <Cpu className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-3xl font-bold text-primary-text">{stats.totalForecastRecords}</div>
            <div className="text-xs text-purple-700 flex items-center gap-1 mt-1 font-medium">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Prophet / XGBoost / LSTM</span>
            </div>
          </div>
        </div>

        {/* Card 4: Trạng thái Server */}
        <div className="p-5 rounded-2xl bg-card border border-border-subtle shadow-xs relative overflow-hidden group hover:border-blue-300 transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-secondary-text">Trạng Thái Hệ Thống</span>
            <div className="p-2.5 rounded-xl bg-blue-50 text-blue-700 border border-blue-200">
              <Server className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-bold text-emerald-700 flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-emerald-500 animate-ping" />
              {stats.systemStatus}
            </div>
            <div className="text-xs text-secondary-text flex items-center gap-1 mt-1 font-mono">
              <span>FastAPI & PostgreSQL OK</span>
            </div>
          </div>
        </div>
      </div>

      {/* Market Commodity Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Danh mục hàng hóa */}
        <div className="lg:col-span-2 space-y-4">
          <div className="p-6 rounded-2xl bg-card border border-border-subtle shadow-xs">
            <div className="flex items-center justify-between pb-4 border-b border-border-subtle">
              <div className="font-semibold text-primary-text flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-brand" />
                Danh Mục Nông Sản & Vùng Miền Trọng Điểm
              </div>
              <span className="text-xs text-secondary-text font-medium">{commodities.length} mặt hàng</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-4">
              {commodities.map((c) => (
                <div
                  key={c.id}
                  className="p-4 rounded-xl bg-canvas border border-border-subtle hover:border-brand/40 transition space-y-2"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="font-semibold text-primary-text text-sm">{c.name}</div>
                      <div className="text-xs font-mono text-brand font-medium mt-0.5">{c.code}</div>
                    </div>
                    <span className="text-[11px] px-2 py-0.5 rounded-md bg-card text-secondary-text border border-border-subtle font-medium">
                      {c.unit}
                    </span>
                  </div>
                  <div className="text-xs text-secondary-text">
                    <span className="text-secondary-text/70">Vùng:</span> {c.region}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Quick Links Card */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <Link
              href="/dashboard/data-control"
              className="p-4 rounded-xl bg-card border border-border-subtle hover:border-brand/40 shadow-xs transition group"
            >
              <div className="text-sm font-semibold text-primary-text group-hover:text-brand flex items-center justify-between">
                <span>Quản Lý Cào Dữ Liệu</span>
                <ArrowUpRight className="w-4 h-4 text-secondary-text group-hover:text-brand transition" />
              </div>
              <p className="text-xs text-secondary-text mt-1">Cào tự động, xem logs và upload file CSV</p>
            </Link>

            <Link
              href="/dashboard/ml-models"
              className="p-4 rounded-xl bg-card border border-border-subtle hover:border-brand/40 shadow-xs transition group"
            >
              <div className="text-sm font-semibold text-primary-text group-hover:text-brand flex items-center justify-between">
                <span>Machine Learning</span>
                <ArrowUpRight className="w-4 h-4 text-secondary-text group-hover:text-brand transition" />
              </div>
              <p className="text-xs text-secondary-text mt-1">So sánh RMSE, Retrain và Model Switcher</p>
            </Link>

            <Link
              href="/dashboard/users"
              className="p-4 rounded-xl bg-card border border-border-subtle hover:border-brand/40 shadow-xs transition group"
            >
              <div className="text-sm font-semibold text-primary-text group-hover:text-brand flex items-center justify-between">
                <span>Quản Lý Người Dùng</span>
                <ArrowUpRight className="w-4 h-4 text-secondary-text group-hover:text-brand transition" />
              </div>
              <p className="text-xs text-secondary-text mt-1">Phân quyền Admin/Analyst và cấp tài khoản</p>
            </Link>
          </div>
        </div>

        {/* Right 1 Col: Điểm giá mới cập nhật */}
        <div className="p-6 rounded-2xl bg-card border border-border-subtle shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
              <span className="font-semibold text-primary-text text-sm flex items-center gap-2">
                <Clock className="w-4 h-4 text-amber-600" />
                Dữ Liệu Giá Mới Nhất
              </span>
              <span className="text-[11px] font-medium text-brand px-1.5 py-0.5 rounded bg-brand-light">Live DB</span>
            </div>

            <div className="divide-y divide-border-subtle mt-3">
              {recentPrices.map((p) => (
                <div key={p.id} className="py-2.5 flex items-center justify-between text-xs">
                  <div>
                    <div className="font-medium text-primary-text">{p.commodityName}</div>
                    <div className="text-[11px] text-secondary-text">{p.recordDate}</div>
                  </div>
                  <div className="text-right">
                    <div className="font-semibold text-brand font-mono">
                      {p.price.toLocaleString('vi-VN')} đ
                    </div>
                    <div className="text-[10px] text-secondary-text truncate max-w-[120px]">
                      {p.source || 'Sở NN&PTNT'}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="pt-4 border-t border-border-subtle mt-4">
            <Link
              href="/dashboard/data-control"
              className="w-full py-2.5 rounded-xl bg-canvas hover:bg-[#EFECE6] text-primary-text text-xs font-semibold flex items-center justify-center gap-1.5 transition border border-border-subtle"
            >
              Xem toàn bộ dữ liệu giá
              <ArrowUpRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
