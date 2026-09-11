import type { Metadata } from "next";
import "./globals.css";
import LayoutWrapper from "@/components/layout/LayoutWrapper";

export const metadata: Metadata = {
  title: "AgroForecast - Hệ thống Dự báo Giá Nông sản & Cảnh báo Thị trường",
  description: "Dashboard dự báo giá nông sản ứng dụng Machine Learning (ARIMA, Prophet, LSTM) và cảnh báo thị trường thông minh.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="vi" className="min-h-full">
      <body className="bg-[#F9F6F2] text-primary-text min-h-screen flex antialiased selection:bg-brand/20">
        <LayoutWrapper>
          {children}
        </LayoutWrapper>
      </body>
    </html>
  );
}
