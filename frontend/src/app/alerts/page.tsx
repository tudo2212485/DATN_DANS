'use client';

import React, { useState, useEffect } from 'react';
import Header from '@/components/layout/Header';
import { INITIAL_ALERT_RULES, COMMODITIES_DATA } from '@/lib/mockData';
import { AlertRuleItem } from '@/types';
import {
  fetchAlertRules,
  createAlertRuleApi,
  toggleAlertRuleApi,
  deleteAlertRuleApi,
  testAlertApi,
} from '@/lib/api';
import { BellRing, Plus, Trash2, CheckCircle2, Send, Mail } from 'lucide-react';

export default function AlertsPage() {
  const [rules, setRules] = useState<AlertRuleItem[]>(INITIAL_ALERT_RULES);
  const [showModal, setShowModal] = useState(false);
  const [testNotificationMsg, setTestNotificationMsg] = useState<string | null>(null);

  // Form State
  const [formCommodityId, setFormCommodityId] = useState(2);
  const [formRuleName, setFormRuleName] = useState('');
  const [formCondition, setFormCondition] = useState<AlertRuleItem['conditionType']>('PRICE_ABOVE');
  const [formThreshold, setFormThreshold] = useState('');
  const [formEmail, setFormEmail] = useState('anhnguyen.analyst@agroforecast.vn');

  // Load rules from API
  useEffect(() => {
    async function loadRules() {
      try {
        const liveRules = await fetchAlertRules();
        if (liveRules && liveRules.length > 0) {
          setRules(liveRules);
        }
      } catch (err) {
        console.error('Error loading rules:', err);
      }
    }
    loadRules();
  }, []);

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
  };

  const handleTestAlert = async (rule: AlertRuleItem) => {
    const res = await testAlertApi(rule.id);
    setTestNotificationMsg(res?.message || `Đã gửi cảnh báo cho quy tắc "${rule.ruleName}" đến ${rule.email}!`);
    setTimeout(() => setTestNotificationMsg(null), 4000);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <Header
        title="Quản lý Cảnh báo Thị trường"
        subtitle="Thiết lập điều kiện cảnh báo tự động đồng bộ CSDL PostgreSQL"
        showLiveBadge={false}
      />

      {/* Notification banner */}
      {testNotificationMsg && (
        <div className="p-4 rounded-2xl bg-brand-badge border border-brand/30 text-brand flex items-center gap-3 animate-fade-in shadow-sm">
          <CheckCircle2 className="w-5 h-5 shrink-0" />
          <span className="text-xs font-bold">{testNotificationMsg}</span>
        </div>
      )}

      {/* Action Bar */}
      <div className="bg-card rounded-2xl border border-border-subtle p-5 shadow-card flex items-center justify-between flex-wrap gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-brand-badge flex items-center justify-center text-brand">
            <BellRing className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-primary-text">
              Quy tắc cảnh báo đang chạy
            </h2>
            <p className="text-xs text-secondary-text">
              Dữ liệu được lưu trữ trực tiếp trong bảng alert_rules của PostgreSQL.
            </p>
          </div>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-brand hover:bg-brand-dark text-white text-xs font-bold transition-all shadow-sm"
        >
          <Plus className="w-4 h-4" />
          <span>Thêm quy tắc mới</span>
        </button>
      </div>

      {/* Rules Table */}
      <div className="bg-card rounded-2xl border border-border-subtle p-6 shadow-card">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-border-subtle text-secondary-text font-bold uppercase tracking-wider pb-2">
                <th className="py-3 px-3">Tên quy tắc</th>
                <th className="py-3 px-3">Nông sản</th>
                <th className="py-3 px-3">Điều kiện kích hoạt</th>
                <th className="py-3 px-3">Email nhận</th>
                <th className="py-3 px-3 text-center">Trạng thái</th>
                <th className="py-3 px-3 text-right">Thao tác</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle">
              {rules.map((rule) => {
                const val = Number(rule.thresholdValue ?? 0);
                const formattedVal = val.toLocaleString('vi-VN');
                const condType = rule.conditionType || 'PRICE_ABOVE';
                const conditionLabel =
                  condType === 'PRICE_ABOVE'
                    ? `Giá > ${formattedVal} đ/kg`
                    : condType === 'PRICE_BELOW'
                    ? `Giá < ${formattedVal} đ/kg`
                    : condType === 'PCT_INC_7D'
                    ? `Tăng > +${formattedVal}% trong 7 ngày`
                    : `Giảm > -${formattedVal}% trong 7 ngày`;

                return (
                  <tr key={rule.id} className="hover:bg-canvas/50 transition-colors">
                    <td className="py-3.5 px-3 font-bold text-primary-text max-w-xs">
                      {rule.ruleName}
                    </td>
                    <td className="py-3.5 px-3">
                      <span className="font-semibold text-primary-text">
                        {rule.commodityName}
                      </span>
                    </td>
                    <td className="py-3.5 px-3">
                      <span className="px-2.5 py-1 rounded-lg bg-canvas border border-border-subtle font-mono font-bold text-primary-text">
                        {conditionLabel}
                      </span>
                    </td>
                    <td className="py-3.5 px-3 text-secondary-text flex items-center gap-1.5">
                      <Mail className="w-3.5 h-3.5 text-secondary-text/80" />
                      <span>{rule.email}</span>
                    </td>
                    <td className="py-3.5 px-3 text-center">
                      <button
                        onClick={() => handleToggle(rule.id)}
                        className={`w-11 h-6 rounded-full transition-colors relative p-0.5 inline-block ${
                          rule.isActive ? 'bg-brand' : 'bg-[#D4CEBE]'
                        }`}
                      >
                        <div
                          className={`w-5 h-5 rounded-full bg-white transition-transform ${
                            rule.isActive ? 'translate-x-5' : 'translate-x-0'
                          }`}
                        />
                      </button>
                    </td>
                    <td className="py-3.5 px-3 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleTestAlert(rule)}
                          title="Gửi thử cảnh báo"
                          className="p-1.5 rounded-lg hover:bg-brand-light text-brand transition-colors"
                        >
                          <Send className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(rule.id)}
                          title="Xóa quy tắc"
                          className="p-1.5 rounded-lg hover:bg-accent-coralLight text-accent-coral transition-colors"
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

      {/* Create Rule Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-card rounded-3xl border border-border-subtle p-6 max-w-md w-full shadow-2xl space-y-4 animate-scale-in">
            <div className="flex items-center justify-between border-b border-border-subtle pb-3">
              <h3 className="text-base font-bold text-primary-text">
                Thiết lập quy tắc cảnh báo mới
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
                  className="w-full bg-canvas border border-border-subtle rounded-xl p-2.5 text-primary-text font-semibold focus:outline-none focus:ring-2 focus:ring-brand/30"
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
                  placeholder="VD: Cảnh báo giá cà phê chạm đỉnh..."
                  value={formRuleName}
                  onChange={(e) => setFormRuleName(e.target.value)}
                  className="w-full bg-canvas border border-border-subtle rounded-xl p-2.5 text-primary-text font-medium focus:outline-none focus:ring-2 focus:ring-brand/30"
                />
              </div>

              <div>
                <label className="font-bold text-secondary-text uppercase tracking-wider block mb-1">
                  Điều kiện kích hoạt
                </label>
                <select
                  value={formCondition}
                  onChange={(e) => setFormCondition(e.target.value as AlertRuleItem['conditionType'])}
                  className="w-full bg-canvas border border-border-subtle rounded-xl p-2.5 text-primary-text font-semibold focus:outline-none focus:ring-2 focus:ring-brand/30"
                >
                  <option value="PRICE_ABOVE">Vượt mức giá trần (Lớn hơn ngưỡng)</option>
                  <option value="PRICE_BELOW">Giảm dưới mức sàn (Nhỏ hơn ngưỡng)</option>
                  <option value="PCT_INC_7D">Tăng đột biến trong 7 ngày (&gt; %)</option>
                  <option value="PCT_DEC_7D">Giảm sâu trong 7 ngày (&gt; %)</option>
                </select>
              </div>

              <div>
                <label className="font-bold text-secondary-text uppercase tracking-wider block mb-1">
                  Giá trị ngưỡng kích hoạt
                </label>
                <input
                  type="number"
                  required
                  placeholder="VD: 65000 (đối với giá) hoặc 5 (đối với %)"
                  value={formThreshold}
                  onChange={(e) => setFormThreshold(e.target.value)}
                  className="w-full bg-canvas border border-border-subtle rounded-xl p-2.5 text-primary-text font-semibold focus:outline-none focus:ring-2 focus:ring-brand/30"
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
                  className="w-full bg-canvas border border-border-subtle rounded-xl p-2.5 text-primary-text font-medium focus:outline-none focus:ring-2 focus:ring-brand/30"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-border-subtle">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-xl text-secondary-text hover:bg-canvas font-bold"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-brand hover:bg-brand-dark text-white font-bold transition-all shadow-sm"
                >
                  Lưu quy tắc
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
