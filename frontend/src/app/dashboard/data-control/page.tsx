'use client';

import React, { useState, useEffect, useRef } from 'react';
import {
  fetchRecentPricesApi,
  triggerScrapeTaskApi,
  fetchCrawlerLogsApi,
  importPricesCsvApi,
  getExportPricesCsvUrl,
  createOrUpdatePriceApi,
  deletePriceRecordApi,
  fetchAdminCommodities,
} from '@/lib/api';
import {
  AdminPriceItem,
  TaskRunResult,
  CrawlerLog,
} from '@/types';
import {
  Database,
  Upload,
  Download,
  Play,
  Plus,
  Trash2,
  CheckCircle2,
  AlertCircle,
  Clock,
  Filter,
  FileText,
  Activity,
} from 'lucide-react';

interface CommodityItem {
  id: number;
  code: string;
  name: string;
}

export default function DashboardDataControlPage() {
  const [prices, setPrices] = useState<AdminPriceItem[]>([]);
  const [crawlerLogs, setCrawlerLogs] = useState<CrawlerLog[]>([]);
  const [commodities, setCommodities] = useState<CommodityItem[]>([]);
  const [selectedCommodityFilter, setSelectedCommodityFilter] = useState<number | undefined>(undefined);

  // Scraper Task state
  const [scrapingDays, setScrapingDays] = useState(30);
  const [scrapeRunning, setScrapeRunning] = useState(false);
  const [scrapeResult, setScrapeResult] = useState<TaskRunResult | null>(null);

  // CSV Import state
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [importing, setImporting] = useState(false);
  const [importResult, setImportResult] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

  // Price Modal state
  const [priceModalOpen, setPriceModalOpen] = useState(false);
  const [priceForm, setPriceForm] = useState({
    commodity_id: 2,
    record_date: new Date().toISOString().split('T')[0],
    price: '',
    price_min: '',
    price_max: '',
    volume: '15000',
    source: 'Cập nhật thủ công bởi Admin',
  });

  const loadAll = async () => {
    try {
      const [pData, lData, cData] = await Promise.all([
        fetchRecentPricesApi(selectedCommodityFilter),
        fetchCrawlerLogsApi(),
        fetchAdminCommodities(),
      ]);
      setPrices(pData);
      setCrawlerLogs(lData);
      setCommodities(cData);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadAll();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedCommodityFilter]);

  const handleTriggerScraper = async () => {
    setScrapeRunning(true);
    try {
      const res = await triggerScrapeTaskApi(scrapingDays);
      setScrapeResult(res);
      // Refresh logs
      const updatedLogs = await fetchCrawlerLogsApi();
      setCrawlerLogs(updatedLogs);
    } catch (err: unknown) {
      setScrapeResult({
        taskName: 'Cào dữ liệu thị trường',
        status: 'FAILED',
        message: err instanceof Error ? err.message : 'Lỗi khi kích hoạt bot cào',
        timestamp: new Date().toLocaleTimeString('vi-VN'),
      });
    } finally {
      setScrapeRunning(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setImporting(true);
    setImportResult(null);
    try {
      const res = await importPricesCsvApi(file);
      setImportResult({ message: res.message, type: 'success' });
      await loadAll();
    } catch (err: unknown) {
      setImportResult({ message: err instanceof Error ? err.message : 'Lỗi khi upload file CSV', type: 'error' });
    } finally {
      setImporting(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleSavePrice = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!priceForm.price || isNaN(Number(priceForm.price))) {
      alert('Vui lòng nhập giá hợp lệ');
      return;
    }

    try {
      await createOrUpdatePriceApi({
        commodity_id: Number(priceForm.commodity_id),
        record_date: priceForm.record_date,
        price: parseFloat(priceForm.price),
        price_min: priceForm.price_min ? parseFloat(priceForm.price_min) : undefined,
        price_max: priceForm.price_max ? parseFloat(priceForm.price_max) : undefined,
        volume: priceForm.volume ? parseFloat(priceForm.volume) : 0,
        source: priceForm.source,
      });
      setPriceModalOpen(false);
      setPriceForm({ ...priceForm, price: '' });
      await loadAll();
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : 'Không thể lưu bản ghi giá');
    }
  };

  const handleDeletePrice = async (id: number) => {
    if (!confirm('Bạn có chắc chắn muốn xóa bản ghi giá này?')) return;
    try {
      await deletePriceRecordApi(id);
      await loadAll();
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : 'Không thể xóa bản ghi giá');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-border-subtle">
        <div>
          <h1 className="text-2xl font-bold text-primary-text flex items-center gap-2.5">
            <Database className="w-6 h-6 text-brand" />
            Quản Lý Dữ Liệu Thị Trường & Bot Scraper
          </h1>
          <p className="text-sm text-secondary-text mt-1">
            Điều khiển Bot cào dữ liệu tức thì, kiểm tra Crawling Logs và nạp/xuất file CSV giá
          </p>
        </div>

        <div className="flex items-center gap-2">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileUpload}
            accept=".csv,.txt"
            className="hidden"
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={importing}
            className="px-3.5 py-2 rounded-xl bg-card hover:bg-canvas text-primary-text border border-border-subtle text-xs font-semibold flex items-center gap-1.5 transition shadow-xs"
          >
            <Upload className="w-3.5 h-3.5 text-brand" />
            {importing ? 'Đang nạp CSV...' : 'Import CSV'}
          </button>

          <a
            href={getExportPricesCsvUrl(selectedCommodityFilter)}
            download="commodity_prices_export.csv"
            className="px-3.5 py-2 rounded-xl bg-card hover:bg-canvas text-primary-text border border-border-subtle text-xs font-semibold flex items-center gap-1.5 transition shadow-xs"
          >
            <Download className="w-3.5 h-3.5 text-secondary-text" />
            Export CSV
          </a>

          <button
            onClick={() => setPriceModalOpen(true)}
            className="px-3.5 py-2 rounded-xl bg-brand hover:bg-brand-hover text-white text-xs font-semibold flex items-center gap-1.5 shadow-xs transition"
          >
            <Plus className="w-3.5 h-3.5" />
            Thêm Điểm Giá
          </button>
        </div>
      </div>

      {/* Alert toast for CSV Import */}
      {importResult && (
        <div
          className={`p-4 rounded-xl text-xs font-medium flex items-center justify-between border ${
            importResult.type === 'success'
              ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
              : 'bg-rose-50 text-rose-800 border-rose-200'
          }`}
        >
          <div className="flex items-center gap-2">
            {importResult.type === 'success' ? (
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            ) : (
              <AlertCircle className="w-4 h-4 text-rose-600" />
            )}
            <span>{importResult.message}</span>
          </div>
          <button onClick={() => setImportResult(null)} className="text-secondary-text hover:text-primary-text">
            ✕
          </button>
        </div>
      )}

      {/* Section 1: Bot Crawler Trigger Panel */}
      <div className="p-6 rounded-2xl bg-card border border-border-subtle shadow-xs space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-base font-semibold text-primary-text flex items-center gap-2">
              <Activity className="w-4 h-4 text-brand" />
              Kích Hoạt Thu Thập Dữ Liệu Tự Động (Manual Crawler Trigger)
            </h2>
            <p className="text-xs text-secondary-text mt-0.5">
              Gửi yêu cầu tới Scraper Engine để cào dữ liệu từ Yahoo Finance, Giacaphe.com và Hiệp hội nông sản
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 text-xs text-secondary-text bg-canvas px-3 py-1.5 rounded-xl border border-border-subtle">
              <span>Phạm vi cào:</span>
              <select
                value={scrapingDays}
                onChange={(e) => setScrapingDays(Number(e.target.value))}
                className="bg-transparent text-brand font-semibold focus:outline-none"
              >
                <option value={7}>7 ngày gần nhất</option>
                <option value={30}>30 ngày gần nhất</option>
                <option value={90}>90 ngày gần nhất</option>
                <option value={365}>1 năm dữ liệu</option>
              </select>
            </div>

            <button
              onClick={handleTriggerScraper}
              disabled={scrapeRunning}
              className="px-4 py-2.5 rounded-xl bg-brand hover:bg-brand-hover text-white text-xs font-semibold flex items-center gap-2 shadow-xs transition disabled:opacity-50"
            >
              <Play className={`w-3.5 h-3.5 fill-current ${scrapeRunning ? 'animate-spin' : ''}`} />
              {scrapeRunning ? 'Đang chạy Bot...' : 'Kích Hoạt Cào Ngay'}
            </button>
          </div>
        </div>

        {scrapeResult && (
          <div className="p-3.5 rounded-xl bg-canvas border border-border-subtle flex items-center justify-between text-xs">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
              <span className="font-semibold text-primary-text">Trạng thái:</span>
              <span className="text-brand font-medium">{scrapeResult.message}</span>
            </div>
            <span className="text-secondary-text text-[11px]">{scrapeResult.timestamp}</span>
          </div>
        )}
      </div>

      {/* Section 2: Crawling Logs Table */}
      <div className="p-6 rounded-2xl bg-card border border-border-subtle shadow-xs space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-base font-semibold text-primary-text flex items-center gap-2">
              <Clock className="w-4 h-4 text-amber-600" />
              Nhật Ký Cào Dữ Liệu Gần Đây (Crawling Logs)
            </h2>
            <p className="text-xs text-secondary-text mt-0.5">
              Theo dõi lịch sử và thời gian thực thi của các Bot cào
            </p>
          </div>
          <span className="text-xs text-secondary-text font-medium">{crawlerLogs.length} tiến trình</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-primary-text">
            <thead className="bg-canvas text-secondary-text uppercase text-[11px] font-semibold border-b border-border-subtle">
              <tr>
                <th className="py-3 px-4">ID</th>
                <th className="py-3 px-4">Tên Bot / Crawler</th>
                <th className="py-3 px-4">Nguồn Thu Thập</th>
                <th className="py-3 px-4">Số Bản Ghi</th>
                <th className="py-3 px-4">Thời Gian Chạy</th>
                <th className="py-3 px-4">Trạng Thái</th>
                <th className="py-3 px-4">Thời Điểm</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle font-mono text-[11px]">
              {crawlerLogs.map((log) => (
                <tr key={log.id} className="hover:bg-canvas/60 transition">
                  <td className="py-3 px-4 text-secondary-text">#{log.id}</td>
                  <td className="py-3 px-4 font-sans font-medium text-primary-text">{log.crawler_name}</td>
                  <td className="py-3 px-4 text-secondary-text">{log.target_source}</td>
                  <td className="py-3 px-4 text-brand font-semibold">{log.records_extracted}</td>
                  <td className="py-3 px-4 text-secondary-text">{log.duration_sec}s</td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-[10px] font-sans font-semibold">
                      {log.status}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-secondary-text">{log.timestamp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Section 3: Price Data Management Table */}
      <div className="p-6 rounded-2xl bg-card border border-border-subtle shadow-xs space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-3 border-b border-border-subtle">
          <div>
            <h2 className="text-base font-semibold text-primary-text flex items-center gap-2">
              <FileText className="w-4 h-4 text-purple-600" />
              Bảng Quản Lý Giá Nông Sản (Price History Records)
            </h2>
            <p className="text-xs text-secondary-text mt-0.5">
              Kiểm tra, điều chỉnh hoặc xóa các điểm giá sai lệch
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <Filter className="w-3.5 h-3.5 text-secondary-text" />
            <select
              value={selectedCommodityFilter || ''}
              onChange={(e) => setSelectedCommodityFilter(e.target.value ? Number(e.target.value) : undefined)}
              className="bg-canvas border border-border-subtle text-primary-text px-3 py-1.5 rounded-xl focus:outline-none"
            >
              <option value="">Tất cả nông sản</option>
              {commodities.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-primary-text">
            <thead className="bg-canvas text-secondary-text uppercase text-[11px] font-semibold border-b border-border-subtle">
              <tr>
                <th className="py-3 px-4">Ngày</th>
                <th className="py-3 px-4">Nông Sản</th>
                <th className="py-3 px-4">Giá Đóng Cửa</th>
                <th className="py-3 px-4">Khối Lượng</th>
                <th className="py-3 px-4">Nguồn Dữ Liệu</th>
                <th className="py-3 px-4 text-right">Thao Tác</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle">
              {prices.map((p) => (
                <tr key={p.id} className="hover:bg-canvas/60 transition">
                  <td className="py-3 px-4 font-mono text-secondary-text">{p.recordDate}</td>
                  <td className="py-3 px-4 font-medium text-primary-text">{p.commodityName}</td>
                  <td className="py-3 px-4 font-bold text-brand font-mono">
                    {p.price.toLocaleString('vi-VN')} đ
                  </td>
                  <td className="py-3 px-4 font-mono text-secondary-text">{p.volume ? p.volume.toLocaleString('vi-VN') : '-'}</td>
                  <td className="py-3 px-4 text-secondary-text text-[11px]">{p.source || 'Nhập thủ công'}</td>
                  <td className="py-3 px-4 text-right">
                    <button
                      onClick={() => handleDeletePrice(p.id)}
                      className="p-1.5 rounded-lg text-secondary-text hover:text-rose-600 hover:bg-rose-50 transition"
                      title="Xóa điểm giá"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal: Thêm điểm giá mới */}
      {priceModalOpen && (
        <div className="fixed inset-0 z-50 bg-primary-text/40 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="w-full max-w-md bg-card border border-border-subtle rounded-2xl p-6 space-y-4 shadow-xl">
            <h3 className="text-lg font-bold text-primary-text flex items-center gap-2">
              <Plus className="w-5 h-5 text-brand" />
              Thêm Điểm Giá Mới
            </h3>

            <form onSubmit={handleSavePrice} className="space-y-3.5 text-xs">
              <div>
                <label className="block text-secondary-text font-medium mb-1">Loại Nông Sản</label>
                <select
                  value={priceForm.commodity_id}
                  onChange={(e) => setPriceForm({ ...priceForm, commodity_id: Number(e.target.value) })}
                  className="w-full bg-canvas border border-border-subtle rounded-xl px-3 py-2 text-primary-text"
                >
                  {commodities.map((c) => (
                    <option key={c.id} value={c.id}>{c.name} ({c.code})</option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-secondary-text font-medium mb-1">Ngày Ghi Nhận</label>
                  <input
                    type="date"
                    value={priceForm.record_date}
                    onChange={(e) => setPriceForm({ ...priceForm, record_date: e.target.value })}
                    className="w-full bg-canvas border border-border-subtle rounded-xl px-3 py-2 text-primary-text"
                    required
                  />
                </div>
                <div>
                  <label className="block text-secondary-text font-medium mb-1">Giá Chính Thức (VNĐ)</label>
                  <input
                    type="number"
                    value={priceForm.price}
                    onChange={(e) => setPriceForm({ ...priceForm, price: e.target.value })}
                    placeholder="VD: 62500"
                    className="w-full bg-canvas border border-border-subtle rounded-xl px-3 py-2 text-primary-text font-mono"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-secondary-text font-medium mb-1">Nguồn Thu Thập</label>
                <input
                  type="text"
                  value={priceForm.source}
                  onChange={(e) => setPriceForm({ ...priceForm, source: e.target.value })}
                  className="w-full bg-canvas border border-border-subtle rounded-xl px-3 py-2 text-primary-text"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-border-subtle">
                <button
                  type="button"
                  onClick={() => setPriceModalOpen(false)}
                  className="px-4 py-2 rounded-xl bg-canvas border border-border-subtle text-secondary-text font-medium hover:bg-[#EFECE6] transition"
                >
                  Hủy Bỏ
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-brand hover:bg-brand-hover text-white font-semibold shadow-xs transition"
                >
                  Lưu Bản Ghi Giá
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
