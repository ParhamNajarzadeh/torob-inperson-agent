import React from "react";

export interface PassageIndoorNavProps {
  shopName: string;
  passageName: string;
  floor: string;
  corridor: string;
  unitNumber: string;
  lockedPriceToman: number;
  holdPassCode: string;
  expiresInMinutes: number;
}

export const PassageIndoorNavigationCard: React.FC<PassageIndoorNavProps> = ({
  shopName,
  passageName,
  floor,
  corridor,
  unitNumber,
  lockedPriceToman,
  holdPassCode,
  expiresInMinutes
}) => {
  return (
    <div className="bg-white rounded-2xl border-2 border-emerald-500 p-4 shadow-md space-y-3">
      <div className="flex items-center justify-between">
        <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">
          ✅ گام ۴ تکمیل شد • کارت رزرو حضوری ۲ ساعته (Price-Lock & Hold Pass)
        </span>
        <span className="text-xs font-bold text-[#D73948]">اعتبار رزرو: {expiresInMinutes} دقیقه</span>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 items-center">
        <div className="md:col-span-2 space-y-1.5">
          <h3 className="text-base font-extrabold text-slate-900">{shopName}</h3>
          <div className="text-xs text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-1">
            <div>🏢 <strong>مرکز خرید / پاساژ:</strong> {passageName}</div>
            <div>🪜 <strong>طبقه و راهرو:</strong> {floor} — {corridor}</div>
            <div>🚪 <strong>شماره پلاک / واحد:</strong> {unitNumber}</div>
            <div>💰 <strong>قیمت قفل‌شده برای شما:</strong> <span className="text-emerald-700 font-bold">{lockedPriceToman.toLocaleString("fa-IR")} تومان</span></div>
          </div>
        </div>
        <div className="flex flex-col items-center justify-center p-3 rounded-xl bg-slate-900 text-white text-center">
          <div className="text-[11px] text-slate-300 mb-1">کد رزرو حضوری مغازه‌دار</div>
          <div className="text-base font-mono font-extrabold tracking-wider text-emerald-400 mb-1">
            {holdPassCode}
          </div>
          <div className="text-[10px] text-slate-400">هنگام ورود به مغازه این کد/QR را نشان دهید</div>
        </div>
      </div>
    </div>
  );
};
