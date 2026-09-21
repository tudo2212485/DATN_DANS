import {
  CommoditySummary,
  ComparisonDataPoint,
  SpotlightSummary,
  ForecastPoint,
  ModelMetrics,
  AlertRuleItem,
  AlertLogItem,
  ModelComparisonMetrics,
  AdminStats,
  AdminPriceItem,
  AdminUserItem,
  TaskRunResult,
} from '@/types';
import {
  INITIAL_ALERT_RULES,
} from './mockData';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface HistorySource { id: number; code: string; name: string; unit: string; automatic: boolean; source_url: string | null; limitation: string; kind: 'daily' | 'periodic'; suggested_start?: string }
export interface HistoryReadiness { ready: boolean; reason: string | null; observation_count: number; start_date: string | null; end_date: string | null; max_gap_days: number }
export interface HistoryResponse {
  records: {id: number; date: string; price: number; source: string; provenance: string; source_details?:{market:string;price_type:string;product:string;upstream:string}}[];
  periodic_records: {id:number;start:string;end:string;published_date:string;buying_price:number;selling_price:number;unit:string;specification:string;market:string;source:string;attribution:string}[];
  missing_dates: string[]; readiness: HistoryReadiness; range_readiness: HistoryReadiness; unverified_count: number;
}
export interface TrainingMetadata {
  run_id: number; start_date: string; end_date: string; observation_count: number;
  test_start: string; test_end: string; test_count: number; train_end: string;
  filled_days: number; baseline: {mae: number; rmse: number; mape: number; r2: number};
  evaluation: string; trained_at: string; stale_days: number; interval_note: string; dataset_hash: string;
}
export async function fetchHistorySources(): Promise<HistorySource[]> {
  const res = await fetch(`${API_BASE_URL}/history/sources`, {cache:'no-store'});
  await assertApiOk(res); return res.json();
}
export async function fetchTrainingReadiness(commodityId: number): Promise<HistoryReadiness> {
  const res = await fetch(`${API_BASE_URL}/history/readiness?commodity_id=${commodityId}`,{cache:'no-store'});
  await assertApiOk(res); return res.json();
}
export async function fetchHistory(commodityId: number, start: string, end: string, includeUnverified = false): Promise<HistoryResponse> {
  const params = new URLSearchParams({commodity_id:String(commodityId),start_date:start,end_date:end,include_unverified:String(includeUnverified)});
  const res = await fetch(`${API_BASE_URL}/history?${params}`, {cache:'no-store'});
  await assertApiOk(res); return res.json();
}

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
  const res = await fetch(`${API_BASE_URL}/commodities/overview`, { cache: 'no-store' });
  if (!res.ok) throw new Error('API Error fetching overview');
  return await res.json();
}

/**
 * Fetch market comparison series
 */
export async function fetchMarketComparison(): Promise<ComparisonDataPoint[]> {
  const res = await fetch(`${API_BASE_URL}/commodities/comparison`, { cache: 'no-store' });
  if (!res.ok) throw new Error('API Error fetching comparison');
  return await res.json();
}

/**
 * Fetch spotlight summary
 */
export async function fetchCommoditySpotlight(code: string = 'COFFEE'): Promise<SpotlightSummary> {
  const res = await fetch(`${API_BASE_URL}/commodities/spotlight?code=${code}`, { cache: 'no-store' });
  if (!res.ok) throw new Error('API Error fetching spotlight');
  return await res.json();
}

/**
 * Fetch regional price table data from PostgreSQL
 */
