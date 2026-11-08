import React from "react";

export interface ProductReviewProps {
  productTitle: string;
  valueScore: number;
  overallVerdict: string;
  dispersionAlert: string;
  authenticityWarning: string;
  pros: string[];
  cons: string[];
  checklist: string[];
  checkedItems: Record<number, boolean>;
  onToggleChecklist: (idx: number) => void;
}

export const ProductReviewAndInspectionCard: React.FC<ProductReviewProps> = ({
  productTitle,
  valueScore,
  overallVerdict,
  dispersionAlert,
  authenticityWarning,
  pros,
  cons,
  checklist,
  checkedItems,
  onToggleChecklist
}) => {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm space-y-3">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3">
        <div>
          <span className="text-xs font-bold text-[#D73948] bg-[#FFF1F2] px-2.5 py-0.5 rounded-full">
            موتور نقد و بررسی هوشمند + رادار اصالت‌سنجی کاتالوگ (EDA + Web Synthesis)
          </span>
          <h3 className="text-base font-bold text-slate-900 mt-1">{productTitle}</h3>
        </div>
        <div className="flex items-center gap-2 bg-slate-900 text-white px-3 py-1.5 rounded-xl">
          <span className="text-xs">ارزش خرید حضوری:</span>
          <span className="text-base font-extrabold text-emerald-400">{valueScore} / ۱۰</span>
        </div>
      </div>

      <p className="text-xs text-slate-700 leading-relaxed bg-slate-50 p-3 rounded-xl">{overallVerdict}</p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
        <div className="p-3 rounded-xl bg-amber-50 border border-amber-200 text-xs text-amber-900">
          <div className="font-bold mb-1">⚠️ هشدار پراکندگی قیمت در دیتاست ترب:</div>
          <div>{dispersionAlert}</div>
        </div>
        <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-xs text-rose-900">
          <div className="font-bold mb-1">🛡️ رادار ریسک کالای فیک / تله واحد فروش (seller_title):</div>
          <div>{authenticityWarning}</div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
        <div className="p-3 rounded-xl bg-emerald-50/60 border border-emerald-100">
          <div className="font-bold text-emerald-800 mb-1.5">نقاط قوت کلیدی:</div>
          <ul className="space-y-1 text-slate-700">
            {pros.map((pr, i) => (
              <li key={i}>✅ {pr}</li>
            ))}
          </ul>
        </div>
        <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
          <div className="font-bold text-slate-800 mb-1.5">نقاط ضعف و نکات پیش از خرید:</div>
          <ul className="space-y-1 text-slate-700">
            {cons.map((cn, i) => (
              <li key={i}>• {cn}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="p-3 rounded-xl border border-slate-200 bg-white">
        <div className="font-bold text-xs text-slate-900 mb-2">
          📋 چک‌لیست تعاملی تست فیزیکی کالا داخل مغازه (پیش از پرداخت کارت به کارت یا ترب‌پی):
        </div>
        <div className="space-y-1.5">
          {checklist.map((item, idx) => (
            <label
              key={idx}
              className="flex items-center gap-2 text-xs text-slate-800 cursor-pointer select-none"
            >
              <input
                type="checkbox"
                checked={!!checkedItems[idx]}
                onChange={() => onToggleChecklist(idx)}
                className="rounded accent-[#D73948]"
              />
              <span className={checkedItems[idx] ? "line-through text-slate-400" : ""}>{item}</span>
            </label>
          ))}
        </div>
      </div>
    </div>
  );
};
