'use client';

import React, { useId, useMemo, useRef, useState } from 'react';
import { useLocation } from '@/contexts/LocationContext';
import { MapPin, ChevronDown, LocateFixed, Search, Check, Loader2, Globe } from 'lucide-react';

const REGION_ORDER = [
  'Nam Trung Bộ',
  'Tây Nguyên',
  'ĐBSCL',
  'Đông Nam Bộ',
  'Miền Bắc',
];

function stripVietnameseTones(text: string): string {
  return text
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/đ/g, 'd')
    .replace(/Đ/g, 'D')
    .toLowerCase();
}

export default function LocationSelector() {
  const {
    provinceCode,
    provinceName,
    regions,
    locating,
    locateFeedback,
    setProvinceCode,
    detectMyLocation,
  } = useLocation();

  const [query, setQuery] = useState('');
  const popoverId = `agro-loc-popover-${useId().replace(/:/g, '')}`;
  const popoverRef = useRef<HTMLDivElement | null>(null);

  const closePopover = () => {
    const el = popoverRef.current as (HTMLDivElement & { hidePopover?: () => void }) | null;
    if (el && typeof el.hidePopover === 'function') {
      try {
        el.hidePopover();
      } catch {
        // Ignore if already closed
      }
    }
  };

  const handleSelect = (code: string) => {
    setProvinceCode(code);
    setQuery('');
    closePopover();
  };

  const handleAutoDetect = async () => {
    const ok = await detectMyLocation();
    if (ok) {
      setTimeout(() => closePopover(), 650);
    }
  };

  const groupedRegions = useMemo(() => {
    const normQ = stripVietnameseTones(query.trim());
    const filtered = regions.filter((r) => {
      if (!normQ) return true;
      return (
        stripVietnameseTones(r.name).includes(normQ) ||
        stripVietnameseTones(r.region_name).includes(normQ) ||
        r.code.includes(normQ)
      );
    });

    const groups: Record<string, typeof filtered> = {};
    for (const item of filtered) {
      const key = item.region_name || 'Khác';
      if (!groups[key]) groups[key] = [];
      groups[key].push(item);
    }

    return Object.entries(groups).sort(([a], [b]) => {
      const ia = REGION_ORDER.indexOf(a);
      const ib = REGION_ORDER.indexOf(b);
      return (ia === -1 ? 99 : ia) - (ib === -1 ? 99 : ib);
    });
  }, [regions, query]);

  const isProvincial = provinceCode !== 'all';

  return (
    <div className="relative">
      <button
        type="button"
        aria-label={`Chọn khu vực hiển thị giá: ${provinceName}`}
        {...({ popovertarget: popoverId } as Record<string, string>)}
        className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg border text-xs font-semibold transition-colors cursor-pointer ${
          isProvincial
            ? 'bg-[#F0F7F4] border-[#2F6F4E]/35 text-[#2F6F4E] hover:bg-[#E5F2EC]'
            : 'bg-[#F8FAF9] border-[#E5E7EB] text-[#1E293B] hover:bg-white'
        }`}
      >
        <MapPin className="w-3.5 h-3.5 text-[#2F6F4E] shrink-0" aria-hidden="true" />
        <span className="max-w-[120px] truncate">{provinceName}</span>
        <ChevronDown className="w-3.5 h-3.5 text-[#64748B] shrink-0" aria-hidden="true" />
      </button>

      <div
        ref={popoverRef}
        id={popoverId}
        {...({ popover: 'auto' } as Record<string, string>)}
        className="agro-location-popover font-sans"
      >
        <div className="p-3 border-b border-[#E5E7EB] bg-[#F8FAF9] space-y-2">
          <button
            type="button"
            disabled={locating}
            onClick={() => void handleAutoDetect()}
            className="w-full inline-flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-[#2F6F4E] hover:bg-[#24583D] text-white text-xs font-semibold transition-colors disabled:opacity-60 cursor-pointer"
          >
            {locating ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin" aria-hidden="true" />
            ) : (
              <LocateFixed className="w-3.5 h-3.5" aria-hidden="true" />
            )}
            <span>{locating ? 'Đang định vị GPS...' : 'Dùng vị trí hiện tại của tôi'}</span>
          </button>

          {locateFeedback && (
            <p
              role={locateFeedback.type === 'error' ? 'alert' : 'status'}
              className={`text-[11px] px-2.5 py-1.5 rounded-md border ${
                locateFeedback.type === 'error'
                  ? 'bg-amber-50 text-amber-900 border-amber-200'
                  : 'bg-[#F0F7F4] text-[#15803D] border-[#15803D]/25'
              }`}
            >
              {locateFeedback.text}
            </p>
          )}

          <div className="relative">
            <Search
              className="w-3.5 h-3.5 text-[#64748B] absolute left-2.5 top-1/2 -translate-y-1/2 pointer-events-none"
              aria-hidden="true"
            />
            <input
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Tìm tỉnh/thành (VD: Khánh Hòa, Đắk Lắk)..."
              aria-label="Tìm kiếm tỉnh thành"
              className="w-full pl-8 pr-3 py-1.5 rounded-lg bg-white border border-[#E5E7EB] text-xs text-[#1E293B] placeholder:text-[#94A3B8] focus:outline-none focus:border-[#2F6F4E]"
            />
          </div>
        </div>

        <div className="max-h-[300px] overflow-y-auto custom-scrollbar p-1.5 space-y-1.5">
          {/* National / Default Option */}
          {!query.trim() && (
            <button
              type="button"
              onClick={() => handleSelect('all')}
              className={`w-full flex items-center justify-between gap-2 px-2.5 py-2 rounded-lg text-left text-xs transition-colors cursor-pointer ${
                provinceCode === 'all'
                  ? 'bg-[#F0F7F4] text-[#2F6F4E] font-semibold'
                  : 'text-[#1E293B] hover:bg-[#F8FAF9]'
              }`}
            >
              <span className="inline-flex items-center gap-2">
                <Globe className="w-3.5 h-3.5 text-[#2F6F4E] shrink-0" aria-hidden="true" />
                <span>Toàn quốc (Vùng trọng điểm)</span>
              </span>
              {provinceCode === 'all' && <Check className="w-3.5 h-3.5 text-[#2F6F4E] shrink-0" />}
            </button>
          )}

          {groupedRegions.length === 0 ? (
            <p className="py-5 text-center text-xs text-[#64748B]">
              Không tìm thấy tỉnh/thành phù hợp.
            </p>
          ) : (
            groupedRegions.map(([regionLabel, items]) => (
              <div key={regionLabel} className="space-y-0.5">
                <div className="px-2.5 pt-1.5 pb-0.5 text-[10.5px] font-bold uppercase tracking-wider text-[#64748B]">
                  {regionLabel}
                </div>
                {items.map((item) => {
                  const selected = provinceCode === item.code;
                  const directCount = item.direct_commodities?.length || 0;
                  return (
                    <button
                      key={item.code}
                      type="button"
                      onClick={() => handleSelect(item.code)}
                      className={`w-full flex items-center justify-between gap-2 px-2.5 py-1.5 rounded-lg text-left text-xs transition-colors cursor-pointer ${
                        selected
                          ? 'bg-[#F0F7F4] text-[#2F6F4E] font-semibold'
                          : 'text-[#334155] hover:bg-[#F8FAF9] hover:text-[#1E293B]'
                      }`}
                    >
                      <span className="truncate">{item.name}</span>
                      <span className="inline-flex items-center gap-1.5 shrink-0">
                        {directCount > 0 && (
                          <span
                            title={`Có ${directCount} mặt hàng khảo sát trực tiếp`}
                            className="px-1.5 py-0.5 rounded bg-[#F0F7F4] text-[#15803D] border border-[#15803D]/20 text-[10px] font-semibold"
                          >
                            {directCount} khảo sát
                          </span>
                        )}
                        {selected && <Check className="w-3.5 h-3.5 text-[#2F6F4E]" />}
                      </span>
                    </button>
                  );
                })}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

