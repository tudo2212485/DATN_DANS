export interface SparklinePoint {
  date: string;
  value: number;
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
}

export interface ComparisonDataPoint {
  date: string;
  rice: number;
  coffee: number;
  pepper: number;
  sugar: number;
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
  trainDate: string;
}

export interface ModelComparisonMetrics {
  modelName: string;
  mae: number;
  rmse: number;
  mape: number;
  r2: number;
  isBest?: boolean;
}

export interface AlertRuleItem {
  id: number;
  commodityId: number;
  commodityName: string;
  ruleName: string;
  conditionType: 'PRICE_ABOVE' | 'PRICE_BELOW' | 'PCT_INC_7D' | 'PCT_DEC_7D';
  thresholdValue: number;
  email: string;
  isActive: boolean;
  createdAt: string;
}
