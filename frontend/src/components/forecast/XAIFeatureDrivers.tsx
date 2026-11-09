'use client';

import React from 'react';

interface FeatureDriver {
  name: string;
  weight: number; // percentage (0 - 100)
  impact: 'positive' | 'negative' | 'neutral';
  description: string;
}

interface XAIFeatureDriversProps {
  commodityCode?: string;
  commodityName?: string;
  modelName?: string;
}

const DRIVER_DATABASE: Record<string, FeatureDriver[]> = {
  COFFEE: [
    { name: 'Thời tiết & lượng mưa Tây Nguyên', weight: 36, impact: 'positive', description: 'Khô hạn giai đoạn phân hóa mầm hoa làm giảm nhẹ năng suất dự kiến' },
    { name: 'Giá kỳ hạn Robusta London', weight: 28, impact: 'positive', description: 'Giá giao dịch trên sàn quốc tế duy trì ở vùng cao hỗ trợ giá thu mua' },
    { name: 'Tỷ giá USD/VND', weight: 18, impact: 'positive', description: 'Tỷ giá quy đổi thuận lợi cho các hợp đồng xuất khẩu FOB' },
    { name: 'Tồn kho cuối vụ trong dân', weight: 12, impact: 'negative', description: 'Lượng hàng dự trữ thu hẹp trước khi bước vào vụ thu hoạch mới' },
    { name: 'Chi phí vận chuyển nội địa', weight: 6, impact: 'neutral', description: 'Cước vận tải từ Tây Nguyên về cảng TP.HCM giữ mức ổn định' },
  ],
  PEPPER: [
    { name: 'Sản lượng thu hoạch Đắk Lắk & Gia Lai', weight: 34, impact: 'positive', description: 'Diện tích canh tác thu hẹp các năm trước làm giảm nguồn cung' },
    { name: 'Đơn hàng xuất khẩu Mỹ & Châu Âu', weight: 26, impact: 'positive', description: 'Nhu cầu nhập khẩu gia vị phục hồi trong quý hiện tại' },
    { name: 'Thời tiết vùng Đông Nam Bộ', weight: 22, impact: 'positive', description: 'Nắng hạn ảnh hưởng đến tỷ lệ đậu hạt tại Bà Rịa - Vũng Tàu' },
    { name: 'Tâm lý trữ hàng của đại lý', weight: 18, impact: 'neutral', description: 'Nông hộ và đại lý bán ra nhỏ giọt theo nhịp giá' },
  ],
  RICE: [
    { name: 'Giá gạo 5% tấm xuất khẩu', weight: 38, impact: 'positive', description: 'Nhu cầu thu mua ổn định từ thị trường Philippines và Indonesia' },
    { name: 'Nguồn nước & xâm nhập mặn ĐBSCL', weight: 28, impact: 'neutral', description: 'Điều kiện thủy văn tương đối thuận lợi cho sinh trưởng lúa' },
    { name: 'Tiến độ thu hoạch tại An Giang, Đồng Tháp', weight: 22, impact: 'negative', description: 'Giai đoạn thu hoạch rộ tạo áp lực điều chỉnh ngắn hạn' },
    { name: 'Chi phí phân bón & vật tư', weight: 12, impact: 'positive', description: 'Chi phí đầu vào neo ở mức cao giữ mặt bằng giá sàn' },
  ],
  SWEET_POTATO: [
    { name: 'Nhu cầu tiêu thụ & xuất khẩu', weight: 42, impact: 'positive', description: 'Hoạt động thu mua đóng cont tại các vựa Vĩnh Long diễn ra đều đặn' },
    { name: 'Sản lượng thu hoạch huyện Bình Tân', weight: 30, impact: 'negative', description: 'Nguồn cung khoai thương phẩm về vựa khá dồi dào' },
    { name: 'Mưa lớn tại vùng trũng ĐBSCL', weight: 18, impact: 'positive', description: 'Ảnh hưởng đến tiến độ thu hoạch và tỷ lệ củ đạt chuẩn loại 1' },
    { name: 'Chi phí vận chuyển lạnh', weight: 10, impact: 'neutral', description: 'Giá cước vận tải đường bộ ổn định' },
  ],
  POTATO: [
    { name: 'Nguồn cung nông sản ôn đới', weight: 35, impact: 'negative', description: 'Áp lực cạnh tranh từ nguồn khoai phân phối tại chợ đầu mối' },
    { name: 'Độ ẩm & sương muối tại Lâm Đồng', weight: 30, impact: 'positive', description: 'Thời tiết ẩm làm giảm tỷ lệ củ thương phẩm loại 1' },
    { name: 'Nhu cầu từ hệ thống bán lẻ TP.HCM', weight: 25, impact: 'positive', description: 'Đơn hàng tiêu thụ ổn định từ chuỗi siêu thị và bếp ăn' },
    { name: 'Chi phí bảo quản kho mát', weight: 10, impact: 'neutral', description: 'Chi phí lưu kho tại Đức Trọng và Đà Lạt không biến động' },
  ],
  STRAWBERRY: [
    { name: 'Sức mua du lịch tại Đà Lạt', weight: 38, impact: 'positive', description: 'Nhu cầu tiêu thụ trực tiếp và làm quà tăng vào dịp cuối tuần' },
    { name: 'Nhiệt độ & bức xạ trong nhà màng', weight: 32, impact: 'positive', description: 'Thời tiết nắng ấm giúp quả chín đều, đạt độ ngọt tiêu chuẩn' },
    { name: 'Chi phí vận chuyển hàng tươi', weight: 18, impact: 'negative', description: 'Đóng gói chống dập và vận chuyển nhanh chiếm tỷ trọng chi phí lớn' },
    { name: 'Cơ cấu giống canh tác', weight: 12, impact: 'positive', description: 'Tỷ lệ giống chất lượng cao giúp giữ giá bán bình quân' },
  ],
  CASHEW: [
    { name: 'Nhu cầu nguyên liệu tại nhà máy Bình Phước', weight: 36, impact: 'positive', description: 'Các xưởng chế biến tăng thu mua điều thô phục vụ đơn hàng' },
    { name: 'Giá điều nhân W320 xuất khẩu', weight: 32, impact: 'positive', description: 'Giá xuất khẩu nhân điều duy trì đà phục hồi nhẹ' },
    { name: 'Thời tiết giai đoạn ra hoa đậu quả', weight: 20, impact: 'negative', description: 'Mưa trái mùa cục bộ ảnh hưởng đến năng suất một số vùng' },
    { name: 'Biến động tỷ giá ngoại tệ', weight: 12, impact: 'positive', description: 'Hỗ trợ giá thu mua quy đổi trong nước' },
  ],
  SUGARCANE: [
    { name: 'Giá thu mua tại bàn cân nhà máy', weight: 40, impact: 'positive', description: 'Chính sách bao tiêu vùng nguyên liệu giữ ổn định giá mua' },
    { name: 'Diễn biến giá đường thế giới', weight: 28, impact: 'positive', description: 'Mặt bằng giá đường quốc tế hỗ trợ giá đường nội địa' },
    { name: 'Chữ đường (CCS) thực tế khi thu hoạch', weight: 22, impact: 'positive', description: 'Thời tiết khô ráo giúp mía tích trữ chữ đường đạt 10–11 CCS' },
    { name: 'Chi phí nhân công thu hoạch & vận chuyển', weight: 10, impact: 'negative', description: 'Chi phí chặt bốc và vận chuyển về nhà máy tăng nhẹ' },
  ],
};

