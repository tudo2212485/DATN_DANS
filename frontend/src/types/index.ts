export interface SparklinePoint {
  date: string;
  value: number;
}

export interface LocationContextData {
  province_code: string;
  province_name: string;
  region_name: string;
  pricing_mode: 'direct' | 'regional_benchmark' | 'national_benchmark' | string;
  reference_province: string;
  reference_province_code?: string | null;
  distance_km: number;
  logistics_spread: number;
  basis_offset: number;
  direct_source?: string | null;
  direct_source_url?: string | null;
  latest_direct_date?: string | null;
  explanation?: string | null;
  note?: string | null;
}

export interface RegionDirectCommodity {
  commodity_id: number;
  commodity_code: string;
  commodity_name: string;
  unit: string;
  latest_price: number;
  latest_date: string;
  source: string;
}

export interface RegionItem {
  code: string;
  name: string;
  region_name: string;
  lat: number;
  lng: number;
  is_major_hub: boolean;
  direct_commodities: RegionDirectCommodity[];
}

export interface LocateRegionResult {
  province_code: string;
  province_name: string;
  region_name: string;
  distance_km: number;
  lat: number;
  lng: number;
  method: string;
}

export interface CommodityProvinceRow {
  province_code: string;
  province_name: string;
  region_name: string;
  price: number;
  formatted_price: string;
  unit: string;
  diff_vs_national: number;
  pricing_mode: 'direct' | 'regional_benchmark' | string;
  reference_province: string;
  distance_km: number;
  logistics_spread: number;
  recorded_date?: string | null;
  source: string;
  source_url?: string | null;
}

export interface CommodityProvinceComparison {
  commodity: {
    id: number;
    code: string;
    name: string;
    unit: string;
    region: string;
  };
  national_price: number;
  formatted_national_price: string;
  latest_date?: string | null;
  provinces: CommodityProvinceRow[];
}

export interface CommoditySummary {
  id: number;
  code: string;
  name: string;
  category: string;
  unit: string;
  region: string;
  currentPrice: number;
  formattedPrice: string;
  changePct: number;
  isPositive: boolean;
  sparkline: SparklinePoint[];
  location_context?: LocationContextData | null;
}

export interface ComparisonDataPoint {
  date: string;
  rice: number;
  coffee: number;
  pepper: number;
  sugar: number;
  strawberry?: number;
  sweet_potato?: number;
  potato?: number;
  cashew?: number;
}

export interface SpotlightSummary {
  commodityCode: string;
  commodityName: string;
  subtitle: string;
  currentPrice: string;
  change3Months: string;
  peakPrice: string;
  trendData: { date: string; value: number }[];
}

export interface ForecastPoint {
  date: string;
  actualPrice?: number;
  predictedPrice: number;
  lowerCI: number;
  upperCI: number;
  isForecast?: boolean;
}

export interface ModelMetrics {
  modelName: 'LSTM' | 'Prophet' | 'ARIMA' | 'XGBoost' | 'RandomForest' | string;
  mae: number;
  rmse: number;
  mape: number;
  r2: number;
  accuracy?: number;
  picp95?: number | null;
  trainDate: string;
}

export interface ModelComparisonMetrics {
  modelName: string;
  mae: number;
  rmse: number;
  mape: number;
  r2: number;
  accuracy?: number;
  picp95?: number | null;
  isBest?: boolean;
}

export interface AlertRuleItem {
  id: number;
  commodityId: number;
  commodityName: string;
  ruleName: string;
  conditionType: 'PRICE_ABOVE' | 'PRICE_BELOW' | 'PCT_INC_7D' | 'PCT_DEC_7D' | 'OUT_OF_CI_95';
  thresholdValue: number;
  email: string;
  isActive: boolean;
  createdAt: string;
}

export interface AlertLogItem {
  id: number;
  ruleId: number;
  ruleName: string;
  commodityName: string;
  triggeredPrice: number;
  message: string;
  status: 'SENT' | 'FAILED' | 'PENDING';
  triggeredAt: string;
  email: string;
}

export interface AdminStats {
  totalCommodities: number;
  totalPriceRecords: number;
  totalForecastRecords: number;
  totalAlertRules: number;
  latestPriceDate: string | null;
  systemStatus: string;
}

export interface AdminPriceItem {
  provenance?: string;
  id: number;
  commodityId: number;
  commodityName: string;
  recordDate: string;
  price: number;
  priceMin?: number | null;
  priceMax?: number | null;
  volume?: number;
  source?: string | null;
}

export interface AdminUserItem {
  id: number;
  email: string;
  fullName: string;
  role: 'admin' | 'analyst' | 'user';
  isActive?: boolean;
  createdAt?: string;
}

export interface TaskRunResult {
  taskId?: number;
  progress?: number;
  taskName: string;
  status: string;
  message: string;
  recordsProcessed?: number;
  timestamp: string;
}

export interface RegionalPriceItem {
  id: number;
  commodityName: string;
  code: string;
  region: string;
  price: string;
  unit: string;
  minMax: string;
  volume: string;
  changePct: number;
  source: string;
  updatedAt: string;
}

export interface CrawlerLog {
  id: number;
  crawler_name: string;
  target_source: string;
  records_extracted: number;
  status: 'SUCCESS' | 'FAILED' | 'RUNNING';
  duration_sec: number;
  timestamp: string;
  details?: string;
}

export interface CSVImportResult {
  message: string;
  records_created: number;
  records_updated: number;
  errors: string[];
}

export interface ActiveModelSetting {
  active_model: string;
  description?: string;
  updated_at?: string;
}




export interface RegionInfo {
  id: string;
  name: string;
  basisSpread: number;
  description?: string;
}

export interface PriceRevisionItem {
  id: number;
  priceId: number;
  commodityId?: number | null;
  commodityName: string;
  recordDate: string;
  previousPrice?: number | null;
  newPrice?: number | null;
  previousSource?: string | null;
  previousProvenance?: string | null;
  actor?: string | null;
  reason?: string | null;
  action: 'UPDATED' | 'DELETED' | string;
  createdAt: string;
}