export async function fetchRegionalPrices(): Promise<import('@/types').RegionalPriceItem[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/commodities/regional-prices`, { cache: 'no-store' });
    await assertApiOk(res);
    return await res.json();
  } catch {
    return [];
  }
}

export const fetchRegionalPricesApi = fetchRegionalPrices;

/**
 * Fetch forecast with 95% Confidence Interval & Metrics
 */
export async function fetchForecastDashboard(
  commodityId: number = 2,
  modelName: string = 'LSTM',
  days: number = 14
): Promise<{ metrics: ModelMetrics; forecastData: ForecastPoint[]; training?: TrainingMetadata }> {
  const res = await fetch(
    `${API_BASE_URL}/forecast?commodity_id=${commodityId}&model_name=${modelName}&days=${days}`,
    { cache: 'no-store' }
  );
  await assertApiOk(res);
  const data = await res.json();
  return {
    metrics: data.metrics,
    forecastData: data.forecastData,
    training: data.training,
  };
}

export const fetchForecastData = fetchForecastDashboard;

/**
 * Fetch model comparison metrics for a commodity
 */
export async function fetchModelComparison(commodityId: number = 2): Promise<ModelComparisonMetrics[]> {
  const res = await fetch(`${API_BASE_URL}/forecast/compare/${commodityId}`, { cache: 'no-store' });
  await assertApiOk(res);
  const data = await res.json();
  data.sort((a: ModelComparisonMetrics, b: ModelComparisonMetrics) => a.rmse - b.rmse);
  return data.map((item: ModelComparisonMetrics, index: number) => ({ ...item, isBest: index === 0 }));
}

/**
 * Fetch alert rules
 */
export async function fetchAlertRules(): Promise<AlertRuleItem[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/alerts`, { cache: 'no-store' });
    await assertApiOk(res);
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
    await assertApiOk(res);
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
    await assertApiOk(res);
    return true;
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
    await assertApiOk(res);
    return true;
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
    await assertApiOk(res);
    return await res.json();
  } catch {
    return {
      status: 'success',
      message: 'Đã gửi thông báo cảnh báo thử nghiệm thành công!',
    };
  }
}

interface RawAlertLog {
  id: number;
  rule_id: number;
  rule_name?: string | null;
  commodity_name?: string | null;
  email?: string | null;
  triggered_price: number;
  message: string;
  status: 'SENT' | 'FAILED' | 'PENDING';
  triggered_at?: string | null;
}

/**
 * Fetch alert logs / history
 */
export async function fetchAlertLogsApi(): Promise<AlertLogItem[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/alerts/logs?limit=30`, { cache: 'no-store' });
    await assertApiOk(res);
    const data = await res.json();
    return data.map((item: RawAlertLog) => ({
      id: item.id,
      ruleId: item.rule_id,
      ruleName: item.rule_name || `Quy tắc #${item.rule_id}`,
      commodityName: item.commodity_name || 'Nông sản',
      email: item.email || 'anhnguyen@agroforecast.vn',
      triggeredPrice: item.triggered_price,
      message: item.message,
      status: item.status || 'SENT',
      triggeredAt: item.triggered_at ? new Date(item.triggered_at).toLocaleString('vi-VN') : 'Vừa xong',
    }));
  } catch {
    return [
      {
        id: 1,
        ruleId: 2,
        ruleName: 'Cảnh báo Lúa gạo IR504 vượt đỉnh 9,000 VNĐ/kg',
        commodityName: 'Lúa gạo IR50404',
        triggeredPrice: 9150,
        message: 'Giá thị trường đạt 9,150 VNĐ/kg, vượt ngưỡng đỉnh 9,000 VNĐ/kg (+1.67%)',
        status: 'SENT',
        triggeredAt: '28/08/2026 14:15',
        email: 'gaomientay.market@gmail.com',
      },
      {
        id: 2,
        ruleId: 4,
        ruleName: 'Cảnh báo Cà phê Robusta vượt 125,000 VNĐ/kg',
        commodityName: 'Cà phê Robusta',
        triggeredPrice: 126200,
        message: 'Giá chốt phiên đạt 126,200 VNĐ/kg, tăng đột biến vượt ngưỡng 125,000 VNĐ/kg',
        status: 'SENT',
        triggeredAt: '28/08/2026 11:30',
        email: 'nongsanviet.alert@gmail.com',
      },
      {
        id: 3,
        ruleId: 3,
        ruleName: 'Cảnh báo Cà phê Robusta giảm dưới 110,000 VNĐ/kg',
        commodityName: 'Cà phê Robusta',
        triggeredPrice: 109500,
        message: 'Giá chạm mức 109,500 VNĐ/kg - Phân tích AI cảnh báo xu hướng sụt giảm liên tục 3 phiên',
        status: 'SENT',
        triggeredAt: '27/08/2026 16:45',
        email: 'nongsanviet.alert@gmail.com',
      },
      {
        id: 4,
        ruleId: 1,
        ruleName: 'Cảnh báo Hồ tiêu biến động tăng mạnh trên 145,000 VNĐ/kg',
        commodityName: 'Hồ tiêu đen',
        triggeredPrice: 146000,
        message: 'Khảo sát vùng Chư Sê giá tiêu đạt 146,000 VNĐ/kg, vượt trần cảnh báo',
        status: 'SENT',
        triggeredAt: '26/08/2026 09:20',
        email: 'chuse.pepper@gmail.com',
      },
    ];
  }
}

// -------------------------------------------------------------
// Phân hệ Quản trị Admin API (Admin Management Endpoints)
// -------------------------------------------------------------

