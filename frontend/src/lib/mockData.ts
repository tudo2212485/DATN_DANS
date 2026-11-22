import { CommoditySummary, ComparisonDataPoint, SpotlightSummary, ModelMetrics, ForecastPoint, AlertRuleItem } from '@/types';

export const COMMODITIES_DATA: CommoditySummary[] = [
  {
    id: 1,
    code: 'RICE',
    name: 'Lúa gạo',
    category: 'Lương thực',
    unit: 'đ/kg',
    region: 'Huyện Châu Phú, An Giang (Tại ruộng)',
    currentPrice: 8450,
    formattedPrice: '8.450',
    changePct: 2.4,
    isPositive: true,
    sparkline: [
      { date: 'T-6', value: 8250 },
      { date: 'T-5', value: 8290 },
      { date: 'T-4', value: 8320 },
      { date: 'T-3', value: 8380 },
      { date: 'T-2', value: 8400 },
      { date: 'T-1', value: 8420 },
      { date: 'T0', value: 8450 },
    ],
  },
  {
    id: 2,
    code: 'COFFEE',
    name: 'Cà phê Robusta',
    category: 'Nông sản xuất khẩu',
    unit: 'đ/kg',
    region: 'Huyện Cư M\'gar, Đắk Lắk (Tại vườn)',
    currentPrice: 62300,
    formattedPrice: '62.300',
    changePct: -1.1,
    isPositive: false,
    sparkline: [
      { date: 'T-6', value: 63800 },
      { date: 'T-5', value: 63500 },
      { date: 'T-4', value: 63100 },
      { date: 'T-3', value: 62900 },
      { date: 'T-2', value: 62700 },
      { date: 'T-1', value: 62400 },
      { date: 'T0', value: 62300 },
    ],
  },
  {
    id: 3,
    code: 'PEPPER',
    name: 'Hồ tiêu',
    category: 'Gia vị & Nông sản',
    unit: 'đ/kg',
    region: 'Huyện Chư Sê, Gia Lai (Tại vườn)',
    currentPrice: 145000,
    formattedPrice: '145.000',
    changePct: 0.7,
    isPositive: true,
    sparkline: [
      { date: 'T-6', value: 143800 },
      { date: 'T-5', value: 144100 },
      { date: 'T-4', value: 144000 },
      { date: 'T-3', value: 144500 },
      { date: 'T-2', value: 144700 },
      { date: 'T-1', value: 144900 },
      { date: 'T0', value: 145000 },
    ],
  },
  {
    id: 4,
    code: 'SUGAR',
    name: 'Mía đường',
    category: 'Cây công nghiệp',
    unit: 'VNĐ/tấn',
    region: 'Huyện Tây Hòa, Phú Yên (Tại ruộng)',
    currentPrice: 1215000,
    formattedPrice: '1.215.000',
    changePct: 3.8,
    isPositive: true,
    sparkline: [
      { date: 'T-6', value: 1180000 },
      { date: 'T-5', value: 1185000 },
      { date: 'T-4', value: 1192000 },
      { date: 'T-3', value: 1200000 },
      { date: 'T-2', value: 1205000 },
      { date: 'T-1', value: 1210000 },
      { date: 'T0', value: 1215000 },
    ],
  },
  {
    id: 5,
    code: 'STRAWBERRY',
    name: 'Dâu tây Đà Lạt',
    category: 'Trái cây đặc sản',
    unit: 'VNĐ/kg',
    region: 'Phường 8, Đà Lạt, Lâm Đồng',
    currentPrice: 100000,
    formattedPrice: '100.000',
    changePct: 2.1,
    isPositive: true,
    sparkline: [
      { date: 'T-6', value: 98000 },
      { date: 'T-5', value: 98500 },
      { date: 'T-4', value: 99000 },
      { date: 'T-3', value: 99200 },
      { date: 'T-2', value: 99500 },
      { date: 'T-1', value: 99800 },
      { date: 'T0', value: 100000 },
    ],
  },
  {
    id: 6,
    code: 'POTATO',
    name: 'Khoai tây Đà Lạt',
    category: 'Rau củ',
    unit: 'VNĐ/kg',
    region: 'Phường 7, Đà Lạt, Lâm Đồng',
    currentPrice: 20000,
    formattedPrice: '20.000',
    changePct: 1.5,
    isPositive: true,
    sparkline: [
      { date: 'T-6', value: 19600 },
      { date: 'T-5', value: 19700 },
      { date: 'T-4', value: 19750 },
      { date: 'T-3', value: 19800 },
      { date: 'T-2', value: 19850 },
      { date: 'T-1', value: 19950 },
      { date: 'T0', value: 20000 },
    ],
  },
  {
    id: 7,
    code: 'SWEET_POTATO',
    name: 'Khoai lang tím Vĩnh Long',
    category: 'Rau củ',
    unit: 'VNĐ/kg',
    region: 'Huyện Bình Tân, Vĩnh Long',
    currentPrice: 16000,
    formattedPrice: '16.000',
    changePct: -0.8,
    isPositive: false,
    sparkline: [
      { date: 'T-6', value: 16300 },
      { date: 'T-5', value: 16250 },
      { date: 'T-4', value: 16200 },
      { date: 'T-3', value: 16150 },
      { date: 'T-2', value: 16100 },
      { date: 'T-1', value: 16050 },
      { date: 'T0', value: 16000 },
    ],
  },
  {
    id: 8,
    code: 'CASHEW',
    name: 'Hạt điều',
    category: 'Cây công nghiệp',
    unit: 'VNĐ/kg',
    region: 'Huyện Bù Đăng, Bình Phước',
    currentPrice: 32500,
    formattedPrice: '32.500',
    changePct: 1.9,
    isPositive: true,
    sparkline: [
      { date: 'T-6', value: 31800 },
      { date: 'T-5', value: 31900 },
      { date: 'T-4', value: 32000 },
      { date: 'T-3', value: 32100 },
      { date: 'T-2', value: 32250 },
      { date: 'T-1', value: 32400 },
      { date: 'T0', value: 32500 },
    ],
  },
];

