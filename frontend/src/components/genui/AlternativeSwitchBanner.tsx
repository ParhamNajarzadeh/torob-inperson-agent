import React from "react";

export interface AlternativeSwitchBannerProps {
  failedShopName: string;
  failureReason: string;
  alternativeShopName: string;
  alternativePassageFloor: string;
  alternativePriceToman: number;
  retryCount: number;
  onTriggerInMallPanic: () => void;
  onAcceptAlternative: () => void;
}

export const AlternativeSwitchBanner: React.FC<AlternativeSwitchBannerProps> = ({
  failedShopName,
  failureReason,
  alternativeShopName,
  alternativePassageFloor,
  alternativePriceToman,
  retryCount,
  onTriggerInMallPanic,
  onAcceptAlternative
}) => {
  return (
    <div className="bg-amber-50 rounded-2xl border-2 border-amber-300 p-4 shadow-sm space-y-3">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-200 text-amber-900">
          موتور جایگزین‌یاب ۳ لایه در همان پاساژ (تلاش {retryCount} از سقف ۳)
        </span>
        <button
          type="button"
          onClick={onTriggerInMallPanic}
          className="px-3 py-1.5 rounded-xl bg-[#D73948] hover:bg-[#BE123C] text-white text-xs font-extrabold shadow-sm"
        >
          🚨 الان جلوی مغازه‌ام و بسته است / موجود ندارد — فوری در همین پاساژ جایگزین بده!
        </button>
      </div>
      <div className="text-xs text-slate-800">
        علت عبور از «{failedShopName}»: <strong className="text-rose-700">{failureReason}</strong>. نزدیک‌ترین جایگزین تاییدشده در{" "}
        <strong>{alternativePassageFloor}</strong> فروشگاه <strong>«{alternativeShopName}»</strong> با قیمت{" "}
        <strong>{alternativePriceToman.toLocaleString("fa-IR")} تومان</strong> است.
      </div>
      <button
        type="button"
        onClick={onAcceptAlternative}
        className="px-4 py-2 rounded-xl bg-slate-900 text-white text-xs font-bold"
      >
        تأیید فروشگاه جایگزین و صدور کارت رزرو حضوری ۲ ساعته ←
      </button>
    </div>
  );
};