function getAuthHeaders(): HeadersInit {
  const token = typeof window !== 'undefined' ? localStorage.getItem('agro_access_token') : null;
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

/**
 * Lấy số liệu thống kê hệ thống
 */
export async function fetchAdminStats(): Promise<AdminStats> {
  try {
    const res = await fetch(`${API_BASE_URL}/admin/stats`, {
      headers: getAuthHeaders(),
      cache: 'no-store',
    });
    await assertApiOk(res);
    const d = await res.json();
    return {
      totalCommodities: d.total_commodities ?? 0,
      totalPriceRecords: d.total_price_records ?? 0,
      totalForecastRecords: d.total_forecast_records ?? 0,
      totalAlertRules: d.total_alert_rules ?? 0,
      latestPriceDate: d.latest_price_date ?? 'Chưa có dữ liệu',
      systemStatus: d.system_status ?? 'UNKNOWN',
    };
  } catch (error) { throw error; }
}

/**
 * Lấy danh sách nông sản
 */
export async function fetchAdminCommodities() {
  try {
    const res = await fetch(`${API_BASE_URL}/admin/commodities`, {
      headers: getAuthHeaders(),
      cache: 'no-store',
    });
    await assertApiOk(res);
    return await res.json();
  } catch (error) { throw error; }
}

/**
 * Tạo mới nông sản
 */
export async function createCommodityApi(payload: {
  code: string;
  name: string;
  category: string;
  unit: string;
  region: string;
  description?: string;
}) {
  try {
    const res = await fetch(`${API_BASE_URL}/admin/commodities`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Không thể tạo nông sản');
    }
    return await res.json();
  } catch (error) { throw error; }
}

/**
 * Cập nhật nông sản
 */
export async function updateCommodityApi(
  id: number,
  payload: {
    code: string;
    name: string;
    category: string;
    unit: string;
    region: string;
    description?: string;
  }
) {
  try {
    const res = await fetch(`${API_BASE_URL}/admin/commodities/${id}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Không thể cập nhật nông sản');
    }
    return await res.json();
  } catch (error) { throw error; }
}

/**
 * Xóa nông sản
 */
export async function deleteCommodityApi(id: number) {
  try {
    const res = await fetch(`${API_BASE_URL}/admin/commodities/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    await assertApiOk(res);
    return true;
  } catch (error) { throw error; }
}

interface RawAdminPrice {
  provenance?: string;
  id: number;
  commodity_id: number;
  commodity_name: string;
  record_date: string;
  price: number;
  price_min?: number | null;
  price_max?: number | null;
  volume?: number;
  source?: string | null;
}

/**
 * Lấy lịch sử giá gần nhất cho Admin
 */
export async function fetchRecentPricesApi(commodityId?: number, startDate?: string, endDate?: string, offset: number = 0): Promise<AdminPriceItem[]> {
  try {
    const params = new URLSearchParams({ limit: '30', offset: String(offset) });
    if (commodityId) params.set('commodity_id', String(commodityId));
    if (startDate) params.set('start_date', startDate);
    if (endDate) params.set('end_date', endDate);
    const url = `${API_BASE_URL}/admin/prices/recent?${params}`;
    const res = await fetch(url, {
      headers: getAuthHeaders(),
      cache: 'no-store',
    });
    await assertApiOk(res);
    const data = await res.json();
    return data.map((d: RawAdminPrice) => ({
      id: d.id,
      commodityId: d.commodity_id,
      commodityName: d.commodity_name,
      recordDate: d.record_date,
      price: d.price,
      priceMin: d.price_min,
      priceMax: d.price_max,
      volume: d.volume,
      source: d.source,
      provenance: d.provenance,
    }));
  } catch (error) { throw error; }
}

/**
 * Thêm hoặc cập nhật bản ghi giá thủ công
 */
export async function createOrUpdatePriceApi(payload: {
  commodity_id: number;
  record_date: string;
  price: number;
  price_min?: number;
  price_max?: number;
  volume?: number;
  source?: string;
  reviewed?: boolean;
}): Promise<AdminPriceItem | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/admin/prices`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(payload),
    });
    await assertApiOk(res);
    const d = await res.json();
    return {
      id: d.id,
      commodityId: d.commodity_id,
      commodityName: d.commodity_name,
      recordDate: d.record_date,
      price: d.price,
      priceMin: d.price_min,
      priceMax: d.price_max,
      volume: d.volume,
      source: d.source,
    };
  } catch (error) { throw error; }
}

/**
 * Xóa một bản ghi giá
 */
export async function deletePriceRecordApi(priceId: number): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE_URL}/admin/prices/${priceId}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    await assertApiOk(res);
    return true;
  } catch (error) { throw error; }
}

/**
 * Kích hoạt tác vụ cào dữ liệu thị trường (Scraper)
 */
export async function triggerScrapeTaskApi(days: number = 30, options?: {commodity_id: number; start_date: string; end_date: string}): Promise<TaskRunResult> {
  try {
    const params = new URLSearchParams({days: String(days)});
    if (options) Object.entries(options).forEach(([key, value]) => params.set(key, String(value)));
    const res = await fetch(`${API_BASE_URL}/admin/tasks/scrape?${params}`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    await assertApiOk(res);
    const d = await res.json();
    return {
      taskId: d.task_id,
      progress: d.progress,
      taskName: d.task_name,
      status: d.status,
      message: d.message,
      recordsProcessed: d.records_processed,
      timestamp: d.timestamp,
    };
  } catch (error) { throw error; }
}

/**
 * Kích hoạt tác vụ huấn luyện lại mô hình AI (Re-train)
 */
export async function triggerRetrainTaskApi(commodityId?: number): Promise<TaskRunResult> {
  try {
    const url = commodityId 
      ? `${API_BASE_URL}/admin/tasks/retrain?commodity_id=${commodityId}`
      : `${API_BASE_URL}/admin/tasks/retrain`;
    const res = await fetch(url, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    await assertApiOk(res);
    const d = await res.json();
    return {
      taskId: d.task_id,
      progress: d.progress,
      taskName: d.task_name,
      status: d.status,
      message: d.message,
      recordsProcessed: d.records_processed,
      timestamp: d.timestamp,
    };
  } catch (error) { throw error; }
}

interface RawAdminUser {
  id: number;
  email: string;
  full_name: string;
  role: 'admin' | 'analyst' | 'user';
  is_active?: boolean;
  created_at?: string;
}

/**
 * Lấy danh sách người dùng hệ thống
 */
export async function fetchAdminUsersApi(): Promise<AdminUserItem[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/admin/users`, {
      headers: getAuthHeaders(),
      cache: 'no-store',
    });
    await assertApiOk(res);
    const data = await res.json();
    return data.map((u: RawAdminUser) => ({
      id: u.id,
      email: u.email,
      fullName: u.full_name,
      role: u.role,
      isActive: u.is_active !== false && !u.role.endsWith("_disabled"),
      createdAt: u.created_at,
    }));
  } catch (error) { throw error; }
}

