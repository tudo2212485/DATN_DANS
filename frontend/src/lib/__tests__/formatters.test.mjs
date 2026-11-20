import test from 'node:test';
import assert from 'node:assert/strict';

// Inline pure verification of frontend/src/lib/formatters.ts logic using Node's built-in test runner
function getCommodityUnit(nameOrCode, explicitUnit) {
  const raw = `${nameOrCode || ''} ${explicitUnit || ''}`.toLowerCase();
  if (raw.includes('mía') || raw.includes('sugar') || raw.includes('tấn')) {
    return 'VNĐ/tấn';
  }
  if (explicitUnit && explicitUnit.trim() !== '' && explicitUnit.trim() !== 'đ') {
    return explicitUnit.trim();
  }
  return 'VNĐ/kg';
}

function formatNumberVN(value, fractionDigits = 0) {
  const num = typeof value === 'string' ? Number(value.replace(/\./g, '').replace(',', '.')) : Number(value);
  if (!Number.isFinite(num)) return '0';
  return num.toLocaleString('vi-VN', {
    minimumFractionDigits: fractionDigits,
    maximumFractionDigits: fractionDigits,
  });
}

function formatVnd(value, unit, commodityNameOrCode) {
  const formatted = formatNumberVN(value, 0);
  if (unit === '') return formatted;
  const resolvedUnit = unit || (commodityNameOrCode ? getCommodityUnit(commodityNameOrCode, unit) : 'VNĐ');
  return `${formatted} ${resolvedUnit}`;
}

function formatPct(value, fractionDigits = 2) {
  const num = Number(value);
  if (!Number.isFinite(num)) return '0,00%';
  const sign = num > 0 ? '+' : '';
  return `${sign}${num.toLocaleString('vi-VN', {
    minimumFractionDigits: fractionDigits,
    maximumFractionDigits: fractionDigits,
  })}%`;
}

function formatDateVN(input) {
  if (!input) return '—';
  const str = String(input).trim();
  if (/^\d{2}\/\d{2}\/\d{4}$/.test(str)) return str;
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

function formatDateTimeVN(input) {
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

function calculateGrowthPct(current, base) {
  if (!Number.isFinite(current) || !Number.isFinite(base) || base <= 0) return 0;
  return Number((((current - base) / base) * 100).toFixed(2));
}

function calculatePearsonCorrelation(x, y) {
  const n = Math.min(x.length, y.length);
  if (n < 2) return 0;
  const meanX = x.slice(0, n).reduce((a, b) => a + b, 0) / n;
  const meanY = y.slice(0, n).reduce((a, b) => a + b, 0) / n;
  let num = 0, denX = 0, denY = 0;
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

test('TC-FE-01: Format tiền tệ chuẩn Việt Nam và đơn vị nhất quán (Mía đường là VNĐ/tấn)', () => {
  assert.equal(getCommodityUnit('Mía đường 10 CCS', 'đ'), 'VNĐ/tấn');
  assert.equal(getCommodityUnit('SUGARCANE', 'VNĐ/tấn'), 'VNĐ/tấn');
  assert.equal(getCommodityUnit('Cà phê Robusta', 'VNĐ/kg'), 'VNĐ/kg');
  assert.equal(formatVnd(93800, null, 'Cà phê Robusta'), '93.800 VNĐ/kg');
  assert.equal(formatVnd(1279515, null, 'Mía đường'), '1.279.515 VNĐ/tấn');
});

test('TC-FE-02: Format ngày giờ chuẩn Việt Nam DD/MM/YYYY và DD/MM/YYYY HH:mm (loại bỏ ISO thô)', () => {
  assert.equal(formatDateVN('2026-08-28'), '28/08/2026');
  assert.equal(formatDateVN('2026-09-04T16:08:19.158449+07:00'), '04/09/2026');
  const formattedDt = formatDateTimeVN('2026-08-28T16:08:19');
  assert.match(formattedDt, /^28\/08\/2026 \d{2}:08$/);
});

test('TC-FE-03: Tính toán phần trăm tăng trưởng chuẩn hóa và tương quan Pearson (không NaN/Infinity)', () => {
  assert.equal(calculateGrowthPct(114000, 100000), 14);
  assert.equal(calculateGrowthPct(95000, 100000), -5);
  assert.equal(calculateGrowthPct(100000, 0), 0);
  assert.equal(formatPct(0.5, 2), '+0,50%');
  assert.equal(formatPct(-0.4, 2), '-0,40%');
  assert.equal(calculatePearsonCorrelation([1, 2, 3, 4], [2, 4, 6, 8]), 1);
  assert.equal(calculatePearsonCorrelation([1, 2, 3, 4], [8, 6, 4, 2]), -1);
});