export const COMPARISON_SERIES: ComparisonDataPoint[] = [
  { date: '01/06', rice: 0.0, coffee: 0.0, pepper: 0.0, sugar: 0.0, strawberry: 0.0, sweet_potato: 0.0, potato: 0.0, cashew: 0.0 },
  { date: '08/06', rice: 1.8, coffee: 2.5, pepper: 1.2, sugar: 3.4, strawberry: 1.5, sweet_potato: -0.8, potato: 0.9, cashew: 1.8 },
  { date: '15/06', rice: 3.2, coffee: 4.8, pepper: 2.1, sugar: 5.9, strawberry: 2.8, sweet_potato: -1.2, potato: 1.5, cashew: 2.4 },
  { date: '22/06', rice: 2.8, coffee: 5.9, pepper: 3.0, sugar: 8.5, strawberry: 3.5, sweet_potato: -0.5, potato: 1.9, cashew: 3.1 },
  { date: '29/06', rice: 4.6, coffee: 4.2, pepper: 2.4, sugar: 8.0, strawberry: 3.9, sweet_potato: -1.0, potato: 2.2, cashew: 2.9 },
  { date: '06/07', rice: 6.5, coffee: 2.6, pepper: 3.8, sugar: 8.9, strawberry: 4.1, sweet_potato: -1.4, potato: 2.0, cashew: 3.3 },
  { date: '13/07', rice: 5.8, coffee: 1.5, pepper: 4.1, sugar: 9.4, strawberry: 4.5, sweet_potato: -1.5, potato: 2.4, cashew: 3.6 },
  { date: '20/07', rice: 7.2, coffee: 1.8, pepper: 4.0, sugar: 9.8, strawberry: 4.3, sweet_potato: -1.2, potato: 2.1, cashew: 3.5 },
  { date: '28/08', rice: 7.9, coffee: 1.9, pepper: 4.1, sugar: 10.1, strawberry: 4.2, sweet_potato: -1.5, potato: 2.1, cashew: 3.5 },
];

export const SPOTLIGHT_SUGAR: SpotlightSummary = {
  commodityCode: 'SUGAR',
  commodityName: 'Mía đường',
  subtitle: 'Xu hướng 3 tháng',
  currentPrice: '1.200 đ/kg',
  change3Months: '+10.1%',
  peakPrice: '1.202 đ/kg',
  trendData: [
    { date: '01/06', value: 1090 },
    { date: '15/06', value: 1120 },
    { date: '01/07', value: 1160 },
    { date: '15/07', value: 1150 },
    { date: '01/08', value: 1180 },
    { date: '15/08', value: 1198 },
    { date: '28/08', value: 1200 },
  ],
};