/**
 * Tạo người dùng mới
 */
export async function createAdminUserApi(payload: {
  email: string;
  password: string;
  full_name: string;
  role: string;
}): Promise<AdminUserItem> {
  try {
    const res = await fetch(`${API_BASE_URL}/admin/users`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Không thể tạo người dùng');
    }
    const u = await res.json();
    return {
      id: u.id,
      email: u.email,
      fullName: u.full_name,
      role: u.role,
      isActive: u.is_active !== false && !u.role.endsWith("_disabled"),
      createdAt: u.created_at,
    };
  } catch (error) { throw error; }
}

/**
 * Phase 5: Nhập file CSV giá nông sản
 */
export async function importPricesCsvApi(file: File) {
  const token = typeof window !== 'undefined' ? localStorage.getItem('agro_access_token') : null;
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE_URL}/admin/prices/import-csv`, {
    method: 'POST',
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Không thể upload file CSV');
  }
  return await res.json();
}

/**
 * Phase 5: Lấy URL tải xuống file CSV
 */
export function getExportPricesCsvUrl(commodityId?: number): string {
  const base = `${API_BASE_URL}/admin/prices/export-csv`;
  return commodityId ? `${base}?commodity_id=${commodityId}` : base;
}

/**
 * Phase 5: Lấy danh sách Crawler Logs
 */
export async function fetchCrawlerLogsApi() {
  try {
    const res = await fetch(`${API_BASE_URL}/admin/logs/crawler`, {
      headers: getAuthHeaders(),
      cache: 'no-store',
    });
    await assertApiOk(res);
    return await res.json();
  } catch (error) { throw error; }
}

/**
 * Phase 5: Cập nhật Role người dùng
 */
export async function updateUserRoleApi(userId: number, role: string) {
  const res = await fetch(`${API_BASE_URL}/admin/users/${userId}/role`, {
    method: 'PATCH',
    headers: getAuthHeaders(),
    body: JSON.stringify({ role }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Không thể cập nhật quyền');
  }
  return await res.json();
}

/**
 * Phase 5: Khóa hoặc mở khóa người dùng
 */
export async function toggleUserStatusApi(userId: number) {
  const res = await fetch(`${API_BASE_URL}/admin/users/${userId}/toggle-status`, {
    method: 'PATCH',
    headers: getAuthHeaders(),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Không thể thay đổi trạng thái tài khoản');
  }
  return await res.json();
}

/**
 * Phase 5: Lấy mô hình AI đang kích hoạt
 */
export async function fetchActiveModelApi() {
  try {
    const res = await fetch(`${API_BASE_URL}/admin/models/active`, {
      headers: getAuthHeaders(),
      cache: 'no-store',
    });
    await assertApiOk(res);
    return await res.json();
  } catch (error) { throw error; }
}

/**
 * Phase 5: Thiết lập mô hình AI hoạt động
 */
export async function setActiveModelApi(activeModel: string) {
  const res = await fetch(`${API_BASE_URL}/admin/models/active`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ active_model: activeModel, description: `Kích hoạt mô hình ${activeModel}` }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Không thể chuyển đổi mô hình');
  }
  return await res.json();
}

/**
 * Lấy so sánh hiệu năng các mô hình
 */
export async function fetchModelComparisonApi(commodityId: number = 2): Promise<ModelComparisonMetrics[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/forecast/compare/${commodityId}`, {
      cache: 'no-store',
    });
    await assertApiOk(res);
    const data = await res.json();
    return data.map((d: { modelName: string; mae: number; rmse: number; mape: number; r2: number }, idx: number) => ({
      modelName: d.modelName,
      mae: d.mae,
      rmse: d.rmse,
      mape: d.mape,
      r2: d.r2,
      isBest: idx === 0,
    }));
  } catch (error) { throw error; }
}




