'use client';

import React, { useState, useEffect } from 'react';
import Header from '@/components/layout/Header';
import { getUser, User } from '@/lib/auth';
import {
  AdminStats,
  AdminPriceItem,
  AdminUserItem,
  TaskRunResult,
} from '@/types';
import {
  fetchAdminStats,
  fetchAdminCommodities,
  createCommodityApi,
  updateCommodityApi,
  deleteCommodityApi,
  fetchRecentPricesApi,
  createOrUpdatePriceApi,
  deletePriceRecordApi,
  triggerScrapeTaskApi,
  triggerRetrainTaskApi,
  fetchAdminUsersApi,
  createAdminUserApi,
} from '@/lib/api';
import {
  ShieldAlert,
  Database,
  TrendingUp,
  Cpu,
  Users,
  Plus,
  Trash2,
  Edit2,
  RefreshCw,
  CheckCircle2,
  AlertCircle,
  Clock,
  Layers,
  Sparkles,
  Server,
  Activity,
  ArrowUpRight,
  Filter,
} from 'lucide-react';
import Link from 'next/link';

type TabType = 'overview' | 'commodities' | 'prices' | 'pipeline' | 'users';

interface CommodityItem {
  id: number;
  code: string;
  name: string;
  category: string;
  unit: string;
  region: string;
  description?: string | null;
}

