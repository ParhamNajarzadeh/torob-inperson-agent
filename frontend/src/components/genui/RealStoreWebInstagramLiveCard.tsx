import React from "react";

export interface RealStoreCardProps {
  shopName: string;
  channelType: "website" | "instagram";
  channelUrl: string;
  datasetPriceToman: number;
  liveScrapedPriceToman: number;
  extractedBioAddress: string;
  promptInjectionSafe: boolean;
}

export const RealStoreWebInstagramLiveCard: React.FC<RealStoreCardProps> = ({
  shopName,
  channelType,
  channelUrl,
  datasetPriceToman,
  liveScrapedPriceToman,
  extractedBioAddress,
  promptInjectionSafe
}) => {
  return (
    <div className="bg-purple-50/70 rounded-2xl border border-purple-200 p-4 shadow-sm">
      <div className="flex items-center justify-between gap-2 mb-2">
        <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-[#7C3AED] text-white">
          🌐 بررسی زنده ۱۱۲ فروشگاه واقعی دیتاست (۹۰ وب‌سایت + ۲۲ اینستاگرام)
        </span>
        {promptInjectionSafe && (
          <span className="text-[11px] font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded-md">
            🛡️ گاردریل System-1: ایمن در برابر Prompt Injection (Noul: 0.01)
          </span>
        )}
      </div>
      <h4 className="font-bold text-sm text-slate-900">{shopName}</h4>
      <p className="text-xs text-slate-600 mt-0.5">
        منبع بررسی‌شده ({channelType === "website" ? "وب‌سایت رسمی" : "پیج اینستاگرام"}):{" "}
        <span className="font-mono text-purple-800">{channelUrl}</span>
      </p>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 mt-3 text-xs bg-white p-3 rounded-xl border border-purple-100">
        <div>
          <span className="text-slate-500 block">قیمت دیتاست ترب:</span>
          <span className="font-bold">{datasetPriceToman.toLocaleString("fa-IR")} تومان</span>
        </div>
        <div>
          <span className="text-slate-500 block">قیمت استخراج‌شده زنده:</span>
          <span className="font-bold text-emerald-700">{liveScrapedPriceToman.toLocaleString("fa-IR")} تومان</span>
        </div>
        <div>
          <span className="text-slate-500 block">واحد استخراج‌شده از بیو/سایت:</span>
          <span className="font-semibold text-slate-800">{extractedBioAddress}</span>
        </div>
      </div>
    </div>
  );
};
