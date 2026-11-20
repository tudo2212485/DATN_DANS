'use client';

import { useBackgroundJob } from '@/components/dashboard/JobStatus';
import AgroGrid, { AgroColumn } from '@/components/ui/AgroGrid';
import { getUser } from '@/lib/auth';
import React, { useState, useEffect, useRef, useMemo } from 'react';
import {
  fetchRecentPricesApi,
  triggerScrapeTaskApi,
  fetchCrawlerLogsApi,
  importPricesCsvApi,
  createOrUpdatePriceApi,
  deletePriceRecordApi,
  fetchAdminCommodities,
  fetchPriceRevisionsApi,
} from '@/lib/api';
import {
  AdminPriceItem,
  CrawlerLog,
  PriceRevisionItem,
} from '@/types';
import {
  formatDateTimeVN,
  formatNumberVN,
  getCommodityUnit,
} from '@/lib/formatters';
import {
  Upload,
  Play,
  Plus,
  Pencil,
  Trash2,
  CheckCircle2,
  AlertCircle,
  RefreshCw,
  ShieldCheck,
} from 'lucide-react';

interface CommodityItem {
  id: number;
  code: string;
  name: string;
  unit?: string;
}

type DataControlTab = 'prices' | 'scraper' | 'audit';

export default function DashboardDataControlPage() {
  const canEdit = getUser()?.role === 'admin';
  const [activeTab, setActiveTab] = useState<DataControlTab>('prices');
  const [toast, setToast] = useState<{ text: string; type: 'success' | 'error'; details?: string[] } | null>(null);
  const [modalError, setModalError] = useState('');

  // Server filters for Tab 1
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [offset, setOffset] = useState(0);
  const [selectedCommodityFilter, setSelectedCommodityFilter] = useState<number | undefined>(undefined);

  // Data state
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true);
  const [reviewed, setReviewed] = useState(true);
  const [prices, setPrices] = useState<AdminPriceItem[]>([]);
  const [crawlerLogs, setCrawlerLogs] = useState<CrawlerLog[]>([]);
  const [revisions, setRevisions] = useState<PriceRevisionItem[]>([]);
  const [commodities, setCommodities] = useState<CommodityItem[]>([]);

  // Scraper state
  const [scrapingDays, setScrapingDays] = useState(30);
  const [scrapeTriggering, setScrapeTriggering] = useState(false);

  // CSV Import state
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [importing, setImporting] = useState(false);

  // Add / Edit Price Modal state
  const [priceModalOpen, setPriceModalOpen] = useState(false);
  const [editingPrice, setEditingPrice] = useState(false);
  const [priceForm, setPriceForm] = useState({
    commodity_id: 2,
    record_date: new Date().toISOString().split('T')[0],
    price: '',
    price_min: '',
    price_max: '',
    volume: '1500',
    source: 'Sở NN&PTNT Đắk Lắk',
  });

  const loadAll = async () => {
    setLoading(true);
    try {
      const [pData, lData, cData, revData] = await Promise.all([
        fetchRecentPricesApi(selectedCommodityFilter, startDate, endDate, offset, 100),
        fetchCrawlerLogsApi(),
        fetchAdminCommodities(),
        fetchPriceRevisionsApi(50),
      ]);
      setPrices(pData);
      setCrawlerLogs(lData);
      setCommodities(cData);
      setRevisions(revData);
    } catch (e) {
      setToast({
        text: e instanceof Error ? e.message : 'Không tải được dữ liệu quản trị',
        type: 'error',
      });
      setPrices([]);
      setCrawlerLogs([]);
    } finally {
      setLoading(false);
    }
  };

  const scrape = useBackgroundJob('scrape', () => {
    void loadAll();
    setToast({
      text: 'Tiến trình thu thập dữ liệu tự động đã hoàn tất và cập nhật bảng Nhật ký.',
      type: 'success',
    });
  });

  useEffect(() => {
    void loadAll();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedCommodityFilter, startDate, endDate, offset]);

  const handleTriggerScraper = async () => {
    setScrapeTriggering(true);
    setToast(null);
    try {
      const res = await triggerScrapeTaskApi(scrapingDays);
      scrape.begin(res);
      setToast({
        text: `Đã kích hoạt thu thập dữ liệu (${scrapingDays} ngày gần nhất). Nhật ký sẽ tự cập nhật khi hoàn tất.`,
        type: 'success',
      });
    } catch (err: unknown) {
      setToast({
        text: err instanceof Error ? err.message : 'Không kích hoạt được thu thập tự động',
        type: 'error',
      });
    } finally {
      setScrapeTriggering(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.csv') && !file.name.toLowerCase().endsWith('.txt')) {
      setToast({
        text: 'Định dạng file không hợp lệ. Vui lòng chọn file .csv (tối đa 5MB).',
        type: 'error',
      });
      e.target.value = '';
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setToast({
        text: 'Dung lượng file vượt quá giới hạn 5MB.',
        type: 'error',
      });
      e.target.value = '';
      return;
    }

    setImporting(true);
    setToast(null);
    try {
      const res = await importPricesCsvApi(file);
      const hasErrors = Boolean(res.errors && res.errors.length > 0);
      setToast({
        text: res.message || `Import thành công: thêm mới ${res.records_created}, cập nhật ${res.records_updated}.`,
        type: hasErrors && res.records_created === 0 && res.records_updated === 0 ? 'error' : 'success',
        details: res.errors,
      });
      await loadAll();
    } catch (err: unknown) {
      setToast({
        text: err instanceof Error ? err.message : 'Lỗi khi nhập dữ liệu từ file CSV',
        type: 'error',
      });
    } finally {
      setImporting(false);
      e.target.value = '';
    }
  };

  const handleSavePrice = async (e: React.FormEvent) => {
    e.preventDefault();
    const numericPrice = parseFloat(priceForm.price);
    if (!Number.isFinite(numericPrice) || numericPrice <= 0) {
      setModalError('Mức giá phải là số dương hợp lệ.');
      return;
    }

    setBusy(true);
    setModalError('');
    try {
      await createOrUpdatePriceApi({
        commodity_id: Number(priceForm.commodity_id),
        record_date: priceForm.record_date,
        price: numericPrice,
        price_min: priceForm.price_min ? parseFloat(priceForm.price_min) : undefined,
        price_max: priceForm.price_max ? parseFloat(priceForm.price_max) : undefined,
        volume: priceForm.volume ? parseFloat(priceForm.volume) : 0,
        source: priceForm.source,
        reviewed,
      });
      setPriceModalOpen(false);
      setPriceForm({ ...priceForm, price: '' });
      setToast({
        text: editingPrice
          ? 'Đã cập nhật điểm giá và lưu vào Lịch sử chỉnh sửa (Audit Log).'
          : 'Đã thêm điểm giá nông sản mới thành công.',
        type: 'success',
      });
      await loadAll();
    } catch (err: unknown) {
      setModalError(err instanceof Error ? err.message : 'Không thể lưu bản ghi giá');
    } finally {
      setBusy(false);
    }
  };

  const handleVerifyPrice = async (p: AdminPriceItem) => {
    setBusy(true);
    setToast(null);
    try {
      await createOrUpdatePriceApi({
        commodity_id: p.commodityId,
        record_date: p.recordDate,
        price: p.price,
        price_min: p.priceMin ?? undefined,
        price_max: p.priceMax ?? undefined,
        volume: p.volume ?? 0,
        source: p.source || 'Sở NN&PTNT',
        reviewed: true,
      });
      setToast({
        text: `Đã xác minh bản ghi giá ${p.commodityName} (${p.recordDate}) và ghi nhận vào Audit Log.`,
        type: 'success',
      });
      await loadAll();
    } catch (err: unknown) {
      setToast({
        text: err instanceof Error ? err.message : 'Không thể xác minh bản ghi giá',
        type: 'error',
      });
    } finally {
      setBusy(false);
    }
  };

  const handleDeletePrice = async (id: number) => {
    if (!confirm('Bạn có chắc chắn muốn xóa bản ghi giá này? Thay đổi sẽ được lưu vào Lịch sử chỉnh sửa.')) return;
    setBusy(true);
    setToast(null);
    try {
      await deletePriceRecordApi(id);
      setToast({
        text: 'Đã xóa bản ghi giá và lưu vết vào Lịch sử chỉnh sửa (Audit Log).',
        type: 'success',
      });
      await loadAll();
    } catch (err: unknown) {
      setToast({
        text: err instanceof Error ? err.message : 'Không thể xóa bản ghi giá',
        type: 'error',
      });
    } finally {
      setBusy(false);
    }
  };

  const priceGridRows = useMemo(() => {
    return prices.map((p) => {
      const unit = getCommodityUnit(p.commodityName);
      const isVerified = p.provenance === 'reviewed' || p.provenance === 'collected';
      return {
        id: p.id,
        recordDate: p.recordDate,
        commodityName: p.commodityName,
        price: p.price,
        unit,
        volume: p.volume ?? 0,
        source: p.source || 'Nhập thủ công',
        isVerified,
        statusLabel: isVerified ? 'Đã xác minh' : 'Chưa xác minh',
        _raw: p,
      };
    });
  }, [prices]);

  const crawlerGridRows = useMemo(() => {
    return crawlerLogs.map((log) => {
      const statusText = String(log.status);
      return {
        id: log.id,
        crawler_name: log.crawler_name,
        details: log.details || log.target_source,
        records_extracted: log.records_extracted,
        duration_sec: Number(log.duration_sec.toFixed(2)),
        statusRaw: statusText,
        statusLabel:
          statusText === 'SUCCESS'
            ? 'Thành công'
            : statusText === 'FAILED'
              ? 'Thất bại'
              : statusText === 'PARTIAL'
                ? 'Một phần'
                : 'Đang chạy',
        timestampFormatted: formatDateTimeVN(log.timestamp),
      };
    });
  }, [crawlerLogs]);

  const auditGridRows = useMemo(() => {
    return revisions.map((rev) => {
      const unit = getCommodityUnit(rev.commodityName);
      const oldText =
        rev.previousPrice != null ? `${formatNumberVN(Math.round(rev.previousPrice))} ${unit}` : '—';
      const newText =
        rev.action === 'DELETED'
          ? 'Đã xóa'
          : rev.newPrice != null
            ? `${formatNumberVN(Math.round(rev.newPrice))} ${unit}`
            : 'Đã cập nhật';
      return {
        id: rev.id,
        actor: rev.actor || 'Quản trị viên',
        commodityName: rev.commodityName,
        recordDate: rev.recordDate,
        priceChange: `${oldText} → ${newText}`,
        oldText,
        newText,
        action: rev.action,
        reason: rev.reason || (rev.action === 'DELETED' ? 'Xóa bản ghi giá' : 'Cập nhật điểm giá'),
        createdAt: rev.createdAt,
      };
    });
  }, [revisions]);

  const isScrapeBusy = scrapeTriggering || scrape.running;

  return (
    <div className="space-y-5 font-sans">
      {/* Compact 1-Line Header */}
      <div className="flex items-center justify-between gap-3 pb-3 border-b border-[#E5E7EB]">
        <h1 className="text-lg sm:text-xl font-bold text-[#1E293B] tracking-tight">
          Quản lý dữ liệu & Scraper
        </h1>

        <button
          type="button"
          onClick={() => void loadAll()}
          disabled={loading}
          className="px-3 py-1.5 rounded-lg bg-white hover:bg-[#F8FAF9] text-[#334155] hover:text-[#1E293B] border border-[#E5E7EB] text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Làm mới</span>
        </button>
      </div>

      {/* Hidden CSV file input */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileUpload}
        accept=".csv,.txt"
        className="hidden"
      />

      {/* Toast Notification Banner */}
      {(toast || scrape.error) && (
        <div
          role={toast?.type === 'error' || scrape.error ? 'alert' : 'status'}
          className={`p-3 rounded-lg text-xs font-medium border space-y-1.5 ${
            toast?.type === 'error' || scrape.error
              ? 'bg-red-50 text-[#DC2626] border-red-200'
              : 'bg-[#F0F7F4] text-[#15803D] border-[#15803D]/25'
          }`}
        >
          <div className="flex items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              {toast?.type === 'error' || scrape.error ? (
                <AlertCircle className="w-4 h-4 shrink-0" />
              ) : (
                <CheckCircle2 className="w-4 h-4 shrink-0" />
              )}
              <span>{scrape.error || toast?.text}</span>
            </div>
            <button
              type="button"
              onClick={() => setToast(null)}
              className="text-[#64748B] hover:text-[#1E293B] font-bold px-1 cursor-pointer"
            >
              ✕
            </button>
          </div>
          {toast?.details && toast.details.length > 0 && (
            <ul className="list-disc list-inside text-[11.5px] space-y-0.5 pt-1 text-amber-800">
              {toast.details.map((line, i) => (
                <li key={i}>{line}</li>
              ))}
            </ul>
          )}
        </div>
      )}

      {/* 3 Horizontal Logical Tabs */}
      <div className="flex flex-wrap items-center gap-1.5 border-b border-[#E5E7EB] pb-2.5">
        <button
          type="button"
          onClick={() => setActiveTab('prices')}
          className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer ${
            activeTab === 'prices'
              ? 'bg-[#2F6F4E] text-white'
              : 'bg-white text-[#334155] hover:text-[#1E293B] border border-[#E5E7EB]'
          }`}
        >
          Dữ liệu giá nông sản ({prices.length})
        </button>

        <button
          type="button"
          onClick={() => setActiveTab('scraper')}
          className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer ${
            activeTab === 'scraper'
              ? 'bg-[#2F6F4E] text-white'
              : 'bg-white text-[#334155] hover:text-[#1E293B] border border-[#E5E7EB]'
          }`}
        >
          Thu thập tự động ({crawlerLogs.length})
        </button>

        <button
          type="button"
          onClick={() => setActiveTab('audit')}
          className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer ${
            activeTab === 'audit'
              ? 'bg-[#2F6F4E] text-white'
              : 'bg-white text-[#334155] hover:text-[#1E293B] border border-[#E5E7EB]'
          }`}
        >
          Lịch sử chỉnh sửa ({revisions.length})
        </button>
      </div>

      {/* TAB 1 (DEFAULT): DỮ LIỆU GIÁ NÔNG SẢN */}
      {activeTab === 'prices' && (
        <section className="bg-white rounded-xl border border-[#E5E7EB] overflow-hidden">
          {/* Compact Single-Row Filter & Action Toolbar */}
          <div className="px-4 py-3 bg-[#F8FAF9] border-b border-[#E5E7EB] flex flex-wrap items-center justify-between gap-2.5">
            <div className="flex flex-wrap items-center gap-2">
              <select
                aria-label="Lọc theo nông sản"
                value={selectedCommodityFilter || ''}
                onChange={(e) => {
                  setOffset(0);
                  setSelectedCommodityFilter(e.target.value ? Number(e.target.value) : undefined);
                }}
                className="bg-white border border-[#E5E7EB] text-[#1E293B] px-2.5 py-1.5 rounded-lg text-xs font-semibold focus:outline-none focus:border-[#2F6F4E]"
              >
                <option value="">Tất cả nông sản</option>
                {commodities.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>

              <div className="flex items-center gap-1.5 bg-white px-2.5 py-1 rounded-lg border border-[#E5E7EB] text-xs">
                <span className="text-[#64748B]">Từ</span>
                <input
                  aria-label="Từ ngày"
                  type="date"
                  value={startDate}
                  onChange={(e) => {
                    setStartDate(e.target.value);
                    setOffset(0);
                  }}
                  className="text-xs tabular-nums text-[#1E293B] focus:outline-none"
                />
                <span className="text-[#CBD5E1]">–</span>
                <span className="text-[#64748B]">Đến</span>
                <input
                  aria-label="Đến ngày"
                  type="date"
                  value={endDate}
                  onChange={(e) => {
                    setEndDate(e.target.value);
                    setOffset(0);
                  }}
                  className="text-xs tabular-nums text-[#1E293B] focus:outline-none"
                />
              </div>

              {(startDate || endDate || selectedCommodityFilter) && (
                <button
                  type="button"
                  onClick={() => {
                    setStartDate('');
                    setEndDate('');
                    setSelectedCommodityFilter(undefined);
                    setOffset(0);
                  }}
                  className="px-2.5 py-1.5 rounded-lg bg-white hover:bg-[#F8FAF9] border border-[#E5E7EB] text-xs font-medium text-[#475569] cursor-pointer"
                >
                  Xóa lọc
                </button>
              )}
            </div>

            <div className="flex flex-wrap items-center gap-2">
              <button
                type="button"
                disabled={!canEdit || importing}
                onClick={() => fileInputRef.current?.click()}
                className="px-3 py-1.5 rounded-lg bg-white hover:bg-[#F0F7F4] text-[#1E293B] border border-[#E5E7EB] text-xs font-semibold inline-flex items-center gap-1.5 transition-colors disabled:opacity-50 cursor-pointer"
              >
                <Upload className="w-3.5 h-3.5 text-[#2F6F4E]" />
                <span>{importing ? 'Đang nạp CSV...' : 'Import CSV'}</span>
              </button>

              <button
                type="button"
                disabled={!canEdit}
                onClick={() => {
                  setEditingPrice(false);
                  setModalError('');
                  setReviewed(true);
                  setPriceForm({
                    commodity_id: commodities[0]?.id || 1,
                    record_date: new Date().toISOString().slice(0, 10),
                    price: '',
                    price_min: '',
                    price_max: '',
                    volume: '1200',
                    source: 'Sở NN&PTNT / Khảo sát địa phương',
                  });
                  setPriceModalOpen(true);
                }}
                className="px-3 py-1.5 rounded-lg bg-[#2F6F4E] hover:bg-[#24583D] text-white text-xs font-semibold inline-flex items-center gap-1.5 transition-colors disabled:opacity-50 cursor-pointer"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Thêm điểm giá</span>
              </button>
            </div>
          </div>

          <div className="p-4">
            <AgroGrid
              fileName={`du-lieu-gia-nong-san-lo-${offset / 100 + 1}`}
              pageSize={15}
              height={440}
              data={priceGridRows}
              columns={[
                { field: 'recordDate', headerText: 'Ngày ghi nhận', kind: 'date', width: 130 },
                {
                  field: 'commodityName',
                  headerText: 'Nông sản',
                  kind: 'text',
                  width: 155,
                  template: (row: Record<string, unknown>) => (
                    <span className="font-semibold text-[#1E293B]">{String(row.commodityName ?? '')}</span>
                  ),
                },
                {
                  field: 'price',
                  headerText: 'Mức giá',
                  kind: 'money',
                  unitField: 'unit',
                  width: 170,
                },
                {
                  field: 'volume',
                  headerText: 'Sản lượng (Tấn)',
                  kind: 'number',
                  width: 135,
                },
                { field: 'source', headerText: 'Nguồn dữ liệu', kind: 'text', width: 220 },
                {
                  field: 'statusLabel',
                  headerText: 'Trạng thái',
                  kind: 'text',
                  align: 'Center',
                  width: 130,
                  template: (row: Record<string, unknown>) => {
                    const verified = Boolean(row.isVerified);
                    return (
                      <span
                        className={`px-2 py-0.5 rounded-md text-[11px] font-semibold ${
                          verified
                            ? 'bg-[#15803D]/10 text-[#15803D]'
                            : 'bg-amber-50 text-amber-800'
                        }`}
                      >
                        {String(row.statusLabel ?? '')}
                      </span>
                    );
                  },
                },
                {
                  field: 'actions',
                  headerText: 'Thao tác',
                  kind: 'text',
                  align: 'Right',
                  width: 130,
                  allowSorting: false,
                  allowFiltering: false,
                  allowSearching: false,
                  exportable: false,
                  template: (row: Record<string, unknown>) => {
                    const p = row._raw as AdminPriceItem | undefined;
                    if (!p) return null;
                    const verified = Boolean(row.isVerified);
                    return (
                      <div className="inline-flex items-center justify-end gap-1">
                        {!verified && (
                          <button
                            type="button"
                            disabled={!canEdit || busy}
                            onClick={() => void handleVerifyPrice(p)}
                            className="p-1.5 rounded-md text-[#15803D] hover:bg-[#F0F7F4] transition-colors disabled:opacity-40 cursor-pointer"
                            title="Xác minh bản ghi giá"
                          >
                            <ShieldCheck className="w-3.5 h-3.5" />
                          </button>
                        )}
                        <button
                          type="button"
                          disabled={!canEdit || busy}
                          onClick={() => {
                            setEditingPrice(true);
                            setModalError('');
                            setReviewed(verified);
                            setPriceForm({
                              commodity_id: p.commodityId,
                              record_date: p.recordDate,
                              price: String(p.price),
                              price_min: String(p.priceMin ?? ''),
                              price_max: String(p.priceMax ?? ''),
                              volume: String(p.volume ?? 0),
                              source: p.source || 'Sở NN&PTNT',
                            });
                            setPriceModalOpen(true);
                          }}
                          className="p-1.5 rounded-md text-[#475569] hover:text-[#2F6F4E] hover:bg-[#F0F7F4] transition-colors disabled:opacity-40 cursor-pointer"
                          title="Sửa điểm giá"
                        >
                          <Pencil className="w-3.5 h-3.5" />
                        </button>
                        <button
                          type="button"
                          disabled={!canEdit || busy}
                          onClick={() => void handleDeletePrice(p.id)}
                          className="p-1.5 rounded-md text-[#475569] hover:text-[#DC2626] hover:bg-red-50 transition-colors disabled:opacity-40 cursor-pointer"
                          title="Xóa điểm giá"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    );
                  },
                },
              ] as AgroColumn[]}
            />

            {/* Chunk Navigation */}
            <div className="mt-2.5 flex items-center justify-between text-xs text-[#64748B]">
              <span className="tabular-nums">
                Lô #{offset / 100 + 1} · {prices.length} bản ghi gần nhất
              </span>
              <div className="flex items-center gap-1.5">
                <button
                  type="button"
                  disabled={offset === 0}
                  onClick={() => setOffset(Math.max(0, offset - 100))}
                  className="px-2.5 py-1 rounded-md bg-white border border-[#E5E7EB] font-medium text-[#334155] hover:bg-[#F8FAF9] disabled:opacity-40 cursor-pointer"
                >
                  Lô mới hơn
                </button>
                <button
                  type="button"
                  disabled={prices.length < 100}
                  onClick={() => setOffset(offset + 100)}
                  className="px-2.5 py-1 rounded-md bg-white border border-[#E5E7EB] font-medium text-[#334155] hover:bg-[#F8FAF9] disabled:opacity-40 cursor-pointer"
                >
                  Lô cũ hơn
                </button>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* TAB 2: THU THẬP TỰ ĐỘNG (SCRAPER) */}
      {activeTab === 'scraper' && (
        <section className="bg-white rounded-xl border border-[#E5E7EB] overflow-hidden">
          {/* Single-Row Scraper Control Bar (No duplicate #3 · SUCCESS box) */}
          <div className="px-4 py-3 bg-[#F8FAF9] border-b border-[#E5E7EB] flex flex-wrap items-center justify-between gap-3">
            <div className="flex flex-wrap items-center gap-2.5">
              <span className="text-xs font-semibold text-[#1E293B]">Thu thập giá tự động</span>
              <div className="flex items-center gap-1.5 text-xs text-[#475569] bg-white px-2.5 py-1.5 rounded-lg border border-[#E5E7EB]">
                <span>Phạm vi:</span>
                <select
                  aria-label="Phạm vi ngày cào"
                  value={scrapingDays}
                  onChange={(e) => setScrapingDays(Number(e.target.value))}
                  className="bg-transparent text-[#1E293B] font-semibold focus:outline-none"
                >
                  <option value={7}>7 ngày gần nhất</option>
                  <option value={30}>30 ngày gần nhất</option>
                  <option value={90}>90 ngày gần nhất</option>
                  <option value={365}>1 năm dữ liệu</option>
                </select>
              </div>
            </div>

            <button
              type="button"
              onClick={handleTriggerScraper}
              disabled={!canEdit || isScrapeBusy}
              className="px-4 py-1.5 rounded-lg bg-[#2F6F4E] hover:bg-[#24583D] text-white text-xs font-semibold inline-flex items-center gap-1.5 transition-colors disabled:opacity-50 cursor-pointer shrink-0"
            >
              {isScrapeBusy ? (
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
              ) : (
                <Play className="w-3.5 h-3.5 fill-current" />
              )}
              <span>{isScrapeBusy ? 'Đang thu thập...' : 'Kích hoạt cào ngay'}</span>
            </button>
          </div>

          {/* Live progress indicator ONLY while actively running */}
          {scrape.running && scrape.job && (
            <div className="px-4 py-2.5 bg-[#F0F7F4] border-b border-[#E5E7EB] space-y-1">
              <div className="flex items-center justify-between text-xs text-[#2F6F4E] font-medium">
                <span>{scrape.job.message || 'Đang thu thập dữ liệu giá nông sản...'}</span>
                <span className="tabular-nums font-semibold">{scrape.job.progress || 0}%</span>
              </div>
              <div className="w-full h-1.5 bg-[#E5E7EB] rounded-full overflow-hidden">
                <div
                  className="h-full bg-[#2F6F4E] transition-all duration-300"
                  style={{ width: `${Math.max(10, scrape.job.progress || 0)}%` }}
                />
              </div>
            </div>
          )}

          {/* Crawler Logs Syncfusion DataGrid with crisp non-truncating column widths */}
          <div className="p-4">
            <AgroGrid
              fileName="nhat-ky-thu-thap-tu-dong"
              pageSize={15}
              height={420}
              data={crawlerGridRows}
              columns={[
                { field: 'id', headerText: 'ID', kind: 'number', width: 75 },
                { field: 'crawler_name', headerText: 'Tiến trình', kind: 'text', width: 225 },
                { field: 'details', headerText: 'Nguồn & Chi tiết', kind: 'text', width: 310 },
                { field: 'records_extracted', headerText: 'Bản ghi', kind: 'number', width: 110 },
                { field: 'duration_sec', headerText: 'Thời gian (s)', kind: 'decimal', digits: 2, width: 135 },
                {
                  field: 'statusLabel',
                  headerText: 'Trạng thái',
                  kind: 'text',
                  width: 130,
                  align: 'Center',
                  template: (row: Record<string, unknown>) => {
                    const raw = String(row.statusRaw ?? '');
                    const badgeClass =
                      raw === 'SUCCESS'
                        ? 'bg-[#15803D]/10 text-[#15803D]'
                        : raw === 'FAILED'
                          ? 'bg-[#DC2626]/10 text-[#DC2626]'
                          : 'bg-amber-50 text-amber-800';
                    return (
                      <span className={`px-2 py-0.5 rounded-md text-[11px] font-semibold ${badgeClass}`}>
                        {String(row.statusLabel ?? '')}
                      </span>
                    );
                  },
                },
                { field: 'timestampFormatted', headerText: 'Thời điểm', kind: 'text', width: 165, align: 'Right' },
              ] as AgroColumn[]}
            />
          </div>
        </section>
      )}

      {/* TAB 3: LỊCH SỬ CHỈNH SỬA (AUDIT LOG) */}
      {activeTab === 'audit' && (
        <section className="bg-white rounded-xl border border-[#E5E7EB] overflow-hidden">
          <div className="px-4 py-3 bg-[#F8FAF9] border-b border-[#E5E7EB] flex items-center justify-between">
            <h2 className="text-[14px] font-bold text-[#1E293B]">
              Lịch sử chỉnh sửa giá (Audit Log)
            </h2>
            <span className="text-xs tabular-nums text-[#64748B] font-medium">
              {revisions.length} thay đổi gần nhất
            </span>
          </div>

          <div className="p-4">
            <AgroGrid
              fileName="lich-su-chinh-sua-gia-audit-log"
              pageSize={15}
              height={440}
              data={auditGridRows}
              columns={[
                { field: 'actor', headerText: 'Ai sửa', kind: 'text', width: 165 },
                {
                  field: 'commodityName',
                  headerText: 'Nông sản',
                  kind: 'text',
                  width: 155,
                  template: (row: Record<string, unknown>) => (
                    <span className="font-semibold text-[#1E293B]">{String(row.commodityName ?? '')}</span>
                  ),
                },
                { field: 'recordDate', headerText: 'Ngày giá', kind: 'text', width: 120 },
                {
                  field: 'priceChange',
                  headerText: 'Giá cũ → Giá mới',
                  kind: 'text',
                  width: 245,
                  template: (row: Record<string, unknown>) => {
                    const isDeleted = String(row.action ?? '') === 'DELETED';
                    return (
                      <span className="tabular-nums text-xs">
                        <span className="text-[#64748B]">{String(row.oldText ?? '—')}</span>
                        <span className="mx-1.5 text-[#94A3B8]">→</span>
                        <strong className={isDeleted ? 'text-[#DC2626]' : 'text-[#2F6F4E]'}>
                          {String(row.newText ?? '—')}
                        </strong>
                      </span>
                    );
                  },
                },
                { field: 'reason', headerText: 'Lý do', kind: 'text', width: 215 },
                { field: 'createdAt', headerText: 'Thời điểm', kind: 'text', width: 165, align: 'Right' },
              ] as AgroColumn[]}
            />
          </div>
        </section>
      )}

      {/* Modal: Thêm / Sửa điểm giá */}
      {priceModalOpen && (
        <div className="fixed inset-0 z-50 bg-[#0F172A]/40 flex items-center justify-center p-4">
          <div className="w-full max-w-md bg-white border border-[#E5E7EB] rounded-xl p-5 space-y-4 shadow-lg">
            <div className="flex items-center justify-between border-b border-[#E5E7EB] pb-2.5">
              <h3 className="text-base font-bold text-[#1E293B]">
                {editingPrice ? 'Cập nhật điểm giá nông sản' : 'Thêm điểm giá mới'}
              </h3>
              <button
                type="button"
                onClick={() => setPriceModalOpen(false)}
                className="text-[#64748B] hover:text-[#1E293B] font-bold text-sm cursor-pointer"
              >
                ✕
              </button>
            </div>

            {modalError && (
              <p role="alert" className="text-xs text-[#DC2626] bg-red-50 border border-red-200 rounded-lg px-3 py-2 font-medium">
                {modalError}
              </p>
            )}

            <form onSubmit={handleSavePrice} className="space-y-3 text-xs">
              <div>
                <label className="block text-[#475569] font-semibold mb-1">Mặt hàng nông sản</label>
                <select
                  value={priceForm.commodity_id}
                  disabled={editingPrice}
                  onChange={(e) => setPriceForm({ ...priceForm, commodity_id: Number(e.target.value) })}
                  className="w-full bg-white border border-[#E5E7EB] rounded-lg px-3 py-2 text-[#1E293B]"
                >
                  {commodities.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name} ({getCommodityUnit(c.name, c.unit)})
                    </option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[#475569] font-semibold mb-1">Ngày ghi nhận</label>
                  <input
                    type="date"
                    value={priceForm.record_date}
                    disabled={editingPrice}
                    onChange={(e) => setPriceForm({ ...priceForm, record_date: e.target.value })}
                    className="w-full bg-white border border-[#E5E7EB] rounded-lg px-3 py-2 text-[#1E293B] tabular-nums"
                    required
                  />
                </div>
                <div>
                  <label className="block text-[#475569] font-semibold mb-1">Mức giá công bố</label>
                  <input
                    type="number"
                    step="any"
                    min="1"
                    value={priceForm.price}
                    onChange={(e) => setPriceForm({ ...priceForm, price: e.target.value })}
                    placeholder="VD: 128000"
                    className="w-full bg-white border border-[#E5E7EB] rounded-lg px-3 py-2 text-[#1E293B] tabular-nums"
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[#475569] font-semibold mb-1">Sản lượng (Tấn)</label>
                  <input
                    type="number"
                    step="any"
                    min="0"
                    value={priceForm.volume}
                    onChange={(e) => setPriceForm({ ...priceForm, volume: e.target.value })}
                    className="w-full bg-white border border-[#E5E7EB] rounded-lg px-3 py-2 text-[#1E293B] tabular-nums"
                  />
                </div>
                <div>
                  <label className="block text-[#475569] font-semibold mb-1">Nguồn dữ liệu</label>
                  <input
                    type="text"
                    value={priceForm.source}
                    onChange={(e) => setPriceForm({ ...priceForm, source: e.target.value })}
                    className="w-full bg-white border border-[#E5E7EB] rounded-lg px-3 py-2 text-[#1E293B]"
                  />
                </div>
              </div>

              <label className="flex items-center gap-2 pt-1 text-[#334155] cursor-pointer">
                <input
                  type="checkbox"
                  checked={reviewed}
                  onChange={(e) => setReviewed(e.target.checked)}
                  className="rounded border-[#CBD5E1] text-[#2F6F4E] focus:ring-[#2F6F4E]"
                />
                <span>Đánh dấu bản ghi này đã xác minh (đủ điều kiện huấn luyện mô hình)</span>
              </label>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-[#E5E7EB]">
                <button
                  type="button"
                  onClick={() => setPriceModalOpen(false)}
                  className="px-3.5 py-1.5 rounded-lg bg-white border border-[#E5E7EB] text-[#475569] font-semibold hover:bg-[#F8FAF9] cursor-pointer"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  disabled={busy}
                  className="px-4 py-1.5 rounded-lg bg-[#2F6F4E] hover:bg-[#24583D] text-white font-semibold disabled:opacity-50 cursor-pointer"
                >
                  {busy ? 'Đang lưu...' : editingPrice ? 'Lưu thay đổi' : 'Thêm điểm giá'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