export const MODEL_METRICS_LIST: Record<string, ModelMetrics> = {
  LSTM: {
    modelName: 'LSTM',
    mae: 420.5,
    rmse: 612.3,
    mape: 0.68,
    r2: 0.965,
    trainDate: '28/08/2026',
  },
  Prophet: {
    modelName: 'Prophet',
    mae: 650.2,
    rmse: 890.1,
    mape: 0.89,
    r2: 0.942,
    trainDate: '28/08/2026',
  },
  ARIMA: {
    modelName: 'ARIMA',
    mae: 890.0,
    rmse: 1150.4,
    mape: 1.15,
    r2: 0.912,
    trainDate: '28/08/2026',
  },
};

// Generate 30 days of mock sample forecast points
const sampleHistory: ForecastPoint[] = [
  { date: '22/08', actualPrice: 62800, predictedPrice: 62800, lowerCI: 62800, upperCI: 62800, isForecast: false },
  { date: '24/08', actualPrice: 62500, predictedPrice: 62500, lowerCI: 62500, upperCI: 62500, isForecast: false },
  { date: '26/08', actualPrice: 62400, predictedPrice: 62400, lowerCI: 62400, upperCI: 62400, isForecast: false },
  { date: '28/08 (Hôm nay)', actualPrice: 62300, predictedPrice: 62300, lowerCI: 62300, upperCI: 62300, isForecast: false },
];

const sampleFuture: ForecastPoint[] = Array.from({ length: 30 }, (_, i) => {
  const day = i + 1;
  const base = 62300;
  const pred = Math.round(base * (1 + 0.0035 * day + Math.sin(day / 2.0) * 0.001));
  const spread = day * 0.005;
  const lower = Math.round(pred * (1 - spread));
  const upper = Math.round(pred * (1 + spread));
  
  // Format date
  const d = new Date(2026, 7, 28 + day);
  const dateStr = `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')} (T+${day})`;
  
  return {
    date: dateStr,
    predictedPrice: pred,
    lowerCI: lower,
    upperCI: upper,
    isForecast: true,
  };
});

export const FORECAST_PREDICTIONS_SAMPLE: ForecastPoint[] = [
  ...sampleHistory,
  ...sampleFuture,
];

export const INITIAL_ALERT_RULES: AlertRuleItem[] = [
  {
    id: 1,
    commodityId: 2,
    commodityName: 'Cà phê Robusta',
    ruleName: 'Cảnh báo Cà phê Robusta vượt 125,000 VNĐ/kg',
    conditionType: 'PRICE_ABOVE',
    thresholdValue: 125000,
    email: 'nongsanviet.alert@gmail.com',
    isActive: true,
    createdAt: '25/08/2026',
  },
  {
    id: 2,
    commodityId: 2,
    commodityName: 'Cà phê Robusta',
    ruleName: 'Cảnh báo Cà phê Robusta giảm dưới 110,000 VNĐ/kg',
    conditionType: 'PRICE_BELOW',
    thresholdValue: 110000,
    email: 'nongsanviet.alert@gmail.com',
    isActive: true,
    createdAt: '26/08/2026',
  },
  {
    id: 3,
    commodityId: 1,
    commodityName: 'Lúa gạo IR50404',
    ruleName: 'Cảnh báo Lúa gạo IR504 vượt đỉnh 9,000 VNĐ/kg',
    conditionType: 'PRICE_ABOVE',
    thresholdValue: 9000,
    email: 'gaomientay.market@gmail.com',
    isActive: true,
    createdAt: '27/08/2026',
  },
  {
    id: 4,
    commodityId: 3,
    commodityName: 'Hồ tiêu đen',
    ruleName: 'Cảnh báo Hồ tiêu biến động tăng mạnh trên 145,000 VNĐ/kg',
    conditionType: 'PRICE_ABOVE',
    thresholdValue: 145000,
    email: 'chuse.pepper@gmail.com',
    isActive: false,
    createdAt: '28/08/2026',
  },
];
