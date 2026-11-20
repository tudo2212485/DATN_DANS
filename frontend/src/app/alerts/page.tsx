'use client';

import React, { useState, useEffect, useMemo } from 'react';
import Header from '@/components/layout/Header';
import AgroGrid, { AgroColumn } from '@/components/ui/AgroGrid';
import { COMMODITIES_DATA } from '@/lib/mockData';
import { AlertRuleItem, AlertLogItem } from '@/types';
import {
  fetchAlertRules,
  createAlertRuleApi,
  updateAlertRuleApi,
  toggleAlertRuleApi,
  deleteAlertRuleApi,
  testAlertApi,
  fetchAlertLogsApi,
  fetchCommoditiesOverview,
} from '@/lib/api';
import {
  formatDateVN,
  formatDateTimeVN,
  formatNumberVN,
  getCommodityUnit,
} from '@/lib/formatters';
import {
  Plus,
  Pencil,
  Trash2,
  CheckCircle2,
  Send,
  Mail,
  TrendingUp,
  TrendingDown,
  Eye,
  RefreshCw,
} from 'lucide-react';

interface CommodityOption {
  id: number;
  name: string;
  unit: string;
}

export default function AlertsPage() {
  const [commodities, setCommodities] = useState<CommodityOption[]>(
    COMMODITIES_DATA.map((c) => ({ id: c.id, name: c.name, unit: c.unit }))
  );
  const [rules, setRules] = useState<AlertRuleItem[]>([]);
  const [logs, setLogs] = useState<AlertLogItem[]>([]);
  const [activeTab, setActiveTab] = useState<'rules' | 'logs'>('rules');
  const [showModal, setShowModal] = useState(false);
  const [editingRuleId, setEditingRuleId] = useState<number | null>(null);
  const [testNotificationMsg, setTestNotificationMsg] = useState<string | null>(null);
  const [emailPreviewRule, setEmailPreviewRule] = useState<AlertRuleItem | null>(null);
  const [loading, setLoading] = useState(false);

  // Commodity filter
  const [commodityFilter, setCommodityFilter] = useState<string>('ALL');

  // Form State
  const [formCommodityId, setFormCommodityId] = useState(2);
  const [formRuleName, setFormRuleName] = useState('');
  const [formCondition, setFormCondition] = useState<AlertRuleItem['conditionType']>('PRICE_ABOVE');
  const [formThreshold, setFormThreshold] = useState('');
  const [formEmail, setFormEmail] = useState('anhnguyen@agroforecast.vn');

  const loadData = async () => {
    setLoading(true);
    try {
      const [liveRules, liveLogs, liveComms] = await Promise.all([
        fetchAlertRules(),
        fetchAlertLogsApi(),
        fetchCommoditiesOverview().catch(() => []),
      ]);
      if (liveRules) setRules(liveRules);
      if (liveLogs) setLogs(liveLogs);
      if (liveComms && liveComms.length > 0) {
        setCommodities(liveComms.map((c) => ({ id: c.id, name: c.name, unit: c.unit })));
      }
    } catch (err) {
      console.error('Error loading alert data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadData();
  }, []);

  const handleToggle = async (id: number) => {
    const target = rules.find((r) => r.id === id);
    if (!target) return;
    const nextState = !target.isActive;
    setRules((prev) => prev.map((r) => (r.id === id ? { ...r, isActive: nextState } : r)));
    await toggleAlertRuleApi(id, nextState);
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Bạn có chắc chắn muốn xóa quy tắc cảnh báo này?')) return;
    setRules((prev) => prev.filter((r) => r.id !== id));
    await deleteAlertRuleApi(id);
  };

  const openCreateModal = () => {
    setEditingRuleId(null);
    setFormCommodityId(commodities[0]?.id || 2);
    setFormRuleName('');
    setFormCondition('PRICE_ABOVE');
    setFormThreshold('');
    setFormEmail('anhnguyen@agroforecast.vn');
    setShowModal(true);
  };

  const openEditModal = (rule: AlertRuleItem) => {
    setEditingRuleId(rule.id);
    setFormCommodityId(rule.commodityId);
    setFormRuleName(rule.ruleName);
    setFormCondition(rule.conditionType);
    setFormThreshold(String(rule.thresholdValue));
    setFormEmail(rule.email);
    setShowModal(true);
  };

  const handleSaveRule = async (e: React.FormEvent) => {
    e.preventDefault();
    const commodity = commodities.find((c) => c.id === formCommodityId);
    const commName = commodity?.name || 'Nông sản';

    const payload = {
      commodity_id: formCommodityId,
      rule_name: formRuleName || `Cảnh báo ${commName}`,
      condition_type: formCondition,
      threshold_value: Number(formThreshold) || 0,
      email: formEmail,
    };

    if (editingRuleId !== null) {
      const updated = await updateAlertRuleApi(editingRuleId, payload);
      if (updated) {
        setRules((prev) => prev.map((r) => (r.id === editingRuleId ? updated : r)));
      } else {
        setRules((prev) =>
          prev.map((r) =>
            r.id === editingRuleId
              ? {
                  ...r,
                  commodityId: formCommodityId,
                  commodityName: commName,
                  ruleName: payload.rule_name,
                  conditionType: formCondition,
                  thresholdValue: payload.threshold_value,
                  email: formEmail,
                }
              : r
          )
        );
      }
      setTestNotificationMsg('Đã cập nhật quy tắc cảnh báo thành công.');
    } else {
      const created = await createAlertRuleApi(payload);
      if (created) {
        setRules((prev) => [created, ...prev]);
      }
      setTestNotificationMsg('Đã tạo và kích hoạt quy tắc cảnh báo mới thành công.');
    }

    setShowModal(false);
    setEditingRuleId(null);
    setFormRuleName('');
    setFormThreshold('');
    setTimeout(() => setTestNotificationMsg(null), 4000);
  };

  const handleTestAlert = async (rule: AlertRuleItem) => {
    const res = await testAlertApi(rule.id);
    setTestNotificationMsg(
      res?.message || `Đã gửi thông báo cảnh báo thử nghiệm "${rule.ruleName}" tới ${rule.email}.`
    );
    setTimeout(() => setTestNotificationMsg(null), 4500);
    const liveLogs = await fetchAlertLogsApi();
    if (liveLogs && liveLogs.length > 0) {
      setLogs(liveLogs);
    }
  };

  const filteredRules = useMemo(() => {
    return rules.filter(
      (r) =>
        commodityFilter === 'ALL' ||
        String(r.commodityId) === commodityFilter ||
        r.commodityName === commodityFilter
    );
  }, [rules, commodityFilter]);

  const ruleRows = useMemo(() => {
    return filteredRules.map((rule) => {
      const val = Number(rule.thresholdValue ?? 0);
      const unit = getCommodityUnit(rule.commodityName);
      const formattedVal = formatNumberVN(val);
      const condType = rule.conditionType || 'PRICE_ABOVE';

      let conditionLabel = `Giá > ${formattedVal} ${unit}`;
      if (condType === 'PRICE_ABOVE') {
        conditionLabel = `Giá > ${formattedVal} ${unit} (Vượt trần)`;
      } else if (condType === 'PRICE_BELOW') {
        conditionLabel = `Giá < ${formattedVal} ${unit} (Chạm sàn)`;
      } else if (condType === 'PCT_INC_7D') {
        conditionLabel = `Tăng > +${formattedVal}% / 7 ngày`;
      } else if (condType === 'PCT_DEC_7D') {
        conditionLabel = `Giảm > -${formattedVal}% / 7 ngày`;
      }

      return {
        id: rule.id,
        ruleName: rule.ruleName,
        commodityName: rule.commodityName,
        conditionType: condType,
        thresholdValue: val,
        conditionLabel,
        email: rule.email,
        isActive: rule.isActive,
        statusLabel: rule.isActive ? 'Đang bật' : 'Đã tắt',
        createdAt: rule.createdAt,
        _raw: rule,
      };
    });
  }, [filteredRules]);

  const activeCount = rules.filter((r) => r.isActive).length;

  return (
    <div className="space-y-5 pb-10 font-sans">
      <Header
        title="Cảnh báo ngưỡng giá nông sản"
        subtitle="Thiết lập quy tắc kiểm tra ngưỡng giá trần/sàn và gửi thông báo tự động qua giao thức SMTP"
        showLiveBadge={true}
      />

      {/* Notification Banner */}
      {testNotificationMsg && (
        <div className="p-3.5 rounded-md bg-[#F0FDF4] border border-[#15803D]/30 text-[#15803D] flex items-center justify-between gap-3 text-xs font-semibold">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-[#15803D] shrink-0" />
            <span>{testNotificationMsg}</span>
          </div>
          <button
            type="button"
            onClick={() => setTestNotificationMsg(null)}
            className="text-[#475569] hover:text-[#0F172A]"
          >
            Đóng
          </button>
        </div>
      )}

      {/* Unified Financial Metric Strip */}
      <section
        aria-label="Thống kê quy tắc cảnh báo"
        className="bg-white rounded-lg border border-[#E5E7EB] grid grid-cols-2 lg:grid-cols-4 divide-y sm:divide-y-0 sm:divide-x divide-[#E5E7EB]"
      >
        <div className="p-4">
          <p className="text-xs font-medium text-[#64748B]">Tổng quy tắc</p>
          <div className="mt-1.5 flex items-baseline gap-1.5">
            <span className="text-2xl font-bold text-[#1E293B] tabular-nums">
              {rules.length}
            </span>
            <span className="text-xs text-[#64748B]">quy tắc</span>
          </div>
        </div>

        <div className="p-4">
          <p className="text-xs font-medium text-[#64748B]">Đang bật</p>
          <div className="mt-1.5 flex items-baseline gap-1.5">
            <span className="text-2xl font-bold text-[#15803D] tabular-nums">
              {activeCount}
            </span>
            <span className="text-xs text-[#15803D] font-semibold">đang theo dõi</span>
          </div>
        </div>

        <div className="p-4">
          <p className="text-xs font-medium text-[#64748B]">Đã kích hoạt</p>
          <div className="mt-1.5 flex items-baseline gap-1.5">
            <span className="text-2xl font-bold text-[#1E293B] tabular-nums">
              {logs.length}
            </span>
            <span className="text-xs text-[#64748B]">lượt cảnh báo</span>
          </div>
        </div>

        <div className="p-4">
          <p className="text-xs font-medium text-[#64748B]">Kênh gửi</p>
          <div className="mt-2 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-[#15803D]" />
            <span className="text-sm font-bold text-[#1E293B]">Kênh gửi: Email SMTP</span>
          </div>
        </div>
      </section>

      {/* Syncfusion Enterprise DataGrid Container */}
      <section className="bg-white rounded-lg border border-[#E2E8F0] overflow-hidden">
        {/* Integrated Single-Row DataGrid Toolbar */}
        <div className="px-4 py-3 bg-[#F8FAFC] border-b border-[#E2E8F0] flex flex-wrap items-center justify-between gap-3">
          {/* Left: Tabs */}
          <div className="flex items-center gap-1.5">
            <button
              type="button"
              onClick={() => setActiveTab('rules')}
              className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-colors cursor-pointer ${
                activeTab === 'rules'
                  ? 'bg-[#166534] text-white'
                  : 'bg-white text-[#475569] hover:text-[#0F172A] border border-[#E2E8F0]'
              }`}
            >
              Danh sách Quy tắc Cảnh báo ({rules.length})
            </button>
            <button
              type="button"
              onClick={() => setActiveTab('logs')}
              className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-colors cursor-pointer ${
                activeTab === 'logs'
                  ? 'bg-[#166534] text-white'
                  : 'bg-white text-[#475569] hover:text-[#0F172A] border border-[#E2E8F0]'
              }`}
            >
              Lịch sử Kích hoạt & Audit Logs ({logs.length})
            </button>
          </div>

          {/* Right: Commodity Filter, Refresh, New Rule (Search/Excel/CSV handled cleanly inside Syncfusion AgroGrid Toolbar) */}
          <div className="flex flex-wrap items-center gap-2">
            {activeTab === 'rules' && (
              <select
                aria-label="Lọc nông sản"
                value={commodityFilter}
                onChange={(e) => setCommodityFilter(e.target.value)}
                className="bg-white border border-[#E5E7EB] text-[#1E293B] px-2.5 py-1.5 rounded-lg text-xs font-medium focus:outline-none focus:border-[#2F6F4E]"
              >
                <option value="ALL">Tất cả nông sản</option>
                {commodities.map((c) => (
                  <option key={c.id} value={String(c.id)}>
                    {c.name}
                  </option>
                ))}
              </select>
            )}

            <button
              type="button"
              onClick={() => void loadData()}
              disabled={loading}
              className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-white hover:bg-[#F8FAF9] text-[#475569] hover:text-[#1E293B] border border-[#E5E7EB] text-xs font-semibold transition-colors cursor-pointer"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
              <span>Làm mới</span>
            </button>

            {activeTab === 'rules' && (
              <button
                type="button"
                onClick={openCreateModal}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#2F6F4E] hover:bg-[#24583D] text-white text-xs font-semibold transition-colors cursor-pointer"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Thêm quy tắc mới</span>
              </button>
            )}
          </div>
        </div>

        {/* TAB 1: RULES TABLE (Syncfusion GridComponent) */}
        {activeTab === 'rules' && (
          <div className="p-4">
            <AgroGrid
              fileName="quy-tac-canh-bao-gia"
              pageSize={15}
              height={420}
              data={ruleRows}
              columns={[
                {
                  field: 'ruleName',
                  headerText: 'Tên quy tắc',
                  kind: 'text',
                  width: 220,
                  template: (row: Record<string, unknown>) => (
                    <div className="leading-tight">
                      <div className="font-semibold text-[#1E293B] truncate">{String(row.ruleName ?? '')}</div>
                      <span className="text-[11px] tabular-nums text-[#64748B]">
                        Tạo: {formatDateVN(String(row.createdAt ?? ''))}
                      </span>
                    </div>
                  ),
                },
                {
                  field: 'commodityName',
                  headerText: 'Nông sản',
                  kind: 'text',
                  width: 145,
                  template: (row: Record<string, unknown>) => (
                    <span className="font-semibold text-[#2F6F4E]">{String(row.commodityName ?? '')}</span>
                  ),
                },
                {
                  field: 'thresholdValue',
                  headerText: 'Điều kiện & Ngưỡng kích hoạt',
                  kind: 'number',
                  align: 'Right',
                  width: 235,
                  template: (row: Record<string, unknown>) => {
                    const condType = String(row.conditionType ?? 'PRICE_ABOVE');
                    const isUpAlert = condType === 'PRICE_ABOVE' || condType === 'PCT_INC_7D';
                    return (
                      <span
                        className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-md border tabular-nums font-semibold text-xs ${
                          isUpAlert
                            ? 'bg-[#DC2626]/10 border-[#DC2626]/20 text-[#DC2626]'
                            : 'bg-[#15803D]/10 border-[#15803D]/20 text-[#15803D]'
                        }`}
                      >
                        {isUpAlert ? (
                          <TrendingUp className="w-3 h-3 shrink-0" />
                        ) : (
                          <TrendingDown className="w-3 h-3 shrink-0" />
                        )}
                        <span>{String(row.conditionLabel ?? '')}</span>
                      </span>
                    );
                  },
                },
                {
                  field: 'email',
                  headerText: 'Email nhận',
                  kind: 'text',
                  width: 195,
                  template: (row: Record<string, unknown>) => (
                    <div className="flex items-center gap-1.5 text-xs text-[#475569]">
                      <Mail className="w-3.5 h-3.5 text-[#64748B] shrink-0" />
                      <span className="truncate" title={String(row.email ?? '')}>
                        {String(row.email ?? '')}
                      </span>
                    </div>
                  ),
                },
                {
                  field: 'statusLabel',
                  headerText: 'Trạng thái',
                  kind: 'text',
                  align: 'Center',
                  width: 105,
                  template: (row: Record<string, unknown>) => {
                    const isActive = Boolean(row.isActive);
                    const id = Number(row.id);
                    return (
                      <button
                        type="button"
                        onClick={() => handleToggle(id)}
                        aria-label={isActive ? 'Tắt quy tắc' : 'Bật quy tắc'}
                        className={`w-10 h-5 rounded-full transition-colors relative p-0.5 inline-block cursor-pointer ${
                          isActive ? 'bg-[#2F6F4E]' : 'bg-[#CBD5E1]'
                        }`}
                        title={isActive ? 'Đang bật - Nhấp để tắt' : 'Đang tắt - Nhấp để bật'}
                      >
                        <div
                          className={`w-4 h-4 rounded-full bg-white transition-transform ${
                            isActive ? 'translate-x-5' : 'translate-x-0'
                          }`}
                        />
                      </button>
                    );
                  },
                },
                {
                  field: 'actions',
                  headerText: 'Thao tác',
                  kind: 'text',
                  align: 'Right',
                  width: 155,
                  allowSorting: false,
                  allowFiltering: false,
                  allowSearching: false,
                  exportable: false,
                  template: (row: Record<string, unknown>) => {
                    const rule = row._raw as AlertRuleItem | undefined;
                    if (!rule) return null;
                    return (
                      <div className="inline-flex items-center justify-end gap-1">
                        <button
                          type="button"
                          onClick={() => openEditModal(rule)}
                          title="Chỉnh sửa quy tắc"
                          className="p-1.5 rounded-md border border-[#E5E7EB] bg-white hover:bg-[#F8FAF9] text-[#475569] hover:text-[#2F6F4E] transition-colors cursor-pointer"
                        >
                          <Pencil className="w-3.5 h-3.5" />
                        </button>
                        <button
                          type="button"
                          onClick={() => setEmailPreviewRule(rule)}
                          title="Xem trước nội dung Email"
                          className="p-1.5 rounded-md border border-[#E5E7EB] bg-white hover:bg-[#F8FAF9] text-[#475569] hover:text-[#1E293B] transition-colors cursor-pointer"
                        >
                          <Eye className="w-3.5 h-3.5" />
                        </button>
                        <button
                          type="button"
                          onClick={() => handleTestAlert(rule)}
                          title="Gửi thử nghiệm cảnh báo ngay"
                          className="p-1.5 rounded-md border border-[#E5E7EB] bg-white hover:bg-[#F0F7F4] text-[#2F6F4E] transition-colors cursor-pointer"
                        >
                          <Send className="w-3.5 h-3.5" />
                        </button>
                        <button
                          type="button"
                          onClick={() => handleDelete(rule.id)}
                          title="Xóa quy tắc"
                          className="p-1.5 rounded-md border border-[#E5E7EB] bg-white hover:bg-red-50 text-[#475569] hover:text-[#DC2626] transition-colors cursor-pointer"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    );
                  },
                },
              ] as AgroColumn[]}
            />
          </div>
        )}

        {/* TAB 2: AUDIT LOGS (Syncfusion GridComponent) */}
        {activeTab === 'logs' && (
          <div className="p-4">
            <AgroGrid
              fileName="lich-su-kich-hoat-canh-bao"
              pageSize={15}
              height={380}
              data={logs.map((log) => {
                const unit = getCommodityUnit(log.commodityName);
                return {
                  id: log.id,
                  triggeredAt: formatDateTimeVN(log.triggeredAt),
                  ruleName: log.ruleName,
                  commodityName: log.commodityName,
                  triggeredPrice: log.triggeredPrice,
                  unit,
                  message: log.message,
                  email: log.email,
                  statusLabel: log.status === 'SENT' ? 'Đã gửi' : log.status,
                };
              })}
              columns={[
                { field: 'triggeredAt', headerText: 'Thời điểm kích hoạt', kind: 'text', width: 155 },
                { field: 'ruleName', headerText: 'Quy tắc áp dụng', kind: 'text', width: 210 },
                { field: 'commodityName', headerText: 'Nông sản', kind: 'text', width: 140 },
                { field: 'triggeredPrice', headerText: 'Mức giá ghi nhận', kind: 'money', unitField: 'unit', width: 165 },
                { field: 'message', headerText: 'Nội dung thông báo', kind: 'text', width: 260 },
                { field: 'email', headerText: 'Email nhận', kind: 'text', width: 185 },
                { field: 'statusLabel', headerText: 'Trạng thái', kind: 'text', width: 110, align: 'Center' },
              ] as AgroColumn[]}
            />
          </div>
        )}
      </section>

      {/* CREATE / EDIT RULE MODAL */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-[#0F172A]/40 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg border border-[#E2E8F0] p-5 max-w-lg w-full shadow-lg space-y-4">
            <div className="flex items-center justify-between border-b border-[#E2E8F0] pb-3">
              <h3 className="text-base font-bold text-[#0F172A]">
                {editingRuleId !== null ? 'Chỉnh sửa quy tắc cảnh báo' : 'Thiết lập quy tắc cảnh báo mới'}
              </h3>
              <button
                type="button"
                onClick={() => setShowModal(false)}
                className="text-[#64748B] hover:text-[#0F172A] font-bold text-sm"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleSaveRule} className="space-y-3 text-xs">
              <div>
                <label className="font-semibold text-[#475569] block mb-1">Nông sản theo dõi</label>
                <select
                  value={formCommodityId}
                  onChange={(e) => setFormCommodityId(Number(e.target.value))}
                  className="w-full bg-white border border-[#E2E8F0] rounded-md p-2 text-[#0F172A] font-semibold focus:outline-none focus:border-[#166534]"
                >
                  {commodities.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name} ({getCommodityUnit(c.name, c.unit)})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="font-semibold text-[#475569] block mb-1">Tên quy tắc</label>
                <input
                  type="text"
                  required
                  placeholder="VD: Cảnh báo Cà phê Robusta vượt 125.000 VNĐ/kg"
                  value={formRuleName}
                  onChange={(e) => setFormRuleName(e.target.value)}
                  className="w-full bg-white border border-[#E2E8F0] rounded-md p-2 text-[#0F172A] focus:outline-none focus:border-[#166534]"
                />
              </div>

              <div>
                <label className="font-semibold text-[#475569] block mb-1">Điều kiện kích hoạt</label>
                <select
                  value={formCondition}
                  onChange={(e) => setFormCondition(e.target.value as AlertRuleItem['conditionType'])}
                  className="w-full bg-white border border-[#E2E8F0] rounded-md p-2 text-[#0F172A] font-semibold focus:outline-none focus:border-[#166534]"
                >
                  <option value="PRICE_ABOVE">Vượt mức giá trần (Giá &gt; Ngưỡng)</option>
                  <option value="PRICE_BELOW">Sụt giảm dưới mức sàn (Giá &lt; Ngưỡng)</option>
                  <option value="PCT_INC_7D">Tăng mạnh trong 7 ngày (&gt; %)</option>
                  <option value="PCT_DEC_7D">Giảm sâu trong 7 ngày (&gt; %)</option>
                </select>
              </div>

              <div>
                <label className="font-semibold text-[#475569] block mb-1">
                  Giá trị ngưỡng kích hoạt (VNĐ hoặc %)
                </label>
                <input
                  type="number"
                  required
                  min="0.01"
                  step="0.01"
                  placeholder="VD: 125000 (cho giá) hoặc 5 (cho %)"
                  value={formThreshold}
                  onChange={(e) => setFormThreshold(e.target.value)}
                  className="w-full bg-white border border-[#E2E8F0] rounded-md p-2 text-[#0F172A] font-mono tabular-nums font-semibold focus:outline-none focus:border-[#166534]"
                />
              </div>

              <div>
                <label className="font-semibold text-[#475569] block mb-1">Email nhận thông báo</label>
                <input
                  type="email"
                  required
                  value={formEmail}
                  onChange={(e) => setFormEmail(e.target.value)}
                  className="w-full bg-white border border-[#E2E8F0] rounded-md p-2 text-[#0F172A] font-mono focus:outline-none focus:border-[#166534]"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-[#E2E8F0]">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-3.5 py-1.5 rounded-md bg-white border border-[#E2E8F0] text-[#475569] hover:bg-[#F8FAFC] font-semibold"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 rounded-md bg-[#166534] hover:bg-[#15803D] text-white font-semibold"
                >
                  {editingRuleId !== null ? 'Lưu Thay Đổi' : 'Lưu & Kích Hoạt'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* EMAIL PREVIEW MODAL */}
      {emailPreviewRule && (
        <div className="fixed inset-0 z-50 bg-[#0F172A]/40 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg border border-[#E2E8F0] p-5 max-w-lg w-full shadow-lg space-y-4">
            <div className="flex items-center justify-between border-b border-[#E2E8F0] pb-3">
              <h3 className="text-base font-bold text-[#0F172A] flex items-center gap-2">
                <Mail className="w-4 h-4 text-[#166534]" />
                <span>Xem trước nội dung Email cảnh báo</span>
              </h3>
              <button
                type="button"
                onClick={() => setEmailPreviewRule(null)}
                className="text-[#64748B] hover:text-[#0F172A] font-bold text-sm"
              >
                ✕
              </button>
            </div>

            <div className="rounded-md border border-[#E2E8F0] bg-[#F8FAFC] p-4 space-y-3 text-xs">
              <div className="flex items-center justify-between border-b border-[#E2E8F0] pb-2.5">
                <span className="font-bold text-[#0F172A]">AgroForecast SMTP Notification</span>
                <span className="text-[11px] text-[#64748B]">TLS Port 587</span>
              </div>

              <div>
                <p className="text-[#475569]">
                  Người nhận: <strong className="text-[#0F172A] font-mono">{emailPreviewRule.email}</strong>
                </p>
                <h4 className="text-sm font-bold text-[#DC2626] mt-1.5">
                  [CẢNH BÁO GIÁ NÔNG SẢN] {emailPreviewRule.ruleName}
                </h4>
              </div>

              <div className="p-3 rounded-md bg-white border border-[#E2E8F0] space-y-1.5">
                <div className="flex justify-between">
                  <span className="text-[#475569]">Mặt hàng:</span>
                  <strong className="text-[#0F172A]">{emailPreviewRule.commodityName}</strong>
                </div>
                <div className="flex justify-between">
                  <span className="text-[#475569]">Ngưỡng thiết lập:</span>
                  <strong className="text-[#0F172A] font-mono tabular-nums">
                    {formatNumberVN(emailPreviewRule.thresholdValue)}{' '}
                    {getCommodityUnit(emailPreviewRule.commodityName)}
                  </strong>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 pt-1">
              <button
                type="button"
                onClick={() => setEmailPreviewRule(null)}
                className="px-3.5 py-1.5 rounded-md bg-white border border-[#E2E8F0] text-[#475569] font-semibold text-xs"
              >
                Đóng
              </button>
              <button
                type="button"
                onClick={() => {
                  void handleTestAlert(emailPreviewRule);
                  setEmailPreviewRule(null);
                }}
                className="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-md bg-[#166534] hover:bg-[#15803D] text-white font-semibold text-xs"
              >
                <Send className="w-3.5 h-3.5" />
                <span>Gửi thử Email này</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
