import type { Metadata } from "next";
import { Be_Vietnam_Pro } from "next/font/google";
import "./globals.css";
import LayoutWrapper from "@/components/layout/LayoutWrapper";
import SyncfusionProvider from "@/components/layout/SyncfusionProvider";
import { LocationProvider } from "@/contexts/LocationContext";

const beVietnamPro = Be_Vietnam_Pro({
  subsets: ["latin", "vietnamese"],
  weight: ["400", "500", "600", "700"],
  display: "swap",
  variable: "--font-sans",
});

export const metadata: Metadata = {
  title: "AgroForecast - Phân tích & Dự báo Giá Nông sản",
  description: "Dự báo giá nông sản Việt Nam bằng ARIMA, Prophet, Random Forest, XGBoost và LSTM; cảnh báo ngưỡng giá tự động.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="vi" className={`min-h-full ${beVietnamPro.variable}`}>
      <body className="font-sans bg-canvas text-primary-text min-h-screen flex antialiased selection:bg-brand/20">
        <SyncfusionProvider>
          <LocationProvider>
            <LayoutWrapper>{children}</LayoutWrapper>
          </LocationProvider>
        </SyncfusionProvider>
      </body>
    </html>
  );
}
