'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import {
  fetchHistory,
  fetchHistorySources,
  HistoryResponse,
  HistorySource,
} from '@/lib/api';
import Header from '@/components/layout/Header';
import AgroGrid, { AgroColumn } from '@/components/ui/AgroGrid';
import FinChart from '@/components/ui/FinChart';
import {
  formatDateVN,
  formatNumberVN,
  formatPct,
  getCommodityUnit,
} from '@/lib/formatters';
import { useLocation } from '@/contexts/LocationContext';
import { ArrowRight, MapPin } from 'lucide-react';

function shiftIsoDate(baseIso: string, deltaDays: number): string {
  const [y, m, d] = baseIso.split('-').map(Number);
  const dt = new Date(y || 2026, (m || 9) - 1, d || 4);
  dt.setDate(dt.getDate() + deltaDays);
  return `${dt.getFullYear()}-${String(dt.getMonth() + 1).padStart(2, '0')}-${String(dt.getDate()).padStart(2, '0')}`;
}

const provenanceLabel: Record<string, string> = {
  collected: 'Thu thập tự động',
  reviewed: 'Đã xác minh',
  unverified: 'Chưa xác minh',
};

const isSafeHttpUrl = (value: unknown): value is string =>
  typeof value === 'string' && /^https?:\/\//i.test(value.trim());

function parseLocalIsoDate(iso: string): Date {
  const [y, m, d] = iso.split('-').map(Number);
  return new Date(y || 2026, (m || 1) - 1, d || 1);
}