const DEFAULT_DRIVERS: FeatureDriver[] = [
  { name: 'Cung cầu tại các chợ đầu mối', weight: 35, impact: 'positive', description: 'Sản lượng giao dịch thực tế qua hệ thống thương lái và vựa thu mua' },
  { name: 'Điều kiện thời tiết vùng trồng', weight: 30, impact: 'positive', description: 'Lượng mưa và nhiệt độ tác động trực tiếp đến năng suất thu hoạch' },
  { name: 'Chu kỳ mùa vụ trong năm', weight: 20, impact: 'negative', description: 'Biến động nguồn cung theo thời điểm chính vụ hoặc trái vụ' },
  { name: 'Chi phí vận chuyển & bảo quản', weight: 15, impact: 'neutral', description: 'Chi phí logistics từ vùng sản xuất đến nơi tiêu thụ' },
];

export default function XAIFeatureDrivers({ commodityCode = 'COFFEE', commodityName = 'Cà phê' }: XAIFeatureDriversProps) {
  const drivers = DRIVER_DATABASE[commodityCode.toUpperCase().replace('_NUT', '')] || DRIVER_DATABASE[commodityCode.toUpperCase()] || DEFAULT_DRIVERS;

  return (
    <div className="bg-white rounded-xl border border-zinc-200/90 p-5 flex flex-col justify-between">
      <div>
        <div className="flex items-baseline justify-between pb-3.5 border-b border-zinc-100">
          <div>
            <h3 className="text-[15px] font-semibold text-zinc-900">
              Yếu tố tác động đến giá {commodityName.toLowerCase()}
            </h3>
            <p className="text-[12.5px] text-zinc-500 mt-0.5">
              Tỷ trọng đóng góp của các biến số thị trường và mùa vụ
            </p>
          </div>
          <span className="text-[11px] font-medium text-zinc-400">
            Tỷ trọng (%)
          </span>
        </div>

        <div className="divide-y divide-zinc-100">
          {drivers.map((driver, index) => {
            const isPositive = driver.impact === 'positive';
            const isNegative = driver.impact === 'negative';
            
            return (
              <div key={index} className="py-3 first:pt-3.5 last:pb-1">
                <div className="flex items-center justify-between gap-3 text-[13px]">
                  <span className="font-medium text-zinc-800">{driver.name}</span>
                  <div className="flex items-center gap-2.5 shrink-0">
                    <span className={`text-[11px] font-medium ${
                      isPositive ? 'text-emerald-700' : isNegative ? 'text-rose-600' : 'text-zinc-500'
                    }`}>
                      {isPositive ? 'Hỗ trợ giá' : isNegative ? 'Gây áp lực' : 'Ổn định'}
                    </span>
                    <span className="font-mono font-semibold text-zinc-900 w-9 text-right">
                      {driver.weight}%
                    </span>
                  </div>
                </div>

                <div className="mt-1.5 w-full h-1.5 rounded-full bg-zinc-100 overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      isPositive ? 'bg-emerald-600' : isNegative ? 'bg-rose-500' : 'bg-zinc-400'
                    }`}
                    style={{ width: `${driver.weight}%` }}
                  />
                </div>

                <p className="mt-1 text-[12px] text-zinc-500 leading-relaxed">
                  {driver.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
