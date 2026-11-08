import React from "react";

export interface LiveVerificationTrackerProps {
  shopName: string;
  transcriptLines: string[];
  onSimulateSeller1Tap: (status: "confirmed_in_stock" | "price_updated" | "out_of_stock") => void;
}

export const LiveVerificationTracker: React.FC<LiveVerificationTrackerProps> = ({
  shopName,
  transcriptLines,
  onSimulateSeller1Tap
}) => {
  return (
    <div className="bg-slate-900 text-white rounded-2xl p-4 shadow-md space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-xs font-bold text-emerald-400">
          🎙️ استعلام زنده وکیل صوتی ترب + میکرو-لینک ۱ کلیکی فروشنده ({shopName})
        </span>
        <span className="text-[11px] bg-slate-800 px-2.5 py-0.5 rounded-full text-slate-300">
          System-1 Classifier Ready
        </span>
      </div>
      <div className="bg-slate-800/90 rounded-xl p-3 text-xs space-y-1.5 font-normal">
        {transcriptLines.map((line, i) => (
          <div key={i} className="leading-relaxed">
            {line}
          </div>
        ))}
      </div>
      <div className="border-t border-slate-700 pt-3">
        <div className="text-xs text-slate-300 mb-2">
          ⚡ شبیه‌ساز پنل میکرو-لینک ۱ کلیکی روی گوشی مغازه‌دار (1-Tap Seller Micro-Webhook):
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => onSimulateSeller1Tap("confirmed_in_stock")}
            className="px-3 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold"
          >
            [✅ موجوده با همین قیمت (ثبت ۱ کلیکی)]
          </button>
          <button
            type="button"
            onClick={() => onSimulateSeller1Tap("price_updated")}
            className="px-3 py-1.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-bold"
          >
            [🔄 موجوده ولی قیمت امروز تغییر کرده]
          </button>
          <button
            type="button"
            onClick={() => onSimulateSeller1Tap("out_of_stock")}
            className="px-3 py-1.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold"
          >
            [❌ فعلاً تمام شده / مغازه بسته است]
          </button>
        </div>
      </div>
    </div>
  );
};
