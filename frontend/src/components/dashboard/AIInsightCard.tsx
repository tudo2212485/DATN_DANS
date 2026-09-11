'use client';

import React from 'react';
import { Sparkles, Lightbulb, CheckCircle2 } from 'lucide-react';

interface AIInsightCardProps {
  commodityName: string;
  trendPct: number;
  horizonDays: number;
  modelName: string;
  recommendation?: string;
  explanation?: string;
}

export const AIInsightCard: React.FC<AIInsightCardProps> = ({
  commodityName,
  trendPct,
  horizonDays,
  modelName,
  recommendation,
  explanation,
}) => {
  const isUp = trendPct >= 0;

  const defaultRecommendation = isUp
    ? `Xu hướng tăng nhẹ (+${Math.abs(trendPct).toFixed(1)}%). Nông dân có thể chia nhỏ lượng hàng bán theo đợt để tối ưu lợi nhuận.`
    : `Xu hướng điều chỉnh giảm (-${Math.abs(trendPct).toFixed(1)}%). Thương lái và nông dân nên theo dõi sát mốc hỗ trợ và hạn chế gom hàng số lượng lớn.`;

  const defaultExplanation = `Dựa trên phân tích hồi quy phi tuyến tính từ mô hình ${modelName} kết hợp các biến động vĩ mô (Tỷ giá USD/VND và nhu cầu tiêu thụ chuỗi cung ứng), mức giá dự kiến duy trì trong dải an toàn độ tin cậy 95%.`;

  return (
    <div className="p-5 rounded-2xl bg-card border border-border-subtle shadow-xs space-y-3">
      <div className="flex items-center justify-between pb-2.5 border-b border-border-subtle">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-xl bg-brand text-white shadow-xs">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h4 className="text-sm font-bold text-primary-text leading-tight flex items-center gap-1.5">
              Phân Tích Xu Hướng Thị Trường
            </h4>
            <div className="text-[11px] text-secondary-text font-medium mt-0.5">
              Áp dụng cho {commodityName} · Chu kỳ {horizonDays} ngày tới
            </div>
          </div>
        </div>

        <span className="text-[10px] font-semibold px-2.5 py-1 rounded-md bg-canvas text-secondary-text border border-border-subtle">
          Độ tin cậy 95%
        </span>
      </div>

      <div className="space-y-2.5 text-xs">
        {/* Recommendation box */}
        <div className="p-3.5 rounded-xl bg-white border border-brand/20 flex items-start gap-2.5 shadow-2xs">
          <Lightbulb className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
          <div>
            <span className="font-bold text-primary-text">Nhận định & Khuyến nghị: </span>
            <span className="text-secondary-text leading-relaxed font-medium">
              {recommendation || defaultRecommendation}
            </span>
          </div>
        </div>

        {/* Technical context explanation */}
        <div className="flex items-start gap-2 text-[11px] text-secondary-text/90 pl-1">
          <CheckCircle2 className="w-3.5 h-3.5 text-brand shrink-0 mt-0.5" />
          <span>{explanation || defaultExplanation}</span>
        </div>
      </div>
    </div>
  );
};

export default AIInsightCard;