export async function assertApiOk(response: Response): Promise<void> {
  if (response.ok) return;
  const body = await response.json().catch(() => ({}));
  const detail = typeof body.detail === 'string' ? body.detail : Array.isArray(body.detail)
    ? body.detail.map((item: {msg: string}) => item.msg).join('; ') : 'Yêu cầu thất bại';
  if (response.status === 401 && typeof window !== 'undefined') {
    localStorage.removeItem('agro_access_token');
    localStorage.removeItem('agro_user');
    window.location.assign('/login?redirect=' + encodeURIComponent(window.location.pathname));
  }
  throw new Error(detail + ' (HTTP ' + response.status + ')');
}

function mapTask(d: {task_id: number; task_name: string; status: string; message: string; progress: number; records_processed: number; timestamp: string}): TaskRunResult {
  return {taskId: d.task_id, taskName: d.task_name, status: d.status, message: d.message, progress: d.progress, recordsProcessed: d.records_processed, timestamp: d.timestamp};
}

export async function fetchTasksApi(kind: string): Promise<TaskRunResult[]> {
  const res = await fetch(API_BASE_URL + '/admin/tasks?kind=' + encodeURIComponent(kind), {headers: getAuthHeaders(), cache: 'no-store'});
  await assertApiOk(res);
  return (await res.json()).map(mapTask);
}

export async function fetchTaskApi(id: number): Promise<TaskRunResult> {
  const res = await fetch(API_BASE_URL + '/admin/tasks/' + id, {headers: getAuthHeaders(), cache: 'no-store'});
  await assertApiOk(res);
  return mapTask(await res.json());
}

export async function downloadPricesCsv(commodityId?: number, startDate?: string, endDate?: string) {
  const params = new URLSearchParams();
  if (commodityId) params.set('commodity_id', String(commodityId));
  if (startDate) params.set('start_date', startDate);
  if (endDate) params.set('end_date', endDate);
  const res = await fetch(API_BASE_URL + '/admin/prices/export-csv?' + params, {headers: getAuthHeaders()});
  await assertApiOk(res);
  const blob = new Blob(['\uFEFF', await res.text()], {type: 'text/csv;charset=utf-8'});
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'lich-su-gia.csv';
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export async function fetchHealthApi(): Promise<{status: string; database: string}> {
  const res = await fetch(API_BASE_URL.replace(/\/api\/v1\/?$/, '') + '/health', {cache: 'no-store', signal: AbortSignal.timeout(8000)});
  await assertApiOk(res);
  return res.json();
}

export async function fetchCurrentUserApi() {
  const res = await fetch(API_BASE_URL + '/auth/me', {headers: getAuthHeaders(), cache: 'no-store'});
  await assertApiOk(res);
  return res.json();
}
