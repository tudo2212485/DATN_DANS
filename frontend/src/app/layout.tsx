import type { Metadata } from "next";
import { Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";
import LayoutWrapper from "@/components/layout/LayoutWrapper";

const plusJakartaSans = Plus_Jakarta_Sans({
  subsets: ["vietnamese", "latin"],
  weight: ["400", "500", "600", "700", "800"],
  display: "swap",
  variable: "--font-plus-jakarta",
});

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
    <html lang="vi" className={`min-h-full ${plusJakartaSans.className}`}>
      <body className="bg-canvas text-primary-text min-h-screen flex antialiased selection:bg-brand/20">
        <LayoutWrapper>
          {children}
        </LayoutWrapper>
      </body>
    </html>
  );
}
