'use client';

import React, { useState, useEffect } from 'react';
import Header from '@/components/layout/Header';
import { INITIAL_ALERT_RULES, COMMODITIES_DATA } from '@/lib/mockData';
import { AlertRuleItem, AlertLogItem } from '@/types';
import {
  fetchAlertRules,
  createAlertRuleApi,
  toggleAlertRuleApi,
  deleteAlertRuleApi,
  testAlertApi,
  fetchAlertLogsApi,
} from '@/lib/api';
import {
  BellRing,
  Plus,
  Trash2,
  CheckCircle2,
  Send,
  Mail,
  Activity,
  ShieldCheck,
  TrendingUp,
  TrendingDown,
  History,
  Eye,
  RefreshCw,
  Clock,
  Sparkles,
  Layers,
  AlertTriangle,
  Zap,
} from 'lucide-react';

export default function AlertsPage() {
  const [rules, setRules] = useState<AlertRuleItem[]>(INITIAL_ALERT_RULES);
  const [logs, setLogs] = useState<AlertLogItem[]>([]);
  const [activeTab, setActiveTab] = useState<'rules' | 'logs'>('rules');
  const [showModal, setShowModal] = useState(false);
  const [testNotificationMsg, setTestNotificationMsg] = useState<string | null>(null);
  const [emailPreviewRule, setEmailPreviewRule] = useState<AlertRuleItem | null>(null);
  const [loadingLogs, setLoadingLogs] = useState(false);

  // Form State
  const [formCommodityId, setFormCommodityId] = useState(2);
  const [formRuleName, setFormRuleName] = useState('');
  const [formCondition, setFormCondition] = useState<AlertRuleItem['conditionType']>('PRICE_ABOVE');
  const [formThreshold, setFormThreshold] = useState('');
  const [formEmail, setFormEmail] = useState('anhnguyen.analyst@agroforecast.vn');

  // Load rules & logs from API
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [liveRules, liveLogs] = await Promise.all([
        fetchAlertRules(),
        fetchAlertLogsApi(),
      ]);
      if (liveRules && liveRules.length > 0) {
        setRules(liveRules);
      }
      if (liveLogs && liveLogs.length > 0) {
        setLogs(liveLogs);
      }
    } catch (err) {
      console.error('Error loading alert data:', err);
    }
  };

  const handleRefreshLogs = async () => {
    setLoadingLogs(true);
    try {
      const liveLogs = await fetchAlertLogsApi();
      setLogs(liveLogs);
    } catch (err) {
      console.error('Error refreshing logs:', err);
    } finally {
      setLoadingLogs(false);
    }
  };

  const handleToggle = async (id: number) => {
    const target = rules.find((r) => r.id === id);
    if (!target) return;
    const nextState = !target.isActive;

    setRules((prev) =>
      prev.map((r) => (r.id === id ? { ...r, isActive: nextState } : r))
    );

    await toggleAlertRuleApi(id, nextState);
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Bạn có chắc chắn muốn xóa quy tắc cảnh báo này?')) return;
    setRules((prev) => prev.filter((r) => r.id !== id));
    await deleteAlertRuleApi(id);
  };

  const handleCreateRule = async (e: React.FormEvent) => {
    e.preventDefault();
    const commodity = COMMODITIES_DATA.find((c) => c.id === formCommodityId);
    if (!commodity) return;

    const payload = {
      commodity_id: formCommodityId,
      rule_name: formRuleName || `Cảnh báo ${commodity.name}`,
      condition_type: formCondition,
      threshold_value: Number(formThreshold) || 0,
      email: formEmail,
    };

    const created = await createAlertRuleApi(payload);
    if (created) {
      setRules([created, ...rules]);
    } else {
      // Local fallback
      const localRule: AlertRuleItem = {
        id: Date.now(),
        commodityId: formCommodityId,
        commodityName: commodity.name,
        ruleName: payload.rule_name,
        conditionType: formCondition,
        thresholdValue: payload.threshold_value,
        email: formEmail,
        isActive: true,
        createdAt: new Date().toLocaleDateString('vi-VN'),
      };
      setRules([localRule, ...rules]);
    }

    setShowModal(false);
    setFormRuleName('');
    setFormThreshold('');
    setTestNotificationMsg('Đã tạo và kích hoạt quy tắc cảnh báo mới thành công!');
    setTimeout(() => setTestNotificationMsg(null), 4000);
  };

  const handleTestAlert = async (rule: AlertRuleItem) => {
    const res = await testAlertApi(rule.id);
    setTestNotificationMsg(res?.message || `Đã kích hoạt cảnh báo thử nghiệm cho "${rule.ruleName}" đến ${rule.email}!`);
    setTimeout(() => setTestNotificationMsg(null), 4500);

    // Append a log entry to local logs
    const newLog: AlertLogItem = {
      id: Date.now(),
      ruleId: rule.id,
      ruleName: rule.ruleName,
      commodityName: rule.commodityName,
      triggeredPrice: rule.thresholdValue,
      message: `[Thử nghiệm] Giá thị trường chạm ngưỡng ${Number(rule.thresholdValue).toLocaleString('vi-VN')} đ - Gửi tới ${rule.email}`,
      status: 'SENT',
      triggeredAt: new Date().toLocaleTimeString('vi-VN') + ' Hôm nay',
      email: rule.email,
    };
    setLogs([newLog, ...logs]);
  };

  // Compute stats
  const activeCount = rules.filter((r) => r.isActive).length;
  const totalCount = rules.length;
  const totalLogsCount = logs.length;

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <Header
        title="Quản lý Cảnh báo Thị trường"
        subtitle="Hệ thống giám sát biến động giá, phát hiện bất thường AI & kích hoạt thông báo tự động"
        showLiveBadge={true}
      />

      {/* Toast Banner */}
      {testNotificationMsg && (
        <div className="p-4 rounded-2xl bg-brand/10 border border-brand/30 text-brand flex items-center justify-between gap-3 animate-in fade-in slide-in-from-top-2 shadow-sm">
          <div className="flex items-center gap-2.5">
            <CheckCircle2 className="w-5 h-5 text-brand shrink-0" />
            <span className="text-xs font-bold text-primary-text">{testNotificationMsg}</span>
          </div>
          <button
            onClick={() => setTestNotificationMsg(null)}
            className="text-secondary-text hover:text-primary-text text-xs font-bold"
          >
            Đóng
          </button>
        </div>
      )}

      {/* 4 Professional KPI Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-card rounded-2xl border border-border-subtle p-5 shadow-card relative overflow-hidden group hover:border-brand/40 transition-all">
          <div className="flex items-center justify-between mb-2.5">
            <span className="text-xs font-bold text-secondary-text uppercase tracking-wider">Tổng số Quy tắc</span>
            <div className="w-8 h-8 rounded-xl bg-amber-500/10 text-amber-600 flex items-center justify-center">
              <Layers className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-black text-primary-text">{totalCount}</span>
            <span className="text-xs font-semibold text-secondary-text">quy tắc</span>
          </div>
          <p className="text-[11px] text-secondary-text mt-2 flex items-center gap-1">
            Lúa gạo, Cà phê, Tiêu, Mía đường
          </p>
        </div>

        <div className="bg-card rounded-2xl border border-border-subtle p-5 shadow-card relative overflow-hidden group hover:border-brand/40 transition-all">
          <div className="flex items-center justify-between mb-2.5">
            <span className="text-xs font-bold text-secondary-text uppercase tracking-wider">Đang Giám sát</span>
            <div className="w-8 h-8 rounded-xl bg-emerald-500/10 text-emerald-600 flex items-center justify-center">
              <Activity className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-black text-emerald-600">{activeCount}</span>
            <span className="text-xs font-bold text-emerald-600 bg-emerald-500/10 px-2 py-0.5 rounded-md">
              Kích hoạt
            </span>
          </div>
          <p className="text-[11px] text-secondary-text mt-2 flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" /> Đang theo dõi theo từng phiên
          </p>
        </div>

        <div className="bg-card rounded-2xl border border-border-subtle p-5 shadow-card relative overflow-hidden group hover:border-brand/40 transition-all">
          <div className="flex items-center justify-between mb-2.5">
            <span className="text-xs font-bold text-secondary-text uppercase tracking-wider">Cảnh báo Đã kích hoạt</span>
            <div className="w-8 h-8 rounded-xl bg-purple-500/10 text-purple-600 flex items-center justify-center">
              <Zap className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-black text-purple-700">{totalLogsCount}</span>
            <span className="text-xs font-semibold text-secondary-text">thông báo</span>
          </div>
          <p className="text-[11px] text-secondary-text mt-2 flex items-center gap-1">
            <Clock className="w-3 h-3 text-secondary-text/70" /> Ghi nhận vào CSDL PostgreSQL
          </p>
        </div>

        <div className="bg-card rounded-2xl border border-border-subtle p-5 shadow-card relative overflow-hidden group hover:border-brand/40 transition-all">
          <div className="flex items-center justify-between mb-2.5">
            <span className="text-xs font-bold text-secondary-text uppercase tracking-wider">Độ tin cậy Gửi Mail</span>
            <div className="w-8 h-8 rounded-xl bg-blue-500/10 text-blue-600 flex items-center justify-center">
              <ShieldCheck className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-black text-primary-text">99.4%</span>
            <span className="text-xs font-bold text-blue-600 bg-blue-500/10 px-2 py-0.5 rounded-md">
              SMTP TLS
            </span>
          </div>
          <p className="text-[11px] text-secondary-text mt-2 flex items-center gap-1">
            Giao thức SMTP Gmail & Email Server
          </p>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex items-center justify-between border-b border-border-subtle pb-px">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setActiveTab('rules')}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-t-xl text-xs font-bold transition-all border-b-2 ${
              activeTab === 'rules'
                ? 'border-brand text-brand bg-brand/5'
                : 'border-transparent text-secondary-text hover:text-primary-text hover:bg-black/[0.02]'
            }`}
          >
            <BellRing className="w-4 h-4" />
            Danh sách Quy tắc Cảnh báo ({rules.length})
          </button>

          <button
            onClick={() => setActiveTab('logs')}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-t-xl text-xs font-bold transition-all border-b-2 ${
              activeTab === 'logs'
                ? 'border-brand text-brand bg-brand/5'
                : 'border-transparent text-secondary-text hover:text-primary-text hover:bg-black/[0.02]'
            }`}
          >
            <History className="w-4 h-4" />
            Lịch sử Kích hoạt & Audit Logs ({logs.length})
          </button>
        </div>

        {activeTab === 'rules' && (
          <button
            onClick={() => setShowModal(true)}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-brand hover:bg-brand-dark text-white text-xs font-bold transition-all shadow-sm"
          >
            <Plus className="w-4 h-4" />
            <span>Thêm quy tắc mới</span>
          </button>
        )}

        {activeTab === 'logs' && (
          <button
            onClick={handleRefreshLogs}
            disabled={loadingLogs}
            className="flex items-center gap-2 px-3.5 py-1.5 rounded-xl border border-border-subtle bg-canvas text-secondary-text hover:text-brand text-xs font-bold transition-all"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loadingLogs ? 'animate-spin' : ''}`} />
            <span>Làm mới nhật ký</span>
          </button>
        )}
      </div>

      {/* TAB 1: RULES TABLE */}
      {activeTab === 'rules' && (
        <div className="space-y-4">
          <div className="bg-card rounded-2xl border border-border-subtle p-6 shadow-card">
            <div className="overflow-x-auto custom-scrollbar">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="border-b border-border-subtle text-secondary-text font-bold uppercase tracking-wider text-[11px]">
                    <th className="py-3 px-4">Tên quy tắc</th>
                    <th className="py-3 px-4">Nông sản</th>
                    <th className="py-3 px-4">Điều kiện kích hoạt</th>
                    <th className="py-3 px-4">Email nhận</th>
                    <th className="py-3 px-4 text-center">Trạng thái</th>
                    <th className="py-3 px-4 text-right">Thao tác</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border-subtle/60">
                  {rules.map((rule) => {
                    const val = Number(rule.thresholdValue ?? 0);
                    const formattedVal = val.toLocaleString('vi-VN');
                    const condType = rule.conditionType || 'PRICE_ABOVE';

                    let badgeColor = 'bg-canvas border-border-subtle text-primary-text';
                    let conditionLabel = `Giá > ${formattedVal} đ/kg`;
                    let IconComponent = TrendingUp;

                    if (condType === 'PRICE_ABOVE') {
                      badgeColor = 'bg-rose-500/10 border-rose-200 text-rose-700';
                      conditionLabel = `Giá > ${formattedVal} đ/kg (Vượt trần)`;
                      IconComponent = TrendingUp;
                    } else if (condType === 'PRICE_BELOW') {
                      badgeColor = 'bg-blue-500/10 border-blue-200 text-blue-700';
                      conditionLabel = `Giá < ${formattedVal} đ/kg (Chạm sàn)`;
                      IconComponent = TrendingDown;
                    } else if (condType === 'PCT_INC_7D') {
                      badgeColor = 'bg-amber-500/10 border-amber-200 text-amber-700';
                      conditionLabel = `Tăng > +${formattedVal}% trong 7 ngày`;
                      IconComponent = TrendingUp;
                    } else if (condType === 'PCT_DEC_7D') {
                      badgeColor = 'bg-orange-500/10 border-orange-200 text-orange-700';
                      conditionLabel = `Giảm sâu > -${formattedVal}% trong 7 ngày`;
                      IconComponent = TrendingDown;
                    } else if (condType === 'OUT_OF_CI_95') {
                      badgeColor = 'bg-purple-500/10 border-purple-200 text-purple-700 font-bold';
                      conditionLabel = `Lệch Dải tin cậy 95% mô hình AI`;
                      IconComponent = Sparkles;
                    }

                    return (
                      <tr key={rule.id} className="hover:bg-black/[0.01] transition-colors">
                        <td className="py-3.5 px-4 font-bold text-primary-text max-w-xs">
                          {rule.ruleName}
                          <span className="text-[10px] text-secondary-text/70 block mt-0.5">
                            Ngày tạo: {rule.createdAt || 'Hôm nay'}
                          </span>
                        </td>
                        <td className="py-3.5 px-4">
                          <span className="font-bold text-brand text-xs">
                            {rule.commodityName}
                          </span>
                        </td>
                        <td className="py-3.5 px-4">
                          <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg border font-mono font-semibold text-xs ${badgeColor}`}>
                            <IconComponent className="w-3.5 h-3.5 shrink-0" />
                            {conditionLabel}
                          </span>
                        </td>
                        <td className="py-3.5 px-4 text-secondary-text">
                          <div className="flex items-center gap-1.5">
                            <Mail className="w-3.5 h-3.5 text-secondary-text/80 shrink-0" />
                            <span className="truncate max-w-[200px]" title={rule.email}>
                              {rule.email}
                            </span>
                          </div>
                        </td>
                        <td className="py-3.5 px-4 text-center">
                          <button
                            onClick={() => handleToggle(rule.id)}
                            className={`w-11 h-6 rounded-full transition-colors relative p-0.5 inline-block ${
                              rule.isActive ? 'bg-brand' : 'bg-[#D4CEBE]'
                            }`}
                            title={rule.isActive ? 'Đang bật - Nhấp để tắt' : 'Đang tắt - Nhấp để bật'}
                          >
                            <div
                              className={`w-5 h-5 rounded-full bg-white transition-transform ${
                                rule.isActive ? 'translate-x-5' : 'translate-x-0'
                              }`}
                            />
                          </button>
                        </td>
                        <td className="py-3.5 px-4 text-right">
                          <div className="flex items-center justify-end gap-1.5">
                            <button
                              onClick={() => setEmailPreviewRule(rule)}
                              title="Xem trước nội dung Email"
                              className="p-1.5 rounded-lg border border-border-subtle bg-canvas hover:bg-black/5 text-secondary-text hover:text-brand transition-all"
                            >
                              <Eye className="w-4 h-4" />
                            </button>

                            <button
                              onClick={() => handleTestAlert(rule)}
                              title="Gửi thử nghiệm cảnh báo ngay"
                              className="p-1.5 rounded-lg border border-border-subtle bg-canvas hover:bg-brand/10 text-brand transition-all"
                            >
                              <Send className="w-4 h-4" />
                            </button>

                            <button
                              onClick={() => handleDelete(rule.id)}
                              title="Xóa quy tắc này"
                              className="p-1.5 rounded-lg border border-border-subtle bg-canvas hover:bg-rose-500/10 text-secondary-text hover:text-rose-600 transition-all"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: AUDIT LOGS (LỊCH SỬ KÍCH HOẠT CẢNH BÁO) */}
      {activeTab === 'logs' && (
        <div className="bg-card rounded-2xl border border-border-subtle p-6 shadow-card space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h3 className="text-base font-bold text-primary-text flex items-center gap-2">
                <History className="w-4 h-4 text-brand" /> Nhật ký Kích hoạt Cảnh báo (Audit Trail)
              </h3>
              <p className="text-xs text-secondary-text mt-0.5">
                Lịch sử các sự kiện chạm ngưỡng giá và gửi thông báo qua giao thức SMTP tới người dùng
              </p>
            </div>
            <span className="px-3 py-1 rounded-lg bg-emerald-500/10 text-emerald-700 font-bold text-xs border border-emerald-200">
              ● Đồng bộ bảng alert_logs (PostgreSQL)
            </span>
          </div>

          <div className="overflow-x-auto custom-scrollbar">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-border-subtle text-secondary-text font-bold uppercase tracking-wider text-[11px]">
                  <th className="py-3 px-4">Thời gian</th>
                  <th className="py-3 px-4">Quy tắc áp dụng</th>
                  <th className="py-3 px-4">Nông sản</th>
                  <th className="py-3 px-4">Mức giá vi phạm</th>
                  <th className="py-3 px-4">Nội dung thông báo</th>
                  <th className="py-3 px-4">Email nhận</th>
                  <th className="py-3 px-4 text-center">Trạng thái</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-subtle/60">
                {logs.map((log) => (
                  <tr key={log.id} className="hover:bg-black/[0.01] transition-colors">
                    <td className="py-3.5 px-4 font-mono font-semibold text-secondary-text whitespace-nowrap">
                      {log.triggeredAt}
                    </td>
                    <td className="py-3.5 px-4 font-bold text-primary-text">
                      {log.ruleName}
                    </td>
                    <td className="py-3.5 px-4 font-semibold text-brand">
                      {log.commodityName}
                    </td>
                    <td className="py-3.5 px-4 font-mono font-bold text-primary-text">
                      {log.triggeredPrice ? `${Number(log.triggeredPrice).toLocaleString('vi-VN')} đ` : '—'}
                    </td>
                    <td className="py-3.5 px-4 text-secondary-text max-w-sm line-clamp-1" title={log.message}>
                      {log.message}
                    </td>
                    <td className="py-3.5 px-4 text-secondary-text text-[11px]">
                      {log.email}
                    </td>
                    <td className="py-3.5 px-4 text-center whitespace-nowrap">
                      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-emerald-500/10 text-emerald-700 font-bold text-[10px] uppercase border border-emerald-200">
                        <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                        {log.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* CREATE RULE MODAL */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-card rounded-3xl border border-border-subtle p-6 max-w-lg w-full shadow-2xl space-y-4 animate-in fade-in zoom-in-95">
            <div className="flex items-center justify-between border-b border-border-subtle pb-3">
              <h3 className="text-base font-bold text-primary-text flex items-center gap-2">
                <BellRing className="w-5 h-5 text-brand" /> Thiết lập quy tắc cảnh báo mới
              </h3>
              <button
                onClick={() => setShowModal(false)}
                className="text-secondary-text hover:text-primary-text font-bold text-sm"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleCreateRule} className="space-y-3.5 text-xs">
              <div>
                <label className="font-bold text-secondary-text uppercase tracking-wider block mb-1">
                  Nông sản theo dõi
                </label>
                <select
                  value={formCommodityId}
                  onChange={(e) => setFormCommodityId(Number(e.target.value))}
                  className="w-full bg-canvas border border-border-subtle rounded-xl p-2.5 text-primary-text font-semibold focus:outline-none focus:border-brand"
                >
                  {COMMODITIES_DATA.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name} ({c.unit})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="font-bold text-secondary-text uppercase tracking-wider block mb-1">
                  Tên gợi nhớ quy tắc
                </label>
                <input
                  type="text"
                  required
                  placeholder="VD: Cảnh báo giá cà phê chạm đỉnh 125,000..."
                  value={formRuleName}
                  onChange={(e) => setFormRuleName(e.target.value)}
                  className="w-full bg-canvas border border-border-subtle rounded-xl p-2.5 text-primary-text font-medium focus:outline-none focus:border-brand"
                />
              </div>

              <div>
                <label className="font-bold text-secondary-text uppercase tracking-wider block mb-1">
                  Điều kiện kích hoạt thông minh
                </label>
                <select
                  value={formCondition}
                  onChange={(e) => setFormCondition(e.target.value as AlertRuleItem['conditionType'])}
                  className="w-full bg-canvas border border-border-subtle rounded-xl p-2.5 text-primary-text font-semibold focus:outline-none focus:border-brand"
                >
                  <option value="PRICE_ABOVE">Vượt mức giá trần (Giá &gt; Ngưỡng)</option>
                  <option value="PRICE_BELOW">Sụt giảm dưới mức sàn (Giá &lt; Ngưỡng)</option>
                  <option value="PCT_INC_7D">Tăng đột biến trong 7 ngày (&gt; %)</option>
                  <option value="PCT_DEC_7D">Giảm sâu liên tiếp 7 ngày (&gt; %)</option>
                  <option value="OUT_OF_CI_95">Bất thường: Lệch khỏi dải tin cậy 95% mô hình AI</option>
                </select>
              </div>

              <div>
                <label className="font-bold text-secondary-text uppercase tracking-wider block mb-1">
                  Giá trị ngưỡng kích hoạt (VNĐ hoặc %)
                </label>
                <input
                  type="number"
                  required
                  placeholder="VD: 65000 (cho giá) hoặc 5 (cho %)"
                  value={formThreshold}
                  onChange={(e) => setFormThreshold(e.target.value)}
                  className="w-full bg-canvas border border-border-subtle rounded-xl p-2.5 text-primary-text font-semibold focus:outline-none focus:border-brand"
                />
              </div>

              <div>
                <label className="font-bold text-secondary-text uppercase tracking-wider block mb-1">
                  Email nhận thông báo
                </label>
                <input
                  type="email"
                  required
                  value={formEmail}
                  onChange={(e) => setFormEmail(e.target.value)}
                  className="w-full bg-canvas border border-border-subtle rounded-xl p-2.5 text-primary-text font-medium focus:outline-none focus:border-brand"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-border-subtle">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-xl text-secondary-text hover:bg-black/5 font-bold"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-brand text-white font-bold transition-all shadow-sm hover:bg-brand/90"
                >
                  Lưu & Kích hoạt
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* EMAIL PREVIEW MODAL */}
      {emailPreviewRule && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-card rounded-3xl border border-border-subtle p-6 max-w-lg w-full shadow-2xl space-y-4 animate-in fade-in zoom-in-95">
            <div className="flex items-center justify-between border-b border-border-subtle pb-3">
              <h3 className="text-base font-bold text-primary-text flex items-center gap-2">
                <Mail className="w-5 h-5 text-brand" /> Xem trước Email Thông báo
              </h3>
              <button
                onClick={() => setEmailPreviewRule(null)}
                className="text-secondary-text hover:text-primary-text font-bold text-sm"
              >
                ✕
              </button>
            </div>

            {/* Email Shell Simulation */}
            <div className="rounded-2xl border border-border-subtle bg-white text-gray-800 p-5 shadow-sm space-y-4 text-xs">
              <div className="flex items-center justify-between border-b border-gray-100 pb-3">
                <div className="flex items-center gap-2 font-bold text-sm text-gray-900">
                  <div className="w-7 h-7 rounded-lg bg-emerald-800 text-white flex items-center justify-center font-black text-xs">
                    AF
                  </div>
                  <span>AgroForecast Alert Engine</span>
                </div>
                <span className="text-[11px] text-gray-400">Gửi qua SMTP TLS</span>
              </div>

              <div>
                <p className="text-gray-500 text-[11px]">Người nhận: <strong className="text-gray-900">{emailPreviewRule.email}</strong></p>
                <h4 className="text-base font-extrabold text-red-600 mt-2">
                  [CẢNH BÁO THỊ TRƯỜNG] {emailPreviewRule.ruleName}
                </h4>
              </div>

              <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-500">Mặt hàng:</span>
                  <strong className="text-gray-900 font-bold">{emailPreviewRule.commodityName}</strong>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Ngưỡng kích hoạt:</span>
                  <strong className="text-gray-900 font-mono">
                    {Number(emailPreviewRule.thresholdValue).toLocaleString('vi-VN')} VNĐ
                  </strong>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Mức giá thị trường:</span>
                  <strong className="text-red-600 font-mono font-bold text-sm">
                    {Number(emailPreviewRule.thresholdValue * 1.02).toLocaleString('vi-VN')} VNĐ
                  </strong>
                </div>
              </div>

              <div className="p-3 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-[11px] space-y-1">
                <div className="flex items-center gap-1 font-bold">
                  <AlertTriangle className="w-3.5 h-3.5 text-amber-700" />
                  <span>Khuyến nghị từ Hệ thống Phân tích AgroForecast:</span>
                </div>
                <p>
                  Mức giá đang có xu hướng vượt ngưỡng rủi ro. Các nhà phân tích và thương lái nên cân nhắc chốt hợp đồng tương lai hoặc điều chỉnh kế hoạch thu mua kho bãi.
                </p>
              </div>

              <div className="pt-2 border-t border-gray-100 text-[10px] text-gray-400 flex items-center justify-between">
                <span>Dự án Tốt nghiệp AgroForecast 2026</span>
                <span>Hệ thống Tự động hóa Cảnh báo Nông sản</span>
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 pt-1">
              <button
                onClick={() => setEmailPreviewRule(null)}
                className="px-4 py-2 rounded-xl text-secondary-text hover:bg-black/5 font-bold text-xs"
              >
                Đóng
              </button>
              <button
                onClick={() => {
                  handleTestAlert(emailPreviewRule);
                  setEmailPreviewRule(null);
                }}
                className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-brand text-white font-bold text-xs hover:bg-brand/90 transition-all shadow-sm"
              >
                <Send className="w-3.5 h-3.5" /> Gửi thử Email này
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