export default function HistoryPage() {
  const { provinceCode, provinceName } = useLocation();
  const [sources, setSources] = useState<HistorySource[]>([]);
  const [commodityId, setCommodityId] = useState(2);
  const [anchorEnd, setAnchorEnd] = useState<string>('2026-11-22');
  const [start, setStart] = useState<string>('');
  const [end, setEnd] = useState<string>('');
  const [data, setData] = useState<HistoryResponse | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const id = Number(new URLSearchParams(window.location.search).get('commodity_id'));
    const initialCid = id > 0 ? id : 2;
    if (id > 0) setCommodityId(id);

    fetchHistorySources()
      .then((list) => {
        setSources(list);
        const current = list.find((s) => s.id === initialCid) || list[0];
        const latest = current?.latest_date || '2026-09-04';
        setAnchorEnd(latest);
        setEnd(latest);
        setStart(shiftIsoDate(latest, -89));
      })
      .catch((e) => setError(e.message));
  }, []);

  const handleSelectCommodity = (newId: number) => {
    setCommodityId(newId);
    const target = sources.find((s) => s.id === newId);
    if (target?.latest_date) {
      setAnchorEnd(target.latest_date);
      setEnd(target.latest_date);
      setStart(shiftIsoDate(target.latest_date, -89));
    }
  };

  useEffect(() => {
    if (!start || !end) return;
    let cancelled = false;
    setLoading(true);
    setError('');
    fetchHistory(commodityId, start, end, false, provinceCode)
      .then((d) => {
        if (!cancelled) setData(d);
      })
      .catch((e) => {
        if (!cancelled) setError(e.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [commodityId, start, end, provinceCode]);

  const source = sources.find((s) => s.id === commodityId);
  const currentUnit = getCommodityUnit(source?.name, source?.unit);

  // Deduplicate by YYYY-MM-DD and sort strictly ascending so multi-year DateTime charts never loop back
  const chart = (() => {
    const byDay = new Map<string, { date: string; price: number }>();
    for (const r of data?.records || []) {
      if (r.date) {
        byDay.set(r.date.slice(0, 10), { date: r.date.slice(0, 10), price: r.price });
      }
    }
    return Array.from(byDay.values()).sort((a, b) => a.date.localeCompare(b.date));
  })();

  const selectedSpanDays = (() => {
    const s = parseLocalIsoDate(start);
    const e = parseLocalIsoDate(end);
    return Math.max(1, Math.round((e.getTime() - s.getTime()) / 86400000) + 1);
  })();

  const chartStats = data?.records.length
    ? (() => {
        const first = data.records[0];
        const last = data.records[data.records.length - 1];
        const prices = data.records.map((r) => r.price);
        const change = first.price ? ((last.price - first.price) / first.price) * 100 : 0;
        return {
          first,
          last,
          min: Math.min(...prices),
          max: Math.max(...prices),
          change,
        };
      })()
    : null;

  const rangeIs = (days: number) => {
    const startDate = new Date(`${start}T00:00:00`);
    const endDate = new Date(`${end}T00:00:00`);
    return Math.round((endDate.getTime() - startDate.getTime()) / 86400000) + 1 === days;
  };

  const chooseRange = (days: number) => {
    const refEnd = source?.latest_date || anchorEnd;
    setEnd(refEnd);
    setStart(shiftIsoDate(refEnd, 1 - days));
  };

  return (
    <div className="space-y-4 max-w-[1440px] mx-auto pb-8 font-sans">
      <Header
        title="Dữ liệu lịch sử giá nông sản"
        subtitle="Chuỗi giá thu mua thực tế tại vùng chuyên canh đã xác minh theo ngày"
      />

      {error && (
        <p role="alert" className="p-3 bg-red-50 text-[#DC2626] border border-red-200 rounded-lg text-xs">
          {error}
        </p>
      )}

      {/* Single Compact Horizontal Filter Toolbar */}
      <div className="bg-white border border-[#E5E7EB] rounded-xl p-3 shadow-card flex flex-wrap items-center justify-between gap-2.5">
        <div className="flex flex-wrap items-center gap-2.5">
          <div className="flex items-center gap-1.5">
            <label htmlFor="history-commodity" className="text-xs font-medium text-[#64748B]">
              Nông sản:
            </label>
            <select
              id="history-commodity"
              aria-label="Nông sản"
              value={commodityId}
              onChange={(e) => handleSelectCommodity(Number(e.target.value))}
              className="rounded-lg border border-[#E5E7EB] bg-[#F8FAF9] px-2.5 py-1.5 text-xs font-semibold text-[#1E293B] focus:outline-none focus:border-[#2F6F4E]"
            >
              {sources.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name} ({getCommodityUnit(s.name, s.unit)})
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-1.5 bg-[#F8FAF9] px-2.5 py-1 rounded-lg border border-[#E5E7EB] text-xs">
            <span className="text-[#64748B]">Từ:</span>
            <input
              aria-label="Từ ngày"
              type="date"
              value={start}
              max={end}
              onChange={(e) => setStart(e.target.value)}
              className="bg-transparent text-xs tabular-nums text-[#1E293B] focus:outline-none"
            />
            <span className="text-[#CBD5E1]">|</span>
            <span className="text-[#64748B]">Đến:</span>
            <input
              aria-label="Đến ngày"
              type="date"
              value={end}
              min={start}
              max={source?.latest_date || anchorEnd}
              onChange={(e) => setEnd(e.target.value)}
              className="bg-transparent text-xs tabular-nums text-[#1E293B] focus:outline-none"
            />
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {/* Quick Period Buttons: 30N | 90N | 1N */}
          <div className="flex items-center gap-0.5 rounded-lg border border-[#E5E7EB] bg-[#F8FAF9] p-0.5">
            {[
              { days: 30, label: '30N' },
              { days: 90, label: '90N' },
              { days: 365, label: '1N' },
            ].map((item) => (
              <button
                key={item.days}
                type="button"
                onClick={() => chooseRange(item.days)}
                className={`rounded-md px-2.5 py-1 text-xs font-semibold tabular-nums transition-colors cursor-pointer ${
                  rangeIs(item.days)
                    ? 'bg-[#2F6F4E] text-white'
                    : 'text-[#334155] hover:text-[#1E293B]'
                }`}
              >
                {item.label}
              </button>
            ))}
          </div>

          <Link
            href={`/forecast?commodity_id=${commodityId}`}
            className="inline-flex items-center gap-1 rounded-lg bg-[#2F6F4E] hover:bg-[#24583D] px-3 py-1.5 text-xs font-semibold text-white transition-colors"
          >
            <span>Dự báo</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>

      {/* Historical Price Chart Card with Single-Row Inline Stats */}
      <section className="p-4 sm:p-5 bg-white rounded-xl border border-[#E5E7EB] shadow-card space-y-3">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-3 pb-3 border-b border-[#E5E7EB]">
          <div>
            <h2 className="font-bold text-[15px] text-[#1E293B] flex flex-wrap items-center gap-2">
              <span>Biến động giá lịch sử {source?.name || ''}</span>
              {provinceCode !== 'all' && data?.location_context && (
                <span
                  className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-semibold ${
                    data.location_context.pricing_mode === 'direct'
                      ? 'bg-[#F0F7F4] text-[#15803D] border border-[#15803D]/20'
                      : 'bg-slate-100 text-slate-700 border border-slate-200'
                  }`}
                >
                  <MapPin className="w-3 h-3 shrink-0" />
                  <span>{data.location_context.note || provinceName}</span>
                </span>
              )}
            </h2>
            <p className="text-xs text-[#64748B] mt-0.5 tabular-nums">
              Đơn vị: {currentUnit} · {data?.records.length || 0} ngày quan sát ({formatDateVN(start)} – {formatDateVN(end)})
              {provinceCode !== 'all' && data?.location_context?.explanation
                ? ` · ${data.location_context.explanation}`
                : ''}
            </p>
          </div>

          {chartStats && (
            <div className="flex flex-wrap items-center gap-4 text-xs tabular-nums bg-[#F8FAF9] px-3.5 py-2 rounded-lg border border-[#E5E7EB]">
              <div>
                <span className="text-[#64748B]">Đầu kỳ: </span>
                <strong className="text-[#1E293B]">{formatNumberVN(chartStats.first.price)}</strong>
              </div>
              <div>
                <span className="text-[#64748B]">Cuối kỳ: </span>
                <strong className="text-[#1E293B]">{formatNumberVN(chartStats.last.price)}</strong>
              </div>
              <div>
                <span className="text-[#64748B]">Thấp nhất: </span>
                <strong className="text-[#1E293B]">{formatNumberVN(chartStats.min)}</strong>
              </div>
              <div>
                <span className="text-[#64748B]">Cao nhất: </span>
                <strong className="text-[#1E293B]">{formatNumberVN(chartStats.max)}</strong>
              </div>
              <div>
                <span className="text-[#64748B]">Biến động: </span>
                <strong
                  className={
                    chartStats.change >= 0 ? 'text-[#15803D]' : 'text-[#DC2626]'
                  }
                >
                  {formatPct(chartStats.change, 2)}
                </strong>
              </div>
            </div>
          )}
        </div>

        {loading ? (
          <div className="h-[340px] flex items-center justify-center text-xs text-[#64748B]">
            Đang tải chuỗi dữ liệu lịch sử...
          </div>
        ) : data && data.records.length > 0 ? (
          <div className="w-full pt-1">
            {(() => {
              const span = Math.max((chartStats?.max ?? 0) - (chartStats?.min ?? 0), 1);
              const pad = Math.max(span * 0.12, (chartStats?.min ?? 0) * 0.005);
              const yMin = Math.max(0, Math.floor(((chartStats?.min ?? 0) - pad) / 100) * 100);
              const yMax = Math.ceil(((chartStats?.max ?? 0) + pad) / 100) * 100;
              const chartRows = chart.map((r) => ({
                x: parseLocalIsoDate(r.date),
                fullDate: `Ngày ${formatDateVN(r.date)}`,
                price: r.price,
                tipText: `${formatNumberVN(r.price)} ${currentUnit}`,
              }));
              const xLabelFormat = selectedSpanDays > 180 ? 'MM/yyyy' : 'dd/MM/yy';
              return (
                <FinChart
                  id={`syncfusion-history-${commodityId}-${provinceCode}-${start}-${end}`}
                  data={chartRows}
                  xName="x"
                  xValueType="DateTime"
                  xLabelFormat={xLabelFormat}
                  height={340}
                  showLegend={false}
                  showCrosshair={true}
                  yMinimum={yMin}
                  yMaximum={yMax}
                  yFormat={(value: number) => formatNumberVN(Math.round(value))}
                  series={[
                    {
                      type: 'Area',
                      name: 'Giá công bố',
                      yName: 'price',
                      color: '#2F6F4E',
                      width: 2,
                      opacity: 0.14,
                      tipField: 'tipText',
                      showMarkers: chartRows.length <= 45,
                    },
                  ]}
                />
              );
            })()}
          </div>
        ) : (
          <div className="py-12 text-center text-xs text-[#64748B]">
            Không có dữ liệu trong khoảng ngày đã chọn.
          </div>
        )}
      </section>

      {/* Historical Price DataGrid (Single Export CSV button inside AgroGrid) */}
      {data && (
        <AgroGrid
          fileName={`lich-su-${source?.code || 'nong-san'}-${start}-${end}`}
          pageSize={15}
          height={420}
          data={[...data.records].reverse().map((r) => ({
            id: r.id,
            date: r.date,
            price: r.price,
            unit: currentUnit,
            source: r.source,
            sourceUrl: r.source_url ?? r.source_details?.source_url ?? (isSafeHttpUrl(r.source) ? r.source : null),
            statusLabel: provenanceLabel[r.provenance] || r.provenance,
          }))}
          columns={[
            { field: 'date', headerText: 'Ngày ghi nhận', kind: 'date', width: 130 },
            {
              field: 'price',
              headerText: `Giá công bố (${currentUnit})`,
              kind: 'money',
              unitField: 'unit',
              width: 180,
            },
            {
              field: 'source',
              headerText: 'Nguồn công bố',
              kind: 'link',
              urlField: 'sourceUrl',
              width: 320,
            },
            { field: 'statusLabel', headerText: 'Trạng thái', kind: 'text', width: 140 },
          ] as AgroColumn[]}
        />
      )}
    </div>
  );
}
