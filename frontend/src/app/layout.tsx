import React from "react";
import "./globals.css";

export const metadata = {
  title: "دستیار هوشمند خرید حضوری ترب در تهران | رادار نقشه‌محور و GenUI",
  description: "میز کار و رادار خرید حضوری ترب در پاساژها و بورس‌های تهران با استعلام صوتی ضدخجالت و میکرو-لینک ۱ کلیکی"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fa" dir="rtl">
      <head>
        <link
          href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css"
          rel="stylesheet"
          type="text/css"
        />
        <script src="https://cdn.tailwindcss.com/3.4.17"></script>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
      </head>
      <body className="min-h-screen bg-[#F8F9FA] text-slate-900 antialiased">{children}</body>
    </html>
  );
}
