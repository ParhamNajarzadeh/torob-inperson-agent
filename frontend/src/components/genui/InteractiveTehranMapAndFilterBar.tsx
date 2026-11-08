import React from "react";

export interface MapFilterProps {
  neighborhood: string;
  onChangeNeighborhood: (n: string) => void;
  requireTorobPay: boolean;
  onToggleTorobPay: () => void;
  openNowOnly: boolean;
  onToggleOpenNow: () => void;
  realShopsDemoMode: boolean;
  onToggleRealShopsMode: () => void;
}

export const InteractiveTehranMapAndFilterBar: React.FC<MapFilterProps> = ({
  neighborhood,
  onChangeNeighborhood,
  requireTorobPay,
  onToggleTorobPay,
  openNowOnly,
  onToggleOpenNow,
  realShopsDemoMode,
  onToggleRealShopsMode
}) => {
  const neighborhoods = ["همه محله‌های تهران", "فردوسی (۵۰.۷٪ مغازه‌ها)", "شیخ هادی / جمهوری (۲۴.۵٪)", "بهارستان (۹.۵٪)", "ولیعصر / ایرانشهر"];
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-3.5 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex flex-wrap items-center gap-1.5">
          {neighborhoods.map((n) => (
            <button
              key={n}
              type="button"
              onClick={() => onChangeNeighborhood(n)}
              className={`px-2.5 py-1 rounded-xl text-xs font-medium transition ${
                neighborhood === n
                  ? "bg-[#D73948] text-white font-bold"
                  : "bg-slate-100 text-slate-700 hover:bg-slate-200"
              }`}
            >
              📍 {n}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <button
            type="button"
            onClick={onToggleTorobPay}
            className={`px-3 py-1 rounded-xl text-xs font-bold border transition ${
              requireTorobPay
                ? "bg-emerald-600 text-white border-emerald-600"
                : "bg-white text-slate-700 border-slate-300"
            }`}
          >
            💳 ترب‌پی حضوری / قسطی
          </button>
          <button
            type="button"
            onClick={onToggleOpenNow}
            className={`px-3 py-1 rounded-xl text-xs font-bold border transition ${
              openNowOnly
                ? "bg-slate-900 text-white border-slate-900"
                : "bg-white text-slate-700 border-slate-300"
            }`}
          >
            🕒 فقط باز در ساعت مراجعه
          </button>
          <button
            type="button"
            onClick={onToggleRealShopsMode}
            className={`px-3 py-1 rounded-xl text-xs font-bold border transition ${
              realShopsDemoMode
                ? "bg-[#7C3AED] text-white border-[#7C3AED]"
                : "bg-purple-50 text-[#7C3AED] border-purple-200"
            }`}
          >
            🌐 دموی ۱۱۲ فروشگاه واقعی (وب/اینستاگرام)
          </button>
        </div>
      </div>
    </div>
  );
};
