/**
 * Unified Vietnamese Financial & Agricultural Data Formatters
 * Ensures consistent tabular numeric display, DD/MM/YYYY dates, and explicit units (VNĐ/kg vs VNĐ/tấn).
 */

export function getCommodityUnit(nameOrCode?: string | null, explicitUnit?: string | null): string {
  const raw = `${nameOrCode || ''} ${explicitUnit || ''}`.toLowerCase();
  if (raw.includes('mía') || raw.includes('sugar') || raw.includes('tấn')) {
    return 'VNĐ/tấn';
  }
  if (explicitUnit && explicitUnit.trim() !== '' && explicitUnit.trim() !== 'đ') {
    return explicitUnit.trim();
  }
  return 'VNĐ/kg';
}

export function formatNumberVN(value: number | string | null | undefined, fractionDigits = 0): string {
  const num = typeof value === 'string' ? Number(value.replace(/\./g, '').replace(',', '.')) : Number(value);
  if (!Number.isFinite(num)) return '0';
  return num.toLocaleString('vi-VN', {
    minimumFractionDigits: fractionDigits,
    maximumFractionDigits: fractionDigits,
  });
}

export function formatVnd(
  value: number | string | null | undefined,
  unit?: string | null,
  commodityNameOrCode?: string | null
): string {
  const formatted = formatNumberVN(value, 0);
  if (unit === '') return formatted;
  const resolvedUnit = unit || (commodityNameOrCode ? getCommodityUnit(commodityNameOrCode, unit) : 'VNĐ');
  return `${formatted} ${resolvedUnit}`;
}

export function formatPct(
  value: number | string | null | undefined,
  fractionDigits = 2
): string {
  const rawNum = Number(value);
  if (!Number.isFinite(rawNum)) return '0,00%';
  const threshold = Math.pow(10, -(fractionDigits + 1));
  const num = Math.abs(rawNum) < threshold ? 0 : rawNum;
  const sign = num > 0 ? '+' : '';
  return `${sign}${num.toLocaleString('vi-VN', {
    minimumFractionDigits: fractionDigits,
    maximumFractionDigits: fractionDigits,
  })}%`;
}

export function formatDateVN(input?: string | Date | null): string {
  if (!input) return '—';
  if (input instanceof Date) {
    if (isNaN(input.getTime())) return '—';
    const d = String(input.getDate()).padStart(2, '0');
    const m = String(input.getMonth() + 1).padStart(2, '0');
    const y = input.getFullYear();
    return `${d}/${m}/${y}`;
  }
  const str = String(input).trim();
  if (/^\d{2}\/\d{2}\/\d{4}$/.test(str)) return str;
  // Tuyệt đối không đưa chuỗi rút gọn DD/MM vào new Date() (tránh JS hiểu nhầm thành năm 2001)
  if (/^\d{1,2}\/\d{1,2}$/.test(str)) return str;
  const ymdMatch = str.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (ymdMatch) {
    return `${ymdMatch[3]}/${ymdMatch[2]}/${ymdMatch[1]}`;
  }
  const parsed = new Date(str);
  if (!isNaN(parsed.getTime())) {
    const d = String(parsed.getDate()).padStart(2, '0');
    const m = String(parsed.getMonth() + 1).padStart(2, '0');
    const y = parsed.getFullYear();
    return `${d}/${m}/${y}`;
  }
  return str;
}

export function formatDateTimeVN(input?: string | Date | null): string {
  if (!input) return '—';
  const str = typeof input === 'string' ? input.trim() : '';
  if (/^\d{2}\/\d{2}\/\d{4}\s+\d{2}:\d{2}/.test(str)) return str;
  if (/^\d{4}-\d{2}-\d{2}$/.test(str)) {
    return formatDateVN(str);
  }
  const parsed = input instanceof Date ? input : new Date(str);
  if (!isNaN(parsed.getTime())) {
    const d = String(parsed.getDate()).padStart(2, '0');
    const m = String(parsed.getMonth() + 1).padStart(2, '0');
    const y = parsed.getFullYear();
    const hh = String(parsed.getHours()).padStart(2, '0');
    const mm = String(parsed.getMinutes()).padStart(2, '0');
    return `${d}/${m}/${y} ${hh}:${mm}`;
  }
  return str || '—';
}

export function calculateGrowthPct(current: number, base: number): number {
  if (!Number.isFinite(current) || !Number.isFinite(base) || base <= 0) return 0;
  return Number((((current - base) / base) * 100).toFixed(2));
}

export function calculatePearsonCorrelation(x: number[], y: number[]): number {
  const n = Math.min(x.length, y.length);
  if (n < 2) return 0;
  const meanX = x.slice(0, n).reduce((a, b) => a + b, 0) / n;
  const meanY = y.slice(0, n).reduce((a, b) => a + b, 0) / n;
  let num = 0;
  let denX = 0;
  let denY = 0;
  for (let i = 0; i < n; i++) {
    const dx = x[i] - meanX;
    const dy = y[i] - meanY;
    num += dx * dy;
    denX += dx * dx;
    denY += dy * dy;
  }
  const denom = Math.sqrt(denX * denY);
  if (denom === 0 || !Number.isFinite(denom)) return 0;
  return Number((num / denom).toFixed(2));
}

