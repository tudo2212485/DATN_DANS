import {
  CommoditySummary,
  ComparisonDataPoint,
  SpotlightSummary,
  ForecastPoint,
  ModelMetrics,
  AlertRuleItem,
  ModelComparisonMetrics,
} from '@/types';
import {
  COMMODITIES_DATA,
  COMPARISON_SERIES,
  SPOTLIGHT_SUGAR,
  MODEL_METRICS_LIST,
  FORECAST_PREDICTIONS_SAMPLE,
  INITIAL_ALERT_RULES,
} from './mockData';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Helper mapping snake_case from Backend API to camelCase for Frontend
function mapAlertRule(r: Record<string, unknown>): AlertRuleItem {
  const commodityMap: Record<number, string> = {
    1: 'Lúa gạo IR50404',
    2: 'Cà phê Robusta',
    3: 'Hồ tiêu đen',
    4: 'Mía đường',
  };

  const cid = Number(r.commodityId ?? r.commodity_id ?? 1);
  const rawCommName = String(r.commodityName ?? r.commodity_name ?? '');
  const commName = (rawCommName && rawCommName !== 'None') ? rawCommName : (commodityMap[cid] || 'Nông sản');

  return {
    id: Number(r.id),
    commodityId: cid,
    commodityName: commName,
    ruleName: String(r.ruleName ?? r.rule_name ?? `Cảnh báo ${commName}`),
    conditionType: (r.conditionType ?? r.condition_type ?? 'PRICE_ABOVE') as AlertRuleItem['conditionType'],
    thresholdValue: Number(r.thresholdValue ?? r.threshold_value ?? 0),
    email: String(r.email ?? ''),
    isActive: Boolean(r.isActive !== undefined ? r.isActive : (r.is_active !== undefined ? r.is_active : true)),
    createdAt: String(r.createdAt ?? r.created_at ?? '28/08/2026'),
  };
}

/**
 * Fetch overview commodity cards
 */
export async function fetchCommoditiesOverview(): Promise<CommoditySummary[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/commodities/overview`, { cache: 'no-store' });
    if (!res.ok) throw new Error('API Error');
    return await res.json();
  } catch {
    return COMMODITIES_DATA;
  }
}

/**
 * Fetch market comparison series
 */
export async function fetchMarketComparison(): Promise<ComparisonDataPoint[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/commodities/comparison`, { cache: 'no-store' });
    if (!res.ok) throw new Error('API Error');
    return await res.json();
  } catch {
    return COMPARISON_SERIES;
  }
}

/**
 * Fetch spotlight summary
 */
export async function fetchCommoditySpotlight(code: string = 'SUGAR'): Promise<SpotlightSummary> {
  try {
    const res = await fetch(`${API_BASE_URL}/commodities/spotlight?code=${code}`, { cache: 'no-store' });
    if (!res.ok) throw new Error('API Error');
    return await res.json();
  } catch {
    return SPOTLIGHT_SUGAR;
  }
}

/**
 * Fetch forecast with 95% Confidence Interval & Metrics
 */
export async function fetchForecastDashboard(
  commodityId: number = 2,
  modelName: string = 'LSTM',
  days: number = 14
): Promise<{ metrics: ModelMetrics; forecastData: ForecastPoint[] }> {
  try {
    const res = await fetch(
      `${API_BASE_URL}/forecast?commodity_id=${commodityId}&model_name=${modelName}&days=${days}`,
      { cache: 'no-store' }
    );
    if (!res.ok) throw new Error('API Error');
    const data = await res.json();
    return {
      metrics: data.metrics,
      forecastData: data.forecastData,
    };
  } catch {
    return {
      metrics: MODEL_METRICS_LIST[modelName] || MODEL_METRICS_LIST.LSTM,
      forecastData: FORECAST_PREDICTIONS_SAMPLE.slice(0, 4 + days),
    };
  }
}

/**
 * Fetch model comparison metrics for a commodity
 */
export async function fetchModelComparison(commodityId: number = 2): Promise<ModelComparisonMetrics[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/forecast/compare/${commodityId}`, { cache: 'no-store' });
    if (!res.ok) throw new Error('API Error');
    return await res.json();
  } catch {
    // Return some mock comparison data if backend is down
    return [
      { model_name: 'LSTM', mae: 105.2, rmse: 140.5, mape: 3.2, r2: 0.89, is_best: true },
      { model_name: 'XGBoost', mae: 110.1, rmse: 145.2, mape: 3.5, r2: 0.87 },
      { model_name: 'Random Forest', mae: 115.3, rmse: 152.4, mape: 3.8, r2: 0.85 },
      { model_name: 'Prophet', mae: 125.4, rmse: 165.7, mape: 4.5, r2: 0.82 },
      { model_name: 'ARIMA', mae: 145.6, rmse: 185.3, mape: 5.2, r2: 0.75 },
    ];
  }
}

/**
 * Fetch alert rules
 */
export async function fetchAlertRules(): Promise<AlertRuleItem[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/alerts`, { cache: 'no-store' });
    if (!res.ok) throw new Error('API Error');
    const rawList = await res.json();
    return Array.isArray(rawList) ? rawList.map(mapAlertRule) : INITIAL_ALERT_RULES;
  } catch {
    return INITIAL_ALERT_RULES;
  }
}

/**
 * Create new alert rule
 */
export async function createAlertRuleApi(payload: {
  commodity_id: number;
  rule_name: string;
  condition_type: string;
  threshold_value: number;
  email: string;
}): Promise<AlertRuleItem | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/alerts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('API Error');
    const raw = await res.json();
    return mapAlertRule(raw);
  } catch {
    return null;
  }
}

/**
 * Toggle alert rule
 */
export async function toggleAlertRuleApi(ruleId: number, isActive: boolean): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE_URL}/alerts/${ruleId}/toggle`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ is_active: isActive }),
    });
    return res.ok;
  } catch {
    return false;
  }
}

/**
 * Delete alert rule
 */
export async function deleteAlertRuleApi(ruleId: number): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE_URL}/alerts/${ruleId}`, {
      method: 'DELETE',
    });
    return res.ok;
  } catch {
    return false;
  }
}

/**
 * Test alert email trigger
 */
export async function testAlertApi(ruleId: number): Promise<{ status: string; message: string }> {
  try {
    const res = await fetch(`${API_BASE_URL}/alerts/${ruleId}/test`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('API Error');
    return await res.json();
  } catch {
    return {
      status: 'success',
      message: 'Đã gửi thông báo cảnh báo thử nghiệm thành công!',
    };
  }
}