export default function AdminPage() {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [activeTab, setActiveTab] = useState<TabType>('overview');
  const [toastMessage, setToastMessage] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  // Stats
  const [stats, setStats] = useState<AdminStats>({
    totalCommodities: 4,
    totalPriceRecords: 6420,
    totalForecastRecords: 120,
    totalAlertRules: 4,
    latestPriceDate: '2026-08-28',
    systemStatus: 'ONLINE',
  });

  // Commodities state
  const [commodities, setCommodities] = useState<CommodityItem[]>([]);
  const [commodityModalOpen, setCommodityModalOpen] = useState(false);
  const [editingCommodity, setEditingCommodity] = useState<CommodityItem | null>(null);
  const [commodityForm, setCommodityForm] = useState({
    code: '',
    name: '',
    category: 'Lương thực',
    unit: 'VNĐ/kg',
    region: '',
    description: '',
  });

  // Price state
  const [prices, setPrices] = useState<AdminPriceItem[]>([]);
  const [selectedCommodityFilter, setSelectedCommodityFilter] = useState<number | undefined>(undefined);
  const [priceForm, setPriceForm] = useState({
    commodity_id: 2,
    record_date: new Date().toISOString().split('T')[0],
    price: '',
    price_min: '',
    price_max: '',
    volume: '15000',
    source: 'Cập nhật thủ công bởi Admin',
  });

  // Pipeline tasks
  const [isScraping, setIsScraping] = useState(false);
  const [isRetraining, setIsRetraining] = useState(false);
  const [scrapeDays, setScrapeDays] = useState(30);
  const [retrainCommodityId, setRetrainCommodityId] = useState<number | undefined>(undefined);
  const [taskLogs, setTaskLogs] = useState<TaskRunResult[]>([]);

  // Users state
  const [users, setUsers] = useState<AdminUserItem[]>([]);
  const [userModalOpen, setUserModalOpen] = useState(false);
  const [userForm, setUserForm] = useState({
    email: '',
    full_name: '',
    password: '',
    role: 'analyst',
  });

  // Notification helper
  const showToast = (text: string, type: 'success' | 'error' = 'success') => {
    setToastMessage({ text, type });
    setTimeout(() => setToastMessage(null), 4000);
  };

  // Initial load
  useEffect(() => {
    const u = getUser();
    setCurrentUser(u);
    loadAllData();
  }, []);

  const loadAllData = async () => {
    try {
      const [s, c, p, usr] = await Promise.all([
        fetchAdminStats(),
        fetchAdminCommodities(),
        fetchRecentPricesApi(),
        fetchAdminUsersApi(),
      ]);
      setStats(s);
      setCommodities(c);
      setPrices(p);
      setUsers(usr);
    } catch (err) {
      console.error('Error loading admin data:', err);
    }
  };

  // --- Handlers: Commodity ---
  const handleOpenCreateCommodity = () => {
    setEditingCommodity(null);
    setCommodityForm({
      code: '',
      name: '',
      category: 'Lương thực',
      unit: 'VNĐ/kg',
      region: '',
      description: '',
    });
    setCommodityModalOpen(true);
  };

  const handleOpenEditCommodity = (com: CommodityItem) => {
    setEditingCommodity(com);
    setCommodityForm({
      code: com.code,
      name: com.name,
      category: com.category,
      unit: com.unit,
      region: com.region,
      description: com.description || '',
    });
    setCommodityModalOpen(true);
  };

  const handleSaveCommodity = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingCommodity) {
        await updateCommodityApi(editingCommodity.id, commodityForm);
        showToast(`Đã cập nhật nông sản "${commodityForm.name}" thành công!`);
      } else {
        await createCommodityApi(commodityForm);
        showToast(`Đã thêm mới nông sản "${commodityForm.name}" thành công!`);
      }
      setCommodityModalOpen(false);
      const c = await fetchAdminCommodities();
      setCommodities(c);
      const s = await fetchAdminStats();
      setStats(s);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Lỗi khi lưu nông sản';
      showToast(msg, 'error');
    }
  };

  const handleDeleteCommodity = async (id: number, name: string) => {
    if (!confirm(`Bạn có chắc chắn muốn xóa nông sản "${name}" và toàn bộ dữ liệu liên quan?`)) return;
    try {
      await deleteCommodityApi(id);
      setCommodities((prev) => prev.filter((c) => c.id !== id));
      showToast(`Đã xóa nông sản "${name}"!`);
      const s = await fetchAdminStats();
      setStats(s);
    } catch {
      showToast('Không thể xóa nông sản', 'error');
    }
  };

  // --- Handlers: Price ---
  const handleSavePrice = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const priceNum = parseFloat(priceForm.price);
      if (isNaN(priceNum) || priceNum <= 0) {
        showToast('Vui lòng nhập giá hợp lệ', 'error');
        return;
      }

      await createOrUpdatePriceApi({
        commodity_id: Number(priceForm.commodity_id),
        record_date: priceForm.record_date,
        price: priceNum,
        price_min: priceForm.price_min ? parseFloat(priceForm.price_min) : undefined,
        price_max: priceForm.price_max ? parseFloat(priceForm.price_max) : undefined,
        volume: priceForm.volume ? parseFloat(priceForm.volume) : undefined,
        source: priceForm.source,
      });

      showToast('Đã lưu điểm giá thành công!');
      const p = await fetchRecentPricesApi(selectedCommodityFilter);
      setPrices(p);
      const s = await fetchAdminStats();
      setStats(s);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Lỗi khi lưu giá';
      showToast(msg, 'error');
    }
  };

  const handleDeletePrice = async (id: number) => {
    if (!confirm('Bạn có chắc muốn xóa bản ghi giá này?')) return;
    try {
      await deletePriceRecordApi(id);
      setPrices((prev) => prev.filter((p) => p.id !== id));
      showToast('Đã xóa bản ghi giá thành công!');
    } catch {
      showToast('Không thể xóa bản ghi giá', 'error');
    }
  };

  const handleFilterCommodityChange = async (cid?: number) => {
    setSelectedCommodityFilter(cid);
    const p = await fetchRecentPricesApi(cid);
    setPrices(p);
  };

  // --- Handlers: Pipeline Tasks ---
  const handleTriggerScrape = async () => {
    setIsScraping(true);
    try {
      const result = await triggerScrapeTaskApi(scrapeDays);
      setTaskLogs((prev) => [result, ...prev]);
      showToast(result.message);
      // Reload stats after triggering
      setTimeout(async () => {
        const s = await fetchAdminStats();
        setStats(s);
        const p = await fetchRecentPricesApi();
        setPrices(p);
      }, 3000);
    } catch {
      showToast('Kích hoạt cào dữ liệu thất bại', 'error');
    } finally {
      setIsScraping(false);
    }
  };

  const handleTriggerRetrain = async () => {
    setIsRetraining(true);
    try {
      const result = await triggerRetrainTaskApi(retrainCommodityId);
      setTaskLogs((prev) => [result, ...prev]);
      showToast(result.message);
      setTimeout(async () => {
        const s = await fetchAdminStats();
        setStats(s);
      }, 3000);
    } catch {
      showToast('Kích hoạt re-train thất bại', 'error');
    } finally {
      setIsRetraining(false);
    }
  };

  // --- Handlers: Users ---
  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const created = await createAdminUserApi(userForm);
      setUsers((prev) => [...prev, created]);
      showToast(`Đã tạo tài khoản "${created.email}" thành công!`);
      setUserModalOpen(false);
      setUserForm({ email: '', full_name: '', password: '', role: 'analyst' });
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Lỗi khi tạo người dùng';
      showToast(msg, 'error');
    }
  };

  // Check role: Must be admin
  const isUnauthorized = currentUser && currentUser.role !== 'admin';

  if (isUnauthorized) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center">
        <div className="max-w-md w-full bg-card rounded-2xl border border-border-subtle p-8 text-center shadow-card">
          <div className="w-16 h-16 rounded-full bg-rose-500/10 text-rose-600 flex items-center justify-center mx-auto mb-4">
            <ShieldAlert className="w-8 h-8" />
          </div>
          <h2 className="text-xl font-bold text-primary-text mb-2">Quyền Truy Cập Bị Từ Chối</h2>
          <p className="text-sm text-secondary-text mb-6">
            Trang Quản trị dữ liệu chỉ dành cho tài khoản có vai trò <strong>Quản trị viên (Admin)</strong>. Tài khoản hiện tại của bạn là <strong>{currentUser?.role}</strong> ({currentUser?.email}).
          </p>
          <div className="space-y-3">
            <Link
              href="/"
              className="block w-full py-2.5 px-4 rounded-xl bg-brand text-white font-bold text-sm shadow-sm hover:bg-brand/90 transition-all"
            >
              Quay lại Bảng điều khiển
            </Link>
            <Link
              href="/login"
              className="block w-full py-2.5 px-4 rounded-xl border border-border-subtle bg-canvas text-secondary-text font-bold text-sm hover:text-primary-text transition-all"
            >
              Đăng nhập lại với tài khoản Admin (admin@agroforecast.vn)
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-7 pb-12">
      {/* Header */}
      <Header
        title="Quản trị Hệ thống & Dữ liệu"
        subtitle="Phân hệ Quản trị viên (Admin Portal) · Cấu hình dữ liệu, Điều phối AI & Vận hành"
        showLiveBadge={true}
      />

      {/* Toast Notification */}
      {toastMessage && (
        <div className={`fixed bottom-6 right-6 z-50 flex items-center gap-3 px-5 py-3.5 rounded-2xl shadow-xl border text-sm font-semibold transition-all duration-300 animate-in fade-in slide-in-from-bottom-3 ${
          toastMessage.type === 'success' 
            ? 'bg-emerald-900/90 text-white border-emerald-700/50 backdrop-blur-md' 
            : 'bg-rose-900/90 text-white border-rose-700/50 backdrop-blur-md'
        }`}>
          {toastMessage.type === 'success' ? (
            <CheckCircle2 className="w-5 h-5 text-emerald-300 shrink-0" />
          ) : (
            <AlertCircle className="w-5 h-5 text-rose-300 shrink-0" />
          )}
          <span>{toastMessage.text}</span>
        </div>
      )}

      {/* Quick KPI Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-card rounded-2xl border border-border-subtle p-5 shadow-card relative overflow-hidden group hover:border-brand/40 transition-all">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-bold text-secondary-text uppercase tracking-wider">Danh mục Nông sản</span>
            <div className="w-8 h-8 rounded-xl bg-amber-500/10 text-amber-600 flex items-center justify-center">
              <Layers className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-black text-primary-text">{stats.totalCommodities}</span>
            <span className="text-xs font-bold text-emerald-600 bg-emerald-500/10 px-2 py-0.5 rounded-md">Hoạt động</span>
          </div>
          <p className="text-[11px] text-secondary-text mt-2 flex items-center gap-1">
            <Clock className="w-3 h-3 text-secondary-text/70" /> Lúa gạo, Cà phê, Hồ tiêu, Mía
          </p>
        </div>

        <div className="bg-card rounded-2xl border border-border-subtle p-5 shadow-card relative overflow-hidden group hover:border-brand/40 transition-all">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-bold text-secondary-text uppercase tracking-wider">Lịch sử Điểm giá</span>
            <div className="w-8 h-8 rounded-xl bg-blue-500/10 text-blue-600 flex items-center justify-center">
              <Database className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-black text-primary-text">{stats.totalPriceRecords.toLocaleString('vi-VN')}</span>
            <span className="text-xs font-semibold text-secondary-text">bản ghi</span>
          </div>
          <p className="text-[11px] text-secondary-text mt-2 flex items-center gap-1">
            Mới nhất: <strong className="text-primary-text">{stats.latestPriceDate || '28/08/2026'}</strong>
          </p>
        </div>

        <div className="bg-card rounded-2xl border border-border-subtle p-5 shadow-card relative overflow-hidden group hover:border-brand/40 transition-all">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-bold text-secondary-text uppercase tracking-wider">Mô hình & Dự báo AI</span>
            <div className="w-8 h-8 rounded-xl bg-purple-500/10 text-purple-600 flex items-center justify-center">
              <Cpu className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-black text-primary-text">{stats.totalForecastRecords}</span>
            <span className="text-xs font-bold text-purple-600 bg-purple-500/10 px-2 py-0.5 rounded-md">5 Thuật toán</span>
          </div>
          <p className="text-[11px] text-secondary-text mt-2">LSTM, Prophet, XGBoost, RF, ARIMA</p>
        </div>

        <div className="bg-card rounded-2xl border border-border-subtle p-5 shadow-card relative overflow-hidden group hover:border-brand/40 transition-all">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-bold text-secondary-text uppercase tracking-wider">Trạng thái Hệ thống</span>
            <div className="w-8 h-8 rounded-xl bg-emerald-500/10 text-emerald-600 flex items-center justify-center">
              <Activity className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-black text-emerald-600 flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
              SẴN SÀNG
            </span>
          </div>
          <p className="text-[11px] text-secondary-text mt-2">API, CSDL & Background Runner ổn định</p>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-border-subtle pb-px overflow-x-auto custom-scrollbar">
        <button
          onClick={() => setActiveTab('overview')}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-t-xl text-xs font-bold transition-all border-b-2 whitespace-nowrap ${
            activeTab === 'overview'
              ? 'border-brand text-brand bg-brand/5'
              : 'border-transparent text-secondary-text hover:text-primary-text hover:bg-black/[0.02]'
          }`}
        >
          <Server className="w-4 h-4" />
          Tổng quan & Vận hành
        </button>

        <button
          onClick={() => setActiveTab('commodities')}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-t-xl text-xs font-bold transition-all border-b-2 whitespace-nowrap ${
            activeTab === 'commodities'
              ? 'border-brand text-brand bg-brand/5'
              : 'border-transparent text-secondary-text hover:text-primary-text hover:bg-black/[0.02]'
          }`}
        >
          <Layers className="w-4 h-4" />
          Danh mục Nông sản ({commodities.length})
        </button>

        <button
          onClick={() => setActiveTab('prices')}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-t-xl text-xs font-bold transition-all border-b-2 whitespace-nowrap ${
            activeTab === 'prices'
              ? 'border-brand text-brand bg-brand/5'
              : 'border-transparent text-secondary-text hover:text-primary-text hover:bg-black/[0.02]'
          }`}
        >
          <TrendingUp className="w-4 h-4" />
          Quản lý & Cập nhật Giá
        </button>

        <button
          onClick={() => setActiveTab('pipeline')}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-t-xl text-xs font-bold transition-all border-b-2 whitespace-nowrap ${
            activeTab === 'pipeline'
              ? 'border-brand text-brand bg-brand/5'
              : 'border-transparent text-secondary-text hover:text-primary-text hover:bg-black/[0.02]'
          }`}
        >
          <Cpu className="w-4 h-4" />
          Điều khiển AI & Thu thập dữ liệu
        </button>

        <button
          onClick={() => setActiveTab('users')}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-t-xl text-xs font-bold transition-all border-b-2 whitespace-nowrap ${
            activeTab === 'users'
              ? 'border-brand text-brand bg-brand/5'
              : 'border-transparent text-secondary-text hover:text-primary-text hover:bg-black/[0.02]'
          }`}
        >
          <Users className="w-4 h-4" />
          Người dùng & Phân quyền ({users.length})
        </button>
      </div>

      {/* TAB 1: OVERVIEW */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Quick Actions Card */}
          <div className="lg:col-span-2 bg-card rounded-2xl border border-border-subtle p-6 shadow-card space-y-5">
            <h3 className="text-base font-bold text-primary-text flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-brand" /> Thao tác Quản trị Nhanh
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <button
                onClick={handleOpenCreateCommodity}
                className="p-4 rounded-xl border border-border-subtle bg-canvas hover:border-brand/40 hover:bg-brand/5 transition-all text-left group"
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="w-9 h-9 rounded-xl bg-amber-500/10 text-amber-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <Plus className="w-5 h-5" />
                  </div>
                  <ArrowUpRight className="w-4 h-4 text-secondary-text group-hover:text-brand transition-colors" />
                </div>
                <h4 className="font-bold text-sm text-primary-text group-hover:text-brand transition-colors">Thêm Nông sản Mới</h4>
                <p className="text-xs text-secondary-text mt-1">Đăng ký mã hàng hóa, đơn vị và vùng canh tác</p>
              </button>

              <button
                onClick={() => setActiveTab('prices')}
                className="p-4 rounded-xl border border-border-subtle bg-canvas hover:border-brand/40 hover:bg-brand/5 transition-all text-left group"
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="w-9 h-9 rounded-xl bg-blue-500/10 text-blue-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <TrendingUp className="w-5 h-5" />
                  </div>
                  <ArrowUpRight className="w-4 h-4 text-secondary-text group-hover:text-brand transition-colors" />
                </div>
                <h4 className="font-bold text-sm text-primary-text group-hover:text-brand transition-colors">Cập nhật Giá Hôm nay</h4>
                <p className="text-xs text-secondary-text mt-1">Nhập giá đóng cửa, giá sàn và trần theo phiên</p>
              </button>

              <button
                onClick={() => setActiveTab('pipeline')}
                className="p-4 rounded-xl border border-border-subtle bg-canvas hover:border-brand/40 hover:bg-brand/5 transition-all text-left group"
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="w-9 h-9 rounded-xl bg-emerald-500/10 text-emerald-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <RefreshCw className="w-5 h-5" />
                  </div>
                  <ArrowUpRight className="w-4 h-4 text-secondary-text group-hover:text-brand transition-colors" />
                </div>
                <h4 className="font-bold text-sm text-primary-text group-hover:text-brand transition-colors">Kích hoạt Cào Dữ liệu</h4>
                <p className="text-xs text-secondary-text mt-1">Tự động lấy dữ liệu từ Yahoo Finance và hiệp hội</p>
              </button>

              <button
                onClick={() => setActiveTab('pipeline')}
                className="p-4 rounded-xl border border-border-subtle bg-canvas hover:border-brand/40 hover:bg-brand/5 transition-all text-left group"
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="w-9 h-9 rounded-xl bg-purple-500/10 text-purple-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <Cpu className="w-5 h-5" />
                  </div>
                  <ArrowUpRight className="w-4 h-4 text-secondary-text group-hover:text-brand transition-colors" />
                </div>
                <h4 className="font-bold text-sm text-primary-text group-hover:text-brand transition-colors">Huấn luyện lại AI</h4>
                <p className="text-xs text-secondary-text mt-1">Re-train LSTM, Prophet, XGBoost với dữ liệu mới</p>
              </button>
            </div>

            {/* Architecture Health Box */}
            <div className="mt-6 pt-5 border-t border-border-subtle space-y-3">
              <h4 className="text-xs font-bold text-secondary-text uppercase tracking-wider">Cấu hình Hệ thống Phục vụ Đồ án</h4>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                <div className="p-3 rounded-xl bg-canvas border border-border-subtle">
                  <span className="text-secondary-text block text-[11px]">Backend Framework</span>
                  <span className="font-bold text-primary-text mt-0.5 block">FastAPI 0.110</span>
                </div>
                <div className="p-3 rounded-xl bg-canvas border border-border-subtle">
                  <span className="text-secondary-text block text-[11px]">Cơ sở Dữ liệu</span>
                  <span className="font-bold text-primary-text mt-0.5 block">PostgreSQL 16</span>
                </div>
                <div className="p-3 rounded-xl bg-canvas border border-border-subtle">
                  <span className="text-secondary-text block text-[11px]">Mô hình Dự báo</span>
                  <span className="font-bold text-primary-text mt-0.5 block">Deep & ML Hybrid</span>
                </div>
                <div className="p-3 rounded-xl bg-canvas border border-border-subtle">
                  <span className="text-secondary-text block text-[11px]">Frontend</span>
                  <span className="font-bold text-primary-text mt-0.5 block">Next.js 14 App Router</span>
                </div>
              </div>
            </div>
          </div>

          {/* Activity Log / Status Sidebar */}
          <div className="bg-card rounded-2xl border border-border-subtle p-6 shadow-card space-y-4 flex flex-col justify-between">
            <div>
              <h3 className="text-base font-bold text-primary-text mb-1">Nhật ký Hoạt động</h3>
              <p className="text-xs text-secondary-text mb-4">Các sự kiện và lệnh thực thi gần nhất</p>

              <div className="space-y-3 text-xs">
                <div className="flex items-start gap-3 p-3 rounded-xl bg-canvas border border-border-subtle">
                  <span className="w-2 h-2 rounded-full bg-emerald-500 mt-1 shrink-0" />
                  <div>
                    <p className="font-bold text-primary-text">Hệ thống CSDL Khởi tạo</p>
                    <p className="text-secondary-text text-[11px] mt-0.5">Nạp thành công 6,400 bản ghi lịch sử giá từ 2022-2026</p>
                    <span className="text-[10px] text-secondary-text/70 mt-1 block">Hệ thống</span>
                  </div>
                </div>

                <div className="flex items-start gap-3 p-3 rounded-xl bg-canvas border border-border-subtle">
                  <span className="w-2 h-2 rounded-full bg-purple-500 mt-1 shrink-0" />
                  <div>
                    <p className="font-bold text-primary-text">Mô hình AI Đã Huấn luyện</p>
                    <p className="text-secondary-text text-[11px] mt-0.5">LSTM & XGBoost đạt MAPE 3.2% cho Cà phê Robusta</p>
                    <span className="text-[10px] text-secondary-text/70 mt-1 block">Pipeline</span>
                  </div>
                </div>

                <div className="flex items-start gap-3 p-3 rounded-xl bg-canvas border border-border-subtle">
                  <span className="w-2 h-2 rounded-full bg-blue-500 mt-1 shrink-0" />
                  <div>
                    <p className="font-bold text-primary-text">Quản trị viên đăng nhập</p>
                    <p className="text-secondary-text text-[11px] mt-0.5">{currentUser?.email || 'admin@agroforecast.vn'}</p>
                    <span className="text-[10px] text-secondary-text/70 mt-1 block">Hôm nay</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="pt-4 border-t border-border-subtle text-xs text-secondary-text">
              <span>Môi trường: </span>
              <strong className="text-primary-text">Development (Localhost)</strong>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: COMMODITIES */}
      {activeTab === 'commodities' && (
        <div className="bg-card rounded-2xl border border-border-subtle p-6 shadow-card space-y-5">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h3 className="text-base font-bold text-primary-text">Danh mục Nông sản Hệ thống</h3>
              <p className="text-xs text-secondary-text mt-0.5">Quản lý mã hàng hóa, phân loại, đơn vị niêm yết và xuất xứ vùng trồng</p>
            </div>
            <button
              onClick={handleOpenCreateCommodity}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-brand text-white text-xs font-bold hover:bg-brand/90 transition-all shadow-sm shrink-0"
            >
              <Plus className="w-4 h-4" /> Thêm Nông sản
            </button>
          </div>

          <div className="overflow-x-auto custom-scrollbar">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="border-b border-border-subtle text-secondary-text font-bold uppercase tracking-wider text-[11px]">
                  <th className="py-3 px-4">ID / Mã Code</th>
                  <th className="py-3 px-4">Tên Nông sản</th>
                  <th className="py-3 px-4">Phân loại</th>
                  <th className="py-3 px-4">Đơn vị</th>
                  <th className="py-3 px-4">Vùng canh tác</th>
                  <th className="py-3 px-4 text-right">Thao tác</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-subtle/60">
                {commodities.map((c) => (
                  <tr key={c.id} className="hover:bg-black/[0.01] transition-colors">
                    <td className="py-3.5 px-4 font-mono font-bold text-brand">
                      {c.code}
                      <span className="text-[10px] text-secondary-text/70 block">ID: #{c.id}</span>
                    </td>
                    <td className="py-3.5 px-4 font-bold text-primary-text text-sm">
                      {c.name}
                      {c.description && <span className="text-xs font-normal text-secondary-text block line-clamp-1">{c.description}</span>}
                    </td>
                    <td className="py-3.5 px-4">
                      <span className="px-2.5 py-1 rounded-md bg-canvas border border-border-subtle font-semibold text-secondary-text">
                        {c.category}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 font-semibold text-primary-text">{c.unit}</td>
                    <td className="py-3.5 px-4 text-secondary-text">{c.region}</td>
                    <td className="py-3.5 px-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleOpenEditCommodity(c)}
                          className="p-1.5 rounded-lg border border-border-subtle hover:bg-black/5 text-secondary-text hover:text-brand transition-all"
                          title="Chỉnh sửa"
                        >
                          <Edit2 className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => handleDeleteCommodity(c.id, c.name)}
                          className="p-1.5 rounded-lg border border-border-subtle hover:bg-rose-500/10 text-secondary-text hover:text-rose-600 transition-all"
                          title="Xóa nông sản"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 3: PRICES */}
      {activeTab === 'prices' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Quick Price Entry Form */}
          <div className="bg-card rounded-2xl border border-border-subtle p-6 shadow-card space-y-4">
            <h3 className="text-base font-bold text-primary-text flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-brand" /> Cập nhật Điểm Giá Mới
            </h3>
            <p className="text-xs text-secondary-text">Nhập thủ công dữ liệu giao dịch thị trường hàng ngày</p>

            <form onSubmit={handleSavePrice} className="space-y-3.5 text-xs">
              <div>
                <label className="font-bold text-secondary-text block mb-1">Chọn Nông sản</label>
                <select
                  value={priceForm.commodity_id}
                  onChange={(e) => setPriceForm({ ...priceForm, commodity_id: Number(e.target.value) })}
                  className="w-full px-3 py-2 rounded-xl bg-canvas border border-border-subtle font-semibold text-primary-text focus:outline-none focus:border-brand"
                >
                  {commodities.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name} ({c.unit})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="font-bold text-secondary-text block mb-1">Ngày ghi nhận</label>
                <input
                  type="date"
                  value={priceForm.record_date}
                  onChange={(e) => setPriceForm({ ...priceForm, record_date: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-canvas border border-border-subtle font-semibold text-primary-text focus:outline-none focus:border-brand"
                  required
                />
              </div>

              <div>
                <label className="font-bold text-secondary-text block mb-1">Mức giá đóng cửa / trung bình</label>
                <input
                  type="number"
                  placeholder="Ví dụ: 62500"
                  value={priceForm.price}
                  onChange={(e) => setPriceForm({ ...priceForm, price: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-canvas border border-border-subtle font-semibold text-primary-text focus:outline-none focus:border-brand text-sm"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-bold text-secondary-text block mb-1">Giá thấp nhất (Sàn)</label>
                  <input
                    type="number"
                    placeholder="Không bắt buộc"
                    value={priceForm.price_min}
                    onChange={(e) => setPriceForm({ ...priceForm, price_min: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-canvas border border-border-subtle font-semibold text-primary-text focus:outline-none focus:border-brand"
                  />
                </div>
                <div>
                  <label className="font-bold text-secondary-text block mb-1">Giá cao nhất (Trần)</label>
                  <input
                    type="number"
                    placeholder="Không bắt buộc"
                    value={priceForm.price_max}
                    onChange={(e) => setPriceForm({ ...priceForm, price_max: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-canvas border border-border-subtle font-semibold text-primary-text focus:outline-none focus:border-brand"
                  />
                </div>
              </div>

              <div>
                <label className="font-bold text-secondary-text block mb-1">Sản lượng giao dịch ước tính</label>
                <input
                  type="number"
                  placeholder="Sản lượng (kg/tấn)"
                  value={priceForm.volume}
                  onChange={(e) => setPriceForm({ ...priceForm, volume: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-canvas border border-border-subtle font-semibold text-primary-text focus:outline-none focus:border-brand"
                />
              </div>

              <div>
                <label className="font-bold text-secondary-text block mb-1">Nguồn dữ liệu / Ghi chú</label>
                <input
                  type="text"
                  value={priceForm.source}
                  onChange={(e) => setPriceForm({ ...priceForm, source: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-canvas border border-border-subtle font-semibold text-primary-text focus:outline-none focus:border-brand"
                />
              </div>

              <button
                type="submit"
                className="w-full py-2.5 rounded-xl bg-brand text-white font-bold text-xs hover:bg-brand/90 transition-all shadow-sm mt-2"
              >
                Lưu Điểm Giá
              </button>
            </form>
          </div>

          {/* Recent Price Records Table */}
          <div className="lg:col-span-2 bg-card rounded-2xl border border-border-subtle p-6 shadow-card space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h3 className="text-base font-bold text-primary-text">Bản ghi Giá Gần đây</h3>
                <p className="text-xs text-secondary-text">Các điểm dữ liệu giá mới nhất được lưu trong hệ thống</p>
              </div>

              {/* Filter */}
              <div className="flex items-center gap-2">
                <Filter className="w-3.5 h-3.5 text-secondary-text" />
                <select
                  value={selectedCommodityFilter ?? ''}
                  onChange={(e) => handleFilterCommodityChange(e.target.value ? Number(e.target.value) : undefined)}
                  className="px-2.5 py-1.5 rounded-lg bg-canvas border border-border-subtle text-xs font-semibold text-secondary-text focus:outline-none focus:border-brand"
                >
                  <option value="">Tất cả nông sản</option>
                  {commodities.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="overflow-x-auto custom-scrollbar max-h-[500px]">
              <table className="w-full text-left border-collapse text-xs">
                <thead className="sticky top-0 bg-card z-10">
                  <tr className="border-b border-border-subtle text-secondary-text font-bold uppercase tracking-wider text-[11px]">
                    <th className="py-2.5 px-3">Ngày</th>
                    <th className="py-2.5 px-3">Nông sản</th>
                    <th className="py-2.5 px-3">Giá ghi nhận</th>
                    <th className="py-2.5 px-3">Biên độ (Min - Max)</th>
                    <th className="py-2.5 px-3">Nguồn dữ liệu</th>
                    <th className="py-2.5 px-3 text-right">Xóa</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border-subtle/60">
                  {prices.map((p) => (
                    <tr key={p.id} className="hover:bg-black/[0.01] transition-colors">
                      <td className="py-2.5 px-3 font-semibold text-primary-text">{p.recordDate}</td>
                      <td className="py-2.5 px-3 font-bold text-brand">{p.commodityName}</td>
                      <td className="py-2.5 px-3 font-bold text-primary-text text-sm">
                        {p.price.toLocaleString('vi-VN')}
                      </td>
                      <td className="py-2.5 px-3 text-secondary-text">
                        {p.priceMin && p.priceMax
                          ? `${p.priceMin.toLocaleString('vi-VN')} - ${p.priceMax.toLocaleString('vi-VN')}`
                          : '—'}
                      </td>
                      <td className="py-2.5 px-3 text-secondary-text text-[11px] truncate max-w-[150px]" title={p.source || ''}>
                        {p.source || 'Hệ thống'}
                      </td>
                      <td className="py-2.5 px-3 text-right">
                        <button
                          onClick={() => handleDeletePrice(p.id)}
                          className="p-1 rounded-md text-secondary-text hover:text-rose-600 hover:bg-rose-500/10 transition-all"
                          title="Xóa điểm giá"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* TAB 4: AI & PIPELINE RUNNER */}
      {activeTab === 'pipeline' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Card: Scraper Trigger */}
          <div className="bg-card rounded-2xl border border-border-subtle p-6 shadow-card space-y-5 flex flex-col justify-between">
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-600 flex items-center justify-center">
                  <RefreshCw className={`w-5 h-5 ${isScraping ? 'animate-spin' : ''}`} />
                </div>
                <div>
                  <h3 className="text-base font-bold text-primary-text">Cào Dữ liệu Thị trường Tự động</h3>
                  <p className="text-xs text-secondary-text">Yahoo Finance API & Bộ sinh dữ liệu chuỗi thời gian</p>
                </div>
              </div>

              <p className="text-xs text-secondary-text leading-relaxed">
                Tác vụ sẽ truy vấn các mã nông sản quốc tế tương đương (Rough Rice ZR=F, Robusta Coffee RC=F, Sugar SB=F) và quy đổi sang đơn vị tiền tệ VNĐ để nạp vào CSDL.
              </p>

              <div>
                <label className="font-bold text-xs text-secondary-text block mb-1.5">Khoảng thời gian thu thập</label>
                <select
                  value={scrapeDays}
                  onChange={(e) => setScrapeDays(Number(e.target.value))}
                  className="w-full px-3 py-2 rounded-xl bg-canvas border border-border-subtle font-semibold text-xs text-primary-text focus:outline-none focus:border-brand"
                >
                  <option value={7}>7 ngày gần nhất (Cập nhật phiên nhanh)</option>
                  <option value={30}>30 ngày gần nhất (Khuyến nghị)</option>
                  <option value={90}>90 ngày gần nhất (3 tháng)</option>
                  <option value={365}>365 ngày (1 năm)</option>
                  <option value={1600}>1,600 ngày (Toàn bộ lịch sử đồ án ~4.3 năm)</option>
                </select>
              </div>
            </div>

            <button
              onClick={handleTriggerScrape}
              disabled={isScraping}
              className="w-full py-3 rounded-xl bg-emerald-700 text-white font-bold text-xs hover:bg-emerald-800 disabled:opacity-50 transition-all flex items-center justify-center gap-2 shadow-sm"
            >
              {isScraping ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" /> Đang cào dữ liệu từ Yahoo Finance...
                </>
              ) : (
                <>
                  <RefreshCw className="w-4 h-4" /> Kích hoạt Cào Dữ liệu Ngay
                </>
              )}
            </button>
          </div>

          {/* Card: Retrain Trigger */}
          <div className="bg-card rounded-2xl border border-border-subtle p-6 shadow-card space-y-5 flex flex-col justify-between">
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-purple-500/10 text-purple-600 flex items-center justify-center">
                  <Cpu className={`w-5 h-5 ${isRetraining ? 'animate-spin' : ''}`} />
                </div>
                <div>
                  <h3 className="text-base font-bold text-primary-text">Huấn luyện lại Mô hình AI</h3>
                  <p className="text-xs text-secondary-text">Machine Learning & Deep Learning Pipeline</p>
                </div>
              </div>

              <p className="text-xs text-secondary-text leading-relaxed">
                Huấn luyện lại thuật toán <strong>LSTM, XGBoost, Random Forest, Facebook Prophet, ARIMA</strong> với dữ liệu giá mới nhất. Tự động tính toán lại sai số MAE, RMSE, MAPE, $R^2$ và dải tin cậy 95%.
              </p>

              <div>
                <label className="font-bold text-xs text-secondary-text block mb-1.5">Phạm vi Nông sản áp dụng</label>
                <select
                  value={retrainCommodityId ?? ''}
                  onChange={(e) => setRetrainCommodityId(e.target.value ? Number(e.target.value) : undefined)}
                  className="w-full px-3 py-2 rounded-xl bg-canvas border border-border-subtle font-semibold text-xs text-primary-text focus:outline-none focus:border-brand"
                >
                  <option value="">Tất cả 4 mặt hàng nông sản (Khuyến nghị)</option>
                  {commodities.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <button
              onClick={handleTriggerRetrain}
              disabled={isRetraining}
              className="w-full py-3 rounded-xl bg-purple-700 text-white font-bold text-xs hover:bg-purple-800 disabled:opacity-50 transition-all flex items-center justify-center gap-2 shadow-sm"
            >
              {isRetraining ? (
                <>
                  <Cpu className="w-4 h-4 animate-spin" /> Đang huấn luyện lại các mô hình AI...
                </>
              ) : (
                <>
                  <Cpu className="w-4 h-4" /> Kích hoạt Huấn luyện lại Mô hình
                </>
              )}
            </button>
          </div>

          {/* Execution Log list if any */}
          {taskLogs.length > 0 && (
            <div className="lg:col-span-2 bg-card rounded-2xl border border-border-subtle p-6 shadow-card space-y-3">
              <h4 className="text-sm font-bold text-primary-text flex items-center gap-2">
                <Activity className="w-4 h-4 text-brand" /> Kết quả Thực thi Tác vụ Vừa kích hoạt
              </h4>
              <div className="space-y-2 text-xs">
                {taskLogs.map((log, i) => (
                  <div key={i} className="p-3 rounded-xl bg-canvas border border-border-subtle flex items-center justify-between">
                    <div>
                      <span className="font-bold text-primary-text">{log.taskName}</span>
                      <p className="text-secondary-text text-[11px] mt-0.5">{log.message}</p>
                    </div>
                    <div className="text-right shrink-0">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-600">
                        {log.status}
                      </span>
                      <span className="text-[10px] text-secondary-text block mt-1">{log.timestamp}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 5: USERS */}
      {activeTab === 'users' && (
        <div className="bg-card rounded-2xl border border-border-subtle p-6 shadow-card space-y-5">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h3 className="text-base font-bold text-primary-text">Danh sách Tài khoản & Phân quyền</h3>
              <p className="text-xs text-secondary-text mt-0.5">Quản lý người dùng hệ thống: Nhà phân tích (Analyst) và Quản trị viên (Admin)</p>
            </div>
            <button
              onClick={() => setUserModalOpen(true)}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-brand text-white text-xs font-bold hover:bg-brand/90 transition-all shadow-sm shrink-0"
            >
              <Plus className="w-4 h-4" /> Thêm Người dùng
            </button>
          </div>

          <div className="overflow-x-auto custom-scrollbar">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="border-b border-border-subtle text-secondary-text font-bold uppercase tracking-wider text-[11px]">
                  <th className="py-3 px-4">ID</th>
                  <th className="py-3 px-4">Họ và tên</th>
                  <th className="py-3 px-4">Email đăng nhập</th>
                  <th className="py-3 px-4">Vai trò (Role)</th>
                  <th className="py-3 px-4">Trạng thái</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-subtle/60">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-black/[0.01] transition-colors">
                    <td className="py-3 px-4 font-mono text-secondary-text">#{u.id}</td>
                    <td className="py-3 px-4 font-bold text-primary-text">{u.fullName}</td>
                    <td className="py-3 px-4 text-secondary-text font-medium">{u.email}</td>
                    <td className="py-3 px-4">
                      {u.role === 'admin' ? (
                        <span className="px-2.5 py-1 rounded-md bg-purple-500/10 text-purple-700 font-extrabold text-[10px] uppercase tracking-wider border border-purple-200">
                          QUẢN TRỊ VIÊN (ADMIN)
                        </span>
                      ) : (
                        <span className="px-2.5 py-1 rounded-md bg-blue-500/10 text-blue-700 font-extrabold text-[10px] uppercase tracking-wider border border-blue-200">
                          NHÀ PHÂN TÍCH (ANALYST)
                        </span>
                      )}
                    </td>
                    <td className="py-3 px-4">
                      <span className="inline-flex items-center gap-1.5 text-emerald-600 font-semibold text-[11px]">
                        <span className="w-2 h-2 rounded-full bg-emerald-500" /> Hoạt động
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* MODAL: Thêm / Sửa Nông sản */}
      {commodityModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-card rounded-2xl border border-border-subtle shadow-2xl max-w-lg w-full p-6 space-y-4 animate-in fade-in zoom-in-95">
            <h3 className="text-base font-bold text-primary-text">
              {editingCommodity ? `Chỉnh sửa: ${editingCommodity.name}` : 'Thêm Nông sản Mới'}
            </h3>

            <form onSubmit={handleSaveCommodity} className="space-y-3.5 text-xs">
              <div>
                <label className="font-bold text-secondary-text block mb-1">Mã Code (Định danh duy nhất)</label>
                <input
                  type="text"
                  placeholder="Ví dụ: RICE_JASMINE, CASHEW_NUT..."
                  value={commodityForm.code}
                  onChange={(e) => setCommodityForm({ ...commodityForm, code: e.target.value.toUpperCase() })}
                  className="w-full px-3 py-2 rounded-xl bg-canvas border border-border-subtle font-mono font-bold text-primary-text focus:outline-none focus:border-brand uppercase"
                  required
                  disabled={!!editingCommodity}
                />
              </div>

              <div>
                <label className="font-bold text-secondary-text block mb-1">Tên Nông sản</label>
                <input
                  type="text"
                  placeholder="Ví dụ: Hạt điều xuất khẩu..."
                  value={commodityForm.name}
                  onChange={(e) => setCommodityForm({ ...commodityForm, name: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-canvas border border-border-subtle font-semibold text-primary-text focus:outline-none focus:border-brand"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-bold text-secondary-text block mb-1">Phân loại</label>
                  <select
                    value={commodityForm.category}
                    onChange={(e) => setCommodityForm({ ...commodityForm, category: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-canvas border border-border-subtle font-semibold text-primary-text focus:outline-none focus:border-brand"
                  >
                    <option value="Lương thực">Lương thực</option>
                    <option value="Cây công nghiệp">Cây công nghiệp</option>
                    <option value="Gia vị xuất khẩu">Gia vị xuất khẩu</option>
                    <option value="Trái cây">Trái cây</option>
                  </select>
                </div>

                <div>
                  <label className="font-bold text-secondary-text block mb-1">Đơn vị niêm yết</label>
                  <input
                    type="text"
                    placeholder="VNĐ/kg, VNĐ/tấn..."
                    value={commodityForm.unit}
                    onChange={(e) => setCommodityForm({ ...commodityForm, unit: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-canvas border border-border-subtle font-semibold text-primary-text focus:outline-none focus:border-brand"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="font-bold text-secondary-text block mb-1">Vùng trồng / Thị trường chính</label>
                <input
                  type="text"
                  placeholder="Ví dụ: Tây Nguyên, Bình Phước..."
                  value={commodityForm.region}
                  onChange={(e) => setCommodityForm({ ...commodityForm, region: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-canvas border border-border-subtle font-semibold text-primary-text focus:outline-none focus:border-brand"
                  required
                />
              </div>

              <div>
                <label className="font-bold text-secondary-text block mb-1">Mô tả chi tiết</label>
                <textarea
                  rows={2}
                  placeholder="Thông tin đặc điểm hàng hóa, độ ẩm, tạp chất..."
                  value={commodityForm.description}
                  onChange={(e) => setCommodityForm({ ...commodityForm, description: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-canvas border border-border-subtle font-semibold text-primary-text focus:outline-none focus:border-brand"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setCommodityModalOpen(false)}
                  className="px-4 py-2 rounded-xl border border-border-subtle text-secondary-text font-bold hover:bg-black/5 transition-all"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-brand text-white font-bold hover:bg-brand/90 transition-all shadow-sm"
                >
                  {editingCommodity ? 'Lưu thay đổi' : 'Tạo mới'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL: Thêm Người dùng */}
      {userModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-card rounded-2xl border border-border-subtle shadow-2xl max-w-md w-full p-6 space-y-4 animate-in fade-in zoom-in-95">
            <h3 className="text-base font-bold text-primary-text">Cấp Tài khoản Người dùng Mới</h3>

            <form onSubmit={handleCreateUser} className="space-y-3.5 text-xs">
              <div>
                <label className="font-bold text-secondary-text block mb-1">Họ và tên</label>
                <input
                  type="text"
                  placeholder="Nguyễn Văn A"
                  value={userForm.full_name}
                  onChange={(e) => setUserForm({ ...userForm, full_name: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-canvas border border-border-subtle font-semibold text-primary-text focus:outline-none focus:border-brand"
                  required
                />
              </div>

              <div>
                <label className="font-bold text-secondary-text block mb-1">Email đăng nhập</label>
                <input
                  type="email"
                  placeholder="analyst@agroforecast.vn"
                  value={userForm.email}
                  onChange={(e) => setUserForm({ ...userForm, email: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-canvas border border-border-subtle font-semibold text-primary-text focus:outline-none focus:border-brand"
                  required
                />
              </div>

              <div>
                <label className="font-bold text-secondary-text block mb-1">Mật khẩu ban đầu</label>
                <input
                  type="password"
                  placeholder="Tối thiểu 6 ký tự"
                  value={userForm.password}
                  onChange={(e) => setUserForm({ ...userForm, password: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-canvas border border-border-subtle font-semibold text-primary-text focus:outline-none focus:border-brand"
                  required
                  minLength={6}
                />
              </div>

              <div>
                <label className="font-bold text-secondary-text block mb-1">Vai trò & Phân quyền</label>
                <select
                  value={userForm.role}
                  onChange={(e) => setUserForm({ ...userForm, role: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-canvas border border-border-subtle font-semibold text-primary-text focus:outline-none focus:border-brand"
                >
                  <option value="analyst">Nhà phân tích (Analyst - Xem và phân tích)</option>
                  <option value="admin">Quản trị viên (Admin - Toàn quyền hệ thống)</option>
                </select>
              </div>

              <div className="flex items-center justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setUserModalOpen(false)}
                  className="px-4 py-2 rounded-xl border border-border-subtle text-secondary-text font-bold hover:bg-black/5 transition-all"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-brand text-white font-bold hover:bg-brand/90 transition-all shadow-sm"
                >
                  Tạo tài khoản
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
